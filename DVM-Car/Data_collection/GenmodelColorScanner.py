import os
import sys
import copy
import queue
import urllib
import requests
sys.path.append(r'py3_lib\Multi_proxy')
sys.path.append(r'py3_lib\AT')
from WebScanner import WebScanner
from ATPageReader import ATPageReader


class GenmodelColorScanner:
    def __init__(self, cf_d):
        self.cf_d = cf_d
        self.at_dreader = ATPageReader()
        self.proxy_file_pa = cf_d['paths']['proxy_file']
        self.thread_num = int(cf_d['paras']['thread_num'])

    def get_year_colors(self, setting_d, year_l):
        t_queue = queue.Queue()

        for year in year_l:
            t_given_d = copy.deepcopy(setting_d)
            t_given_d['year-from'] = year
            t_given_d['year-to'] = year
            url = self.cf_d.tar_web + urllib.parse.urlencode(t_given_d)
            t_queue.put([year, url, None])

        return t_queue

    def rst_func(self, task_key, raw_rst, empty):
        return True, self.at_dreader.extract_color_l(raw_rst.text)

    def scan_color_l(self, setting_d, year_l):
        proxy_l_pa = self.proxy_file_pa
        web_Scanner = WebScanner(proxy_l_pa, given_rst_func=self.rst_func)
        t_queuqe = self.get_year_colors(setting_d, year_l)
        rsts_d = web_Scanner.process_url_requests(t_queuqe, self.thread_num)
        return rsts_d