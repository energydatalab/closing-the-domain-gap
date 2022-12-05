import pandas as pd
from itertools import product
import os
import shutil
import json
from collections import defaultdict
from argparse import ArgumentParser
import random
from pathlib import Path
        
def fetch(csv_path, domain, action):
    df = pd.read_csv(csv_path)
    df = df.rename(columns={"HAS WIND TURBINE? (Y(1)/N(0))": "wt", "Image Name":"img"}).astype({"wt": "object"})
    df["img"] = df.apply(lambda x: x["img"].rstrip("' ").lstrip("' "), axis=1)    
    df["wt"] = df.apply(lambda x: str(x["wt"]), axis=1)
    yes = df[df['wt'] == '1']
    no = df[df['wt'] == '0']
    
    total = df.shape[0]
    num_real = yes.shape[0]
    num_bg = no.shape[0]
    num_bad = total - num_real - num_bg
    
    wt = list(yes["img"].values)
    bg = list(no["img"].values)

    for i, img in enumerate(wt):
        wt[i] = wt[i].split(".")[0]

    for i, img in enumerate(bg):
        bg[i] = bg[i].split(".")[0]

    print('-------------------------------------------------------')
    print(f'For {domain} {action} -- {total} Total -- {num_real} WT -- {num_bg} Background -- {num_bad} Faulty')
    return wt, bg 

def process(file_root, image_root, label_root, out_root, domain, action):
    csv_path = file_root + '/' + f'Wind Turbine Jitter - {domain} {action}.csv'
    curr_image_root = f'{image_root}/{domain}_{action.lower()}'
    curr_label_root = f'{label_root}/{domain}_{action.lower()}' 
    
    wt, bg = fetch(csv_path, domain, action)

    if action == 'Train':
        wtp = out_root + '/images/' + domain + '/Real'
        wtlp = out_root + '/labels/' + domain + '/Real'
    else:
        wtp = out_root + '/images/' + domain + '/Test'
        wtlp = out_root + '/labels/' + domain + '/Test'

    bgp = out_root + '/images/' + domain + '/Background'
    bglp = out_root + '/labels/' + domain + '/Background'

    os.makedirs(wtp, exist_ok=True)
    os.makedirs(wtlp, exist_ok=True)
    os.makedirs(bgp, exist_ok=True)
    os.makedirs(bglp, exist_ok=True)

    for img in [x for x in os.listdir(curr_image_root) if ('.jpg' in x) and (x[:-4] in bg)]:
        try:
            img_path = os.path.join(curr_image_root,img)
            lbl_path = os.path.join(curr_label_root, img.split(".")[0] + ".txt")
            if img[:-4] in wt:
                shutil.copy2(img_path, wtp)
                if Path(lbl_path).is_file():
                    shutil.copy2(lbl_path, wtlp)
                else:
                    print(f"Could not find:{img}, {domain} {action}")
                    with open(wtlp + '/' + img.split(".")[0] + ".txt", 'w') as fp:
                        pass
            elif img[:-4] in bg:
                shutil.copy2(img_path, bgp)
                with open(bglp + '/' + img.split(".")[0] + ".txt", 'w') as fp:
                    pass
        except Exception as e:
            print(e)
            
    wtc = len([x for x in os.listdir(wtp) if '.jpg' in x])
    bgc = len([x for x in os.listdir(bgp) if '.jpg' in x])
    wtlc = len([x for x in os.listdir(wtlp) if '.txt' in x])
    bglc = len([x for x in os.listdir(bglp) if '.txt' in x])

    print(f'WT Images: {len(wt)}, Copied: {wtc} -- BG: {len(bg)}, Copied: {bgc}')
    print(f'WT Labels: {len(wt)}, Copied: {wtlc} -- BG: {len(bg)}, Copied: {bglc}')
    
def process_all(file_root, image_root, label_root, out_root):
    actions = ['Train', 'Test']
    domains = ['EM', 'NE', 'NW', 'SW', 'MW']
    for domain, action in product(domains, actions):         
        process(file_root, image_root, label_root, out_root, domain, action)
    
if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument('-i', '--image_root',
                        help='root of the folder where images are found',
                        type=str)
    parser.add_argument('-l', '--label_root',
                        help='root of the folder where labels are found',
                        type=str)
    parser.add_argument('-o', '--output_root',
                        help='path to output directory',
                        type=str)
    parser.add_argument('-c', '--csv_paths',
                        help='path to directory with csvs of annotations',
                        type=str)
    
    args = parser.parse_args()
    process_all(args.csv_paths, args.image_root, args.label_root, args.output_root)