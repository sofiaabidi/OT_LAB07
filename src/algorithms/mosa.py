"""Multiobjective Simulated Annealing: population of chains, normalized
summed worsened-objective energy for dominated moves, Boltzmann acceptance and archive.
Temperature T0=.1, cooling=.97 per population sweep, move scale=.1.
Lecture Part 4 slide 41 acceptance; parallel chains are a declared extension.
Incomparable neighbours always accepted. Normalized T0=.1 is not raw-unit T0=100.
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

def acceptance(old,new,T,weight=None,ca=0.,cb=0.):
    # Lecture Part 4 slide 41: incomparable neighbours always accepted.
    if cb<=1e-10<ca: return 1.
    if ca<=1e-10<cb: return 0.
    if ca>1e-10 and cb>1e-10:
        delta=max(cb-ca,0)*10
        return 1. if delta==0 else float(np.exp(-delta/max(T,1e-12)))
    if not dominates(old,new): return 1.
    delta=float(np.maximum(np.asarray(new)-old,0).sum())
    return float(np.exp(-delta/max(T,1e-12)))

def iterate(s):
    n=min(s.n,s.budget-s.used); T=s.params.get('T0',.1)*s.params.get('cooling',.97)**s.generation
    y=np.array([mutate(s.p,s.x[i],s.rng,s.params.get('scale',.1)) for i in range(n)])
    f,c=evaluate(s,y); s.record(y,f,c)
    for i in range(n):
        old=s.p.normalized(s.f[i]); new=s.p.normalized(f[i])
        if s.rng.random()<acceptance(old,new,T,None,s.cv[i],c[i]): s.x[i],s.f[i],s.cv[i]=y[i],f[i],c[i]

def run(problem,budget=10000,seed=DEFAULT_OPTIMIZER_SEED,**params):
    return execute(initialize,iterate,problem,budget,seed,**params)
