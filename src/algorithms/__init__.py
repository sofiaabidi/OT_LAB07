"""Separate modules implement the 37 catalogue mechanisms."""
import importlib
NAMES = ['weighted_sum', 'epsilon_constraint', 'benson', 'weight_metric', 'value_function', 'goal_programming', 'lexicographic', 'topsis', 'vikor', 'vega', 'moga', 'nsga', 'npga', 'nsga2', 'nsga3', 'spea2', 'pesa2', 'moead', 'moead_de', 'moead_aco', 'constrained_nsga2', 'mopso', 'mogwo', 'moabc', 'moaco', 'mosa', 'mode', 'motlbo', 'moba', 'moma', 'rvea', 'ibea', 'sms_emoa', 'hype', 'r_nsga2', 'mgda', 'gradnorm']
def load(number):
    return importlib.import_module('src.algorithms.'+NAMES[number-1])
