from argparse import ArgumentParser
import os
from itertools import product
import pandas as pd
import shutil
from pathlib import Path

def move_NW():
    out_imgs = os.path.join('/scratch/cek28/jitter/wt', 'images', 'NW', 'Background')
    out_lbls = os.path.join('/scratch/cek28/jitter/wt', 'labels', 'NW', 'Background')
    image_root = '/scratch/cek28/images/jitter/NW_Background_extra'

    imgs = [x[:-4] for x in os.listdir(image_root) if '.jpg' in x]
    lbls = imgs

    for img in imgs:
        img_path = os.path.join(image_root, f'{img}.jpg')
        out_img_path = os.path.join(out_imgs, f'{img}_6000.jpg')
        shutil.copy2(img_path, out_img_path)
    
    for lbl in imgs:
        lbl_path = os.path.join(out_lbls, f'{lbl}_6000.txt')
        with open(lbl_path, 'w') as f:
                pass
def move():
    domains = ['NW']

    image_root = '/scratch/cek28/images/jitter'
    out_root = '/scratch/cek28/jitter/wt'

    df = pd.read_csv('/scratch/cek28/jitter/wt/wt_csvs/additional_background/Wind Turbine Jitter - background.csv')

    for dom in domains:
        curr_dom = pd.DataFrame(df[dom].dropna())
        imgs = curr_dom.apply(lambda x: x[dom].rstrip("' ").lstrip("' ").split(".")[0], axis=1).values
        lbls = imgs

        out_imgs = os.path.join(out_root, 'images', dom, 'Background')
        out_lbls = os.path.join(out_root, 'labels', dom, 'Background')

        os.makedirs(out_imgs, exist_ok=True)
        os.makedirs(out_lbls, exist_ok=True)

        for img in imgs:
            img_path = os.path.join(image_root, f'{dom}_Background', f'{img}.jpg')
            shutil.copy2(img_path, out_imgs)
        
        for lbl in lbls:
            lbl_path = os.path.join(out_lbls, f'{lbl}.txt')
            with open(lbl_path, 'w') as f:
                pass

if __name__ == "__main__":
    move_NW()



