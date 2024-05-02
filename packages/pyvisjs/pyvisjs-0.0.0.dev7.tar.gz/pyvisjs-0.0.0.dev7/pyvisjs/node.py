from .base_dictable import BaseDictable

class Node(BaseDictable):
    def __init__(self, id, label:str=None, color:str=None, shape="dot", size=None, cid=None, **kwargs):
        super().__init__()
        self.id = id
        self.label = label or str(id)
        self.color = color
        self.shape = shape
        self.size = size
        self.cid = cid

        for key, value in kwargs.items():
            setattr(self, key, value)

    def __repr__(self):
        return f"Node({self.id}, \'{self.label}\', \'{self.color}\', \'{self.shape}\', {self.size}, {self.cid})"