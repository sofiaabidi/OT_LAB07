"""MOEA/D-ACO for tours: each weight has edge pheromone, weighted
distance/time heuristic, neighbour Tchebycheff replacement and deposits.
Defaults alpha=1 beta=2 evaporation=.1. Requires P8.
Shared defaults: population=40, budget=10000, optimizer seed=720.
Constraints: Deb feasibility comparison unless the stated method uses scalar penalty.
Lecture decks supplied on 12 October 2026; teaching variants documented in docs/lecture_alignment.md.
"""
import numpy as np
from src.project_config import DEFAULT_OPTIMIZER_SEED
from src.algorithms.common import State, evaluate, execute, offspring, merge, tournament, environmental, mutate, crossover
from src.moo_utils import dominates, dominance_matrix, non_dominated_sort, crowding_distance, normalize, reference_vectors, archive, nondominated, hypervolume

def initialize(problem,budget=10000,seed=DEFAULT_OPTIMIZER_SEED,**params):
    s=State(problem,budget,seed,**params)
    s.extra['w']=reference_vectors(s.n,problem.m)
    d=np.linalg.norm(s.extra['w'][:,None]-s.extra['w'][None,:],axis=2)
    s.extra['neighbours']=np.argsort(d,axis=1)[:,:min(10,s.n)]
    s.extra['ideal']=s.p.normalized(s.f).min(0)
    s.extra['tau']=np.ones((s.n,15,15))
    return s

def tchebycheff(f,w,ideal): return np.max(np.maximum(w,1e-6)*np.abs(f-ideal),axis=-1)
def update(s,i,y,f,cv):
    z=s.p.normalized(f); s.extra['ideal']=np.minimum(s.extra['ideal'],z)
    for j in s.extra['neighbours'][i]:
        old=s.p.normalized(s.f[j]); w=s.extra['w'][j]
        if (cv<=1e-10<s.cv[j]) or (cv>1e-10 and s.cv[j]>cv) or (cv<=1e-10 and s.cv[j]<=1e-10 and tchebycheff(z,w,s.extra['ideal'])<=tchebycheff(old,w,s.extra['ideal'])):
            s.x[j],s.f[j],s.cv[j]=y,f,cv
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
    for i in range(min(s.n,s.budget-s.used)):
        w=s.extra['w'][i]; eta=1/np.maximum(w[0]*DIST/2200+w[1]*TIME/3300,1e-9)
        tau=s.extra['tau'][i]; y=construct(s.rng,tau,eta)
        f,c=evaluate(s,y[None]); s.record(y[None],f,c); update(s,i,y,f[0],c[0])
        tau*=.9; deposit(tau,s.x[i],1/(1+tchebycheff(s.p.normalized(s.f[i]),w,s.extra['ideal'])))

def run(problem,budget=10000,seed=DEFAULT_OPTIMIZER_SEED,**params):
    return execute(initialize,iterate,problem,budget,seed,**params)
