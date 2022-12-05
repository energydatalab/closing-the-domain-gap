import os
import glob
from itertools import product
from PIL import Image
import random
from PIL import Image
from skimage.io import imread, imsave

def crop_image(img, new_squared_size: int, random_crop: bool, rdist:int):
    """crop the center of the image a defined squared size
       bool random_crop for randomly cropping the image by shifting size rdist in them
       horizontal and vertical directions"""

    # get current dimensions
    width, height = img.size
    # crop image
    new_width = new_squared_size
    new_height = new_width
    
    # handle the case of random cropping by initializing horizontal and vertical shifts
    hshift = 0
    vshift = 0
    if random_crop:
        hshift = random.randint(-rdist, rdist)
        vshift = random.randint(-rdist, rdist)
    
    # https://stackoverflow.com/questions/16646183/crop-an-image-in-the-centre-using-pil.
    left = (width - new_width)/2 + hshift
    top = (height - new_height)/2 + vshift
    right = (width + new_width)/2 + hshift
    bottom = (height + new_height)/2 + vshift
    img = img.crop((left, top, right, bottom))
    return img

def crop_background(txt_path):
    f = open(txt_path, 'r')
    imgs = f.read().split('\n')
    imgs[:] = [x for x in imgs if x != '']

    for img in imgs:
        curr = Image.open(img)
        processed = crop_image(curr, 608, False, 0)
        processed.save(img)
    
                        
crop_background("/scratch/cek28/jitter/wt/other/scripts/checked_images.txt")
