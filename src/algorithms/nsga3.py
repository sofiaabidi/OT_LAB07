"""NSGA-III: front ranking, simplex-lattice reference association and niche
occupancy survival. Normalize by observed ranges (simplification of intercepts).
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

def associate(f,vectors):
    z=f-f.min(0); z=z/np.maximum(np.ptp(f,axis=0),1e-12)
    v=vectors/np.maximum(np.linalg.norm(vectors,axis=1,keepdims=True),1e-12)
    projection=z@v.T
    distance=np.sqrt(np.maximum((z*z).sum(1)[:,None]-projection*projection,0))
    return distance.argmin(1),distance
def select(f,cv,n,rng):
    chosen=[]
    for front in non_dominated_sort(f,cv):
        if len(chosen)+len(front)<=n: chosen.extend(front)
        else:
            vectors=reference_vectors(n,f.shape[1]); group,d=associate(f,vectors)
            counts=np.bincount(group[chosen],minlength=len(vectors)); remaining=list(front)
            while len(chosen)<n:
                available=np.unique(group[remaining]); low=counts[available].min()
                niche=rng.choice(available[counts[available]==low]); candidates=[i for i in remaining if group[i]==niche]
                pick=min(candidates,key=lambda i:d[i,niche]) if counts[niche]==0 else rng.choice(candidates)
                chosen.append(pick); remaining.remove(pick); counts[niche]+=1
            break
    return np.array(chosen)
def iterate(s):
    y=offspring(s,tournament(s)); f,cv=evaluate(s,y); s.record(y,f,cv)
    merge(s,y,f,cv,lambda f,c,n:select(f,c,n,s.rng))

def run(problem,budget=10000,seed=DEFAULT_OPTIMIZER_SEED,**params):
    return execute(initialize,iterate,problem,budget,seed,**params)
