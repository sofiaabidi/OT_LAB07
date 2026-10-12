"""MOBA: frequency velocity toward archive leader, pulse-controlled local
random walk, loudness acceptance. fmin=0 fmax=2, loudness*=.95,
pulse=1*(1-exp(-.1*g)). Pareto archive stores all visited feasible points.
Shared defaults: population=40, budget=10000, seed=63.
Constraints: Deb feasibility comparison unless the stated method uses scalar penalty.
Lecture decks supplied on 12 October 2026; teaching variants documented in docs/lecture_alignment.md.
"""
import numpy as np
from src.algorithms.common import archive_leader, State, evaluate, execute, offspring, merge, tournament, environmental, mutate, crossover
from src.moo_utils import dominates, dominance_matrix, non_dominated_sort, crowding_distance, normalize, reference_vectors, archive, nondominated, hypervolume

def initialize(problem,budget=10000,seed=63,**params):
    s=State(problem,budget,seed,**params)
    s.extra['v']=np.zeros_like(s.x)
    return s

def schedules(g,A0=.9): return A0*.95**g,1-np.exp(-.1*g)
def iterate(s):
    n=min(s.n,s.budget-s.used); A,pulse=schedules(s.generation); y=[]
    for i in range(n):
        leader=archive_leader(s)[0]; freq=s.rng.uniform(0,2)
        s.extra['v'][i]+=(leader-s.x[i])*freq
        z=s.x[i]+s.extra['v'][i]
        if s.rng.random()>pulse: z=leader+.01*A*s.rng.normal(size=len(leader))*(s.p.upper-s.p.lower)
        y.append(s.p.repair(z))
    y=np.array(y); f,c=evaluate(s,y); s.record(y,f,c)
    for i in range(n):
        if dominates(f[i],s.f[i],c[i],s.cv[i]) and s.rng.random()<A: s.x[i],s.f[i],s.cv[i]=y[i],f[i],c[i]

def run(problem,budget=10000,seed=63,**params):
    return execute(initialize,iterate,problem,budget,seed,**params)
