from typing import TypeVar
from abc import ABC, abstractmethod

from model.stones import Stone

T = TypeVar('T')


class TreeNode:
    __slots__ = ['stone', 'left', 'right']

    def __init__(self, stone):
        self.stone: Stone = stone
        self.left: TreeNode = None 
        self.right: TreeNode = None

class StoneBinarySearchTree():
    def __init__(self, stones: list[Stone]):
        self.root: TreeNode = None
        for s in stones:
            self.insert(s)

    def insert(self, stone: Stone):
        if not self.root:
            self.root = TreeNode(stone)
        else:
            current = self.root
            while True:
                # 以weight作為排序依據
                if stone.weight < current.stone.weight:
                    if current.left:
                        current = current.left
                    else:
                        current.left = TreeNode(stone)
                        break
                else:
                    if current.right:
                        current = current.right
                    else:
                        current.right = TreeNode(stone)
                        break  

    # 中序非遞迴遍歷
    def inorder(self):
        stack: list[TreeNode] = []
        current: TreeNode = self.root
        result: list[Stone] = []
        
        while stack or current:
            while current:
                stack.append(current)
                current = current.left
            
            current = stack.pop()
            result.append(current.stone)
            current = current.right
        
        return result

    # 前序非遞迴遍歷
    def preorder(self):
        stack = []
        current: TreeNode = self.root 
        result: list[Stone] = []
        
        while stack or current:
            while current:
                result.append(current.stone)
                stack.append(current)
                current = current.left
            
            current = stack.pop()
            current = current.right
        
        return result
    
    # 後序非遞迴遍歷
    def postorder(self):
        stack = []
        current: TreeNode = self.root
        result: list[Stone] = []
        last_visited: TreeNode = None
        
        while stack or current:
            while current:
                stack.append(current)
                current = current.left

            current = stack[-1]
            if current.right is None or current.right == last_visited:
                result.append(current.stone)
                stack.pop()
                last_visited = current
                current = None
            else:
                current = current.right

        return result
    
    def levelorder(self):
        queue: list[TreeNode] = []
        result: list[Stone] = []
        if self.root:
            queue.append(self.root)
        
        while queue:
            current = queue.pop(0)
            result.append(current.stone)
            if current.left:
                queue.append(current.left)
            if current.right:
                queue.append(current.right)
        
        return result
    
class TrieNode:
    __slots__ = ['char', 'children']
    
    def __init__(self, char=None):
        self.char: str = char
        self.children: list[TrieNode] = list()

    @property
    def is_end(self):
        return len(self.children) == 0

class TrieTree:
    def __init__(self):
        self.root = TrieNode()

    def get_children(self, node:TrieNode, char:str):
        for child in node.children:
            if child.char == char:
                return child
        return None

    def insert(self, word):
        node = self.root
        for char in word:
            child = self.get_children(node, char)
            
            if not child:
                new_node = TrieNode(char)
                node.children.append(new_node)
                node = new_node
            else:
                node = child

    def search(self, word):
        node = self.root
        for char in word:
            child = self.get_children(node, char)
            if not child:
                return False
            node = child
        
        return node.is_end

    def start_with(self, prefix):
        node = self.root
        for char in prefix:
            child = self.get_children(node, char)
            if not child:
                return False
            node = child
        return True
    
    def list_prefix(self, prefix: str):
        result = []
        node = self.root
        for char in prefix:
            child = self.get_children(node, char)
            if not child:
                return result
            node = child

        self._dfs(node, prefix, result)
        return result

    def _dfs(self, node: TrieNode, current_word: str, result: list):
        if node.is_end:
            result.append(current_word)
        
        for child_node in node.children:
            self._dfs(child_node, current_word + child_node.char, result)
        

class HashNode:
    __slots__ = ['key', 'value', 'next']

    def __init__(self, key, value):
        self.key: int = key
        self.value: Stone = value
        self.next: HashNode = None

class HashTable:
    def __init__(self, capacity=10):
        self.capacity = capacity
        self.size = 0
        self.table:list[HashNode | None] = [None] * self.capacity

    def _hash(self, key):
        return hash(key) % self.capacity

    def insert(self, key, value):
        index = self._hash(key)
        node = self.table[index]

        while node:
            if node.key == key:
                node.value = value
                return
            node = node.next

        new_node = HashNode(key, value)
        new_node.next = self.table[index]
        self.table[index] = new_node
        self.size += 1

    def search(self, key):
        index = self._hash(key)
        node = self.table[index]

        while node:
            if node.key == key:
                return node.value
            node = node.next
        return None

    def delete(self, key):
        index = self._hash(key)
        node = self.table[index]
        prev = None

        while node:
            if node.key == key:
                if prev:
                    prev.next = node.next
                else:
                    self.table[index] = node.next
                self.size -= 1
                return True
            prev = node
            node = node.next
        return False

    def display(self):
        for i, node in enumerate(self.table):
            print(f"索引 {i}:", end=" ")
            current = node
            while current:
                print(f"[{current.key}: {current.value}]", end=" -> ")
                current = current.next
            print("None")

