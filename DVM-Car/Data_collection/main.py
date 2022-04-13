import os
import sys
sys.path.append(r'py3_lib\basic')
from ATListScanner import ATListScanner
sys.path.append(r'py3_lib\basic')
from read_ini import read_ini_as_d
from ADJsonScanner import ADJsonScanner
from ATImageScanner import ATImageScanner
from DataTransfer import DataTransfer


def read_expand_l(expand_l_pa):

    with open(expand_l_pa, 'r') as f_in:
        targets_d = eval(f_in.readline())
    return targets_d

def scan_a_modelyear(tar_model_str, year_l):
    print('scan task for ', tar_model_str, ' start:')
    # -- scan ad list
    t_at_list_Scanner = ATListScanner(cf_d)
    t_f_pa = t_at_list_Scanner.scan_ad_l(tar_model_str, year_l)

    # -- scan jsons
    t_json_scaner = ADJsonScanner(cf_d, tar_model_str)
    t_json_scaner.scan_information(t_f_pa)

    # -- scan images
    img_Scanner = ATImageScanner(cf_d, tar_model_str)
    img_Scanner.scan_images()
    print('scan task for ', tar_model_str, ' finished.')


def transfer():
    img_dir = 'DVM_scan_data/Raw_data_part3/img_dir'
    cloud_dir = 'DVM/Whole_raw_dataset/whole_raw'
    list_dir = 'DVM_scan_data/Raw_data_part3/ad_list_files'
    cloud_list_dir = 'DVM/Whole_raw_dataset/all_attributes_files/Whole/list_files'
    json_dir = 'DVM_scan_data/Raw_data_part3/json_dir'
    cloud_json_dir = 'DVM/Whole_raw_dataset/all_attributes_files/Whole/json_files'
    t_transor = DataTransfer(img_dir, cloud_dir, list_dir, cloud_list_dir, json_dir=json_dir, cloud_json_dir=cloud_json_dir)
    t_transor.transfer_all()

cf_d = read_ini_as_d(r'expend_initial.ini')

targets_d = read_expand_l(cf_d['paths']['expand_l_pa'])
ad_list_dir = cf_d['paths']['ad_list_dir']

# -- Remember to modify the image_table path in ini file !!!!
for tar_model_str in targets_d:
    scan_a_modelyear(tar_model_str, targets_d[tar_model_str])
