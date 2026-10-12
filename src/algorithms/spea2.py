"""SPEA2: strength S, raw fitness R=sum strengths of dominators;
density 1/(sigma_k+2), fixed archive, lexicographic nearest-distance truncation.
Shared defaults: population=40, budget=10000, seed=63.
Constraints: Deb feasibility comparison unless the stated method uses scalar penalty.
Lecture decks supplied on 12 October 2026; teaching variants documented in docs/lecture_alignment.md.
"""
import numpy as np
from src.algorithms.common import State, evaluate, execute, offspring, merge, tournament, environmental, mutate, crossover
from src.moo_utils import dominates, dominance_matrix, non_dominated_sort, crowding_distance, normalize, reference_vectors, archive, nondominated, hypervolume

def initialize(problem,budget=10000,seed=63,**params):
    return State(problem,budget,seed,**params)

def fitness(f,cv):
    d=dominance_matrix(f,cv); strength=d.sum(1); raw=d.T@strength
    z=normalize(f,f.min(0),f.max(0)); dist=np.linalg.norm(z[:,None]-z[None,:],axis=2)
    np.fill_diagonal(dist,np.inf); k=max(1,int(np.sqrt(len(f))))
    density=1/(np.sort(dist,axis=1)[:,k-1]+2)
    return raw+density

def select(f,cv,n):
    fit=fitness(f,cv); ids=list(np.flatnonzero(fit<1))
    if len(ids)<n: return np.argsort(fit,kind='stable')[:n]
    z=normalize(f,f.min(0),f.max(0))
    while len(ids)>n:
        d=np.linalg.norm(z[ids,None]-z[None,ids],axis=2); np.fill_diagonal(d,np.inf)
        rows=np.sort(d,axis=1); victim=min(range(len(ids)),key=lambda i:tuple(rows[i]))
        ids.pop(victim)
    return np.array(ids)

def iterate(s):
    fit=fitness(s.f,s.cv); pairs=s.rng.integers(s.n,size=(s.n,2)); ids=[a if fit[a]<fit[b] else b for a,b in pairs]
    y=offspring(s,ids); f,cv=evaluate(s,y); s.record(y,f,cv); merge(s,y,f,cv,select)

def run(problem,budget=10000,seed=63,**params):
    return execute(initialize,iterate,problem,budget,seed,**params)
