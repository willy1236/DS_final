from PyQt6.QtWidgets import QGraphicsView, QGraphicsScene, QLineEdit, QPushButton, QLabel
from PyQt6.QtGui import QPixmap
from modules.base import BaseModule
from model.trees import TrieTree, MaxHeap

trie_tree = TrieTree()
trie_tree.insert("apple")
trie_tree.insert("banana")
trie_tree.insert("orange")
trie_tree.insert("grape")
trie_tree.insert("peach")
trie_tree.insert("pear")
trie_tree.insert("plum")
trie_tree.insert("pineapple")
trie_tree.insert("peanut")
trie_tree.insert("pepper")
trie_tree.insert("potato")
trie_tree.insert("pumpkin")
trie_tree.insert("tomato")

max_heap = MaxHeap()

class DesignModule(BaseModule):
    def __init__(self):
        super().__init__("設計添加")

        panel = self.create_left_panel()

        self.heap_btn = QPushButton('開始設計')
        self.heap_btn.clicked.connect(self.start_processing)
        panel.layout().addWidget(self.heap_btn)
        
        design_label = QLabel("設計樣式")
        panel.layout().addWidget(design_label)

        self.design_edit = QLineEdit()
        self.design_edit.setPlaceholderText("輸入設計樣式")
        # self.max_capacity_edit.setText("1000")
        panel.layout().addWidget(self.design_edit)

        self.start_btn = QPushButton('開始設計')
        self.start_btn.clicked.connect(self.start_processing)
        panel.layout().addWidget(self.start_btn)
        
        self.label = QLabel()
        panel.layout().addWidget(self.label)

        panel.layout().addStretch()
        self.layout().addWidget(panel)

        self.grview = QGraphicsView()
        scene = QGraphicsScene()
        #scene.setSceneRect(0, 0, 300, 400)
        img = QPixmap(r"C:\Users\willy\OneDrive\圖片\螢幕擷取畫面\螢幕擷取畫面 2024-12-24 193252.png")
        scene.addPixmap(img)
        self.grview.setScene(scene)
        self.layout().addWidget(self.grview)
        

    def start_processing(self):
        text = self.design_edit.text()
        result = trie_tree.search(text)
        if result:
            self.label.setText("找到了")
        else:
            self.label.setText("沒找到")
