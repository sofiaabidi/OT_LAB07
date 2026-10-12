"""MOACO: two pheromone matrices, randomized tradeoff exponent,
probabilistic valid tour construction, evaporation and archive deposits.
Defaults alpha=1 beta=2 evaporation=.1. P8 only.
Shared defaults: population=40, budget=10000, seed=63.
Constraints: Deb feasibility comparison unless the stated method uses scalar penalty.
Lecture decks supplied on 12 October 2026; teaching variants documented in docs/lecture_alignment.md.
"""
import numpy as np
from src.algorithms.common import State, evaluate, execute, offspring, merge, tournament, environmental, mutate, crossover
from src.moo_utils import dominates, dominance_matrix, non_dominated_sort, crowding_distance, normalize, reference_vectors, archive, nondominated, hypervolume

def initialize(problem,budget=10000,seed=63,**params):
    s=State(problem,budget,seed,**params)
    s.extra['tau']=np.ones((2,15,15))
    return s

def construct(rng,tau,heuristic,alpha=1.,beta=2.):
    tour=[int(rng.integers(len(tau)))]; remaining=list(set(range(len(tau)))-set(tour))
    while remaining:
        scores=tau[tour[-1],remaining]**alpha*heuristic[tour[-1],remaining]**beta
        scores=scores/scores.sum(); city=int(rng.choice(remaining,p=scores)); tour.append(city); remaining.remove(city)
    return np.array(tour)
def deposit(tau,tour,amount):
    for a,b in zip(tour,np.roll(tour,-1)): tau[a,b]+=amount; tau[b,a]+=amount
def iterate(s):
    from src.problems import DIST,TIME
    y=[]
    for _ in range(min(s.n,s.budget-s.used)):
        w=s.rng.random(); tau=s.extra['tau'][0]**w*s.extra['tau'][1]**(1-w)
        eta=1/np.maximum(w*DIST/2200+(1-w)*TIME/3300,1e-9)
        y.append(construct(s.rng,tau,eta))
    y=np.array(y); f,c=evaluate(s,y); s.record(y,f,c); merge(s,y,f,c)
    s.extra['tau']*=.9
    for tour,ff in zip(s.ax,s.af):
        for j in range(2): deposit(s.extra['tau'][j],tour,1/max(ff[j],1e-9))

def run(problem,budget=10000,seed=63,**params):
    return execute(initialize,iterate,problem,budget,seed,**params)
