import os
import sys
from own_pathes import own_path_d
sys.path.append(own_path_d['TF'])
import numpy as np
from shutil import copyfile

def copy_pics(rst_d, copy_to_dir):
    for angle in rst_d:
        folder_pa = os.path.join(copy_to_dir, str(angle))

        if not os.path.exists(folder_pa):
            os.makedirs(folder_pa)

        for pic_pa in rst_d[angle]:
            pic_na = pic_pa.split('/')[-1]
            copyfile(pic_pa, os.path.join(folder_pa, pic_na))

def predict_angle():
    weight_pa = 'Data/Classical_dl_model_paras/My_own/own_car_angle_weights/19550epoches.ckpt'
    tar_dir = 'Data/Data_disk2/research/scaned_2019_dvm/tmp_working_space'
    python_loc = '/home/tech/.conda/envs/py37tf14th16/bin/python'
    python_fpa = 'Projects/DVM/New_DVM/Image_processing/stage1_pred_car_angles/VGG_for_car_angle.py'

    log_fpa = 'Data/Data_disk2/research/scaned_2019_dvm/tmp_working_space/log.txt'

    for i in range(1, 10):
        pic_num = 50000
        if i == 9: pic_num = 21641

        iden_rst_pa = f'Data/Data_disk2/research/scaned_2019_dvm/tmp_working_space/angle_label_rst_6_13_{i}.txt'
        data_fpa = f'Data/Data_disk2/research/scaned_2019_dvm/tmp_working_space/for_angle_clasificaiton_train_{i}.tfrecords'
        os.system(f'{python_loc} {python_fpa} {data_fpa} {pic_num} {weight_pa} {iden_rst_pa} > {log_fpa}' )
        print('finish ', i)


def transform_identify_rst(match_d, rst_fpa):
    output_dir = 'Data/Data_disk2/research/scaned_2019_dvm/tmp_check'
    with open(rst_fpa) as f_in:
        rst_l = eval(f_in.readline())
    for ele in rst_l:
        pic_idx, angle, prob = ele
        if angle in [0, '0']: continue

        pic_fpa = match_d[pic_idx]
        t_out_folder = os.path.join(output_dir, str(angle))
        if not os.path.exists(t_out_folder):
            os.makedirs(t_out_folder)
        copyfile(pic_fpa, os.path.join(t_out_folder, pic_fpa.split('/')[-1]))


t_dir = 'Data/Data_disk2/research/scaned_2019_dvm/tmp_working_space'
match_l = []
for npy_fpa in [os.path.join(t_dir, fna) for fna in os.listdir(t_dir) if 'pic_indx' in fna]:
    match_l += list(np.load(npy_fpa, allow_pickle=True).item().items())

match_d = dict([(item[1], item[0]) for item in match_l])

pic_l_f_pa = 'Data/tmp/new_angle_6_30_pic_l'
copy_to_dir = '/home/tech/Desktop/tmp'

for i in range(9, 10):
    iden_rst_pa = f'Data/Data_disk2/research/scaned_2019_dvm/tmp_working_space/angle_label_rst_6_13_{i}.txt'
    transform_identify_rst(match_d, iden_rst_pa)

# -- If you want to creat folder to manually label images
# copy_pics(rst_d, copy_to_dir)