from argparse import ArgumentParser
import os
from itertools import product
import pandas as pd
import shutil
from pathlib import Path

def num2img(image_root, domain, action, number):
    return os.path.join(image_root, f'{domain}_{action.lower()}/{domain}_{number}.jpg')

def num2lbl(label_root, domain, action, number):
    return os.path.join(label_root, f'{domain}_{action.lower()}/{domain}_{number}.txt')

def move():
    domains = ['SW','NW']
    actions = ['Train', 'Test']
    image_root = '/scratch/cek28/images/jitter'
    label_root = '/scratch/cek28/labels/jitter'
    out_root = '/scratch/cek28/jitter/wt/'

    for dom, action in product(domains, actions):
        curr = pd.read_csv(f'../reclustering_2/{dom}_{action.lower()}_coord.csv')
        imgs = curr['ID'].values
        lbls = curr['ID'].values

        out_imgs = os.path.join(out_root, 'images', dom, action)
        out_lbls = os.path.join(out_root, 'labels', dom, action)

        os.makedirs(out_imgs, exist_ok=True)
        os.makedirs(out_lbls, exist_ok=True)

        for img in imgs:
            train = num2img(image_root, dom, 'Train', img)
            test = num2img(image_root, dom, 'Test', img)
            if Path(train).is_file():
                shutil.copy2(train, out_imgs)
            else:
                shutil.copy2(test, out_imgs)
        
        for lbl in lbls:
            train = num2lbl(label_root, dom, 'Train', lbl)
            test = num2lbl(label_root, dom, 'Test', lbl)
            if Path(train).is_file():
                shutil.copy2(train, out_lbls)
            else:
                shutil.copy2(test, out_lbls)

if __name__ == "__main__":
    move()



