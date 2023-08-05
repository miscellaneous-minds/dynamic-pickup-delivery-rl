import math
from Problem import Node

class Vehicle:
    def __init__(self, index, position: Node, capacity, step_interval, index_to_order: dict):
        self.index = index
        self.position = position
        self.capacity = capacity
        self.step_interval = step_interval
        self.index_to_order = index_to_order
        self.duration_time = 0
        self.route = []
        self.log = []
        # Need to be added: own features which determine acceptance to offer given states
    
    def update(self, t):
        vehicle_step_reward = 0
        vehicle_step_log = []
        self.duration_time += self.step_interval
        while self.distance(self.position, self.route[0]) < self.duration_time:
            d = self.distance(self.position, self.route[0])
            self.position = self.route.pop(0)
            self.duration_time -= d
            vehicle_step_reward -= d
            if(self.index_to_order[self.position.index].t_arrival < t-self.duration_time):
                overtime = t - self.duration_time - self.index_to_order[self.position.index].t_arrival
                vehicle_step_reward -= 1000 * overtime
            self.capacity += self.position.size
            if(self.position.type == 'pickup'): vehicle_step_log.append((self.position.index, 'in process'))
            if(self.position.type == 'delivery'): vehicle_step_log.append((self.position.index, 'complete'))
            self.log.append((t - self.duration_time, self.index, self.position))
        return vehicle_step_reward, vehicle_step_log
    
    def distance(node1: Node, node2: Node):
        return int(math.sqrt((node1.x-node2.x)**2 + (node1.y-node2.y)**2))
    
    def accept_probability(self, states):
        return 1

