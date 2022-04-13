import os
import sys
sys.path.append('Reusable_tools/Image_related/Car_plate_processing/new')
from car_plate_detection import process_given_images


def find_pic_pa(given_root_pa, given_na):
    # given_na = given_na.replace('.jpg', '.npy')

    folder = '/'.join(given_na.split('$$')[:4])
    folder_pa = os.path.join(given_root_pa, folder)
    pic_pa = os.path.join(folder_pa, given_na)
    if os.path.exists(pic_pa):
        return pic_pa
    else:
        return None


def get_useful_pic_set():
    pic_s = set()
    table_pa = 'New_DVM/DVM_tables/Image_table_updating/ws_dstore/image_table_useful_only_7_4-1.csv'
    with open(table_pa, 'r') as f_in:
        cont = f_in.readlines()

        for line in cont[1:]:
            pic_s.add(line.strip().split(',')[1])

    return pic_s


def get_processed_pic_set(f_pa):
    with open(f_pa, 'r') as f_in:
        cont = f_in.readlines()

        return set([line.strip() for line in cont])


def get_rst_pic_na(rst_file_pa):
    with open(rst_file_pa, 'r') as f_in:
        cont = f_in.readlines()

        return set([line.strip().split(',')[0] for line in cont])


useful_pic_s = get_useful_pic_set()
wpod_net_path = "Reusable_tools/Image_related/Car_plate_processing/new/data/lp-detector/wpod-net_update1.h5"
root_dir = 'DVM/Whole_raw_dataset/whole_raw'

rst_file_pa = 'New_DVM/Image_processing/mask_number_plate/plate_positions.txt'
rsult_pic_s = get_rst_pic_na(rst_file_pa)

processed_f_pa = 'New_DVM/Image_processing/mask_number_plate/processed_l.txt'
processed_pic_s = get_processed_pic_set(processed_f_pa)

print(len(useful_pic_s))
print(len(rsult_pic_s))

print(len(processed_pic_s))

waiting_s = useful_pic_s - rsult_pic_s - processed_pic_s
print('waiting process ', len(waiting_s))

img_l = []
pic_num = 0
for pic_na in list(waiting_s)[:10000]:
    rst = find_pic_pa(root_dir, pic_na)
    if rst is not None:
        img_l.append(rst)

print('start detecting')
process_given_images()