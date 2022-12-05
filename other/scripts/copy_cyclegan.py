import os
from shutil import copyfile
from itertools import product
import json
from PIL import Image
from collections import Counter

    # base = '/scratch/cek28/pytorch-CycleGAN-and-pix2pix/results'
    # out = '/scratch/cek28/jitter/wt/images/Cyclegan'

    # domains = ["EM", "NW", "SW"]
    # d = json.load(open("/scratch/cek28/jitter/wt/domain_overview.json", "r"))

    # for d1, d2 in product(domains, domains):
    #     combo = d1 + '_' + d2
    #     source = os.path.join(base, combo, 'test_latest', 'images')
    #     destination = os.path.join(out, combo)

    #     os.makedirs(destination, exist_ok=True)

    #     correct = set(d[d1]['Real'][:100])
    #     correct_copied = 0

    #     for img in os.listdir(source):
            
    #         img_path = os.path.join(source, img)

    #         tag = d1 + '_' + img.split("_")[1]
    #         img_final = os.path.join(destination, f'{tag}.jpg')

    #         if tag in correct:
    #             if 'fake_B' in img:
    #                 if len(img.split("_")) < 5:
    #                     img_png = Image.open(img_path)
    #                     img_png.save(img_final, quality=100)
    #                     #copyfile(img_path, img_final)
    #                     correct_copied += 1

    #     print(f'Copied {correct_copied} correctly for {combo}')

root = '/scratch/cek28/jitter/wt/images/'

domains = ["EM", "NW", "SW"]
d = json.load(open("/scratch/cek28/jitter/wt/domain_overview.json", "r"))

for d1, d2 in product(domains, domains):
    combo = d1 + '_' + d2
    source = os.path.join(root, 'CycadaJPG', combo)
    destination = os.path.join(root, 'Cycada', combo)

    os.makedirs(destination, exist_ok=True)

    correct = set(d[d1]['Real'][:100])
    correct_copied = 0

    for img in os.listdir(source):
        
        img_path = os.path.join(source, img)

        tag = img.split(".")[0]
        img_final = os.path.join(destination, f'{tag}.jpg')

        #print(tag)
        #print(tag in correct)
        if tag in correct:
            img_png = Image.open(img_path)
            img_png.save(img_final, quality=100)
            #copyfile(img_path, img_final)
            correct_copied += 1

    print(f'Copied {correct_copied} correctly for {combo}')





