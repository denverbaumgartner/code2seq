#!/usr/bin/env bash

data_dir=$1
data_name=$(basename "${data_dir}")
data=${data_dir}/${data_name}
test=${data_dir}/${data_name}.val.c2s
run_name=$2
model_dir=models/sql-${run_name}
model_prefix=${model_dir}/model
save_prefix=${model_dir}/save
cuda=${3:-0}
seed=${4:-239}

mkdir -p "${model_dir}"
mkdir -p "${model_prefix}"
mkdir -p "${save_prefix}"
set -e
CUDA_VISIBLE_DEVICES=$cuda python -u code2seq.py \
  --data="${data}" \
  --test="${test}" \
  --model_path="${model_prefix}" \
  --save_path="${save_prefix}" \
  --seed="${seed}"