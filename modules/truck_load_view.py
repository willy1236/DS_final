from PyQt6.QtWidgets import QTableWidget, QTableWidgetItem, QLineEdit, QPushButton, QLabel
from PyQt6.QtGui import QIntValidator
from modules.base import BaseModule
from model.trees import truck_loader

class TruckLoadModule(BaseModule):
    def __init__(self):
        super().__init__("卡車載重管理")

        # 左側面板
        panel = self.create_left_panel()
        label = QLabel("最大載重")
        panel.layout().addWidget(label)

        self.max_capacity_edit = QLineEdit()
        self.max_capacity_edit.setPlaceholderText("輸入最大載重")
        self.max_capacity_edit.setValidator(QIntValidator())
        self.max_capacity_edit.setText("500")
        panel.layout().addWidget(self.max_capacity_edit)

        self.start_btn = QPushButton('開始載重')
        self.start_btn.clicked.connect(self.start_trucks_load_thread)
        panel.layout().addWidget(self.start_btn)
        panel.layout().addStretch()

        self.layout().addWidget(panel)

        self.truck_table = QTableWidget()
        self.truck_table.setColumnCount(3)
        self.truck_table.setHorizontalHeaderLabels(["卡車編號", "總載重", "載運石頭編號"])
        self.layout().addWidget(self.truck_table)

    def start_trucks_load(self):
        max_capacity = int(self.max_capacity_edit.text())
        stone_unloaded = [stone for stone in self.stones.copy() if stone.weight <= max_capacity]
        truck_number = 0
        self.truck_table.clearContents()
        while stone_unloaded:
            truck_load_weight, contain, stone_unloaded = truck_loader(stone_unloaded, max_capacity)
            
            self.truck_table.setRowCount(truck_number + 1)
            self.truck_table.setItem(truck_number, 0, QTableWidgetItem(str(truck_number + 1)))
            self.truck_table.setItem(truck_number, 1, QTableWidgetItem(str(truck_load_weight)))
            self.truck_table.setItem(truck_number, 2, QTableWidgetItem(", ".join([str(stone.number) for stone in contain])))
            truck_number += 1
            
        self.start_btn.setDisabled(False)

    def start_trucks_load_thread(self):
        self.start_btn.setDisabled(True)
        self.executor.submit(self.start_trucks_load)