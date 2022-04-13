import os
from FileListor import FileListor
from shutil import copyfile


class DataTransfer:
    def __init__(self, img_dir, cloud_img_dir, list_dir=None, cloud_list_dir=None, json_dir=None, cloud_json_dir=None):
        self.img_dir = img_dir
        self.cloud_img_dir = cloud_img_dir
        self.list_dir = list_dir
        self.cloud_list_dir = cloud_list_dir
        self.json_dir = json_dir
        self.cloud_json_dir = cloud_json_dir

    def transfer_images(self):
        t_listor = FileListor()
        t_listor.list_all_tar_files(self.img_dir, ['jpg'])
        for pic_pa in t_listor.tar_file_list:
            pic_na = os.path.basename(pic_pa)
            genmodel_pa = os.path.exists(os.path.join(self.cloud_img_dir,'/'.join(pic_na.split('$$')[:2])))

            if not os.path.exists(genmodel_pa):
                print('Funny!!! genmodel dir not exist', genmodel_pa)
                continue
            else:
                folder_dir = os.path.join(self.cloud_img_dir,'/'.join(pic_na.split('$$')[:4]))
                if not os.path.exists(folder_dir):
                    os.makedirs(folder_dir)
                copy_to_pa = os.path.join(folder_dir,pic_na)

                if not os.path.exists(copy_to_pa):
                    copyfile(pic_pa, copy_to_pa)
                else:
                    print(copy_to_pa, 'already_exist')

    def transfer_jsons(self):
        t_listor = FileListor()
        t_listor.list_all_tar_files(self.json_dir, ['txt'])
        for src_f_pa in t_listor.tar_file_list:
            file_na = os.path.basename(src_f_pa)
            folder_na = src_f_pa.split('/')[-2].replace('||', '$$')
            folder_pa = os.path.join(self.cloud_json_dir, folder_na)
            if not os.path.exists(folder_pa):
                os.makedirs(folder_pa)
            dst_pa = os.path.join(folder_pa, file_na)
            copyfile(src_f_pa, dst_pa)

    def transfer_adlist(self):
        t_listor = FileListor()
        t_listor.list_all_tar_files(self.list_dir, ['txt'])
        for src_f_pa in t_listor.tar_file_list:
            append_to_pa = os.path.join(self.cloud_list_dir, os.path.basename(src_f_pa))
            if not os.path.exists(append_to_pa):
                print('Funny, not exist list file', append_to_pa)
                continue
            else:
                with open(src_f_pa, 'r') as f_in:
                    with open(append_to_pa, 'a') as f_out:
                        for line in f_in.readlines():
                            f_out.write(line)

    def transfer_all(self):
        self.transfer_images()
        self.transfer_adlist()
        self.transfer_jsons()


