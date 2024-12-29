import os

from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import (QGraphicsScene, QGraphicsView, QLabel, QLineEdit,
                             QPushButton)

from model.trees import StoneMaxHeap, TrieTree
from modules.base import BaseModule

trie_tree = TrieTree()
for path in os.listdir(r"designs"):
    trie_tree.insert(path[:-4])

max_heap = StoneMaxHeap()

class DesignModule(BaseModule):
    def __init__(self):
        super().__init__("設計展示")

        panel = self.init_left_panel()
        
        panel.layout().addWidget(QLabel("設計樣式"))

        self.design_edit = QLineEdit()
        self.design_edit.setPlaceholderText("輸入設計樣式或類型")
        panel.layout().addWidget(self.design_edit)

        self.start_btn = QPushButton('設計查詢')
        self.start_btn.clicked.connect(self.design_search)
        panel.layout().addWidget(self.start_btn)
        
        self.label = QLabel()
        panel.layout().addWidget(self.label)

        panel.layout().addStretch()

        self.grview = QGraphicsView()
        self.scene = QGraphicsScene()
        #scene.setSceneRect(0, 0, 300, 400)
        img = QPixmap(r"")
        self.scene.addPixmap(img)
        self.grview.setScene(self.scene)
        self.layout().addWidget(self.grview)
        

    def design_search(self):
        text = self.design_edit.text()
        if trie_tree.start_with(text):
            lst = trie_tree.list_prefix(text)
            self.label.setText(f"找到以下設計：\n{'\n'.join(lst)}")
            self.scene.clear()
            self.scene.addPixmap(QPixmap(r"designs/" + lst[0] + ".png"))
        else:
            self.label.setText(f"沒找到名為 {text} 的設計")
