from PyQt6.QtWidgets import QLabel, QProgressBar, QPushButton, QTableWidgetItem

from modules.base import BaseModule
from model.stones import Stone


class RawStonesModule(BaseModule):
    def __init__(self):
        super().__init__("未加工玉石管理")

        # 左側面板
        panel = self.init_left_panel()

        self.add_btn = QPushButton('新增玉石')
        self.add10_btn = QPushButton('新增10個玉石')
        self.add50_btn = QPushButton('新增50個玉石')
        self.sort_btn = QPushButton('開始排序')
        self.sorting_progress = QProgressBar()

        self.add_btn.clicked.connect(self.add_table_stone)
        self.add10_btn.clicked.connect(self.add_raw_stone_10)
        self.add50_btn.clicked.connect(self.add_raw_stone_50)
        self.sort_btn.clicked.connect(self.insertion_sort_raw_stones)
        
        panel.layout().addWidget(self.add_btn)
        panel.layout().addWidget(self.add10_btn)
        panel.layout().addWidget(self.add50_btn)
        panel.layout().addWidget(self.sort_btn)
        panel.layout().addWidget(QLabel('進度：'))
        panel.layout().addWidget(self.sorting_progress)
        panel.layout().addStretch()

        # 表格
        self.table = self.create_stone_table()
        self.layout().addWidget(self.table)

    def add_raw_stone_10(self):
        for _ in range(10):
            self.add_table_stone()
    
    def add_raw_stone_50(self):
        for _ in range(50):
            self.add_table_stone()

    def insertion_sort_raw_stones(self):
        n = len(self.stones)
        for i in range(1, n):
            self.sorting_progress.setValue((int(i / n * 100)))
            
            # 插入排序
            key = self.stones[i]
            j = i - 1
            while j >= 0 and self.stones[j].weight > key.weight:
                self.stones[j + 1] = self.stones[j]
                j -= 1
            self.stones[j + 1] = key
            
            
        self.update_table()
        self.sorting_progress.setValue(100)