#!/bin/bash

export CUDA_VISIBLE_DEVICES=4
export PYTHONPATH="/scratch/cek28/repro_bass/yolov3/:$PYTHONPATH"

python efficient_run_train_test.py --device 4 --supplemental_batch_size 0 --experiment Baseline
python efficient_run_train_test.py --device 4 --supplemental_batch_size 6 --experiment Optimal_Ratio_6