class TruckTreeNode:
    __slots__ = ['current_weight', 'remain_weight', 'index', 'left', 'right', 'parent']

    def __init__(self, index:int, current_weight:int, remain_weight:int, parent=None):
        self.current_weight = current_weight
        self.remain_weight = remain_weight
        self.index = index
        self.left: TruckTreeNode = None
        self.right: TruckTreeNode = None
        self.parent: TruckTreeNode = parent


def truck_loader(stones: list[Stone], max_capacity: int):
    # Branch and Bound 演算法
    total_weight = sum(stone.weight for stone in stones)
    
    root = TruckTreeNode(0, 0, total_weight)
    stack = [root]
    best_node = root

    while stack:
        node = stack.pop()

        # 剪枝: 剩餘重量 + 當前重量無法超越最佳重量
        if node.index < len(stones) and node.current_weight + node.remain_weight > best_node.current_weight:
            next_stone_weight = stones[node.index].weight

            # 左子節點：選擇當前玉石
            left_weight = node.current_weight + next_stone_weight
            if left_weight <= max_capacity:
                node.left = TruckTreeNode(node.index + 1, left_weight, node.remain_weight - next_stone_weight, parent=node)
                if left_weight > best_node.current_weight:
                    best_node = node.left
                stack.append(node.left)

            # 右子節點：不選擇當前玉石
            # 剪枝: 當前重量 + 剩餘重量 - 下個玉石重量 無法超越最佳重量
            if node.current_weight + (node.remain_weight - next_stone_weight) > best_node.current_weight:
                node.right = TruckTreeNode(node.index + 1, node.current_weight, node.remain_weight - next_stone_weight, parent=node)
                stack.append(node.right)

    # 回溯路徑
    contain_stones: list[Stone] = []
    selected_indices = set()
    current = best_node
    while current.parent is not None:
        if current.parent.left == current:
            selected_indices.add(current.index - 1)
        current = current.parent

    contain_stones = [stones[i] for i in selected_indices]
    remaining_stones = [stone for i, stone in enumerate(stones) if i not in selected_indices]

    return best_node.current_weight, contain_stones, remaining_stones


class Heap[T](ABC):
    def __init__(self):
        self.heap:list[T] = []

    def __len__(self):
        return len(self.heap)
    
    def _parent(self, index):
        return (index - 1) // 2

    def _left_child(self, index):
        return 2 * index + 1

    def _right_child(self, index):
        return 2 * index + 2

    def _swap(self, i, j):
        self.heap[i], self.heap[j] = self.heap[j], self.heap[i]

    @abstractmethod
    def _heapify_up(self, index: int):
        ...

    @abstractmethod
    def _heapify_down(self, index: int):
        ...

    def peek(self):
        if not self.heap:
            return None
        return self.heap[0]
    
    def push(self, value: T):
        self.heap.append(value)
        self._heapify_up(len(self.heap) - 1)

    def pop(self):
        if not self.heap:
            return None
        if len(self.heap) == 1:
            return self.heap.pop()
        
        self._swap(0, len(self.heap) - 1)
        min_value = self.heap.pop()
        self._heapify_down(0)
        return min_value

    def __str__(self):
        return str(self.heap)
    
    @property
    def is_empty(self):
        return len(self.heap) == 0

class StoneMaxHeap(Heap[Stone]):
    def _heapify_up(self, index:int):
        parent = self._parent(index)
        while index > 0 and self.heap[index].hardness > self.heap[parent].hardness:
            self._swap(index, parent)
            index = parent
            parent = self._parent(index)

    def _heapify_down(self, index:int):
        size = len(self.heap)
        while True:
            left = self._left_child(index)
            right = self._right_child(index)
            largest = index

            if left < size and self.heap[left].hardness > self.heap[largest].hardness:
                largest = left
            if right < size and self.heap[right].hardness > self.heap[largest].hardness:
                largest = right

            if largest == index:
                break

            self._swap(index, largest)
            index = largest
    
class DijkstraMinHeap(Heap[tuple[int, int]]):
    def _heapify_up(self, index: int):
        parent = self._parent(index)
        while index > 0 and self.heap[index][1] < self.heap[parent][1]:
            self._swap(index, parent)
            index = parent
            parent = self._parent(index)

    def _heapify_down(self, index: int):
        size = len(self.heap)
        while True:
            left = self._left_child(index)
            right = self._right_child(index)
            smallest = index

            if left < size and self.heap[left][1] < self.heap[smallest][1]:
                smallest = left
            if right < size and self.heap[right][1] < self.heap[smallest][1]:
                smallest = right

            if smallest == index:
                break

            self._swap(index, smallest)
            index = smallest

class GraphMinHeap(Heap[tuple[int, int, int]]):
    # Tuple: (weight, node1, node2)
    def _heapify_up(self, index: int):
        parent = self._parent(index)
        while index > 0 and self.heap[index][0] < self.heap[parent][0]:
            self._swap(index, parent)
            index = parent
            parent = self._parent(index)

    def _heapify_down(self, index: int):
        size = len(self.heap)
        while True:
            left = self._left_child(index)
            right = self._right_child(index)
            smallest = index

            if left < size and self.heap[left][0] < self.heap[smallest][0]:
                smallest = left
            if right < size and self.heap[right][0] < self.heap[smallest][0]:
                smallest = right

            if smallest == index:
                break

            self._swap(index, smallest)
            index = smallest