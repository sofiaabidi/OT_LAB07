"""MOGWO: alpha, beta, delta archive leaders; decreasing encircling
coefficient a=2*(1-used/budget), average three proposed positions.
Binary masks use a sigmoid transfer, then at-least-one repair.
Shared defaults: population=40, budget=10000, seed=63.
Constraints: Deb feasibility comparison unless the stated method uses scalar penalty.
Lecture decks supplied on 12 October 2026; teaching variants documented in docs/lecture_alignment.md.
"""
import numpy as np
from src.algorithms.common import archive_leader, State, evaluate, execute, offspring, merge, tournament, environmental, mutate, crossover
from src.moo_utils import dominates, dominance_matrix, non_dominated_sort, crowding_distance, normalize, reference_vectors, archive, nondominated, hypervolume

def initialize(problem,budget=10000,seed=63,**params):
    return State(problem,budget,seed,**params)

def encircle(x,leaders,A,C): return np.mean(leaders-A*np.abs(C*leaders-x),axis=0)
def iterate(s):
    n=min(s.n,s.budget-s.used); a=2*(1-s.used/s.budget); y=[]
    for i in range(n):
        leaders=archive_leader(s,3)
        A=2*a*s.rng.random(leaders.shape)-a; C=2*s.rng.random(leaders.shape)
        z=encircle(s.x[i],leaders,A,C)
        if s.p.kind=='binary': z=(s.rng.random(len(z))<1/(1+np.exp(-z))).astype(float)
        y.append(s.p.repair(z))
    y=np.array(y); f,c=evaluate(s,y); s.record(y,f,c); s.x[:n],s.f[:n],s.cv[:n]=y,f,c

def run(problem,budget=10000,seed=63,**params):
    return execute(initialize,iterate,problem,budget,seed,**params)
