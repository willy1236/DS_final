import sys

from PyQt6.QtWidgets import (QApplication, QHBoxLayout, QMainWindow,
                             QPushButton, QToolBar, QWidget)

from modules.bst_view import BSTModule
from modules.raw_stone_view import RawStonesModule
from modules.transport_view import TransportModule
from modules.truck_load_view import TruckLoadModule
from modules.design_view import DesignModule
from modules.finished_product_view import FinishedProductModule
from modules.factory_area_view import FactoryAreaModule


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("自動化玉石加工管理系統")
        self.setGeometry(100, 100, 1200, 800)
        
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QHBoxLayout(self.central_widget)
        
        self.modules = {
            "未加工玉石管理": RawStonesModule(),
            "二元搜尋樹": BSTModule(),
            "運輸管理": TransportModule(),
            "卡車載重管理": TruckLoadModule(),
            "加工廠區": FactoryAreaModule(),
            "設計添加": DesignModule(),
            "成品管理": FinishedProductModule(),
            
        }
        
        self.create_toolbar()
        
        self.content_widget = QWidget()
        self.content_layout = QHBoxLayout(self.content_widget)
        self.main_layout.addWidget(self.content_widget)
        
        self.switch_module("未加工玉石管理")

    def create_toolbar(self):
        toolbar = QToolBar()
        self.addToolBar(toolbar)
        
        for module_name in self.modules.keys():
            btn = QPushButton(module_name)
            btn.clicked.connect(lambda checked, m=module_name: self.switch_module(m))
            toolbar.addWidget(btn)
    
    def switch_module(self, module_name: str):
        while self.content_layout.count():
            item = self.content_layout.takeAt(0)
            if item.widget():
                item.widget().setParent(None)
        
        if module_name in self.modules:
            self.content_layout.addWidget(self.modules[module_name])

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()