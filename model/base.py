from random import randint
from threading import Thread
from time import sleep

from .stones import Stone
from .trees import MaxHeap


class Queue:
    def __init__(self):
        self.items = list()

    @property
    def is_empty(self):
        return len(self.items) == 0
    
    def push(self, item):
        self.items.append(item)

    def pop(self):
        if not self.is_empty:
            return self.items.pop(0)
        return None
    
    def __len__(self):
        return len(self.items)

class ProcessingMachine:
    def __init__(self, pos_x, pos_y):
        self.queue = Queue()
        self.pos = (pos_x, pos_y)
        self.thread = Thread(target=self.process)
        self.heap: MaxHeap = None
        self.now_processing: Stone = None
    
    def __len__(self):
        return len(self.queue) + 1 if self.now_processing else len(self.queue)
    
    def add_stone(self, stone):
        self.queue.push(stone)
    
    def start(self):
        self.thread.start()

    def process(self):
        while True:
            if not self.queue.is_empty:
                self.now_processing = self.queue.pop()
                print(f"機器{self.pos}：正在加工 {self.now_processing}")
                sleep(randint(1, 3))
                self.now_processing.processing_degree += 1
                print(f"機器{self.pos}：{self.now_processing} 加工完成")
                if self.now_processing.processing_degree < 3:
                    self.heap.push(self.now_processing)
                self.now_processing = None
            
            sleep(1)