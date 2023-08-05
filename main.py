import argparse
import json
import numpy as np
import os
from copy import deepcopy
from tqdm import tqdm
import time
from Dispatcher import *
from Optimizer import *
from Vehicle import *

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('config', type=str, help='Path to experiment configuration file')
    parser.add_argument('--cuda', type=str, default='0')
    args = parser.parse_args()
    with open('config/training_config.json') as f:
        training_config = json.load(f)
    with open(args.config) as f:
        agent_config = json.load(f)
    step_interval = training_config['step_interval']
    episode_length = training_config['episode_length']
    rng = np.random.default_rng(training_config['random_seed'])
    map_size = training_config['map_size']
    order_num = training_config['order_num']
    vehicle_num = training_config['vehicle_num']
    product_size = np.array([1, 2, 6, 18])
    product_probability = np.array(training_config['product_probability'])
    vehicle_capacity = np.array([3, 6, 12, 18, 24, 30])
    vehicle_probability = np.array(training_config['vehicle_capacity_probability'])
    vehicle_capacity_sample = rng.choice(vehicle_capacity, vehicle_num, p=vehicle_probability)
    max_time = step_interval * episode_length
    problem = Problem(rng, order_num, vehicle_num, max_time, product_size, product_probability)
    vehicles = {}
    for i in range(vehicle_num):
        position = Node(-1, rng.random() * map_size, rng.random() * map_size, 0, 'none')
        vehicles[i] = Vehicle(i, position, vehicle_capacity_sample[i], step_interval, problem.index_to_order)
    # Optimizer can be suboptimal, full-sweep, heuristic(four-action), etc.
    if(training_config['optimizer type'] == 'Suboptimal'): optimizer = Suboptimal_Optimizer()
    
    if(training_config['agent type'] == 'Myopic_Greedy'): dispatcher = Myopic_Greedy(rng, problem, vehicles, optimizer)
    else: dispatcher = Myopic_Bandit(rng, problem, vehicles, optimizer)
    t = 0
    for l in range(episode_length):
        dispatcher.update(t)
        dispatcher.dispatch()
        t += step_interval

