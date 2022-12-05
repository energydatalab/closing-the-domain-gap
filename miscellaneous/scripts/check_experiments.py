import os
from itertools import product

def check_experiment(root, experiment):
    def format(root, experiment, d1, d2, n):
        return os.path.join(root, experiment, f't_{d1}_v_{d2}_{n}', 'weights', 'results.txt')

    runs = []
    domains = ['SW','NW','EM']
    trials = ['0', '1', '2', '3']
    print(f'EXPERIMENT -- {experiment}\n')
    for d1, d2, n in product(domains, domains, trials):
        trial = format(root, experiment, d1, d2, n)

        try:
            with open(trial, "r") as f:
                lines = f.readlines()
                if len(lines) != 300:
                    print(experiment, d1, d2, n, len(lines))
                previous = -100
                for line in lines:
                    curr = int(line.strip().split("/")[0])
                    if curr < previous:
                        print(experiment, d1, d2, n, "OUT OF ORDER")
                        break
                    previous = curr

            
        except Exception as E:
            print(E)
            runs.append([experiment, d1, d2, n, 'DNE', True, True, 0])

    print('\n-----------------------------\n')

def process_all(root, experiments):
    for experiment in experiments:
        check_experiment(root, experiment)

if __name__ == "__main__":
    root = '/scratch/cek28/jitter/wt/experiment_results/1st'
    experiments = ['Color_Equalize_Domain_100', 'Cyclegan_100', 'Lower_Bound_100']
    process_all(root, experiments)