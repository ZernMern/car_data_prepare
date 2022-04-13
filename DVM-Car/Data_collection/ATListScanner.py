import os
import sys
import copy
import queue
import urllib
sys.path.append(r'py3_lib\DVM')
sys.path.append(r'py3_lib\AT')

from GenmodelColorScanner import GenmodelColorScanner
from at_tools import get_def_para_d
from ATPageReader import ATPageReader
from WebScanner import WebScanner
from AttributeChecker import AttributeChecker


class ATListScanner:
    def __init__(self, cf_d):
        self.cf_d = cf_d
        self.max_page_num = int(cf_d['paras']['max_page_num'])
        self.at_dreader = ATPageReader()
        self.thread_num = int(cf_d['paras']['thread_num'])
        self.attr_checker = AttributeChecker()
        print('Node1')

    def prepare_cand_para_d_l(self, model_str, year_l):
        at_color_Scanner = GenmodelColorScanner(self.cf_d)
        color_d = at_color_Scanner.scan_color_l(get_def_para_d(model_str=model_str), year_l)

        can_d_l = []
        for year in year_l:
            for color in color_d[year]:
                for page in range(1, self.max_page_num+1):

                    t_para_d = get_def_para_d(model_str=model_str)
                    t_para_d['colour'] = color
                    t_para_d['page'] = str(page)
                    t_para_d['year-from'] = year
                    t_para_d['year-to'] = year

                    can_d_l.append(t_para_d)
        return can_d_l


    def get_task_queue(self, can_d_l):
        t_queue = queue.Queue()

        for idx in range(len(can_d_l)):
            key = str(idx)+ '_' + can_d_l[idx]['colour']
            url = self.cf_d.tar_web + urllib.parse.urlencode(can_d_l[idx])
            t_queue.put([key, url, None])

        return t_queue

    def rst_func(self, key_str, raw_rst, empty):
        new_rst_d = {}
        rst_d = self.at_dreader.read_list_page_infor(raw_rst.text, key_str.split('_')[1])
        for ad_id in rst_d:
            rst_l = self.attr_checker.adv_short_list_check(ad_id+'||'+rst_d[ad_id])
            if rst_l is None:
                continue
            new_rst_d[ad_id] = '||'.join(rst_l)
        return True, new_rst_d

    def get_scaned_ad_ids(self, image_table_pa):
        adv_set = set()
        with open(image_table_pa, 'r') as f_in:
            for line in f_in.readlines()[1:]:
                adv_set.add(line.split('_')[0])
        return adv_set

    def scan_ad_l(self, model_str, year_l, given_queue = None):
        already_get_adv_ids = None
        # -- list already scaned ones
        # image_table_pa = find_latest_img_table()
        # already_get_adv_ids = self.get_scaned_ad_ids(image_table_pa)

        # -- scan target color and put into candidate dict


        # -- prepare target candidate dict

        if given_queue is not None:
            task_queue = given_queue
        else:
            cand_d_l = self.prepare_cand_para_d_l(model_str, year_l)
            task_queue = self.get_task_queue(cand_d_l)

        web_Scanner = WebScanner(self.cf_d['paths']['proxy_file'], given_rst_func=self.rst_func)
        rsts_d = web_Scanner.process_url_requests(task_queue, self.thread_num)
        print('end stage')
        total_d = {}
        for t_key in rsts_d:
            total_d.update(rsts_d[t_key])

        t_f_pa = os.path.join(self.cf_d['paths']['ad_list_dir'], '{}$${}.txt'.format(*model_str.split('$$')))
        with open(t_f_pa, 'w') as f_out:
            for adv_id in total_d:
                if already_get_adv_ids is not None and adv_id in already_get_adv_ids:
                    print(adv_id, 'already exist')
                    continue
                f_out.write('{}\n'.format(total_d[adv_id].replace('\n', '\$$n')))

        return t_f_pa

