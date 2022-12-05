import random
import os.path
import json
import torchvision.transforms as transforms
from data.base_dataset import BaseDataset
import scipy.io
import numpy as np
from skimage import io
from PIL import Image
from PIL.ImageOps import invert

class WTDataset(BaseDataset):
    def name(self):
        return 'WTDataset'
    def initialize(self, opt):
        self.opt = opt
        self.root = opt.dataroot
        print(opt)

        # Get the image folders and labels folders
        source_img_dir = os.path.join(opt.dataroot, 'wt','images', opt.source_domain,'Real')
        source_background_img_dir = os.path.join(opt.dataroot, 'wt','images',opt.source_domain,'Background')
        target_img_dir = os.path.join(opt.dataroot, 'wt','images', opt.target_domain,'Background')
        source_lbl_dir = source_img_dir.replace('images','labels')
        target_lbl_dir = target_img_dir.replace('images','labels')

        # Read in the domain_overview
        domains = json.load(open("domain_overview.json", "r"))
        source_nums = set(domains[opt.source_domain]['Real'][:opt.source_number])
        source_background_nums = set(domains[opt.source_domain]['Background'][:opt.source_background_number])
        target_nums = set(domains[opt.target_domain]['Background'][:opt.target_number])

        # Read the list of images (for both source and target domain)
        source_imgs, target_imgs = [], []
        source_paths, target_paths = [], []
        self.source_label, self.target_label = [], []

        # Add the img with target
        for file in os.listdir(source_img_dir):
           if file.split(".")[0] in source_nums:
                source_paths.append(os.path.join(source_img_dir, file))
                self.source_label.append(1)

        # Add the img using background
        for file in os.listdir(source_background_img_dir):
            if file.split(".")[0] in source_background_nums:
                source_paths.append(os.path.join(source_background_img_dir, file))
                self.source_label.append(0)

        # For target images
        for file in os.listdir(target_img_dir):
            if file.split(".")[0] in target_nums:
                target_paths.append(os.path.join(target_img_dir, file))
                self.target_label.append(0)

        # Get them to self
        self.source_paths = source_paths
        self.target_paths = target_paths

        self.transform = transforms.Compose([
            transforms.Resize(size=(608,608)),
            transforms.ToTensor(),
            transforms.Normalize((0.5, 0.5, 0.5),
                                 (0.5, 0.5, 0.5))])
        # Shuffle the source indices
        temp = list(zip(self.source_paths, self.source_label))
        random.shuffle(temp)
        res1, res2 = zip(*temp)
        res1, res2 = list(res1), list(res2)
        self.source_paths = res1
        self.source_label = res2
       
        # Shuffle the target indices
        temp = list(zip(self.target_paths, self.target_label))
        random.shuffle(temp)
        res1, res2 = zip(*temp)
        res1, res2 = list(res1), list(res2)
        self.target_paths = res1
        self.target_label = res2

        self.source_label = np.array(self.source_label).astype('int')
        self.target_label = np.array(self.target_label).astype('int')

        self.A_size = len(self.source_paths)
        self.B_size = len(self.target_paths)

    def __getitem__(self, index):
        A_path = self.source_paths[index % self.A_size]
        if self.opt.serial_batches:
            index_B = index % self.B_size
        else:
            index_B = random.randint(0, self.B_size - 1)
        B_path = self.target_paths[index_B]

        A_img  = self.transform(Image.open(A_path))
        B_img = self.transform(Image.open(B_path))
        
        item = {}
        item.update({'A': A_img,
                     'A_paths': A_path
                 })
        
        item.update({'B': B_img,
                     'B_paths': B_path
                 })
        return item
    
    def __len__(self):
        return max(self.A_size, self.B_size)