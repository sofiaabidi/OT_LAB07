"""IBEA: additive epsilon indicator I(a,b)=max_j(a_j-b_j);
outgoing fitness -sum_j exp(-I(i,j)/kappa), largest removed, iterative worst removal with recalculation.
kappa=.05; normalized objective ranges; feasibility penalty before indicator.
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

def indicator(f):
    z=normalize(f,f.min(0),f.max(0)); return np.max(z[:,None]-z[None,:],axis=2)
def fitness(f,kappa=.05):
    I=indicator(f); mat=np.exp(np.clip(-I/kappa,-100,100)); np.fill_diagonal(mat,0)
    return -mat.sum(1)
def select(f,cv,n,kappa=.05):
    ids=list(range(len(f)))
    while len(ids)>n:
        fit=fitness(f[ids],kappa); violation=cv[ids]
        victim=int(np.argmax(violation)) if np.any(violation>1e-10) else int(np.argmax(fit))
        ids.pop(victim)
    return np.array(ids)
def iterate(s):
    fit=fitness(s.f,s.params.get('kappa',.05)); pairs=s.rng.integers(s.n,size=(s.n,2)); ids=[a if fit[a]<fit[b] else b for a,b in pairs]
    y=offspring(s,ids); f,c=evaluate(s,y); s.record(y,f,c)
    merge(s,y,f,c,lambda f,c,n:select(f,c,n,s.params.get('kappa',.05)))

def run(problem,budget=10000,seed=DEFAULT_OPTIMIZER_SEED,**params):
    return execute(initialize,iterate,problem,budget,seed,**params)
