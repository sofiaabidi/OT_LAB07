"""Niched Pareto Genetic Algorithm: direct binary tournament with comparison-set crowding.
Direct dominance decides; otherwise smaller comparison-set niche count wins.
Defaults: comparison_size=2, sigma=.3; objective distances normalized.
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

def niche_count(f,sigma=.3):
    z=normalize(f,f.min(0),f.max(0)); d=np.linalg.norm(z[:,None]-z[None,:],axis=2)
    return np.maximum(0,1-(d/sigma)**2).sum(1)

def comparison_niches(f,a,b,comparison,sigma=.3,ideal=None,nadir=None):
    ideal=f.min(0) if ideal is None else ideal
    nadir=f.max(0) if nadir is None else nadir
    z=normalize(f,ideal,nadir)
    d=np.linalg.norm(z[[a,b],None]-z[None,np.asarray(comparison)],axis=2)
    return np.maximum(0,1-(d/sigma)**2).sum(1)

def pareto_tournament(f,cv,a,b,comparison,sigma=.3,ideal=None,nadir=None):
    # Chapter 5 Non-Elitist MOEAs, slide 27: direct contestant dominance;
    # the separately drawn comparison set is used only for crowding.
    if dominates(f[a],f[b],cv[a],cv[b]): return a
    if dominates(f[b],f[a],cv[b],cv[a]): return b
    nc=comparison_niches(f,a,b,comparison,sigma,ideal,nadir)
    return a if nc[0]<=nc[1]+1e-12 else b

def select(s):
    chosen=[]
    for _ in range(s.n):
        a,b=s.rng.choice(s.n,2,replace=False)
        pool=np.setdiff1d(np.arange(s.n),[a,b])
        c=s.rng.choice(pool,min(len(pool),s.params.get('comparison_size',2)),replace=False)
        chosen.append(pareto_tournament(s.f,s.cv,a,b,c,s.params.get('sigma',.3)))
    return chosen

def iterate(s):
    y=offspring(s,select(s)); f,cv=evaluate(s,y); s.record(y,f,cv)
    s.x[:len(y)],s.f[:len(y)],s.cv[:len(y)]=y,f,cv

def run(problem,budget=10000,seed=DEFAULT_OPTIMIZER_SEED,**params):
    return execute(initialize,iterate,problem,budget,seed,**params)
