import itertools
import os

import pandas as pd
import torch
import torch.distributed as dist
import torch.multiprocessing as mp
from peft import PeftModel
from torch.nn.parallel import DistributedDataParallel as DDP
from torch.utils.data import DataLoader, DistributedSampler, TensorDataset
from tqdm import tqdm
from transformers import AutoModelForSequenceClassification, AutoTokenizer, logging

logging.set_verbosity_error()


def read_fa(file_path):
    chrom_dic = {}
    with open(file_path, "r") as f:
        lines = pd.DataFrame(f.readlines(), columns=["sequence"])
        lines["sequence"] = lines["sequence"].str.rstrip("\n")

        mask = lines["sequence"].str.startswith(">")
        index = lines[mask].index
        for i in range(len(index)):
            chrom = lines.loc[index[i], "sequence"].lstrip(">").split(" ")[0]
            left = index[i] + 1
            right = index[i + 1] if i + 1 < len(index) else None
            chrom_dic["chr{}".format(chrom)] = "".join(lines[left:right]["sequence"])
            print("chr{}".format(chrom))

    return chrom_dic


def divide(datas: pd.DataFrame, valtest_percentage: float, random_seed: int):
    _train = datas.sample(frac=1 - valtest_percentage, random_state=random_seed)
    _val = datas.drop(_train.index)
    return _train, _val


def _get_model_and_dataset(
    model_name_or_path: str,
    lora_model_path: str,
    model_max_length: int,
    texts: list,
):
    tokenizer = AutoTokenizer.from_pretrained(
        model_name_or_path,
        model_max_length=model_max_length,
        padding_side="right",
        use_fast=True,
        trust_remote_code=True,
    )
    model = AutoModelForSequenceClassification.from_pretrained(
        model_name_or_path, num_labels=1, trust_remote_code=True
    )
    if lora_model_path:
        model = PeftModel.from_pretrained(model, lora_model_path)

    input_ids = tokenizer(
        texts,
        return_tensors="pt",
        padding="max_length",
        max_length=tokenizer.model_max_length,
        truncation=True,
    )["input_ids"]
    dataset = TensorDataset(torch.arange(input_ids.shape[0]), input_ids)

    return model, dataset


def classify(
    texts: list,
    model_name_or_path: str = "liminghong/DNABERT-2-117M",
    lora_model_path: str = os.path.join(os.path.dirname(__file__), "adapter_model"),
    model_max_length: int = 1250,
    batch_size: int = 32,
):
    model, dataset = _get_model_and_dataset(
        model_name_or_path, lora_model_path, model_max_length, texts
    )

    model.cuda()
    model.eval()

    results = []
    for _, input_ids in tqdm(DataLoader(dataset, batch_size=batch_size, shuffle=False)):
        with torch.no_grad():
            _output = model(input_ids.cuda())
        results.extend(_output["logits"].flatten().tolist())
    return results


def _ddp_inference(rank, world_size, queue, model, dataset, batch_size):
    dist.init_process_group(backend="gloo", rank=rank, world_size=world_size)
    torch.cuda.set_device(rank)

    model = model.to(rank)
    model = DDP(model, device_ids=[rank])
    model.eval()

    sampler = DistributedSampler(
        dataset, num_replicas=world_size, rank=rank, shuffle=False
    )
    data_loader = DataLoader(
        dataset, sampler=sampler, batch_size=batch_size, shuffle=False
    )

    results = []
    for index, input_ids in data_loader:
        with torch.no_grad():
            _output = model(input_ids.to(rank))
        results.extend(list(zip(index.tolist(), _output["logits"].flatten().tolist())))
    queue.put(results)

    dist.destroy_process_group()


def parallel_classify(
    texts: list,
    model_name_or_path: str = "liminghong/DNABERT-2-117M",
    lora_model_path: str = os.path.join(os.path.dirname(__file__), "adapter_model"),
    model_max_length: int = 1250,
    world_size: int = torch.cuda.device_count(),
    batch_size: int = 32,
    MASTER_ADDR: str = "localhost",
    MASTER_PORT: str = "12355",
):
    model, dataset = _get_model_and_dataset(
        model_name_or_path, lora_model_path, model_max_length, texts
    )

    os.environ["TOKENIZERS_PARALLELISM"] = "false"
    os.environ["MASTER_ADDR"] = MASTER_ADDR
    os.environ["MASTER_PORT"] = MASTER_PORT

    ctx = mp.get_context("spawn")
    queue = ctx.Queue()
    for i in range(world_size):
        p = ctx.Process(
            target=_ddp_inference,
            args=(i, world_size, queue, model, dataset, batch_size),
        )
        p.start()
    results = [queue.get() for _ in range(world_size)]

    results = list(itertools.chain(*results))
    results = (
        pd.DataFrame(results).drop_duplicates().sort_values(by=0)[1].values.tolist()
    )

    return results
