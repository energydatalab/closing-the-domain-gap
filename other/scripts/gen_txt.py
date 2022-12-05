from argparse import ArgumentParser
import random
import os
from itertools import product
import json

def select_imgs(action, number, root, domain, domain_dict, test=False):
    if action == 'Real' and test == True:
        numbers = domain_dict[domain][action][100: 100 + number]
    elif 'Real' in action:
        numbers = domain_dict[domain]['Real'][:number]
    elif action in ['Background', 'Synthetic']:
        numbers = domain_dict[domain][action][:number]
    
    imgs = num2img(root, domain, action, numbers)
    lbls = num2lbl(root, domain, action, numbers)

    if 'Real' in action:
        lbls = num2lbl(root, domain, 'Real', numbers)

    return imgs, lbls

def select_synthetic(number, train_domain, test_domain, root, domain_dict):
    key = f's_{train_domain}_t_{test_domain}'
    numbers = domain_dict['Synthetic'][key][:number]
    c = [os.path.join(root, 'images', 'Synthetic', f'{key}/{_}.jpg') for _ in numbers]
    cl = [os.path.join(root, 'labels', 'Synthetic', f'{key}/{_}.txt') for _ in numbers]
    return c, cl

def select_cyclegan(number, train_domain, test_domain, root, domain_dict):
    key = f'{train_domain}_{test_domain}'
    numbers = domain_dict[train_domain]['Real'][:number]
    imgs = [os.path.join(root, 'images', 'Cyclegan', f'{key}/{_}.jpg') for _ in numbers]
    lbls = [os.path.join(root, 'labels', train_domain, 'Real', f'{_}.txt') for _ in numbers]
    return imgs, lbls

def select_cycada(number, train_domain, test_domain, root, domain_dict):
    key = f'{train_domain}_{test_domain}'
    numbers = domain_dict[train_domain]['Real'][:number]
    imgs = [os.path.join(root, 'images', 'Cycada', f'{key}/{_}.jpg') for _ in numbers]
    lbls = [os.path.join(root, 'labels', train_domain, 'Real', f'{_}.txt') for _ in numbers]
    return imgs, lbls

def select_histogram_matching_domain(number, train_domain, test_domain, root, domain_dict):
    key = f'Real_Histogram_Matching_Domain_{test_domain}'
    numbers = domain_dict[train_domain]['Real'][:number]
    imgs = [os.path.join(root, 'images', train_domain, f'{key}/{_}.jpg') for _ in numbers]
    lbls = [os.path.join(root, 'labels', train_domain, 'Real', f'{_}.txt') for _ in numbers]
    return imgs, lbls

def num2img(root, domain, action, numbers):
    return [os.path.join(root, 'images', f'{domain}/{action}/{_}.jpg') for _ in numbers]

def num2lbl(root, domain, action, numbers):
    return [os.path.join(root, 'labels', f'{domain}/{action}/{_}.txt') for _ in numbers]

def make_data_file(experiment_root, train_domain, test_domain, train_images_out, test_images_out, supplementary_images_out):
    try:
        f = open(os.path.join(experiment_root, f'Train_{train_domain}_Test_{test_domain}.data'), 'r+')
        f.truncate(0)
    except:
        pass

    with open(os.path.join(experiment_root, f'Train_{train_domain}_Test_{test_domain}.data'), 'w') as f:                                    
        f.write('train=' + train_images_out+ '\n')
        f.write('classes=1\n')
        f.write('valid=' + test_images_out + '\n')
        f.write('supplement=' + supplementary_images_out + '\n')
        f.write('names=./data/wnd.names\n')
        f.write('backup=backup/\n')
        f.write('eval=wnd')

def make_txt_file(path, objects):
    f = open(path,'w')
    f.writelines(line + '\n' for line in objects[:-1])
    f.write(objects[-1])
    f.close

def make_shapes_file(path, length):
    f = open(path,'w')
    f.writelines('608 608\n' for line in range(length-1))
    f.write('608 608')
    f.close

