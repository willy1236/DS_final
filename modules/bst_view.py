from PyQt6.QtWidgets import (QFrame, QLabel, QProgressBar, QPushButton,
                             QTableWidget, QVBoxLayout)

from modules.base import BaseModule
from stones import StoneBinaryTree


class BSTModule(BaseModule):
    def __init__(self):
        super().__init__("二元搜尋樹")
        panel = QFrame()
        panel.setFrameStyle(QFrame.Shape.Box)
        panel.setFixedWidth(200)
        left_layout = QVBoxLayout(panel)

        self.preorder_btn = QPushButton('前序遍歷')
        self.inorder_btn = QPushButton('中序遍歷')
        self.postorder_btn = QPushButton('後序遍歷')
        self.sorting_progress = QProgressBar()

        self.preorder_btn.clicked.connect(self.preorder_sort)
        self.inorder_btn.clicked.connect(self.inorder_sort)
        self.postorder_btn.clicked.connect(self.postorder_sort)
        
        left_layout.addWidget(self.preorder_btn)
        left_layout.addWidget(self.inorder_btn)
        left_layout.addWidget(self.postorder_btn)
        left_layout.addWidget(QLabel('進度：'))
        left_layout.addWidget(self.sorting_progress)
        left_layout.addStretch()
            
        self.layout().addWidget(panel)
        
        # 表格
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["編號", "長度", "寬度", "高度", "重量", "材質"])
        self.layout().addWidget(self.table)

    def preorder_sort(self):
        self.sorting_progress.setValue(0)
        bst = StoneBinaryTree(self.stones)
        self._update_table(self.table, bst.preorder())
        self.sorting_progress.setValue(100)

    def inorder_sort(self):
        self.sorting_progress.setValue(0)
        bst = StoneBinaryTree(self.stones)
        self._update_table(self.table, bst.inorder())
        self.sorting_progress.setValue(100)

    def postorder_sort(self):
        self.sorting_progress.setValue(0)
        bst = StoneBinaryTree(self.stones)
        self._update_table(self.table, bst.postorder())
        self.sorting_progress.setValue(100)