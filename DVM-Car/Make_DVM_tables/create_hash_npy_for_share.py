import numpy as np


def read_img_tables(hash_d):
    mapping_d = {}

    img_table_fpa = 'Data/Projects_working/DVM/image_tables/image_table_with_manual_rst_2019_11_28-05.csv' #image_table_with_manual_rst_2020_09_10-01.csv
    with open(img_table_fpa, 'r') as f_in:
        for line in f_in.readlines()[1:]:
            pieces = line.strip().split(',')
            pic_na = pieces[1]
            adv_id = pieces[0].split('_')[0]
            if adv_id not in hash_d: continue
            shared_na = pic_na.replace(adv_id, hash_d[adv_id][1])
            # mapping_d[pic_na] = shared_na
            mapping_d[shared_na] = pic_na

    return mapping_d


mapping_d = np.load('Projects/DVM/New_DVM/DVM_tables/Prepare_shared_dataset/adv_hash_dict_simple.pkl', allow_pickle=True)

rst_d = read_img_tables(mapping_d)
np.save('Projects/DVM/New_DVM/DVM_tables/Prepare_shared_dataset/back', rst_d)