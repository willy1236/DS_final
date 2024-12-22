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