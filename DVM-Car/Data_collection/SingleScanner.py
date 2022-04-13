import time
import random
import requests
import threading
from bs4 import BeautifulSoup
from urllib.error import HTTPError


class SingleGreper(threading.Thread):
    def __init__(self, thread_id, task_queue, in_perf_recorder, shared_result_d,
                 given_url_func=None, given_rst_func=None, rest_time=1):
        threading.Thread.__init__(self)
        self.thread_id = thread_id
        self.perf_recorder = in_perf_recorder
        self.proxy_d = {'https': self.perf_recorder.proxy_queue.get()}
        self.header = {'User-Agent': "Mozilla/5.0"}
        self.task_queue = task_queue
        self.shared_result_d = shared_result_d
        self.interval_time = rest_time

        if given_url_func is not None:
            self.url_func = given_url_func
        else:
            self.url_func = self.proc_url
        if given_rst_func is not None:
            self.rst_func = given_rst_func
        else:
            self.rst_func = self.proc_rst

    def proc_url(self, given_url, other_paras=None):
        return requests.get(given_url, headers=self.header, proxies=self.proxy_d, timeout=5)

    def proc_rst(self, task_key, response, other_paras=None, shared_result_d=None):
        soup = BeautifulSoup(response.content, "html.parser")
        return True, soup

    def deal_error(self, error_na):
        if error_na not in self.perf_recorder.error_message_s:
            print('New scan error !', error_na)
            self.perf_recorder.error_message_s.add(error_na)

    def run(self):
        while True:
            # -- Get the next url
            try:
                task_key, given_url, other_paras = self.task_queue.get(False)
            except:
                print('Thread ', self.thread_id, ' end')
                return None             # -- End the thread
            response = None
            try:
                response = self.url_func(given_url, other_paras=other_paras)
            except HTTPError as h_error:
                print('Target url error, skip this url', given_url)
                self.deal_error(type(h_error).__name__) # -- Target url not exisitng so not put back to queue

            except Exception as funny_error:
                self.deal_error(type(funny_error).__name__)

                self.task_queue.put([task_key, given_url, other_paras])
                time.sleep(random.randint(1, 2))

                judge = self.perf_recorder.add_proxy_fail(self.thread_id, self.proxy_d['https'], '')
                if judge == 'Suspend':
                    if self.perf_recorder.proxy_queue.qsize() > 0:
                        self.proxy_d = {'https': self.perf_recorder.proxy_queue.get(False)}
                    else:
                        print('thread', self.thread_id, ' end1')
                        return None     # -- End the thread
                continue
            if response is not None:
                if response.status_code == 404:
                    print('404 for {} '.format(task_key))
                    continue
                if response.status_code == 403:
                    print('403 for {} '.format(task_key))
                    self.deal_error('403')
                    self.task_queue.put([task_key, given_url, other_paras])
                    return None  # -- 403 means the website has identify the proxy as a untrusted source
            # -- Process rst
            time.sleep(random.randint(self.interval_time, self.interval_time+3))
            performed, rst = self.rst_func(task_key, response, other_paras)
            if performed is True:
                self.perf_recorder.success(self.proxy_d['https'])
                self.shared_result_d[task_key] = rst

            left_size = self.task_queue.qsize()
            # if left_size % 100 == 0:
            print('Left scan task size', left_size)