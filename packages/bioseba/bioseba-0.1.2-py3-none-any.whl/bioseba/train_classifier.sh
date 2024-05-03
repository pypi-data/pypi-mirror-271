num_gpu=4
DATA_PATH='/lmh_data/data/CDBGenerator/5kb/BPE'
MAX_LENGTH=1250
LR=1e-4

export OMP_NUM_THREADS=4
export TOKENIZERS_PARALLELISM="false"

# NotImplementedError: Using RTX 3090 or 4000 series doesn't support faster communication broadband via P2P or IB.
# Please set `NCCL_P2P_DISABLE="1"` and `NCCL_IB_DISABLE="1"` or use `accelerate launch` which will do this automatically.
export NCCL_P2P_DISABLE=1
export NCCL_IB_DISABLE=1

# if report to neptune, need to provide the following information and remove "#" on run_finetune.py:287.
# export NEPTUNE_API_TOKEN=""
# export NEPTUNE_PROJECT=""

torchrun --standalone --nnodes=1 --nproc_per_node=${num_gpu} run_finetune.py \
    --model_name_or_path /lmh_data/work/test/DNABERT-2-117M \
    --data_path  ${DATA_PATH} \
    --kmer -1 \
    --run_name DNABERT2_${DATA_PATH} \
    --model_max_length ${MAX_LENGTH} \
    --per_device_train_batch_size 8 \
    --per_device_eval_batch_size 32 \
    --learning_rate ${LR} \
    --num_train_epochs 12 \
    --save_steps 200 \
    --output_dir output/dnabert2 \
    --evaluation_strategy steps \
    --eval_steps 200 \
    --lr_scheduler_type cosine \
    --warmup_steps 400 \
    --logging_steps 100 \
    --overwrite_output_dir True \
    --log_level info \
    --use_lora True \
    --ddp_find_unused_parameters True \
    --lora_r 8 \
    --lora_alpha 16 \
    --lora_target_modules Wqkv,pooler,classifier \
    --modules_to_save pooler,classifier
