import os
import sys
import skimage.io
ROOT_DIR = 'Reusable_tools/TF/segment_car/RCNN'
sys.path.append(ROOT_DIR)
from mrcnn import utils
import mrcnn.model as modellib
from mrcnn import visualize
sys.path.append(os.path.join(ROOT_DIR, "samples/coco/"))
import coco
import numpy as np
from FileListor import FileListor
from LoadOrWriteObj import write_or_read_obj
import pickle


class InferenceConfig(coco.CocoConfig):
    GPU_COUNT = 1
    IMAGES_PER_GPU = 1


config = InferenceConfig()
config.display()

MODEL_DIR = os.path.join(ROOT_DIR, "logs")
COCO_MODEL_PATH = os.path.join(ROOT_DIR, "mask_rcnn_coco.h5")

if not os.path.exists(COCO_MODEL_PATH):
    utils.download_trained_weights(COCO_MODEL_PATH)

class_names = ['BG', 'person', 'bicycle', 'car', 'motorcycle', 'airplane',
               'bus', 'train', 'truck', 'boat', 'traffic light',
               'fire hydrant', 'stop sign', 'parking meter', 'bench', 'bird',
               'cat', 'dog', 'horse', 'sheep', 'cow', 'elephant', 'bear',
               'zebra', 'giraffe', 'backpack', 'umbrella', 'handbag', 'tie',
               'suitcase', 'frisbee', 'skis', 'snowboard', 'sports ball',
               'kite', 'baseball bat', 'baseball glove', 'skateboard',
               'surfboard', 'tennis racket', 'bottle', 'wine glass', 'cup',
               'fork', 'knife', 'spoon', 'bowl', 'banana', 'apple',
               'sandwich', 'orange', 'broccoli', 'carrot', 'hot dog', 'pizza',
               'donut', 'cake', 'chair', 'couch', 'potted plant', 'bed',
               'dining table', 'toilet', 'tv', 'laptop', 'mouse', 'remote',
               'keyboard', 'cell phone', 'microwave', 'oven', 'toaster',
               'sink', 'refrigerator', 'book', 'clock', 'vase', 'scissors',
               'teddy bear', 'hair drier', 'toothbrush']


def scan_mask(in_pic_l, out_dir):

    for pic_pa in in_pic_l:
        try:
            image = skimage.io.imread(pic_pa)
            pic_na = os.path.basename(pic_pa)
            save_pa = os.path.join(out_dir, pic_na.split('.')[0]) + '.npy'
            if '$$' not in pic_na or os.path.exists(save_pa): continue

            results = model.detect([image], verbose=0)[0]
            if 3 not in results['class_ids']:
                continue
            else:
                match_rst = list(np.where(results['class_ids'] == 3)[0])

                tar_mask = (0, 0)
                for mask_idx in match_rst:
                    mask_size = np.sum(results['masks'][:, :, mask_idx])
                    if mask_size > tar_mask[1]:

                        tar_mask = (mask_idx, mask_size)

                np.save(save_pa, results['masks'][:, :, tar_mask[0]])

        except Exception as e:
            print('Wrong with pic', pic_na, str(e))


def find_pic_pa(given_root_pa, given_na):
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


model = modellib.MaskRCNN(mode="inference", model_dir=MODEL_DIR, config=config)
model.load_weights(COCO_MODEL_PATH, by_name=True)

IMAGE_ROOT_DIR = 'DVM/Whole_raw_dataset/whole_raw'
output_dir = 'DVM/Whole_raw_dataset/whole_seg'

pre_tupe = ('Fiat', 'Grande Punto')
maker_l = sorted(os.listdir(IMAGE_ROOT_DIR))
maker_l.index(pre_tupe[0])

useful_pic_s = get_useful_pic_set()


for folder_na in maker_l[maker_l.index(pre_tupe[0]):]:
    genmodel_pa = os.path.join(IMAGE_ROOT_DIR, folder_na)
    out_genmodel_pa = os.path.join(output_dir, folder_na)
    if not os.path.exists(out_genmodel_pa):
        os.makedirs(out_genmodel_pa)

    genmodel_l = sorted(os.listdir(genmodel_pa))
    if folder_na == pre_tupe[0]:
        genmodel_l = genmodel_l[genmodel_l.index(pre_tupe[1]):]

    for trim_na in genmodel_l:
        trim_pa = os.path.join(genmodel_pa, trim_na)
        out_trim_pa = os.path.join(out_genmodel_pa, trim_na)
        if os.path.exists(os.path.join(out_trim_pa, 'segmentation_rst.pkl')):
            continue

        print('Start ', folder_na + ' ' + trim_na)

        if not os.path.exists(out_trim_pa):
            os.makedirs(out_trim_pa)

        listor = FileListor()
        listor.list_all_tar_files(trim_pa, ['jpg', 'png'])
        listor.tar_file_list = [ele for ele in listor.tar_file_list if ele.split('/')[-1] in useful_pic_s]

        scan_mask(listor.tar_file_list, out_trim_pa)
