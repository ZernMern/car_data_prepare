from PerformRecorder import PerformRecorder
from SingleScanner import SingleGreper


class WebScanner:
    def __init__(self, proxy_file_pa, given_url_func=None, given_rst_func=None,rest_time=1):
        self.adv_list_status = {}
        self.proxy_file = proxy_file_pa
        self.pre_included_l = []
        self.url_func = given_url_func
        self.rst_func = given_rst_func
        self.rest_time = rest_time

    def prepare_perf_recorder(self):
        with open(self.proxy_file, 'r') as f_in:
            proxy_l = [':'.join(line.strip().split('||')[1:]) for line in f_in.readlines()]
        return PerformRecorder(proxy_l)

    def process_url_requests(self, task_queue, thread_num):
        """ task_queue : urls in Queue.Queue """

        perf_recorder = self.prepare_perf_recorder()

        my_pool = []
        shared_result_d = {}
        if thread_num > perf_recorder.proxy_queue.qsize():
            print(f'Given thread number {thread_num} excess the proxy number {perf_recorder.proxy_queue.qsize()}!')

        for thread_id in range(min(thread_num, perf_recorder.proxy_queue.qsize(), task_queue.qsize())):
            t = SingleGreper(thread_id,  task_queue, perf_recorder,
                             shared_result_d, given_url_func=self.url_func, given_rst_func=self.rst_func,rest_time=self.rest_time)
            t.setDaemon(True)
            t.start()
            my_pool.append(t)

        for t in my_pool:
            t.join()

        return shared_result_d


