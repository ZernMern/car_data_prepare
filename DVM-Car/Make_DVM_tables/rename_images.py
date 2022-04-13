import os
import time
import shutil
from DataFileDealer import DataFileDealer
from LoadOrWriteObj import write_or_read_obj
from FileListor import FileListor


adv_hash_pa = 'Projects/DVM/New_DVM/DVM_tables/Prepare_shared_dataset/' \
              'adv_hash_dict_simple.pkl'
img_root = 'Data/Data_disk/tmp/shared_data/single_ziped_images/new_zip'
unmatched_dir = 'Data/Data_disk/tmp/shared_data/unfound_ones'

hash_d = write_or_read_obj(adv_hash_pa)

# t_hash = write_or_read_obj('Projects/DVM/New_DVM/DVM_tables/Prepare_shared_dataset/adv_hash_dict_complex.pkl')

for folder_na in os.listdir(img_root):
    print('start', folder_na)

    t_listor = FileListor()
    file_pa = os.path.join(img_root, folder_na)
    t_listor.list_all_tar_files(file_pa, ['jpg', 'pkl'])
    for son_file in t_listor.tar_file_list:
        pieces1 = son_file.split('/')
        pieces2 = pieces1[-1].split('$$')
        adv_id = pieces2[-2]

        if len(adv_id) < 10:
            continue

        #-- If not found the id
        if adv_id not in hash_d:
            file_na = son_file.split('/')[-1]
            shutil.move(son_file, os.path.join( unmatched_dir, file_na))
            continue

        pieces2[-2] = hash_d[adv_id][1]
        pieces1[-1] = '$$'.join(pieces2)
        new_file = '/'.join(pieces1)

        try:
            shutil.move(son_file, new_file)
        except:
            print('wrong with ')
            print(son_file)
            time.sleep(2)

    print('end', folder_na)