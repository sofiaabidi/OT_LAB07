"""MODE: DE/rand/1 and forced binomial crossover; trial replaces target
only if it dominates under Deb rules. F=.5, CR=.9. Output archive retains tradeoffs.
Shared defaults: population=40, budget=10000, seed=63.
Constraints: Deb feasibility comparison unless the stated method uses scalar penalty.
Lecture decks supplied on 12 October 2026; teaching variants documented in docs/lecture_alignment.md.
"""
import numpy as np
from src.algorithms.common import State, evaluate, execute, offspring, merge, tournament, environmental, mutate, crossover
from src.moo_utils import dominates, dominance_matrix, non_dominated_sort, crowding_distance, normalize, reference_vectors, archive, nondominated, hypervolume

def initialize(problem,budget=10000,seed=63,**params):
    return State(problem,budget,seed,**params)

def donor(a,b,c,F=.5): return a+F*(b-c)
def iterate(s):
    n=min(s.n,s.budget-s.used); y=[]
    for i in range(n):
        pool=np.delete(np.arange(s.n),i); a,b,c=s.rng.choice(pool,3,replace=False)
        d=donor(s.x[a],s.x[b],s.x[c],s.params.get('F',.5)); mask=s.rng.random(len(d))<s.params.get('CR',.9); mask[s.rng.integers(len(d))]=True
        y.append(s.p.repair(np.where(mask,d,s.x[i])))
    y=np.array(y); f,c=evaluate(s,y); s.record(y,f,c)
    for i in range(n):
        if dominates(f[i],s.f[i],c[i],s.cv[i]): s.x[i],s.f[i],s.cv[i]=y[i],f[i],c[i]

def run(problem,budget=10000,seed=63,**params):
    return execute(initialize,iterate,problem,budget,seed,**params)
