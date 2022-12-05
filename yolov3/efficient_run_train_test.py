from dataset import Dataset
import os
import subprocess
import itertools
import argparse
import pwd

parser = argparse.ArgumentParser()

parser.add_argument('--out_path', default='/scratch/cek28/jitter/wt/experiment_results/')
parser.add_argument('--train_path', default='/scratch/cek28/jitter/wt/experiments/')
parser.add_argument('--experiment')
parser.add_argument('--val_path', default='/scratch/cek28/jitter/wt/experiments/Test/')
parser.add_argument('--epochs', default='300')
parser.add_argument('--device')
parser.add_argument('--supplemental_batch_size', default='1')

args = parser.parse_args()

out_path = args.out_path
train_path = args.train_path
val_path = args.val_path
experiment = args.experiment
supplemental_batch_size =  args.supplemental_batch_size
experiment_path = os.path.join(train_path, experiment + "/")

datasets = []

domains = ["EM", "NW", "SW"]
trials = [0, 1, 2, 3, 4]
combinations = list(itertools.product(domains, domains, trials))

combinations = [("EM", "SW", 5)]

# iterate through domain + trial combinations
for src, dst, i in combinations:
  # first 5 trials are real trials vs rerun trial (after 5 runs)
  if i <= 4:
    num = i
    experiment_out_path = os.path.join(out_path, experiment + "/")
  else:
    num = i - 5
    experiment_out_path = os.path.join(out_path, "Reruns", experiment + "/",)

  dataset_string = """Dataset(img_txt=experiment_path+'Train_{src}_Test_{dst}_Images.txt',
                    lbl_txt=experiment_path+'Train_{src}_Test_{dst}_Labels.txt',
                    out_dir=experiment_out_path+'t_{src}_v_{dst}_{num}/',
                    img_txt_val=val_path+'{dst}_Images.txt',
                    lbl_txt_val=val_path+'{dst}_Labels.txt',
                    img_txt_supplement=experiment_path+'Train_{src}_Test_{dst}_Supplement_Images.txt',
                    lbl_txt_supplement=experiment_path+'Train_{src}_Test_{dst}_Supplement_Labels.txt')""".format(src=src,dst=dst,num=num)

  datasets.append(eval(dataset_string))

for trial in datasets:
  subprocess.run(['python', 'run_save_train_test.py',
                    '--img_list', trial.get_img_txt(), 
                    '--lbl_list', trial.get_lbl_txt(),
                    '--epochs', args.epochs,
                    '--out_dir', trial.get_out_dir(),
                    '--img_list_val', trial.get_img_txt_val(),
                    '--lbl_list_val', trial.get_lbl_txt_val(),
                    '--version', 'v2',
                    '--device', args.device,
                    '--experiment', experiment,
                    '--supplement_batch_size', supplemental_batch_size,
                    '--img_list_supplement', trial.get_img_txt_supplement(),
                    '--lbl_list_supplement', trial.get_lbl_txt_supplement()])