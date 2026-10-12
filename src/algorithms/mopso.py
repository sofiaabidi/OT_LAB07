"""MOPSO: inertia velocity, personal best, crowding-selected archive
leader, occasional mutation. Defaults inertia=.4, c1=c2=1.5.
Shared defaults: population=40, budget=10000, seed=63.
Constraints: Deb feasibility comparison unless the stated method uses scalar penalty.
Lecture decks supplied on 12 October 2026; teaching variants documented in docs/lecture_alignment.md.
"""
import numpy as np
from src.algorithms.common import State, evaluate, execute, offspring, merge, tournament, environmental, mutate, crossover
from src.moo_utils import dominates, dominance_matrix, non_dominated_sort, crowding_distance, normalize, reference_vectors, archive, nondominated, hypervolume

def initialize(problem,budget=10000,seed=63,**params):
    s=State(problem,budget,seed,**params)
    s.extra.update(v=np.zeros_like(s.x),pb=s.x.copy(),pf=s.f.copy(),pc=s.cv.copy())
    return s

def velocity(v,x,pbest,leader,r1,r2,inertia=.4):
    return inertia*v+1.5*r1*(pbest-x)+1.5*r2*(leader-x)
def iterate(s):
    n=min(s.n,s.budget-s.used); y=[]
    crowd=crowding_distance(s.af); weights=np.where(np.isinf(crowd),2.,crowd+1e-6); weights/=weights.sum()
    for i in range(n):
        leader=s.ax[s.rng.choice(len(s.ax),p=weights)]
        s.extra['v'][i]=velocity(s.extra['v'][i],s.x[i],s.extra['pb'][i],leader,s.rng.random(len(leader)),s.rng.random(len(leader)),s.params.get('inertia',.4))
        limit=.2*(s.p.upper-s.p.lower); s.extra['v'][i]=np.clip(s.extra['v'][i],-limit,limit)
        z=s.p.repair(s.x[i]+s.extra['v'][i]); y.append(mutate(s.p,z,s.rng) if s.rng.random()<.1 else z)
    y=np.array(y); f,c=evaluate(s,y); s.record(y,f,c)
    for i in range(n):
        if dominates(f[i],s.extra['pf'][i],c[i],s.extra['pc'][i]) or (not dominates(s.extra['pf'][i],f[i],s.extra['pc'][i],c[i]) and s.rng.random()<.5):
            s.extra['pb'][i],s.extra['pf'][i],s.extra['pc'][i]=y[i],f[i],c[i]
    s.x[:n],s.f[:n],s.cv[:n]=y,f,c

def run(problem,budget=10000,seed=63,**params):
    return execute(initialize,iterate,problem,budget,seed,**params)
