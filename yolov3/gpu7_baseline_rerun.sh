#!/bin/bash

export CUDA_VISIBLE_DEVICES=7
export PYTHONPATH="/scratch/cek28/repro_bass/yolov3/:$PYTHONPATH"

python efficient_run_train_test.py --device 7 --supplemental_batch_size 1 --experiment Baseline