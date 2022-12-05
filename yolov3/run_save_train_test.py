import argparse
import os
import subprocess
from glob import glob
import shutil 

parser = argparse.ArgumentParser()
parser.add_argument('--img_list', type=str, default='none', help='directory of train imgs')                                             # if yes, input absolute path
parser.add_argument('--lbl_list', type=str, default='none', help='directory of train labels')                                           # if yes, input absolute path
parser.add_argument('--epochs', type=str, default='300', help='num epochs')
parser.add_argument('--out_dir', type=str, default='/home/fcw/batch_size_experiments/', help='directory to output imgs')
parser.add_argument('--img_list_val', type=str, default='none', help='directory of val imgs')                                             # if yes, input absolute path
parser.add_argument('--lbl_list_val', type=str, default='none', help='directory of val labels') 
parser.add_argument('--img_list_supplement', type=str, default='none', help='directory of supplement imgs')                                             # if yes, input absolute path
parser.add_argument('--lbl_list_supplement', type=str, default='none', help='directory of supplement labels') 
parser.add_argument('--version', type=str, default='v0', help='version num')
parser.add_argument('--device', type=str, default='1', help='gpu id')
parser.add_argument('--supplement_batch_size', type=str, default='1', help='supplement batch size')
parser.add_argument('--experiment', type=str, default='1', help='returns name of experiment')


opt = parser.parse_args()

def make_data_file(out_root, img_list, lbl_list, version, img_list_val, lbl_list_val, img_list_supplement, lbl_list_supplement, supplement_batch_size, epochs):
    if not os.path.exists(out_root):                                                                    # make root dir
        os.makedirs(out_root)

    try:
        f = open(out_root + 'train_data_' + version + '.data', 'r+')
        f.truncate(0)
    except:
        pass

    with open(out_root + 'train_data_' + version + '.data', 'w') as f:                                     # create master label text file
        f.write('train=' + img_list + '\n')
        f.write('train_label=' + lbl_list + '\n')
        f.write('supplement=' + img_list_supplement + '\n')
        f.write('supplement_label=' + lbl_list_supplement + '\n')
        f.write('valid=' + img_list_val + '\n')
        f.write('valid_label=' + lbl_list_val + '\n')
        f.write('supplemental_batch_size=' + supplement_batch_size + '\n')
        f.write('classes=1\n')
        f.write('names=./data/wnd.names\n')
        f.write('backup=backup/\n')
        f.write('eval=wnd')


def run_train(out_root, epochs, device, supplement_batch_size):
    subprocess.run(['python', 'train_mixed_batch.py',                                                    # train gp_gan
                    '--cfg', './cfg/yolov3-spp.cfg',
                    '--data', out_root + 'train_data_' + version + '.data',
                    '--img-size', '608',
                    '--epochs', epochs,
                    '--batch-size', '8',
                    '--supplement-batch-size', supplement_batch_size,
                    '--device', device])


def run_test(out_root, device):
    subprocess.run(['python', 'test.py',                                                    # test gp_gan
                    '--cfg', './cfg/yolov3-spp.cfg',
                    '--data', out_root + 'train_data_' + version + '.data',
                    '--img-size', '608',
                    '--weights', out_root + 'weights/best.pt', # DONE
                    '--device', device,
                    '--experiment_final', experiment])

img_list = opt.img_list
lbl_list = opt.lbl_list
epochs = opt.epochs
out_root = opt.out_dir
img_list_val = opt.img_list_val
lbl_list_val = opt.lbl_list_val
version = opt.version
device = opt.device
img_list_supplement = opt.img_list_supplement
lbl_list_supplement = opt.lbl_list_supplement
supplement_batch_size = opt.supplement_batch_size
experiment = opt.experiment

def main(img_list, lbl_list, out_root, epochs, version, device, img_list_supplement, lbl_list_supplement, supplement_batch_size):
    make_data_file(out_root, img_list, lbl_list, version, img_list_val, lbl_list_val, img_list_supplement, lbl_list_supplement, supplement_batch_size, epochs)
    print("Made .data file\n")

    #Change back
    run_train(out_root, epochs, device, supplement_batch_size)
    print("Finished Training\n")

    run_test(out_root, device)
    print("Finished Testing\n")

main(img_list, lbl_list, out_root, epochs, version, device, img_list_supplement, lbl_list_supplement, supplement_batch_size)
