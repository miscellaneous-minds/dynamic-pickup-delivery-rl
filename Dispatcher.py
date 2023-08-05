from Problem import *
from Vehicle import *
from Optimizer import *

class Dispatcher:
    def __init__(self, rng, problem: Problem, vehicles: dict, optimizer: Optimizer):
        self.rng = rng
        self.problem = problem
        self.cumulative_reward = 0
        self.vehicles = vehicles
        self.optimizer = optimizer
        self.buffer = []
    
    def update(self, t):
        new_orders = self.problem.update(t)
        self.buffer.append(new_orders)
        step_reward = 0
        for i in len(self.vehicles):
            vehicle_step_reward, vehicle_step_log = self.vehicles[i].update(self.problem.clock)
            step_reward += vehicle_step_reward
            for log in vehicle_step_log:
                self.problem.index_to_order[log[0]].state = log[1]
        self.cumulative_reward += step_reward

    def dispatch(self):
        pass
    
    def release(self, order: Order, states):
        pass

# Name of dispatcher is 'Release type'_'Dispatcher type'
# e.g. Myopic/DQN, Greedy/Bandit/RL

class Myopic_Greedy(Dispatcher):
    def __init__(self, rng, problem: Problem, vehicles: dict, optimizer: Optimizer):
        super.__init__(self, rng, problem, vehicles, optimizer)

    def update(self, t):
        super.update(self, t)

    def dispatch(self):
        # Decide whether each order in buffer should be dispatched
        waiting_orders = []
        release_orders = []
        states = 0
        for order in self.buffer:
            if(self.release(order, states)): release_orders.append(order)
            else: waiting_orders.append(order)
        self.buffer = waiting_orders
        
        # For each order, decide which vehicle is responsible, then dispatch with acceptance probability, if rejected: return order to buffer
        for order in release_orders:
            min_vehicle = 0
            min_eta = int(self.problem.map_size * math.sqrt(2) * self.problem.order_num)
            min_route = []
            for i in len(self.vehicles):
                route, eta = self.optimizer(self.vehicles[i].route + [order.pickup_node, order.delivery_node])
                if(eta < min_eta):
                    min_vehicle = i
                    min_route = route
                    min_eta = eta
            accept = self.rng.choice([True, False], 1, p=self.vehicles[min_vehicle].accept_probability(states))
            if(accept): self.vehicles[min_vehicle].route = min_route
            else: self.buffer.append(order)
            # At next step after rejection, dispatcher can offer to the same vehicle again -> Is this ok?
        return
    
    def release(self, order: Order, states):
        return True

class Myopic_Bandit(Dispatcher):
    def __init__(self, problem: Problem, vehicles: dict, optimizer: Optimizer):
        super.__init__(self, problem, vehicles, optimizer)

    def update(self, t):
        super.update(self, t)

    def dispatch(self):
        release_orders = []
        states = 0
        for order in self.buffer:
            if(self.release(order, states)):
                self.buffer.remove(order)
                release_orders.append(order)
        return
    
    def release(self, order: Order, states):
        return True