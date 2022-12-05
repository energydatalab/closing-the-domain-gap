import pandas as pd
import json
import random

f = open('domain_overview.json','r')
domain_dict = json.load(f)
f.close()

domains = ['EM', 'NE', 'NW', 'SW', 'MW']
df = pd.read_csv('/scratch/cek28/jitter/wt/wt_csvs/additional_background/Wind Turbine Jitter - background.csv')

for dom in domains:
    curr_dom = pd.DataFrame(df[dom].dropna())
    imgs = curr_dom.apply(lambda x: x[dom].rstrip("' ").lstrip("' ").split(".")[0], axis=1).values
    random.shuffle(imgs)
    domain_dict[dom]['Background'].extend(imgs)

f = open('domain_overview.json', 'w')
json.dump(domain_dict, f)
f.close()