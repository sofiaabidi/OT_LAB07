"""RVEA: reference-vector association and angle-penalized distance (APD),
penalty strength alpha=2. Range-adapt vectors every 10 generations.
One best member per vector, fill unoccupied slots by APD.
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
    s.extra['v']=reference_vectors(s.n,problem.m)
    return s

def apd(f,vectors,progress,alpha=2.):
    z=normalize(f,f.min(0),f.max(0)); length=np.maximum(np.linalg.norm(z,axis=1),1e-12)
    v=vectors/np.maximum(np.linalg.norm(vectors,axis=1,keepdims=True),1e-12)
    angles=np.arccos(np.clip(z@v.T/length[:,None],-1,1)); group=angles.argmin(1)
    pair=np.arccos(np.clip(v@v.T,-1,1)); np.fill_diagonal(pair,np.inf); gamma=np.maximum(pair.min(1),1e-12)
    value=length*(1+alpha*progress*angles[np.arange(len(f)),group]/gamma[group])
    return group,value
def select(f,cv,n,vectors,progress):
    group,value=apd(f,vectors,progress); ids=[]
    for g in np.unique(group):
        candidates=np.flatnonzero(group==g); ids.append(min(candidates,key=lambda i:(cv[i],value[i])))
    rest=np.setdiff1d(np.arange(len(f)),ids)
    ids.extend(sorted(rest,key=lambda i:(cv[i],value[i]))[:n-len(ids)])
    return np.array(ids[:n])
def iterate(s):
    y=offspring(s); f,c=evaluate(s,y); s.record(y,f,c)
    if s.generation%10==0: s.extra['v']=reference_vectors(s.n,s.p.m)*np.maximum(np.ptp(np.r_[s.f,f],axis=0),1e-9)
    merge(s,y,f,c,lambda f,c,n:select(f,c,n,s.extra['v'],s.used/s.budget))

def run(problem,budget=10000,seed=DEFAULT_OPTIMIZER_SEED,**params):
    return execute(initialize,iterate,problem,budget,seed,**params)
