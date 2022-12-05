import pandas as pd
import os
import json


def load_data():
    nw = pd.read_csv('NW.csv')
    em = pd.read_csv('EM.csv')
    sw = pd.read_csv('SW.csv')

    def convert_to_num(df):
        processed = list(set(df[(df['Turbine Overlap'] == 'Y') | (df['Background Overlap'] == 'Y')]['Train'].values))
        processed = [x.split(".")[0] for x in processed]
        return processed

    nw, em, sw = convert_to_num(nw), convert_to_num(em), convert_to_num(sw)        

    d = json.load(open("/scratch/cek28/jitter/wt/domain_overview.json", "r"))

    return nw, em, sw, d

def num2img(root, domain, action, numbers):
    return [os.path.join(root, 'images', f'{domain}/{action}/{_}.jpg') for _ in numbers]

def num2lbl(root, domain, action, numbers):
    return [os.path.join(root, 'labels', f'{domain}/{action}/{_}.txt') for _ in numbers]

def remove(paths):
    for path in path:
        os.remove(path)

def remove_from_json(d, domain, action, numbers):
    for number in numbers:
        d[domain][action].remove(number)
    return d

def process_all():
    nw, em, sw, d = load_data()
    root = '/scratch/cek28/jitter/wt/'

    domains = [('NW', nw),
               ('EM', em),
               ('SW', sw)]

    for domain, numbers in domains:
        im_paths = num2img(root, domain, 'Real', numbers)
        lbl_paths = num2lbl(root, domain, 'Real', numbers)
        shadow_lbl_paths = num2lbl(root, domain, 'Real_Shadow', numbers)
        
        d = remove_from_json(d, domain, 'Real', numbers)

        for path in im_paths:
            os.remove(path)

        for path in lbl_paths:
            os.remove(path)
        
        for path in shadow_lbl_paths:
            os.remove(path)
    
    f = open("/scratch/cek28/jitter/wt/domain_overview.json", "w")
    json.dump(d, f)
    f.close()





