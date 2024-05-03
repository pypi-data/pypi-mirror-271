import os

import click
import gdown
import pandas as pd
import torch
from tqdm import tqdm

from bioseba.DNAGPT.dna_gpt.model import DNAGPT
from bioseba.DNAGPT.dna_gpt.tokenizer import KmerTokenizer
from bioseba.DNAGPT.dna_gpt.utils import seed_all_rng
from bioseba.util import classify, read_fa


@click.group()
def cli():
    pass


@cli.command()
@click.option("--data_dir_path", help="Folder path for boundary files", type=str)
@click.option("--fasta_path", type=str)
@click.option("--output_path", type=str)
def get_sequence_seed(data_dir_path, fasta_path, output_path):
    file_paths = [
        os.path.join(data_dir_path, file)
        for _, _, files in os.walk(data_dir_path, topdown=False)
        for file in files
    ]

    datas = pd.DataFrame()
    for file_path in tqdm(file_paths):
        _data = pd.read_csv(
            file_path,
            compression="gzip",
            sep="\t",
            header=None,
            names=["chrom", "start", "end", "level", "score"],
        )
        _data["source"] = os.path.splitext(os.path.basename(file_path))[0]
        datas = pd.concat([datas, _data])
    datas = datas.set_index(["chrom", "start", "end", "source"])

    fa_dic = read_fa(fasta_path)

    def _generate_target(series):
        chrom, start, end, source = series.name
        return fa_dic[chrom][start:end]

    datas["target"] = datas.apply(_generate_target, axis=1)

    def _generate_sequence(series):
        flank_len = 100
        chrom, start, end, source = series.name
        return fa_dic[chrom][start : start + flank_len]

    datas["sequence"] = datas.apply(_generate_sequence, axis=1)

    datas = datas[~datas["sequence"].str.contains("N")]
    datas = datas[~datas["target"].str.contains("N")]

    count = datas.groupby(["target"]).size().reset_index(name="counts")
    count = count[count["counts"] > 10]
    datas = pd.merge(count, datas, on=["target"], how="left").drop_duplicates(
        subset="target"
    )

    datas.to_csv(output_path, sep="\t")


def get_model(model_name):
    special_tokens = (
        ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
        + ["+", "-", "*", "/", "=", "&", "|", "!"]
        + ["M", "B"]
        + ["P"]
        + ["R", "I", "K", "L", "O", "Q", "S", "U", "V"]
        + ["W", "Y", "X", "Z"]
    )
    if model_name in ("dna_gpt0.1b_h",):
        tokenizer = KmerTokenizer(6, special_tokens, dynamic_kmer=False)
    else:
        tokenizer = KmerTokenizer(6, special_tokens, dynamic_kmer=True)

    vocab_size = len(tokenizer)
    model = DNAGPT.from_name(model_name, vocab_size)
    return model, tokenizer


def load_model(model, weight_path, device=None, dtype=None):
    state = torch.load(weight_path, map_location="cpu")
    if "model" in state.keys():
        model.load_state_dict(state["model"], strict=False)
    else:
        model.load_state_dict(state, strict=False)
    print(f"loading model weights from {weight_path}")
    model.to(device=device, dtype=dtype)
    model = model.eval()
    return model


def generate(
    model,
    tokenizer,
    prompt,
    max_len=256,
    num_samples=1,
    temperature=1.0,
    top_k=0,
    top_p=0,
):
    print(f"max length is {max_len}")
    device = next(model.parameters()).device
    prompt_ids = tokenizer.encode(prompt, max_len=max_len, device=device)
    print(f"prompt token ids: {prompt_ids.tolist()}")
    max_new_tokens = max_len - len(prompt_ids)
    outputs = []
    for k in tqdm(range(num_samples)):
        x = prompt_ids[None, :]
        y = model.generate(
            x,
            max_new_tokens,
            temperature=temperature,
            top_k=top_k,
            top_p=top_p,
            do_sample=True,
            stop_ids=(tokenizer.unk_id, tokenizer.pad_id),
        )
        output = tokenizer.decode(y[0].tolist())
        output = output[len(prompt) :]
        outputs.append(output)
    return outputs


DEFAULT_G_MODEL = {
    "dna_gpt0.1b_h.pth": {
        "path": os.path.join(
            os.path.dirname(__file__), "DNAGPT/checkpoints/dna_gpt0.1b_h.pth"
        ),
        "url": "https://drive.google.com/uc?id=15m6CH3zaMSqflOaf6ec5VPfiulg-Gh0u",
    },
    "dna_gpt0.1b_m": {
        "path": os.path.join(
            os.path.dirname(__file__), "DNAGPT/checkpoints/dna_gpt0.1b_m.pth"
        ),
        "url": "https://drive.google.com/uc?id=1C0BRXfz7RNtCSjSY1dKQeR1yP7I3wTyx",
    },
    "dna_gpt3b_m.pth": {
        "path": os.path.join(
            os.path.dirname(__file__), "DNAGPT/checkpoints/dna_gpt3b_m.pth.pth"
        ),
        "url": "https://drive.google.com/uc?id=1pQ3Ai7C-ObzKkKTRwuf6eshVneKHzYEg",
    },
}


@cli.command()
@click.option("--seed_path", type=str)
@click.option(
    "--num_samples", type=int, default=100, help="number samples of generation"
)
@click.option("--output_path", type=str)
@click.option("--random_state", type=int, default=42)
@click.option("--g_model_name", type=str, default="dna_gpt0.1b_m")
@click.option(
    "--g_weight_path", type=str, default=DEFAULT_G_MODEL["dna_gpt0.1b_m"]["path"]
)
@click.option("--g_max_len", type=int, default=512)
@click.option("--g_temperature", type=float, default=1.0, help="sample temperature")
@click.option("--g_topk", type=int, default=0, help="sample topk")
@click.option("--g_topp", type=float, default=0.95, help="sample topp")
@click.option("--c_model_name_or_path", type=str, default="liminghong/DNABERT-2-117M")
@click.option(
    "--c_lora_model_path",
    type=str,
    default=os.path.join(os.path.dirname(__file__), "adapter_model"),
)
@click.option("--c_max_len", type=int, default=1250)
def generate_sequence(
    seed_path,
    num_samples,
    output_path,
    random_state,
    g_model_name,
    g_weight_path,
    g_max_len,
    g_temperature,
    g_topk,
    g_topp,
    c_model_name_or_path,
    c_lora_model_path,
    c_max_len,
):
    seeds = pd.read_csv(seed_path, sep="\t", index_col=0)
    seed = seeds.sample(n=1, random_state=random_state)

    torch.set_grad_enabled(False)
    seed_all_rng(random_state)

    if g_model_name in DEFAULT_G_MODEL.keys():
        _info = DEFAULT_G_MODEL[g_model_name]
        if g_weight_path == _info["path"] and not os.path.exists(_info["path"]):
            gdown.download(_info["url"], _info["path"])

    prompt = "<R>" + seed["sequence"].item()
    model, tokenizer = get_model(g_model_name)
    model = load_model(model, g_weight_path, device="cuda", dtype=torch.float16)
    texts = generate(
        model,
        tokenizer,
        prompt,
        max_len=min(g_max_len, model.max_len),
        num_samples=num_samples,
        temperature=g_temperature,
        top_k=g_topk,
        top_p=g_topp,
    )

    scores = classify(texts, c_model_name_or_path, c_lora_model_path, c_max_len)
    predict_results = pd.DataFrame({"text": texts, "score": scores})
    predict_results = predict_results.sort_values(by="score", ascending=False)
    predict_results.to_csv(output_path)


if __name__ == "__main__":
    cli()
