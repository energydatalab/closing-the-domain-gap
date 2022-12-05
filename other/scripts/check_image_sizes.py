import os
import glob
from itertools import product
from PIL import Image

domains = ["SW", "NW", "EM", "MW", "NE"]
image_dir = "/scratch/cek28/jitter/wt/images/"
actions = ["Real","Test", "Background"]
output_file = "/scratch/cek28/jitter/wt/other/scripts/checked_images.txt"

def check_files(domains, image_dir, actions, output_file):

    bad_size = []

    for domain in domains:
        for action in actions:
            current_directory = os.path.join(image_dir, domain, action)
            current_image_files = glob.glob(current_directory + "/*.jpg")

            for img in current_image_files:
                curr = Image.open(img)
                if curr.size != (608,608):
                    bad_size.append(f'{img}' + '\n')

    with open(output_file, "w") as f:
        f.writelines(bad_size)
    
                        
check_files(domains, image_dir, actions, output_file)