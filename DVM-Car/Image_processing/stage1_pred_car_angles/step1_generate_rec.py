import os
import sys
from own_pathes import own_path_d
sys.path.append(own_path_d['TF'])
from CallRecWriter import CallRecWriter
from FileListor import FileListor


def tmp_label_method(pic_idx, pic_pa):
    label_l = [0]*9
    label_l[0] = pic_idx
    return label_l


tar_dir = 'Data/Data_disk2/research/scaned_2019_dvm/img_dir'
output_rec_fpa = 'Data/Data_disk2/research/scaned_2019_dvm/tmp_working_space/for_angle_clasificaiton'
output_match_d_fpa = 'Data/Data_disk2/research/scaned_2019_dvm/tmp_working_space/pic_indx'
file_listor = FileListor()
file_listor.list_all_tar_files(tar_dir, ['jpg', 'png', 'JPEG'])

rec_writer = CallRecWriter(given_label_method=tmp_label_method)
rec_writer.generate_rec(file_listor.tar_file_list, output_rec_fpa, output_match_d_fpa, include_test=False)