# @Author : JM_Huang
# @Time   : 14/06/21

import os
import sys
from own_pathes import own_path_d
sys.path.append(own_path_d['Pic'])
sys.path.append(own_path_d['Other_ppl_based_models'])
from pic_utils import whiten_and_resize, crop_img_n_mask, my_resize_img
import numpy as np
from Plate_detection.PlateDetector import PlateDetector
from PIL import Image


def read_adv_info(tab_fpa):
    cont_d = {}
    with open(tab_fpa) as f_in:
        for line in f_in.readlines()[1:]:
            pieces = line.strip().split(',')
            t_l = pieces[:2] + [pieces[7], pieces[6], pieces[3]]

            if pieces[7] in ['2019', '2020', '2021']:
                cont_d[pieces[3]] = '$$'.join(t_l)
    return cont_d


def location_img_dir(root_dir, img_fna):
    pieces = img_fna.split('$$')
    maker, model, year, color = pieces[:4]
    maker_dir = os.path.join(root_dir, maker)
    assert os.path.exists(maker_dir)

    color_dir = os.path.join(maker_dir, model, year, color)
    if not os.path.exists(color_dir):
        os.makedirs(color_dir)

    return os.path.join(color_dir, img_fna)


def resized_imgs(img_npa, t_mask):
    new_img_npa, new_mask_npa = crop_img_n_mask(t_mask, img_npa)
    if new_img_npa is None:
        return None, None

    resized_img = my_resize_img(Image.fromarray(new_img_npa), tar_shape_l=[300, 300])
    resied_mask_img = my_resize_img(Image.fromarray((new_mask_npa).astype('uint8')), bg_color='black',
                                    tar_shape_l=[300, 300])
    return np.array(resized_img), np.array(resied_mask_img)[:,:,0]


ad_tab_fpa = 'Projects/DVM/New_DVM/Prepare_shared_dataset/DVM-Car_V2.0/Ad_table.csv'
adv_str_d = read_adv_info(ad_tab_fpa)
adv_hasher = np.load('Lib/DVM_crucial_data/adv_hash_dict_simple_210612.npy', allow_pickle=True).item()
t_pd = PlateDetector()
out_root_dir = 'Data/Data_disk2/research/facelift/data/resized_DVM'
added_img_d = {}
square_sized_npy_dir = 'Data/Data_disk2/research/scaned_2019_dvm/final_npy'

for i in range(1, 9):
    pic_num = 0
    npy_dir = f'Data/Data_disk2/research/scaned_2019_dvm/tmp_check/{i}_pos'
    img_dir = f'Data/Data_disk2/research/scaned_2019_dvm/tmp_check/{i}'

    for fna in [ fna for fna in os.listdir(npy_dir) if '.npy' in fna]:
        npy_fpa = os.path.join(npy_dir, fna)
        img_fpa = os.path.join(img_dir, fna.replace('.npy', '.jpg'))
        adv_id, img_id = fna.split('$$')[4], fna.split('$$')[-1]
        new_fna = adv_str_d['$$'.join(adv_hasher[adv_id])] + '$$' +img_id.replace('.npy', '.jpg')
        output_fpa = location_img_dir(out_root_dir, new_fna)
        t_mask = np.load(npy_fpa, allow_pickle=True).item()
        t_mask = t_mask['car_mask'] if 'car_mask' in t_mask else None

        if t_mask is None or len(t_mask.shape) >2:
            continue

        img_npa = np.array(Image.open(img_fpa))

        # -- Blur Image
        blured_img = t_pd.blur_a_img(img_npa)
        if blured_img is not None:
            img_npa = np.array(blured_img)
        else:
            continue

        # if os.path.exists(output_fpa): continue
        resized_img_npa, resized_mask_npa = resized_imgs(img_npa, t_mask)
        if resized_img_npa is None: continue

        pic_num += 1
        if pic_num%100==0: print('processed', pic_num)

        rst_img = whiten_and_resize(resized_img_npa, resized_mask_npa)


        rst_img.save(output_fpa)
        added_img_d[new_fna] = i

        # np.save(os.path.join(square_sized_npy_dir, fna), resized_mask_npa)

    np.save('ws_dstore/added_img', added_img_d)
