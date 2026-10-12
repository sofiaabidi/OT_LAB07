"""NSGA: nondominated layers, dummy fitness and within-front sharing.
Sharing radius sigma=.3; non-elitist generational replacement.
Shared defaults: population=40, budget=10000, seed=63.
Constraints: Deb feasibility comparison unless the stated method uses scalar penalty.
Lecture decks supplied on 12 October 2026; teaching variants documented in docs/lecture_alignment.md.
"""
import numpy as np
from src.algorithms.common import State, evaluate, execute, offspring, merge, tournament, environmental, mutate, crossover
from src.moo_utils import dominates, dominance_matrix, non_dominated_sort, crowding_distance, normalize, reference_vectors, archive, nondominated, hypervolume

def initialize(problem,budget=10000,seed=63,**params):
    return State(problem,budget,seed,**params)

def niche_count(f,sigma=.3):
    z=normalize(f,f.min(0),f.max(0)); d=np.linalg.norm(z[:,None]-z[None,:],axis=2)
    return np.maximum(0,1-(d/sigma)**2).sum(1)
def fitness(f,cv,sigma=.3):
    out=np.zeros(len(f)); dummy=float(len(f))
    for front in non_dominated_sort(f,cv):
        out[front]=dummy/niche_count(f[front],sigma)
        dummy=max(out[front].min()-.01,1e-8)
    return out
def iterate(s):
    fit=fitness(s.f,s.cv,s.params.get('sigma',.3)); ids=s.rng.choice(s.n,s.n,p=fit/fit.sum())
    y=offspring(s,ids); f,cv=evaluate(s,y); s.record(y,f,cv)
    s.x[:len(y)],s.f[:len(y)],s.cv[:len(y)]=y,f,cv

def run(problem,budget=10000,seed=63,**params):
    return execute(initialize,iterate,problem,budget,seed,**params)
