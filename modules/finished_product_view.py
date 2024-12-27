from PyQt6.QtGui import QIntValidator
from PyQt6.QtWidgets import QLabel, QLineEdit, QPushButton, QTableWidgetItem

from model.trees import HashTable
from modules.base import BaseModule


class FinishedProductModule(BaseModule):
    def __init__(self):
        super().__init__("成品管理")

        self.hash_table = HashTable(1000)

        panel = self.init_left_panel()

        panel.layout().addWidget(QLabel("查詢成品"))

        self.stone_number_edit = QLineEdit()
        self.stone_number_edit.setPlaceholderText("輸入成品編號")
        self.stone_number_edit.setValidator(QIntValidator())
        panel.layout().addWidget(self.stone_number_edit)

        self.search_btn = QPushButton('查詢')
        self.search_btn.clicked.connect(self.search_stone)
        panel.layout().addWidget(self.search_btn)

        self.list_all_btn = QPushButton('列出所有成品')
        self.list_all_btn.clicked.connect(self.list_all_stones)
        panel.layout().addWidget(self.list_all_btn)
        
        panel.layout().addStretch()

        self.finished_table = self.create_stone_table()
        self.layout().addWidget(self.finished_table)

    def search_stone(self):
        self.finished_table.clearContents()
        self.finished_table.setRowCount(1)
        if self.stone_number_edit.text():
            stone_number = int(self.stone_number_edit.text())
            stone = self.hash_table.search(stone_number)
            if stone:
                self.finished_table.setItem(0, 0, QTableWidgetItem(str(stone.number)))
                self.finished_table.setItem(0, 1, QTableWidgetItem(str(stone.weight)))
                self.finished_table.setItem(0, 2, QTableWidgetItem(str(stone.hardness)))
                self.finished_table.setItem(0, 3, QTableWidgetItem(stone.material.value))
                self.finished_table.setItem(0, 4, QTableWidgetItem(stone.design if stone.design else "無"))


    def list_all_stones(self):
        self.finished_table.setRowCount(len(self.stones))
        for i, stone in enumerate([stone for stone in self.stones if stone.processing_degree == 3]):
            self.hash_table.insert(stone.number, stone)
            self.finished_table.setItem(i, 0, QTableWidgetItem(str(stone.number)))
            self.finished_table.setItem(i, 1, QTableWidgetItem(str(stone.weight)))
            self.finished_table.setItem(i, 2, QTableWidgetItem(str(stone.hardness)))
            self.finished_table.setItem(i, 3, QTableWidgetItem(stone.material.value))
            self.finished_table.setItem(i, 4, QTableWidgetItem(stone.design if stone.design else "無"))