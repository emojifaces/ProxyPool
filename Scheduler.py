import time

TESTER_CYCLE = 20
GETTER_CYCLE = 20
TESTER_ENABLED = True
GETTER_ENABLED = True
API_ENABLED = True

API_HOST = 'localhost'
API_PORT = 5000

from multiprocessing import Process
from app import app
from Getter import Getter
from Tester import Tester


class Scheduler():
    def scheduler_tester(self,cycle=TESTER_CYCLE):
        tester = Tester()
        while True:
            print('测试器开始运行')
            tester.run()
            time.sleep(cycle)

    def scheduler_getter(self,cycle=GETTER_CYCLE):
        getter = Getter()
        while True:
            print('开始抓取代理')
            getter.run()
            time.sleep(cycle)

    def scheduler_api(self):
        app.run(API_HOST,API_PORT)

    def run(self):
        print('代理池开始运行')
        if TESTER_ENABLED:
            tester_process = Process(target=self.scheduler_tester)
            tester_process.start()

        if GETTER_ENABLED:
            getter_process = Process(target=self.scheduler_getter)
            getter_process.start()

        if API_ENABLED:
            api_process = Process(target=self.scheduler_api)
            api_process.start()

if __name__ == '__main__':
    scheduler = Scheduler()
    scheduler.run()