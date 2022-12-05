import pandas as pd
from itertools import product
import os
import json
from collections import defaultdict
from argparse import ArgumentParser
import random
from pathlib import Path

def generate(root):
    f = open('/scratch/cek28/jitter/wt/domain_overview.json','r')
    domain_dict = json.load(f)
    f.close()

    types = ['Cyclegan']
    domains = ['NW','SW']

    domain_dict['Cyclegan'] = defaultdict(lambda: [])
    
    for s, t in [('EM','SW'), ('SW', 'EM')]:
        domain_dict['Cyclegan'][f's_{s}_t_{t}'] = []

        for f in [x.split(".")[0] for x in os.listdir(os.path.join(root, 'images', 'Cyclegan', f's_{s}_t_{t}')) if '.jpg' in x]:
            domain_dict['Cyclegan'][f's_{s}_t_{t}'].append(f)
        random.shuffle(domain_dict['Cyclegan'][f's_{s}_t_{t}'])

    # domain_dict = defaultdict(lambda: {
    #     'Test':[],
    #     'Real':[],
    #     'Synthetic':[],
    #     'Background': [],
    # })

    # for domain, type in product(domains, types):
    #     domain_dict[domain][type] = []         
    #     for f in [x.split(".")[0] for x in os.listdir(os.path.join(root, 'images', domain, type)) if '.jpg' in x]:
    #         domain_dict[domain][type].append(f)
    #     random.shuffle(domain_dict[domain][type])

    f = open('/scratch/cek28/jitter/domain_overview.json', 'w')
    json.dump(domain_dict, f)
    f.close()
    
if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument('-r', '--root',
                        help='root of the folder where images are found',
                        type=str,
                        default = '/scratch/cek28/jitter/wt/')
    args = parser.parse_args()
    generate(args.root)