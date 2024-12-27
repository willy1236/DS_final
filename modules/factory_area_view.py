from time import sleep

from PyQt6.QtWidgets import QLabel, QPushButton, QTableWidget, QTableWidgetItem

from model.base import ProcessingMachine
from model.trees import MaxHeap
from modules.base import BaseModule

max_heap = MaxHeap()
processing_machine = {
    0: [ProcessingMachine(0, 2) ,ProcessingMachine(4, 2), ProcessingMachine(8, 2)],
    1: [ProcessingMachine(0, 5) ,ProcessingMachine(4, 5), ProcessingMachine(8, 5)],
    2: [ProcessingMachine(0, 9) ,ProcessingMachine(4, 9), ProcessingMachine(8, 9)]
}

areas_matrix = list()
for _ in range(10):
    areas_matrix.append([0] * 10)

class FactoryAreaModule(BaseModule):
    def __init__(self):
        super().__init__("加工廠區")

        panel = self.init_left_panel()
        self.start_processing_btn = QPushButton('開始加工')
        self.start_processing_btn.clicked.connect(self.start_processing)
        panel.layout().addWidget(self.start_processing_btn)

        self.processing_count_label = QLabel("待加工：0")
        panel.layout().addWidget(self.processing_count_label)

        panel.layout().addStretch()

        self.area_table = QTableWidget()
        self.area_table.setColumnCount(10)
        self.area_table.setRowCount(10)
        for j in range(self.area_table.columnCount()):
            self.area_table.setColumnWidth(j, 15)
            for i in range(self.area_table.rowCount()):
                self.area_table.setItem(i, j, QTableWidgetItem(str(areas_matrix[i][j])))
        self.layout().addWidget(self.area_table)
        
    def update_area_table(self):
        for i in range(self.area_table.rowCount()):
            for j in range(self.area_table.columnCount()):
                self.area_table.setItem(i, j, QTableWidgetItem(str(areas_matrix[i][j])))
        
    def build_priority_queue(self):
        for st in [stone for stone in self.stones if stone.processing_degree < 3]:
            max_heap.push(st)

        self.processing_count_label.setText(f"待加工：{len(max_heap)}")

    def start_processing(self):
        self.build_priority_queue()
        self.executor.submit(self.processing_thread)

    def processing_thread(self):
        has_stone = True
        for machines in processing_machine.values():
            for machine in machines:
                machine.heap = max_heap
                machine.start()
        
        while has_stone:
            stone = max_heap.pop()
            if stone:
                machines = processing_machine[stone.processing_degree]
                min_queue_machine = min(machines, key=lambda x: len(x))
                min_queue_machine.add_stone(stone)
            else:
                has_stone = False
            
            for machines in processing_machine.values():
                for machine in machines:
                    areas_matrix[machine.pos[0]][machine.pos[1]] = len(machine)
                    if len(machine) > 0:
                        has_stone = True
            
            self.update_area_table()
            self.processing_count_label.setText(f"待加工：{len(max_heap)}")
                
            sleep(0.5)

