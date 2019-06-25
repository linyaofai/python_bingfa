# Robot
import threading
from queue import Queue

class ThreadBot(threading.Thread):  # 线程子类，继承start/join等方法
    def __init__(self):
        super().__init__(target=self.manage_table)  # 目标函数，下面定义,默认是run方法，可以在这里指定
        self.cutlery = Cutlery(knives=0, forks=0)   # 每个机器人携带的餐具
        self.tasks = Queue()    # 机器人接收的任务被添加到任务队列

    def manage_table(self):
        while True:   # 机器人只接受三种工作
            task = self.tasks.get()
            if task == 'prepare table':
                kitchen.give(to=self.cutlery, knives=4, forks=4)
            elif task == 'clear table':
                self.cutlery.give(to=kitchen, knives=4, forks=4)
            elif task == 'shutdown':
                return
# Cutlery
from attr import attrs, attrib  # 开源库，不影响线程或协程，使实例属性的初始化更轻松

@attrs
class Cutlery:
    knives = attrib(default=0)
    forks = attrib(default=0)

    def give(self, to: 'Cutlery', knives=0, forks=0):   # 用于与其它实例交互
        self.change(-knives, -forks)
        to.change(knives, forks)

    def change(self, knives, forks):
        self.knives += knives
        self.forks += forks

kitchen = Cutlery(knives=100, forks=100)
bots = [ThreadBot() for i in range(10)]    # 创建了10个线程机器人

import sys

for bot in bots:
    for i in range(int(sys.argv[1])):   # 从命令行获取桌子的数量，然后给每个机器人安排所有桌子的任务
        bot.tasks.put('prepare table')
        bot.tasks.put('clear table')
    bot.tasks.put('shutdown')

print(f'Kitchen inventory before service: {kitchen}')
for bot in bots:
    bot.start()
for bot in bots:
    bot.join()
print(f'Kitchen inventory after service: {kitchen}')