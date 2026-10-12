"""VEGA: partition selection by objective, pool subpopulations, crossover and mutation.
Tournament by one objective; no parent+child elitism.
Shared defaults: population=40, budget=10000, seed=63.
Constraints: Deb feasibility comparison unless the stated method uses scalar penalty.
Lecture decks supplied on 12 October 2026; teaching variants documented in docs/lecture_alignment.md.
"""
import numpy as np
from src.algorithms.common import State, evaluate, execute, offspring, merge, tournament, environmental, mutate, crossover
from src.moo_utils import dominates, dominance_matrix, non_dominated_sort, crowding_distance, normalize, reference_vectors, archive, nondominated, hypervolume

def initialize(problem,budget=10000,seed=63,**params):
    return State(problem,budget,seed,**params)

def select(s):
    winners=[]
    for i in range(s.n):
        j=i%s.p.m; a,b=s.rng.integers(s.n,size=2)
        winners.append(a if (s.cv[a],s.f[a,j])<(s.cv[b],s.f[b,j]) else b)
    return np.array(winners)
def iterate(s):
    y=offspring(s,select(s)); f,cv=evaluate(s,y); s.record(y,f,cv)
    if len(y)==s.n: s.x,s.f,s.cv=y,f,cv
    else: s.x[:len(y)],s.f[:len(y)],s.cv[:len(y)]=y,f,cv

def run(problem,budget=10000,seed=63,**params):
    return execute(initialize,iterate,problem,budget,seed,**params)
