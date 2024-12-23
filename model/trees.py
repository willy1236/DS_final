from .stones import Stone


class TreeNode:
    def __init__(self, stone):
        self.stone: Stone = stone
        self.left: TreeNode = None 
        self.right: TreeNode = None

class StoneBinaryTree():
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
        stack = []
        current:TreeNode = self.root
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
        current:TreeNode = self.root 
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
        current:TreeNode = self.root
        result: list[Stone] = []
        last_visited:TreeNode = None
        
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
        queue:list[TreeNode] = []
        result:list[Stone] = []
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
    def __init__(self):
        self.children = {}
        self.isEnd = False

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.isEnd = True

    def search(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                return False
            node = node.children[char]
        return node.isEnd

    def startsWith(self, prefix):
        node = self.root
        for char in prefix:
            if char not in node.children:
                return False
            node = node.children[char]
        return True

class HashNode:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.next = None

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
    def __init__(self, index:int, current_weight:int, remain_weight:int, parent=None):
        self.current_weight = current_weight
        self.remain_weight = remain_weight
        self.index = index
        self.left: TruckTreeNode = None
        self.right: TruckTreeNode = None
        self.parent: TruckTreeNode = parent


def truck_loader(stones:list[Stone], max_capacity:int):
    total_weight = sum([stone.weight for stone in stones])
    root = TruckTreeNode(0, 0, total_weight)
    stack = [root]
    best_node = root

    while stack:
        node = stack.pop()
        
        if node.index < len(stones) and total_weight - node.current_weight > best_node.current_weight:
            next_stone_weight = stones[node.index].weight

            left_weight = node.current_weight + next_stone_weight
            if left_weight <= max_capacity:
                node.left = TruckTreeNode(node.index + 1, left_weight, node.remain_weight - next_stone_weight, parent=node)
                stack.append(node.left)
                if left_weight > best_node.current_weight:
                    best_node = node.left

            node.right = TruckTreeNode(node.index + 1, node.current_weight, node.remain_weight - next_stone_weight, parent=node)
            stack.append(node.right)

    # 回推路徑
    contain_stones:list[Stone] = []
    current = best_node
    while current.parent is not None:
        if current.parent.left == current:
            contain_stones.append(stones[current.index - 1])
        current = current.parent

    contain_stones.reverse()

    return best_node.current_weight, contain_stones