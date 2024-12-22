import sys

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QBrush, QPainter, QPen
from PyQt6.QtWidgets import (QGroupBox, QGraphicsEllipseItem,
                             QComboBox, QGraphicsScene,
                             QGraphicsTextItem, QGraphicsView, QLabel,
                             QProgressBar, QPushButton, QTableWidgetItem,
                             QVBoxLayout, QWidget)

from modules.base import BaseModule

# Adjacency List
graph = {
    1: [(4, 4), (5, 3)],
    2: [(4, 7)],
    3: [(4, 8), (6, 11)],
    4: [(1, 4), (2, 7), (3, 8), (7, 4), (6, 11)],
    5: [(1, 3), (4, 4), (7, 15)],
    6: [(3, 11), (4, 11), (7, 6), (8, 14)],
    7: [(5, 15), (6, 6), (9, 5)],
    8: [(6, 14), (9, 10), (10, 8)],
    9: [(7, 5)],
    10: [(8, 8)]
}

node_positions = {
    1: (200, 100),
    2: (80, 200),
    3: (150, 300),
    4: (250, 200),
    5: (350, 120),
    6: (350, 300),
    7: (500, 180),
    8: (500, 250),
    9: (650, 100),
    10: (650, 280)
}

class GraphVisualizer(QGraphicsView):
    def __init__(self):
        super().__init__()
        self.scene = QGraphicsScene()
        self.setScene(self.scene)
        self.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.draw_graph()

    def draw_graph(self):
        # 畫邊
        pen = QPen(Qt.GlobalColor.black)
        for node, edges in graph.items():
            x1, y1 = node_positions[node]
            for edge, weight in edges:
                x2, y2 = node_positions[edge]
                self.scene.addLine(x1, y1, x2, y2, pen)
                # 顯示權重
                weight_text = QGraphicsTextItem(str(weight))
                weight_text.setPos((x1 + x2) / 2, (y1 + y2) / 2)
                self.scene.addItem(weight_text)
        
        # 畫節點
        for node, (x, y) in node_positions.items():
            ellipse = QGraphicsEllipseItem(x - 15, y - 15, 30, 30)
            ellipse.setBrush(QBrush(Qt.GlobalColor.yellow))
            self.scene.addItem(ellipse)
            text = QGraphicsTextItem(str(node))
            text.setPos(x - 5, y - 10)
            self.scene.addItem(text)
            # 節點編號標註
            node_label = QGraphicsTextItem(f'Node {node}')
            node_label.setPos(x - 25, y - 35)
            self.scene.addItem(node_label)

class TransportModule(BaseModule):
    def __init__(self):
        super().__init__("運輸管理")
        # 左側面板
        panel = self.create_left_panel()
    
        start_group = QGroupBox("起點")
        start_layout = QVBoxLayout()
        self.start_combo = QComboBox()
        for node in node_positions.keys():
            self.start_combo.addItem(str(node))
        start_layout.addWidget(self.start_combo)
        start_group.setLayout(start_layout)
        panel.layout().addWidget(start_group)

        end_group = QGroupBox("終點")
        end_layout = QVBoxLayout()
        self.end_combo = QComboBox()
        for node in node_positions.keys():
            self.end_combo.addItem(str(node))
        end_layout.addWidget(self.end_combo)
        end_group.setLayout(end_layout)
        panel.layout().addWidget(end_group)
        
        self.path_btn = QPushButton('演算法尋路')
        # self.path_btn.clicked.connect(self.find_path)
        panel.layout().addWidget(self.path_btn)
        
        panel.layout().addStretch()
        self.layout().addWidget(panel)

        # 圖的視覺化
        self.graph_view = GraphVisualizer()
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.graph_view)
        self.label = QLabel('請選擇起點和終點')
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(self.label)

        main_container = QWidget()
        main_container.setLayout(main_layout)
        self.layout().addWidget(main_container)


