"""MO-TLBO: teacher phase x+r*(teacher-TF*mean); learner phase
towards better peer or away from worse peer. TF shrinks from 2 to 1.
Nondominated replacement, archive tracks nondominated proposals.
Shared defaults: population=40, budget=10000, seed=63.
Constraints: Deb feasibility comparison unless the stated method uses scalar penalty.
Lecture decks supplied on 12 October 2026; teaching variants documented in docs/lecture_alignment.md.
"""
import numpy as np
from src.algorithms.common import archive_leader, State, evaluate, execute, offspring, merge, tournament, environmental, mutate, crossover
from src.moo_utils import dominates, dominance_matrix, non_dominated_sort, crowding_distance, normalize, reference_vectors, archive, nondominated, hypervolume

def initialize(problem,budget=10000,seed=63,**params):
    return State(problem,budget,seed,**params)

def teacher_move(x,teacher,mean,r,tf): return x+r*(teacher-tf*mean)
def iterate(s):
    for phase in range(2):
        teacher=archive_leader(s)[0]; mean=s.x.mean(0); tf=2-s.used/s.budget
        for i in range(s.n):
            if s.used>=s.budget: return
            r=s.rng.random(len(mean))
            if phase==0: z=teacher_move(s.x[i],teacher,mean,r,tf)
            else:
                j=int(s.rng.choice(np.delete(np.arange(s.n),i)))
                direction=s.x[j]-s.x[i] if dominates(s.f[j],s.f[i],s.cv[j],s.cv[i]) else s.x[i]-s.x[j]
                z=s.x[i]+r*direction
            y=s.p.repair(z); f,c=evaluate(s,y[None]); s.record(y[None],f,c)
            if not dominates(s.f[i],f[0],s.cv[i],c[0]): s.x[i],s.f[i],s.cv[i]=y,f[0],c[0]

def run(problem,budget=10000,seed=63,**params):
    return execute(initialize,iterate,problem,budget,seed,**params)
