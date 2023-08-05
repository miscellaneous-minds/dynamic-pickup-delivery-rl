class Optimizer:
    def __init__(self):
        self.route = []
    
    def optimize(self):
        pass

class Suboptimal_Optimizer(Optimizer):
    def __init__(self):
        super.__init__()
    
    def optimize(self, route, added_nodes):
        self.route = route
        self.pickup_node = added_nodes[0]
        self.delivery_node = added_nodes[1]
        # Find the smallest inserting position for each two added nodes
        self.route = []    