def generate_txt(output_root, real, synthetic, background, test_background, test_real, cyclegan, cycada, gray_equalize_domain, gray_equalize_individual, color_equalize_domain, color_equalize_individual, gray_world_domain, supplement_real, real_histogram_matching_domain, experiment, root, domain_dict):
    domains = ['SW', 'NW', 'EM']
    experiment_root = output_root + '/' + experiment

    os.makedirs(output_root + '/' + experiment, exist_ok=True)
    
    for train_domain, test_domain in product(domains, domains):

        # Get correct paths
        train_images_out = output_root + '/' + experiment + '/' + f'Train_{train_domain}_Test_{test_domain}_Images.txt'
        train_labels_out = output_root + '/' + experiment  + '/' + f'Train_{train_domain}_Test_{test_domain}_Labels.txt'
        supplement_images_out = output_root + '/' + experiment + '/' + f'Train_{train_domain}_Test_{test_domain}_Supplement_Images.txt'
        supplement_labels_out = output_root + '/' + experiment + '/' + f'Train_{train_domain}_Test_{test_domain}_Supplement_Labels.txt'

        train_shapes_out = output_root + '/' + experiment + '/' + f'Train_{train_domain}_Test_{test_domain}_Images.shapes'
        supplement_shapes_out = output_root + '/' + experiment + '/' + f'Train_{train_domain}_Test_{test_domain}_Supplement_Images.shapes'

        # Get correct real images and labels
        train_imgs, train_lbls = select_imgs('Real', real, root, train_domain, domain_dict)
        
        # Here we generate the supplement labels
        supplement_imgs, supplement_lbls = [], []

        if test_real > 0:
            imgs, lbls = select_imgs('Real', test_real, root, test_domain, domain_dict, test=True)
            supplement_imgs.extend(imgs)
            supplement_lbls.extend(lbls)   

        if test_background > 0:
            imgs, lbls = select_imgs('Background', test_background, root, test_domain, domain_dict, test=True)
            supplement_imgs.extend(imgs)
            supplement_lbls.extend(lbls)
        
        if supplement_real > 0:
            imgs, lbls = select_imgs('Real', supplement_real, root, train_domain, domain_dict)
            supplement_imgs.extend(imgs)
            supplement_lbls.extend(lbls)

        if cyclegan > 0:
            imgs, lbls = select_cyclegan(cyclegan, train_domain, test_domain, root, domain_dict)
            supplement_imgs.extend(imgs)
            supplement_lbls.extend(lbls)

        if cycada > 0:
            imgs, lbls = select_cycada(cycada, train_domain, test_domain, root, domain_dict)
            supplement_imgs.extend(imgs)
            supplement_lbls.extend(lbls)

        if synthetic > 0:
            imgs, lbls = select_synthetic(synthetic, train_domain, test_domain, root, domain_dict)
            supplement_imgs.extend(imgs)
            supplement_lbls.extend(lbls)
        
        if real_histogram_matching_domain > 0:
            imgs, lbls = select_histogram_matching_domain(real_histogram_matching_domain, train_domain, test_domain, root, domain_dict)
            supplement_imgs.extend(imgs)
            supplement_lbls.extend(lbls)

        supplement_types = [('Background', background), 
                            ('Real_Gray_Equalize_Domain', gray_equalize_domain), ('Real_Gray_Equalize_Individual', gray_equalize_individual),
                            ('Real_Color_Equalize_Domain', color_equalize_domain), ('Real_Color_Equalize_Individual', color_equalize_individual),
                            ('Real_Gray_World_Domain', gray_world_domain)]

        for type, number in supplement_types:
            imgs, lbls = select_imgs(type, number, root, train_domain, domain_dict, test=False)
            supplement_imgs.extend(imgs)
            supplement_lbls.extend(lbls)

        # Write to files
        images_out = [(train_images_out, train_imgs),                    
                      (supplement_images_out, supplement_imgs)]
        
        labels_out = [(train_labels_out, train_lbls),
                      (supplement_labels_out,supplement_lbls)]

        shapes_out = [(train_shapes_out, len(train_imgs)),
                      (supplement_shapes_out, len(supplement_imgs))]
    
        for path, imgs in images_out:
            make_txt_file(path, imgs)
        
        for path, lbls in labels_out:
            make_txt_file(path, lbls)

        for path, length in shapes_out:
            make_shapes_file(path, length)
            
if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument('-o', '--output_root',
                        help='path to output directory',
                        default='/scratch/cek28/jitter/wt/experiments',
                        type=str)
    parser.add_argument('-i', '--root',
                        help='path to root directory',
                        default='/scratch/cek28/jitter/wt',
                        type=str)
    parser.add_argument('-s', '--synthetic',
                        help='number of synthetic images to include in train',
                        default=0,
                        type=int)
    parser.add_argument('-tbg', '--test_background',
                        help='number of background images from test domain to include in training supplement',
                        default=0,
                        type=int)
    parser.add_argument('-bg', '--background',
                        help='number of background images to include in train',
                        default=0,
                        type=int)
    parser.add_argument('-r', '--real',
                        help='number of real images to include in train',
                        default=100,
                        type=int)
    parser.add_argument('-e', '--experiment',
                        help='name of the experiment (for pathing purposes)',
                        type=str)
    parser.add_argument('-tr', '--test_real',
                        help = 'number of test domain real images to include',
                        default=0,
                        type=int)
    parser.add_argument('-cg', '--cyclegan',
                        help = 'number of cyclegan images to include',
                        default=0,
                        type=int)
    parser.add_argument('-cy', '--cycada',
                        help = 'number of supplement cycada images to include',
                        default=0,
                        type=int)
    parser.add_argument('-ged', '--real_gray_equalize_domain',
                        help = 'number of histogram equalized by domain gray images to include',
                        default=0,
                        type=int)
    parser.add_argument('-gei', '--real_gray_equalize_individual',
                        help = 'number of histogram equalized by individual image gray images to include',
                        default=0,
                        type=int)
    parser.add_argument('-ced', '--real_color_equalize_domain',
                        help = 'number of histogram equalized by domain color images to include',
                        default=0,
                        type=int)
    parser.add_argument('-cei', '--real_color_equalize_individual',
                        help = 'number of histogram equalized by individual image color images to include',
                        default=0,
                        type=int)
    parser.add_argument('-gwd', '--real_gray_world_domain',
                        help = 'gray world domain source images to include',
                        default=0,
                        type=int)
    parser.add_argument('-sr', '--supplement_real',
                        help = 'real supplements',
                        default=0,
                        type=int)
    parser.add_argument('-hmd', '--real_histogram_matching_domain',
                        help = 'number of real histogram matching domain images to includes from train',
                        default=0,
                        type=int)
    args = parser.parse_args()
    f = open('/scratch/cek28/jitter/wt/domain_overview.json', 'r')
    domain_dict = json.load(f)
    generate_txt(args.output_root, 
                args.real, 
                args.synthetic, 
                args.background, 
                args.test_background, 
                args.test_real, 
                args.cyclegan,
                args.cycada,
                args.real_gray_equalize_domain,
                args.real_gray_equalize_individual,
                args.real_color_equalize_domain,
                args.real_color_equalize_individual,
                args.real_gray_world_domain,
                args.supplement_real,
                args.real_histogram_matching_domain,
                args.experiment, 
                args.root, 
                domain_dict)