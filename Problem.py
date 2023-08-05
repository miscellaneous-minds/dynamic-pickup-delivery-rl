class Node:
    def __init__(self, index, x, y, size, type: str):
        self.index = index
        self.x = x
        self.y = y
        self.size = size
        self.type = type

class Order:
    def __init__(self, index, t, speed, size, pickup_node: Node, delivery_node: Node):
        self.index = index
        self.t_init = t
        if(speed == 'quick'): self.t_arrival = t + 20
        else: self.t_arrival = t + 100
        self.size = size
        self.pickup_node = pickup_node
        self.delivery_node = delivery_node
        self.state = 'waiting'

class Problem:
    def __init__(self, rng, map_size, order_num, vehicle_num, max_time, product_size, product_probability):
        self.rng = rng
        self.map_size = map_size
        self.order_num = order_num
        self.vehicle_num = vehicle_num
        self.max_time = max_time
        self.product_size = product_size
        self.product_probability = product_probability
        self.clock = 0
        self.index_to_order = {}
        self.orders = []
        self.latest_order = 0
        self.product_sizes = self.rng.choice(self.product_size, order_num, p = self.product_probability)
        for i in self.order_num:
            pickup_node = Node(i, self.rng.random() * self.map_size, self.rng.random() * self.map_size, -self.product_sizes[i], 'pickup')
            delivery_node = Node(i, self.rng.random() * self.map_size, self.rng.random() * self.map_size, self.product_sizes[i], 'delivery')
            order = Order(i, int(self.rng.random() * self.max_time), 'regular', self.product_sizes[i], pickup_node, delivery_node)
            self.index_to_order[i] = order
            self.orders.append(order)
        self.orders.sort(key = lambda x: x.t_init)
    
    def update(self, t):
        self.clock = t
        if(self.latest_order >= self.order_num): return []
        new_orders = []
        while self.latest_order < self.order_num and self.orders[self.latest_order].t_init < self.clock:
            new_orders.append(self.orders[self.latest_order])
            self.latest_order += 1
        return new_orders
        
