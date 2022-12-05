import os
import shutil
import json
import random

def fetch(base, technique, train, test, img):
    supplemental = os.path.join(base, technique, f'Train_{train}_Test_{test}_Supplement_Images.txt')
    with open(supplemental, 'r') as f:
        lines = f.readlines()
        for line in lines:
            if img in line:
                return line.rstrip()
    print(f"No image found for {technique} {train} {test} {img}")

def process_all(techniques, domain_pairs, base, out, domain_dict):
    os.mkdir(out)
    paths = open(os.path.join(out, 'image_paths.txt'), 'w')

    for train, test in domain_pairs:
        img = random.choice(domain_dict[test]['Background'][:100])
        for technique in techniques:
            technique_example = fetch(base, technique, train, test, img)
            paths.write(technique_example + '\n')
            image_name = technique + '_' + technique_example.split("/")[-1]
            shutil.copy(technique_example, os.path.join(out, image_name))
    
    paths.close()

if __name__ == "__main__":
    techniques = ['Baseline', 'Color_Equalize_Domain', 'Cycada', 'Cyclegan', 'Gray_World', 'Histogram_Matching']
    techniques = ['Lower_Bound', 'Optimal_Ratio_1']
    domain_pairs = [("NW", "EM"), ("NW", "SW"), ("SW", "EM"), ("SW", "SW"), ("EM", "NW")]
    base = '/scratch/cek28/jitter/wt/experiments'
    out = '/scratch/cek28/jitter/wt/other/background_technique_examples'
    domain_dict = json.load(open('/scratch/cek28/jitter/wt/domain_overview.json', 'r'))
    process_all(techniques, domain_pairs, base, out, domain_dict)
    
