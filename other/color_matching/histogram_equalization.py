import cv2
import numpy as np
import os
import json

def color_equalize_single(img):
    # Code for Histogram Equalization taken from: 
    # https://stackoverflow.com/questions/31998428/opencv-python-equalizehist-colored-image

    img_yuv = cv2.cvtColor(img, cv2.COLOR_BGR2YUV)

    # equalize the histogram of the Y channel
    img_yuv[:,:,0] = cv2.equalizeHist(img_yuv[:,:,0])

    # convert the YUV image back to RGB format
    img_output = cv2.cvtColor(img_yuv, cv2.COLOR_YUV2BGR)

    return img_output

def color_equalize_domain(paths, out_path):
    num_imgs = len(paths)

    y_array = []
    for path in paths:
        img = cv2.imread(path)
        img_yuv = cv2.cvtColor(img, cv2.COLOR_BGR2YUV)
        y_array.extend(img_yuv[:,:,0].flatten())
    
    y_array = np.array(y_array, dtype='uint8')
    equalized = cv2.equalizeHist(y_array)
    multiple = 608*608

    for i, path in enumerate(paths):
        img = cv2.imread(path)
        img_yuv = cv2.cvtColor(img, cv2.COLOR_BGR2YUV)
        converted = np.reshape(equalized[i * multiple: (i + 1) * multiple], (608,608))
        img_yuv[:,:,0] = converted
        img_output = cv2.cvtColor(img_yuv, cv2.COLOR_YUV2BGR)
        cv2.imwrite(os.path.join(out_path, path.split("/")[-1]), img_output)

def gray_equalize_single(img):
    # Code for gray histogram equalization taken from:
    # https://docs.opencv.org/3.4/d4/d1b/tutorial_histogram_equalization.html

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    final = cv2.equalizeHist(gray)
    return final

def gray_equalize_domain(paths, out_path):
    num_imgs = len(paths)

    gray_array = []
    for path in paths:
        img = cv2.imread(path)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        gray_array.extend(gray.flatten())

    gray_array = np.array(gray_array, dtype='uint8')
    equalized = cv2.equalizeHist(gray_array)
    multiple = 608*608

    for i, path in enumerate(paths):
        img_output = np.reshape(equalized[i * multiple: (i + 1) * multiple], (608,608))
        cv2.imwrite(os.path.join(out_path, path.split("/")[-1]), img_output)

def process_directory(paths, out_path, method, scope):
   
    os.makedirs(out_path, exist_ok=True)

    if scope == 'Individual':
        for path in paths:
            img = cv2.imread(path)
            if method == 'Color_Equalize':
                img = color_equalize_single(img)
            elif method == 'Gray_Equalize':
                img = gray_equalize_single(img)
            
            cv2.imwrite(os.path.join(out_path, path.split("/")[-1]), img)
    
    if scope == 'Domain':
        if method == 'Color_Equalize':
            color_equalize_domain(paths, out_path)
        elif method == 'Gray_Equalize':
            gray_equalize_domain(paths, out_path)

def process_all():

    root = '/scratch/cek28/jitter/wt'
    domain_dict = json.load(open("/scratch/cek28/jitter/wt/domain_overview.json", "r"))
    domains = ['NW', 'SW', 'EM']
    actions = ['Real', 'Test']
    methods = ['Color_Equalize', 'Gray_Equalize']
    scopes = ['Individual', 'Domain']


    def num2img(root, domain, action, numbers):
        return [os.path.join(root, 'images', f'{domain}/{action}/{_}.jpg') for _ in numbers]

    def num2lbl(root, domain, action, numbers):
        return [os.path.join(root, 'labels', f'{domain}/{action}/{_}.txt') for _ in numbers]

    for domain in domains:
        for action in actions:
            for method in methods:
                for scope in scopes:

                    out_path = os.path.join(root, 'images', domain, f'{action}_{method}_{scope}')

                    if action == 'Real':
                        numbers = domain_dict[domain][action][:100]
                    else:
                        numbers = domain_dict[domain][action]
                    
                    paths = num2img(root, domain, action, numbers)

                    process_directory(paths, out_path, method, scope)

if __name__ == "__main__":
    process_all()
