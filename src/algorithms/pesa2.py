"""PESA-II: archive adaptive grid regions; region tournament selects lower
occupancy region, then uniform individual. Default grid divisions=8.
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

def regions(f,divisions=8):
    z=normalize(f,f.min(0),f.max(0)); cells=np.minimum((z*divisions).astype(int),divisions-1)
    _,group,counts=np.unique(cells,axis=0,return_inverse=True,return_counts=True)
    return group,counts

def iterate(s):
    s.x,s.f,s.cv=s.ax.copy(),s.af.copy(),s.ac.copy(); s.n=len(s.x)
    group,counts=regions(s.f,s.params.get('divisions',8)); parents=[]
    for _ in range(s.n):
        a,b=s.rng.integers(len(counts),size=2); region=a if counts[a]<counts[b] else b
        parents.append(s.rng.choice(np.flatnonzero(group==region)))
    y=offspring(s,parents); f,cv=evaluate(s,y)
    # Remove from most occupied regions until archive fits.
    x=np.r_[s.ax,y]; ff=np.r_[s.af,f]; cc=np.r_[s.ac,cv]; ids=list(nondominated(ff,cc)); limit=s.params.get('population',40)
    while len(ids)>limit:
        groups,c=regions(ff[ids]); g=np.argmax(c); positions=np.flatnonzero(groups==g)
        ids.pop(int(s.rng.choice(positions)))
    s.ax,s.af,s.ac=x[ids],ff[ids],cc[ids]

def run(problem,budget=10000,seed=DEFAULT_OPTIMIZER_SEED,**params):
    return execute(initialize,iterate,problem,budget,seed,**params)
