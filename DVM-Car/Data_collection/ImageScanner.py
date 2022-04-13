import os
import json
import queue
import threading
from WebScanner import WebScanner


class ImageScanner(threading.Thread):
    def __init__(self, cf_d, tar_model_str):
        self.cf_d = cf_d
        self.tar_json_dir = os.path.join(cf_d['paths']['ad_json_dir'], tar_model_str)
        self.thread_num = int(cf_d['paras']['thread_num'])
        self.tar_img_dir = os.path.join(cf_d['paths']['ad_img_dir'], tar_model_str)
        if not os.path.exists(self.tar_img_dir):
            os.makedirs(self.tar_img_dir)

    def get_task_queue(self):
        t_queue = queue.Queue()

        for f_na in os.listdir(self.tar_json_dir):
            pic_num = 1

            f_pa = os.path.join(self.tar_json_dir, f_na)
            with open(f_pa, 'r') as f_in:
                t_json = json.loads(f_in.readline())
                if 'advert' in t_json:
                    if 'imageUrls' in t_json['advert']:
                        for url in t_json['advert']['imageUrls']:
                            pic_id = f_na.replace('.txt', '_{}'.format(pic_num))
                            save_pa = os.path.join(self.tar_img_dir, '{}$$image_{}.jpg'.format(f_na.replace('.txt', ''), pic_num))

                            t_queue.put([pic_id, url.replace('{resize}', 'w800h600'), save_pa])
                            pic_num += 1

        return t_queue

    def rst_func(self, pic_id, response, save_pa):
        with open(save_pa, 'wb') as handler:
            handler.write(response.content)
        return True, True

    def scan_images(self):

        proxy_l_pa = self.cf_d['paths']['proxy_file']
        web_Scanner = WebScanner(proxy_l_pa, given_rst_func=self.rst_func, rest_time=1)
        task_queue = self.get_task_queue()
        rsts_d = web_Scanner.process_url_requests(task_queue, self.thread_num)



