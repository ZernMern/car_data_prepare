# -- @Author   : JM_Huang
# -- @Time     : 28/10/19

import os
import sys
import cv2
import numpy as np
from PIL import Image
from own_pathes import own_path_d
sys.path.append(own_path_d['Other_ppl_based_models'])
sys.path.append(own_path_d['Pic'])


def check_done(cand_img_dir, pos_npy_dir):
    finished = False
    last_ten = os.listdir(cand_img_dir)[-16:]
    for ele in last_ten:
        if ele.replace('.jpg', '.npy') in os.listdir(pos_npy_dir):
            finished = True

    return finished

# # step 1
root_dir = 'Data/Data_disk2/research/scaned_2019_dvm/tmp_check'
python_loc = '/home/tech/.conda/envs/py37tf14th16/bin/python'
python_fpa = 'Projects/DVM/New_DVM/Image_processing/stage1_pred_car_angles/mask_car_pos.py'

for folder in [fna for fna in os.listdir(root_dir) if 'pos' not in fna]:
    cand_img_dir = os.path.join(root_dir, folder)
    pos_npy_dir = os.path.join(root_dir, folder+'_pos')

    if not os.path.exists(pos_npy_dir): os.makedirs(pos_npy_dir)

    while check_done(cand_img_dir, pos_npy_dir) == False:
        print('process ', cand_img_dir)
        os.system(f'{python_loc} {python_fpa} {cand_img_dir} {pos_npy_dir}')

