from typing import TYPE_CHECKING
from concurrent.futures import ThreadPoolExecutor

from PyQt6.QtWidgets import (QFrame, QHBoxLayout, QTableWidget,
                             QTableWidgetItem, QVBoxLayout, QWidget)

from model.stones import Stone


class BaseModule(QWidget):
    stones: list[Stone] = list()

    if TYPE_CHECKING:
        table: QTableWidget
    
    def __init__(self, name):
        super().__init__()
        self.name = name
        self.init_ui()
        
        self.executor = ThreadPoolExecutor(max_workers=1)

    def init_ui(self):
        layout = QHBoxLayout(self)
        # self.label = QLabel(f"{self.name}的內容")
        # self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # layout.addWidget(self.label)

    def create_left_panel(self):
        panel = QFrame()
        panel.setFrameStyle(QFrame.Shape.Box)
        panel.setFixedWidth(200)
        left_layout = QVBoxLayout(panel)
        return panel
    
    def create_stone_table(self):
        table = QTableWidget()
        table.setColumnCount(5)
        table.setHorizontalHeaderLabels(["編號", "重量", "硬度", "材質", "設計"])
        return table

    def update_table(self, stones: list[Stone] = None):
        stones = stones or self.stones
        self.table.setRowCount(len(stones))
        for i, stone in enumerate(stones):
            self.table.setItem(i, 0, QTableWidgetItem(str(stone.number)))
            self.table.setItem(i, 1, QTableWidgetItem(str(stone.weight)))
            self.table.setItem(i, 2, QTableWidgetItem(str(stone.hardness)))
            self.table.setItem(i, 3, QTableWidgetItem(stone.material.value))
            self.table.setItem(i, 4, QTableWidgetItem(stone.design if stone.design else "無"))

    def add_table_stone(self):
        row_count = self.table.rowCount()
        st = Stone.generate(row_count + 1)
        self.stones.append(st)

        self.table.setRowCount(row_count + 1)
        self.table.setItem(row_count, 0, QTableWidgetItem(str(st.number)))
        self.table.setItem(row_count, 1, QTableWidgetItem(str(st.weight)))
        self.table.setItem(row_count, 2, QTableWidgetItem(str(st.hardness)))
        self.table.setItem(row_count, 3, QTableWidgetItem(st.material.value))
        self.table.setItem(row_count, 4, QTableWidgetItem(st.design if st.design else "無"))