from PyQt6.QtWidgets import QLabel, QProgressBar, QPushButton, QTableWidgetItem

from modules.base import BaseModule
from stones import Stone


class RawStonesModule(BaseModule):
    def __init__(self):
        super().__init__("未加工石頭管理")

        # 左側面板
        panel = self.create_left_panel()

        self.add_btn = QPushButton('新增石頭')
        self.sort_btn = QPushButton('開始排序')
        self.sorting_progress = QProgressBar()

        self.add_btn.clicked.connect(self.add_raw_stone)
        self.sort_btn.clicked.connect(self.sort_raw_stones)
        
        panel.layout().addWidget(self.add_btn)
        panel.layout().addWidget(self.sort_btn)
        panel.layout().addWidget(QLabel('進度：'))
        panel.layout().addWidget(self.sorting_progress)
        panel.layout().addStretch()
            
        self.layout().addWidget(panel)
        
        # self.input_1 = QLineEdit(self)
        # self.input_1.move(20,20)

        # 表格
        self.table = self.create_stone_table()
        self.layout().addWidget(self.table)

    def add_raw_stone(self):
        row_count = self.table.rowCount()
        st = Stone.generate(row_count + 1)
        self.stones.append(st)

        self.table.setRowCount(row_count + 1)
        self.table.setItem(row_count, 0, QTableWidgetItem(str(st.number)))
        self.table.setItem(row_count, 1, QTableWidgetItem(str(st.length)))
        self.table.setItem(row_count, 2, QTableWidgetItem(str(st.width)))
        self.table.setItem(row_count, 3, QTableWidgetItem(str(st.height)))
        self.table.setItem(row_count, 4, QTableWidgetItem(str(st.weight)))
        self.table.setItem(row_count, 5, QTableWidgetItem(st.material.value))

    def sort_raw_stones(self):
        n = len(self.stones)
        for i in range(1, n):
            self.sorting_progress.setValue((int(i / n) * 100))
            
            # 插入排序
            key = self.stones[i]
            j = i - 1
            while j >= 0 and self.stones[j].weight > key.weight:
                self.stones[j + 1] = self.stones[j]
                j -= 1
            self.stones[j + 1] = key
            
            self._update_table(self.table)

        self.sorting_progress.setValue(100)