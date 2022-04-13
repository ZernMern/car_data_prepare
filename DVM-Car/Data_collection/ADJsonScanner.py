import os
import time
import json
import queue
import urllib
import random
import requests
import threading
from bs4 import BeautifulSoup

from ATPageReader import ATPageReader
from WebScanner import WebScanner


class ADJsonScanner(threading.Thread):
    def __init__(self, cf_d, tar_model_str):
        self.cf_d = cf_d
        self.at_reader = ATPageReader()
        self.thread_num = int(cf_d['paras']['thread_num'])
        self.maker, self.genmodel = tar_model_str.split('||')
        self.json_folder = os.path.join(cf_d['paths']['ad_json_dir'], tar_model_str)
        if not os.path.exists(self.json_folder):
            os.makedirs(self.json_folder)

    def get_task_queue(self, lines):
        t_queue = queue.Queue()

        for line in lines:
            in_str_l = line.strip().split('||')
            if len(in_str_l) < 9:
                continue
            advert_id = in_str_l[0]

            advert_url = self.cf_d.tar_web.format(advert_id)
            t_queue.put([advert_id, advert_url, in_str_l])

        return t_queue

    def rst_func(self, adv_id, response, in_str_l):
        rst = json.loads(response.text)

        genmodel_str = os.path.basename(self.json_folder).replace('||', '$$')
        try:
            year_str = in_str_l[1][:4]
        except:
            year_str = 'Unknown'

        file_na = '$$'.join([genmodel_str, year_str, in_str_l[8], adv_id]) + '.txt'
        json_f_pa = os.path.join(self.json_folder, file_na)

        with open(json_f_pa, 'w') as outfile:
            json.dump(rst, outfile)
        return True, True

    def scan_information(self, adv_l_f_pa):
        proxy_l_pa = self.cf_d['paths']['proxy_file']
        web_Scanner = WebScanner(proxy_l_pa, given_rst_func=self.rst_func,rest_time=5)

        with open(adv_l_f_pa, 'r') as f_in:
            lines = f_in.readlines()
        task_queue = self.get_task_queue(lines)
        rsts_d = web_Scanner.process_url_requests(task_queue, self.thread_num)