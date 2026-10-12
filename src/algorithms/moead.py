"""MOEA/D: reference weights, neighbourhood mating, running ideal,
cooperative Tchebycheff replacement. Neighbourhood size=10.
Shared defaults: population=40, budget=10000, seed=63.
Constraints: Deb feasibility comparison unless the stated method uses scalar penalty.
Lecture decks supplied on 12 October 2026; teaching variants documented in docs/lecture_alignment.md.
"""
import numpy as np
from src.algorithms.common import State, evaluate, execute, offspring, merge, tournament, environmental, mutate, crossover
from src.moo_utils import dominates, dominance_matrix, non_dominated_sort, crowding_distance, normalize, reference_vectors, archive, nondominated, hypervolume

def initialize(problem,budget=10000,seed=63,**params):
    s=State(problem,budget,seed,**params)
    s.extra['w']=reference_vectors(s.n,problem.m)
    d=np.linalg.norm(s.extra['w'][:,None]-s.extra['w'][None,:],axis=2)
    s.extra['neighbours']=np.argsort(d,axis=1)[:,:min(10,s.n)]
    s.extra['ideal']=s.p.normalized(s.f).min(0)
    return s

def tchebycheff(f,w,ideal): return np.max(np.maximum(w,1e-6)*np.abs(f-ideal),axis=-1)
def update(s,i,y,f,cv):
    z=s.p.normalized(f); s.extra['ideal']=np.minimum(s.extra['ideal'],z)
    for j in s.extra['neighbours'][i]:
        old=s.p.normalized(s.f[j]); w=s.extra['w'][j]
        if (cv<=1e-10<s.cv[j]) or (cv>1e-10 and s.cv[j]>cv) or (cv<=1e-10 and s.cv[j]<=1e-10 and tchebycheff(z,w,s.extra['ideal'])<=tchebycheff(old,w,s.extra['ideal'])):
            s.x[j],s.f[j],s.cv[j]=y,f,cv
def iterate(s):
    for i in range(min(s.n,s.budget-s.used)):
        a,b=s.rng.choice(s.extra['neighbours'][i],2,replace=False)
        y=mutate(s.p,crossover(s.p,s.x[a],s.x[b],s.rng),s.rng)
        f,c=evaluate(s,y[None]); s.record(y[None],f,c); update(s,i,y,f[0],c[0])

def run(problem,budget=10000,seed=63,**params):
    return execute(initialize,iterate,problem,budget,seed,**params)
