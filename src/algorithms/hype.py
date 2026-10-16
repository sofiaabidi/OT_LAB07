"""HypE: Monte Carlo hypervolume fitness with equal shared credits,
iterative contribution deletion. Samples=256 selection, final HV uses 8192.
Credits account for shared dominated samples; noisy selection is a limitation.
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

def contributions(f,reference,rng,samples=256,k=1):
    low=np.minimum(f.min(0),0); pts=rng.uniform(low,reference,(samples,f.shape[1]))
    hit=np.all(pts[None]>=f[:,None],axis=2); count=hit.sum(0); weight=np.zeros(samples)
    # Bonus 5E slide 17 teaching rule: equal credit to every dominator.
    positive=count>0
    weight[positive]=1/count[positive]
    return hit@weight/samples*np.prod(reference-low)
def select(f,cv,n,rng,samples):
    ids=list(range(len(f))); z=normalize(f,f.min(0),f.max(0)); ref=np.full(f.shape[1],1.1)
    while len(ids)>n:
        if np.any(cv[ids]>1e-10): victim=int(np.argmax(cv[ids]))
        else: victim=int(np.argmin(contributions(z[ids],ref,rng,samples,len(ids)-n)))
        ids.pop(victim)
    return np.array(ids)
def iterate(s):
    y=offspring(s,tournament(s)); f,c=evaluate(s,y); s.record(y,f,c)
    merge(s,y,f,c,lambda f,c,n:select(f,c,n,s.rng,s.params.get('samples',256)))

def run(problem,budget=10000,seed=DEFAULT_OPTIMIZER_SEED,**params):
    return execute(initialize,iterate,problem,budget,seed,**params)
