"""Constrained NSGA-II: feasible beats infeasible, lower violation wins
among infeasible, Pareto rank then crowding among feasible.
NSGA-II in this project also supports Deb rules; this module exposes the rule.
Shared defaults: population=40, budget=10000, optimizer seed=720.
Constraints: Deb feasibility comparison unless the stated method uses scalar penalty.
Lecture decks supplied on 12 October 2026; teaching variants documented in docs/lecture_alignment.md.
"""
import numpy as np
from src.project_config import DEFAULT_OPTIMIZER_SEED
from src.algorithms.common import State, evaluate, execute, offspring, merge, tournament, environmental, mutate, crossover
from src.moo_utils import dominates, dominance_matrix, non_dominated_sort, crowding_distance, normalize, reference_vectors, archive, nondominated, hypervolume

def initialize(problem,budget=10000,seed=DEFAULT_OPTIMIZER_SEED,**params):
    return State(problem,budget,seed,**params)

def deb_compare(a,b,ca,cb): return dominates(a,b,ca,cb)
def iterate(s):
    y=offspring(s,tournament(s)); f,cv=evaluate(s,y); s.record(y,f,cv); merge(s,y,f,cv)

def run(problem,budget=10000,seed=DEFAULT_OPTIMIZER_SEED,**params):
    return execute(initialize,iterate,problem,budget,seed,**params)
