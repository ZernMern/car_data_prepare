import os
import sys
sys.path.append('Reusable_tools/Image_related/Car_plate_processing/new')
from blur_plate_region import blur_image
from PIL import Image


def find_pic_pa(given_root_pa, given_na):

    folder = '/'.join(given_na.split('$$')[:4])
    folder_pa = os.path.join(given_root_pa, folder)
    pic_pa = os.path.join(folder_pa, given_na)
    if os.path.exists(pic_pa):
        return pic_pa
    else:
        return None


rst_pa = 'New_DVM/Image_processing/mask_number_plate/plate_positions.txt'
root_dir = 'DVM/Whole_raw_dataset/whole_raw'

with open(rst_pa, 'r') as f_in:
    cont = f_in.readlines()
    print(cont[-1].strip())
    quit()
    pieces = cont[-1].strip().split(',')
    pic_na = pieces[0]

    pic_pa = find_pic_pa(root_dir, pic_na)
    rst_array = blur_image(pic_pa, cont[-1].strip())
    Image.fromarray(rst_array).show()

# def check_seg_and_useful():

def get_useful_pic_set():
    pic_s = set()
    table_pa = 'New_DVM/DVM_tables/Image_table_updating/ws_dstore/image_table_useful_only_7_4-1.csv'
    with open(table_pa, 'r') as f_in:
        cont = f_in.readlines()

        for line in cont[1:]:
            pic_s.add(line.strip().split(',')[1])

    return pic_s