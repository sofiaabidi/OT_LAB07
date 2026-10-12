"""MOABC: employed and onlooker differential-coordinate proposals,
Deb dominance greedy replacement, abandoned-source scouts. Limit=20.
Shared defaults: population=40, budget=10000, seed=63.
Constraints: Deb feasibility comparison unless the stated method uses scalar penalty.
Lecture decks supplied on 12 October 2026; teaching variants documented in docs/lecture_alignment.md.
"""
import numpy as np
from src.algorithms.common import State, evaluate, execute, offspring, merge, tournament, environmental, mutate, crossover
from src.moo_utils import dominates, dominance_matrix, non_dominated_sort, crowding_distance, normalize, reference_vectors, archive, nondominated, hypervolume

def initialize(problem,budget=10000,seed=63,**params):
    s=State(problem,budget,seed,**params)
    s.extra['fail']=np.zeros(s.n,int)
    return s

def neighbour(s,i):
    j=int(s.rng.choice(np.delete(np.arange(s.n),i))); k=s.rng.integers(len(s.x[i])); y=s.x[i].copy()
    y[k]+=s.rng.uniform(-1,1)*(s.x[i,k]-s.x[j,k]); return s.p.repair(y)
def iterate(s):
    rank=np.zeros(s.n)
    for j,front in enumerate(non_dominated_sort(s.f,s.cv)): rank[front]=j
    crowd=crowding_distance(s.f)
    prob=np.where(np.isinf(crowd),2.,crowd+1e-6); prob/=prob.sum()
    for phase in range(2):
        for q in range(s.n):
            if s.used>=s.budget: return
            i=q if phase==0 else int(s.rng.choice(s.n,p=prob))
            scout=s.extra['fail'][i]>=s.params.get('limit',20)
            y=s.p.sample(s.rng,1)[0] if scout else neighbour(s,i)
            f,c=evaluate(s,y[None]); s.record(y[None],f,c)
            if scout or dominates(f[0],s.f[i],c[0],s.cv[i]):
                s.x[i],s.f[i],s.cv[i]=y,f[0],c[0]; s.extra['fail'][i]=0
            else: s.extra['fail'][i]+=1

def run(problem,budget=10000,seed=63,**params):
    return execute(initialize,iterate,problem,budget,seed,**params)
