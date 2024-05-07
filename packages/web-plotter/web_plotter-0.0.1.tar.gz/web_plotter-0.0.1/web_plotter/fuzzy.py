from flask import jsonify
from web_plotter.helper import numArguments

class FuzzyNode:
    def __init__(self, execute_backend_callback=lambda: None):
        self._kids = []
        self.execute_backend_callback = execute_backend_callback

    def __str__(self) -> str:
        return "base class should implement a name"

    def __hash__(self):
        return hash(str(self))

    def updateFrontEnd(self):
        return jsonify('close virtual window')

    def transition(self):
        return self

    def executeBackend(self):
        # extremely important: late binding closures are a problem so we use default arguments for them in the callbacks
        # do not change the code to use them here, otherwise we may face problems

        if numArguments(self.execute_backend_callback) == 1:
            self.execute_backend_callback(self)
        else:
            self.execute_backend_callback()

    def getChosenNode(self, str_chosen_node: str):
        for kid in self._kids:
            if str(kid) == str_chosen_node:
                return kid
    
    @property
    def kids(self):
        ## list → the names of each node can change depending on the situation
        return list(map(str, self._kids))
    
        ## dict → names of each node cannot change
        # return list(self._kids.keys())
    @kids.setter
    def kids(self, new_kids):
        self.setKids(new_kids)

    def setKids(self, new_kids):
        self._kids = list(new_kids)
        
    def addKid(self, kid, pos=-1):
        ## list
        if pos == -1:
            self._kids.append(kid)
        else:
            self._kids.insert(pos, kid)
        
        ## dict
        # self._kids[str(kid)]are = kid

    def addKids(self, kids):
        ## list
        self._kids += kids

        ## dict
        # for kid in kids:
        #     self.addKid(kid)


class RootNode(FuzzyNode):
    def __init__(self):
        if not hasattr(self, "_kids"):
            super().__init__()

    def __str__(self) -> str:
        return "root"

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(RootNode, cls).__new__(cls)
        return cls.instance
    def updateFrontEnd(self):
        return jsonify('open virtual window')

class TerminalNode(FuzzyNode):
    def __init__(self, root_node, display_str, update_front_end, *args, **kwargs):
        self.root_node = root_node
        self.display_str = display_str
        self.update_front_end = update_front_end
        super().__init__(*args, **kwargs)

    def updateFrontEnd(self):
        return jsonify(self.update_front_end)
    
    def __str__(self):
        return self.display_str

    def transition(self):
        return self.root_node

class ChoiceNode(FuzzyNode):
    def __init__(self, display_str, update_front_end, root_node, *args, **kwargs):
        self.display_str = display_str
        self.update_front_end = update_front_end
        self.root_node = root_node
        super().__init__(*args, **kwargs)

    def updateFrontEnd(self):
        return jsonify(self.update_front_end)

    def __str__(self):
        if callable(self.display_str):
            return self.display_str()
        else:
            return self.display_str

    def transition(self):
        return self

    def executeBackend(self):
        super().executeBackend()
        self.addKid(self.root_node, 0)


class CurrentNodeHandler:
    def __init__(self, initial_node: FuzzyNode):
        self.root_node = initial_node
        self.assign(initial_node)

    def assign(self, current_node):
        self._current_node = current_node

    def get(self):
        return self._current_node

