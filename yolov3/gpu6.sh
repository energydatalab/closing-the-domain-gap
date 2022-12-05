#!/bin/bash

export CUDA_VISIBLE_DEVICES=6
export PYTHONPATH="/scratch/cek28/repro_bass/yolov3/:$PYTHONPATH"

python efficient_run_train_test.py --device 6 --supplemental_batch_size 1 --experiment Cycada
python efficient_run_train_test.py --device 6 --supplemental_batch_size 8 --experiment Optimal_Ratio_8