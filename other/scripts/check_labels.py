import os
import glob

domains = ["NW", "SW"]
label_dir = "/scratch/cek28/jitter/wt/labels/"
actions = ["Real","Test"]
output_file = "/scratch/cek28/jitter/wt/other/scripts/checked.txt"

def check_files(domains, label_dir, actions, output_file):
    """
    
    Args:
        reg_file ([type]): 
    """
    no_lbls = []

    for domain in domains:
        for action in actions:
            current_directory = os.path.join(label_dir, domain, action)
            current_lbl_files = glob.glob(current_directory + "/*.txt")
            for lbl in current_lbl_files:
                with open(lbl, 'r') as f:
                    lines = f.read().split('\n')
                    lines[:] = [x for x in lines if x != '']
                    lines_len = len(lines)
                    if lines_len == 0:
                        no_lbls.append(lbl + "\n")

    with open(output_file, "w") as f:
        f.writelines(no_lbls)
    
    
                        
check_files(domains, label_dir, actions, output_file)