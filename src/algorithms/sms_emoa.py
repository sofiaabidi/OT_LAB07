"""SMS-EMOA: one offspring, nondominated sorting, delete least HV
contribution in worst front. Exact 2-D exclusive contributions.
Reference is component maximum + .1 in normalized coordinates.
Shared defaults: population=40, budget=10000, seed=63.
Constraints: Deb feasibility comparison unless the stated method uses scalar penalty.
Lecture decks supplied on 12 October 2026; teaching variants documented in docs/lecture_alignment.md.
"""
import numpy as np
from src.algorithms.common import State, evaluate, execute, offspring, merge, tournament, environmental, mutate, crossover
from src.moo_utils import dominates, dominance_matrix, non_dominated_sort, crowding_distance, normalize, reference_vectors, archive, nondominated, hypervolume

def initialize(problem,budget=10000,seed=63,**params):
    return State(problem,budget,seed,**params)

def contributions(f,reference):
    if f.shape[1]!=2: raise ValueError('SMS-EMOA implementation supports two objectives')
    if len(f)==1: return np.array([hypervolume(f,reference)])
    # Worst nondominated layer: sorted staircase exclusive rectangles.
    order=np.argsort(f[:,0]); z=f[order]; left=np.r_[reference[1],z[:-1,1]]; right=np.r_[z[1:,0],reference[0]]
    out=np.zeros(len(f)); out[order]=np.maximum(right-z[:,0],0)*np.maximum(left-z[:,1],0); return out

def select(f,cv,n):
    worst=non_dominated_sort(f,cv)[-1]
    if np.any(cv[worst]>1e-10): victim=worst[np.argmax(cv[worst])]
    else:
        z=normalize(f,f.min(0),f.max(0)); victim=worst[np.argmin(contributions(z[worst],np.full(f.shape[1],1.1)))]
    return np.delete(np.arange(len(f)),victim)
def iterate(s):
    y=offspring(s,tournament(s),1); f,c=evaluate(s,y); s.record(y,f,c); merge(s,y,f,c,select)

def run(problem,budget=10000,seed=63,**params):
    return execute(initialize,iterate,problem,budget,seed,**params)
