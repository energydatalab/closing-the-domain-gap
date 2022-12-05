import os
from itertools import product
import pandas as pd
from collections import defaultdict

def scrape(trial, test, experiment, d1, d2, n):
    num_lines = 300
    full = True
    in_order = True
    mAP = -10
        
    with open(trial, "r") as f:
        lines = f.readlines()
            
        # Check that the correct number of epochs has been run
        num_lines = len(lines)
        if num_lines != 300:
            full = False
            print(experiment, d1, d2, n, num_lines)
        previous = -100

        # Check that the epochs were in order
        for line in lines:
            curr = int(line.strip().split("/")[0])
            if curr < previous:
                in_order = False
                print(experiment, d1, d2, n, "OUT OF ORDER")
                break
            previous = curr

    # Gather the mAP
    with open(test, "r") as f:
        lines = f.readlines()
        mAP = float(lines[2].strip())

    return [experiment, d1, d2, n, mAP, in_order, full, num_lines]

def scrape_experiment(root, experiment):
    def format_results(root, experiment, d1, d2, n):
        return os.path.join(root, experiment, f't_{d1}_v_{d2}_{n}', 'weights', 'results.txt')

    def format_test_results(root, experiment, d1, d2, n):
        return os.path.join(root, experiment, f't_{d1}_v_{d2}_{n}', 'weights', 'test_results.txt')

    domains = ['EM','NW','SW']
    trials = ['0', '1', '2', '3', '4']
    experiment_results = []

    print(f'EXPERIMENT -- {experiment}\n')
    for d1, d2, n in product(domains, domains, trials):
        try:
            trial = format_results(root, experiment, d1, d2, n)
            test = format_test_results(root, experiment, d1, d2, n)
            result = scrape(trial, test, experiment, d1, d2, n)
            experiment_results.append(result)
        except Exception as E:
            #print(E)
            experiment_results.append([experiment, d1, d2, n, 'DNE', False, False, 0])

    print('\n-----------------------------\n')

    return experiment_results

def process(root, experiments):

    # process each experiment
    all_experiments = []

    for experiment in experiments:
        # check current
        curr_experiment = scrape_experiment(root, experiment)
        all_experiments.extend(curr_experiment)

    exp = pd.DataFrame(all_experiments)
    exp.columns = ['Experiment', 'Source_Domain', 'Test_Domain', 'Trial_Number', 'mAP', 'Epochs_In_Order', 'Completed', 'Number_Epochs_Completed']
    exp.to_csv(os.path.join(root, 'results.csv'), index=False)

def process_all(root, experiments):
    process(root, experiments)
    process(os.path.join(root, 'Reruns'), experiments)

    results = pd.read_csv(os.path.join(root, 'results.csv'))

    reruns = pd.read_csv(os.path.join(root, 'Reruns', 'results.csv'))
    final_results = []

    used = defaultdict(lambda: 0)

    for i, row in results.iterrows():
        if row['Epochs_In_Order'] and row['Completed']:
            final_results.append(list(row.values) + [False, 'DNE'])
            continue

        experiment, s, t = row["Experiment"], row["Source_Domain"], row["Test_Domain"]
        trial_string = f'{experiment}_{s}_{t}'
        iteration = used[trial_string]

        found = False
        for j in range(iteration, 5):
            rerun = reruns[(reruns.Experiment == experiment) & 
                            (reruns.Source_Domain == s) & 
                            (reruns.Test_Domain == t) & 
                            (reruns.Trial_Number == j)].iloc[0]
            
            used[trial_string] = j + 1

            if rerun['Completed'] and rerun['Epochs_In_Order']:
                format_rerun = [experiment, s, t, row["Trial_Number"], rerun['mAP'], rerun['Epochs_In_Order'], 
                                rerun['Completed'], rerun['Number_Epochs_Completed'], True, 
                                f'{experiment}_{s}_{t}_{j}']
                final_results.append(format_rerun)
                found = True
                break
        if found == False:
            final_results.append(list(row.values) + [False, 'No Rerun Found'])
    
    cols = ['Experiment', 'Source_Domain', 'Test_Domain', 'Trial_Number', 'mAP', 
            'Epochs_In_Order', 'Completed', 'Number_Epochs_Completed', 'Is_Rerun', 'Rerun_Title']
    final = pd.DataFrame(final_results)
    final.columns = cols

    final.to_csv(os.path.join(root, 'final.csv'), index=False)

if __name__ == "__main__":
    root = '/scratch/cek28/jitter/wt/experiment_results/'
    experiments = ['Baseline', 'Upper_Bound', 'Cycada', 'Cyclegan', 'Lower_Bound', 'Histogram_Matching', 'Gray_World', 'Color_Equalize_Domain', 'Optimal_Ratio_1', 'Optimal_Ratio_2', 'Optimal_Ratio_3', 'Optimal_Ratio_4', 'Optimal_Ratio_5', 'Optimal_Ratio_6', 'Optimal_Ratio_7', 'Optimal_Ratio_8']
    process_all(root, experiments)