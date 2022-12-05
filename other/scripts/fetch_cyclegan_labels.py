#import glob
import os
import glob
from shutil import copyfile
import re

cycle_dir = "/scratch/cek28/jitter/wt/images/Cyclegan"
cycle_labels_dir = "/scratch/cek28/jitter/wt/labels/Cyclegan"
labels_dir = "/scratch/cek28/jitter/wt/labels"

subdirs = [('EM', 's_EM_t_SW'),
           ('SW', 's_SW_t_EM')]

for dom, subdir in subdirs:
  cyclegan_images = os.path.join(cycle_dir, subdir)
  cyclegan_labels_out = os.path.join(cycle_labels_dir, subdir)
  if not os.path.exists(cyclegan_labels_out):
            os.makedirs(cyclegan_labels_out, exist_ok=True)

  for file in [x for x in os.listdir(cyclegan_images) if '.jpg' in x]:
    label_path = os.path.join(labels_dir, dom, 'Real',file.replace(".jpg", ".txt"))
    output_label = os.path.join(cyclegan_labels_out, file.replace(".jpg", ".txt"))
    copyfile(label_path, output_label)
