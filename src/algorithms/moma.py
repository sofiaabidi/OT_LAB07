"""MOMA: NSGA-II global search and normalized combined-improvement hill-climb on a subset
of children. Local fraction=.25, mutation scale=.02. Local calls count in budget.
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

def iterate(s):
    y=offspring(s,tournament(s)); f,c=evaluate(s,y); s.record(y,f,c)
    count=min(int(len(y)*s.params.get('local_fraction',.25)),s.budget-s.used)
    local_order=np.argsort(-crowding_distance(f),kind='stable')[:count]
    for i in local_order:
        z=mutate(s.p,y[i],s.rng,.02); ff,cc=evaluate(s,z[None]); s.record(z[None],ff,cc)
        if (cc[0]<=1e-10<c[i]) or (cc[0]<=1e-10 and c[i]<=1e-10 and np.sum(s.p.normalized(f[i])-s.p.normalized(ff[0]))>0): y[i],f[i],c[i]=z,ff[0],cc[0]
    merge(s,y,f,c)

def run(problem,budget=10000,seed=DEFAULT_OPTIMIZER_SEED,**params):
    return execute(initialize,iterate,problem,budget,seed,**params)
