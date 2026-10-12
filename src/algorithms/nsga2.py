"""NSGA-II: fast front sorting, crowded binary tournament, SBX and mutation,
parent+offspring elitist survival. Permutations use OX and swap/inversion.
Shared defaults: population=40, budget=10000, seed=63.
Constraints: Deb feasibility comparison unless the stated method uses scalar penalty.
Lecture decks supplied on 12 October 2026; teaching variants documented in docs/lecture_alignment.md.
"""
import numpy as np
from src.algorithms.common import State, evaluate, execute, offspring, merge, tournament, environmental, mutate, crossover
from src.moo_utils import dominates, dominance_matrix, non_dominated_sort, crowding_distance, normalize, reference_vectors, archive, nondominated, hypervolume

def initialize(problem,budget=10000,seed=63,**params):
    return State(problem,budget,seed,**params)

def iterate(s):
    y=offspring(s,tournament(s)); f,cv=evaluate(s,y); s.record(y,f,cv); merge(s,y,f,cv)

def run(problem,budget=10000,seed=63,**params):
    return execute(initialize,iterate,problem,budget,seed,**params)
