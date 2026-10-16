"""MOEA/D-DE: neighbourhood donor x_a+F*(x_b-x_c), binomial
crossover CR=.9 with forced coordinate, F=.5; cooperative scalar replacement.
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
    return s

def tchebycheff(f,w,ideal): return np.max(np.maximum(w,1e-6)*np.abs(f-ideal),axis=-1)
def update(s,i,y,f,cv):
    z=s.p.normalized(f); s.extra['ideal']=np.minimum(s.extra['ideal'],z)
    for j in s.extra['neighbours'][i]:
        old=s.p.normalized(s.f[j]); w=s.extra['w'][j]
        if (cv<=1e-10<s.cv[j]) or (cv>1e-10 and s.cv[j]>cv) or (cv<=1e-10 and s.cv[j]<=1e-10 and tchebycheff(z,w,s.extra['ideal'])<=tchebycheff(old,w,s.extra['ideal'])):
            s.x[j],s.f[j],s.cv[j]=y,f,cv
def de_trial(s,i,pool):
    a,b,c=s.rng.choice(pool,3,replace=False); donor=s.x[a]+s.params.get('F',.5)*(s.x[b]-s.x[c])
    mask=s.rng.random(len(donor))<s.params.get('CR',.9); mask[s.rng.integers(len(mask))]=True
    return s.p.repair(np.where(mask,donor,s.x[i]))
def iterate(s):
    for i in range(min(s.n,s.budget-s.used)):
        y=de_trial(s,i,s.extra['neighbours'][i]); f,c=evaluate(s,y[None]); s.record(y[None],f,c); update(s,i,y,f[0],c[0])

def run(problem,budget=10000,seed=DEFAULT_OPTIMIZER_SEED,**params):
    return execute(initialize,iterate,problem,budget,seed,**params)
