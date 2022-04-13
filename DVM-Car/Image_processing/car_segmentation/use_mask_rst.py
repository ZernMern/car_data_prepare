import os
import sys
import numpy as np
from own_pathes import own_path_d
sys.path.append(own_path_d['DVM_tools'])

from FileListor import FileListor
from DVMCopyer import DVMCopyer
from shutil import copyfile



tar_dir = 'DVM/Whole_raw_dataset/whole_seg/Audi'  #
img_root_pa = 'DVM/Whole_raw_dataset/whole_raw'
listor = FileListor()
listor.list_all_tar_files(tar_dir, ['npy'])

def get_mid_matrix(data):
    quat_x_len = int(data.shape[0] / 4)
    quat_y_len = int(data.shape[1] / 4)

    mid_matrix = data[quat_x_len:quat_x_len*3,quat_y_len:quat_y_len*3]
    return np.sum(mid_matrix) / np.prod(mid_matrix.shape)

pic_num = 1
copy_to_dir = '/home/tech/Desktop/tmp'

for file_pa in listor.tar_file_list[:300]:

    data = np.load(file_pa)

    pic_na = os.path.basename(file_pa).split('.')[0]
    # print(pic_na, np.prod(data.shape), np.sum(data), np.sum(data)/np.prod(data.shape))
    space_ratio = np.sum(data) / np.prod(data.shape)
    mid_space_ratio = get_mid_matrix(data)

    pic_pa = DVMCopyer().find_pic_pa(img_root_pa, pic_na)
    new_pic_na = '{}_{}_pic_num_{}'.format(round(space_ratio,3), round(mid_space_ratio,3), pic_num)
    copy_to_pic_pa = os.path.join(copy_to_dir, new_pic_na)
    copyfile(pic_pa, copy_to_pic_pa)
    pic_num += 1
