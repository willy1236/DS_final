from PyQt6.QtWidgets import (QHBoxLayout, QTableWidget, QTableWidgetItem,
                             QWidget)

from stones import Stone


class BaseModule(QWidget):
    stones: list[Stone] = list()
    
    def __init__(self, name):
        super().__init__()
        self.name = name
        self.init_ui()

    
    def init_ui(self):
        layout = QHBoxLayout(self)
        # self.label = QLabel(f"{self.name}的內容")
        # self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # layout.addWidget(self.label)

    def _update_table(self, table: QTableWidget, stones: list[Stone] = None):
        stones = stones or self.stones
        self.table.setRowCount(len(stones))
        for i, stone in enumerate(stones):
            table.setItem(i, 0, QTableWidgetItem(str(stone.number)))
            table.setItem(i, 1, QTableWidgetItem(str(stone.length)))
            table.setItem(i, 2, QTableWidgetItem(str(stone.width)))
            table.setItem(i, 3, QTableWidgetItem(str(stone.height)))
            table.setItem(i, 4, QTableWidgetItem(str(stone.weight)))
            table.setItem(i, 5, QTableWidgetItem(stone.material.value))