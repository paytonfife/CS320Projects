from collections import deque
import pandas as pd

# project: p3
# submitter: pjfife
# partner: none
# hours: 6
                
        
class GraphSearcher:
    def __init__(self):
        self.visited = set()
        self.order = []
        self.sequence = ""

    def go(self, node):
        raise Exception("must be overridden in sub classes -- don't change me here!")

    def dfs_search(self, node):
        self.order = []
        self.visited.clear()
        self.dfs_visit(node)

    def dfs_visit(self, node):
        if node in self.visited:
            return
        self.visited.add(node)
        self.order.append(node)
        children = self.go(node)
        for c in children:
            self.dfs_visit(c)
            
    def bfs_search(self, node):
        self.visited.clear()
        self.bfs_visit(node)
    
    def bfs_visit(self, node):
        todo = deque([node])
        while len(todo) > 0:
            curr = todo.popleft()
            if curr in self.visited:
                pass
            self.visited.add(curr)
            self.order.append(curr)
            children = self.go(curr)
            for c in children:
                if c not in todo and c not in self.visited:
                    todo.append(c)
        
class FileSearcher(GraphSearcher):
    def __init_(self):
        super().__init__()
        self.sequence = ""
        
    def go(self, node):
        with open('file_nodes/'+node) as f:
            text = f.read()
        lines = text.split('\n')
        mess = lines[0]
        self.sequence = str(self.sequence) + str(mess)
        children = lines[1]
        return children.split(',')
        
    def message(self):
        return str(self.sequence)
            
            
class MatrixSearcher(GraphSearcher):
    def __init__(self, df):
        super().__init__()
        self.df = df

    def go(self, node):
        children = []
        for node, has_edge in self.df.loc[f"{node}"].items():
            if has_edge:
                children.append(node)
        return children

    
class WebSearcher(GraphSearcher):
    def __init__(self, driver):
        super().__init__()
        self.driver = driver
        self.tablelist = []
        
    def go(self, url):
        self.driver.get(url)
        pagesource = self.driver.page_source
        children1 = self.driver.find_elements(by = 'tag name', value = 'a')
        smalltable = pd.read_html(pagesource)[0]
        self.tablelist.append(smalltable)
        result = []
        for link in children1:
            attr = link.get_attribute('href')
            result.append(attr)
        return result
    
    def table(self):
        return pd.concat(self.tablelist, ignore_index = True)
        

    
    
    
    
    
    
    
    
    
    
    
    
    
    