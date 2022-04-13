import copy
import time
import queue


class PerformRecorder:

    def __init__(self, proxy_l):
        self.proxy_status = {}
        self.proxy_queue = queue.Queue()
        self.error_message_s = set()
        for proxy_str in proxy_l:
            self.proxy_status[proxy_str] = 0
            self.proxy_queue.put(proxy_str)

    def get_useful_proxies(self):
        return [proxy_str for proxy_str in self.proxy_status if self.proxy_status[proxy_str] == 0]

    def success(self,proxy_str):
        # if self.proxy_status[proxy_str] > 0:
        #     print proxy_str, 'is good, now refresh'
        self.proxy_status[proxy_str] = 0

    def add_proxy_fail(self, thread_id, proxy_str, other_message):
        self.proxy_status[proxy_str] += 1

        # print 'Thread ', thread_id, ' with ',proxy_str, ' fail', self.proxy_status[proxy_str], 'times'

        if self.proxy_status[proxy_str] > 2:
            time.sleep(5)
        if self.proxy_status[proxy_str] > 10:
            print(proxy_str,' Killed')
            return 'Suspend'
        return None
