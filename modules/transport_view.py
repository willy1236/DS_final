from math import inf
from collections import defaultdict

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QBrush, QPainter, QPen, QFont
from PyQt6.QtWidgets import (QComboBox, QGraphicsEllipseItem, QGraphicsScene,
                             QGraphicsTextItem, QGraphicsView, QGroupBox,
                             QLabel, QPushButton, QVBoxLayout, QWidget)

from modules.base import BaseModule
from model.base import Queue
from model.trees import DijkstraMinHeap, GraphMinHeap

# Adjacency List
graph = {
    1: [(4, 4), (5, 3)],
    2: [(4, 7)],
    3: [(4, 8), (6, 11)],
    4: [(1, 4), (2, 7), (3, 8), (6, 11), (7, 4)],
    5: [(1, 3), (7, 15)],
    6: [(3, 11), (4, 11), (7, 6), (8, 14)],
    7: [(4, 4), (5, 15), (6, 6), (9, 5)],
    8: [(6, 14), (9, 10), (10, 8)],
    9: [(7, 5), (8, 10)],
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

class UnionFind:
    def __init__(self, size: int):
        self.parent = list(range(size + 1))
        self.rank = [0] * (size + 1)

    def find(self, x: int) -> int:
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])  # Path compression
        return self.parent[x]

    def union(self, x: int, y: int) -> bool:
        rootX = self.find(x)
        rootY = self.find(y)
        
        if rootX != rootY:
            if self.rank[rootX] > self.rank[rootY]:
                self.parent[rootY] = rootX
            elif self.rank[rootX] < self.rank[rootY]:
                self.parent[rootX] = rootY
            else:
                self.parent[rootY] = rootX
                self.rank[rootX] += 1
            return True
        return False

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
        panel = self.init_left_panel()
    
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
        
        self.bfs_btn = QPushButton('BFS拜訪')
        self.dfs_btn = QPushButton('DFS拜訪')
        self.prim_btn = QPushButton('Prim演算法')
        self.kruskal_btn = QPushButton('Kruskal演算法')
        self.sollin_btn = QPushButton('Sollin演算法')
        self.dijkstra_btn = QPushButton('Dijkstra尋路')
        
        self.bfs_btn.clicked.connect(self.start_bfs)
        self.dfs_btn.clicked.connect(self.start_dfs)
        self.prim_btn.clicked.connect(self.prim)
        self.kruskal_btn.clicked.connect(self.kruskal)
        self.sollin_btn.clicked.connect(self.sollin)
        self.dijkstra_btn.clicked.connect(self.dijkstra)

        panel.layout().addWidget(self.bfs_btn)
        panel.layout().addWidget(self.dfs_btn)
        panel.layout().addWidget(self.prim_btn)
        panel.layout().addWidget(self.kruskal_btn)
        panel.layout().addWidget(self.sollin_btn)
        panel.layout().addWidget(self.dijkstra_btn)
        
        panel.layout().addStretch()

        # 圖的視覺化
        self.graph_view = GraphVisualizer()
        graph_layout = QVBoxLayout()
        graph_layout.addWidget(self.graph_view)

        font = QFont()
        font.setPointSize(14)
        self.label = QLabel('請選擇起點和終點')
        self.label.setFont(font)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        graph_layout.addWidget(self.label)

        graph_container = QWidget()
        graph_container.setLayout(graph_layout)
        self.layout().addWidget(graph_container)
        
    def start_bfs(self):
        start = int(self.start_combo.currentText())
        order = self.bfs(start)
        self.label.setText(f'BFS順序：{order}')

    def start_dfs(self):
        start = int(self.start_combo.currentText())
        order = self.dfs(start)
        self.label.setText(f'DFS順序：{order}')

    @staticmethod
    def bfs(start):
        visited = set()
        queue:Queue[int] = Queue()
        queue.push(start)
        order = []
        
        while not queue.is_empty:
            node = queue.pop()
            if node not in visited:
                visited.add(node)
                order.append(node)
                for neighbor, _ in graph.get(node, []):
                    if neighbor not in visited:
                        queue.push(neighbor)
        return order

    @classmethod
    def dfs(cls, start, visited=None):
        if visited is None:
            visited = set()
        visited.add(start)
        order = [start]
        for neighbor, _ in graph.get(start, []):
            if neighbor not in visited:
                order.extend(cls.dfs(neighbor, visited))
        return order

    def dijkstra(self):
        def construct_path(previous, end):
            path = []
            current = end
            while current is not None:
                path.append(current)
                current = previous[current]
            path.reverse()
            return path

        start = int(self.start_combo.currentText())
        end = int(self.end_combo.currentText())
        if start == end:
            self.label.setText('起點和終點相同')
            return
        
        distance = {node: inf for node in graph}
        distance[start] = 0
        previous = {node: None for node in graph}

        min_heap = DijkstraMinHeap()
        min_heap.push((start, 0))

        while not min_heap.is_empty:
            current_node, current_distance = min_heap.pop()

            for neighbor, weight in graph[current_node]:
                new_dist = current_distance + weight
                if new_dist < distance[neighbor]:
                    distance[neighbor] = new_dist
                    previous[neighbor] = current_node
                    min_heap.push((neighbor, new_dist))
        
        path = [str(i) for i in construct_path(previous, end)]
        self.label.setText(f'從節點{start}到節點{end}的最短成本：{distance[end]}，路徑為 {"->".join(path)}')

    def prim(self):
        start = int(self.start_combo.currentText())
        mst_edges = []
        visited = set()
        min_heap = GraphMinHeap()
        
        visited.add(start)
        for neighbor, weight in graph[start]:
            min_heap.push((weight, start, neighbor))
        
        while not min_heap.is_empty:
            weight, node1, node2 = min_heap.pop()
            
            if node2 in visited:
                continue
            
            mst_edges.append((node1, node2, weight))
            visited.add(node2)
            
            for neighbor, weight in graph[node2]:
                if neighbor not in visited:
                    min_heap.push((weight, node2, neighbor))

        mst_text = ", ".join(f"({u}, {v})" for u, v, w in mst_edges)
        mst_sum = sum([w for u, v, w in mst_edges])
        self.label.setText(f"Prim's method MST: {mst_text}，總成本：{mst_sum}")

    def kruskal(self):
        min_heap = GraphMinHeap()
        for node, neighbors in graph.items():
            for neighbor, weight in neighbors:
                if node < neighbor:
                    min_heap.push((weight, node, neighbor))

        uf = UnionFind(len(graph))

        mst = []
        mst_weight = 0
        while not min_heap.is_empty:
            weight, u, v = min_heap.pop()
            if uf.union(u, v):
                mst.append((u, v, weight))
                mst_weight += weight

        mst_text = ", ".join(f"({u}, {v})" for u, v, w in mst)
        self.label.setText(f"Kruskal's method MST: {mst_text}，總成本：{mst_weight}")

    def sollin(self):
        parent = {node: node for node in graph}
        rank = {node: 0 for node in graph}
        mst = []
        
        def find(x: int) -> int:
            if parent[x] != x:
                parent[x] = find(parent[x])
            return parent[x]

        def union(x: int, y: int) -> bool:
            rootX = find(x)
            rootY = find(y)

            if rootX != rootY:
                if rank[rootX] > rank[rootY]:
                    parent[rootY] = rootX
                elif rank[rootX] < rank[rootY]:
                    parent[rootX] = rootY
                else:
                    parent[rootY] = rootX
                    rank[rootX] += 1
                return True
            return False
        
        min_heap = GraphMinHeap()

        for u in graph:
            for v, weight in graph[u]:
                min_heap.push((weight, u, v))
        
        while len(mst) < len(graph) - 1:
            weight, u, v = min_heap.pop()
            
            if union(u, v):
                mst.append((u, v, weight))
        
        mst_text = ", ".join(f"({u}, {v})" for u, v, w in mst)
        mst_sum = sum([w for u, v, w in mst])
        self.label.setText(f"Sollin's method MST: {mst_text}，總成本：{mst_sum}")