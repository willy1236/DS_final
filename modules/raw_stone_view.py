from PyQt6.QtWidgets import QLabel, QProgressBar, QPushButton, QTableWidgetItem

from modules.base import BaseModule
from model.stones import Stone


class RawStonesModule(BaseModule):
    def __init__(self):
        super().__init__("未加工石頭管理")

        # 左側面板
        panel = self.create_left_panel()

        self.add_btn = QPushButton('新增石頭')
        self.add10_btn = QPushButton('新增10個石頭')
        self.add50_btn = QPushButton('新增50個石頭')
        self.sort_btn = QPushButton('開始排序')
        self.sorting_progress = QProgressBar()

        self.add_btn.clicked.connect(self.add_table_stone)
        self.add10_btn.clicked.connect(self.add_raw_stone_10)
        self.add50_btn.clicked.connect(self.add_raw_stone_50)
        self.sort_btn.clicked.connect(self.sort_raw_stones)
        
        panel.layout().addWidget(self.add_btn)
        panel.layout().addWidget(self.add10_btn)
        panel.layout().addWidget(self.add50_btn)
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

    def add_raw_stone_10(self):
        for _ in range(10):
            self.add_table_stone()
    
    def add_raw_stone_50(self):
        for _ in range(50):
            self.add_table_stone()

    def sort_raw_stones(self):
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