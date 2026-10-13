"""R-NSGA-II: nondominated fronts, normalized distance to aspiration,
epsilon clearing to spread preferred survivors. epsilon=.05; default balanced
normalized aspiration [.5,.5], P14 uses natural [1.8,-12]; callers may override.
Shared defaults: population=40, budget=10000, optimizer seed from project config.
Constraints: Deb feasibility comparison unless the stated method uses scalar penalty.
Lecture decks supplied on 12 October 2026; teaching variants documented in docs/lecture_alignment.md.
"""
import numpy as np
from src.project_config import DEFAULT_OPTIMIZER_SEED
from src.algorithms.common import State, evaluate, execute, offspring, merge, tournament, environmental, mutate, crossover
from src.moo_utils import dominates, dominance_matrix, non_dominated_sort, crowding_distance, normalize, reference_vectors, archive, nondominated, hypervolume

def initialize(problem,budget=10000,seed=DEFAULT_OPTIMIZER_SEED,**params):
    return State(problem,budget,seed,**params)

def preference_select(f,cv,n,p,epsilon=.05,reference=None,
                      reference_is_normalized=False):
    z=p.normalized(f)
    if reference is None:
        ref=p.normalized(np.array([1.8,-12])) if p.key=='P14' else np.full(p.m,.5)
    else:
        reference=np.asarray(reference,float)
        if reference.shape!=(p.m,): raise ValueError('reference must have one value per objective')
        ref=reference if reference_is_normalized else p.normalized(reference)
    chosen=[]
    for front in non_dominated_sort(f,cv):
        if len(chosen)+len(front)<=n: chosen.extend(front); continue
        order=front[np.argsort(np.linalg.norm(z[front]-ref,axis=1))]; deferred=[]
        for i in order:
            if len(chosen)>=n: break
            if chosen and np.min(np.linalg.norm(z[chosen]-z[i],axis=1))<epsilon: deferred.append(i)
            else: chosen.append(i)
        for i in deferred:
            if len(chosen)<n: chosen.append(i)
        break
    return np.array(chosen)
def iterate(s):
    y=offspring(s,tournament(s)); f,c=evaluate(s,y); s.record(y,f,c)
    merge(s,y,f,c,lambda f,c,n:preference_select(
        f,c,n,s.p,s.params.get('epsilon',.05),s.params.get('reference'),
        s.params.get('reference_is_normalized',False)))

def run(problem,budget=10000,seed=DEFAULT_OPTIMIZER_SEED,**params):
    return execute(initialize,iterate,problem,budget,seed,**params)
