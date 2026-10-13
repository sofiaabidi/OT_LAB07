"""Shared bookkeeping and variation, not an interchangeable optimizer.

Each algorithm supplies its own selection/update. Archive is a passive recording
archive unless explicitly used by that algorithm; it is not fed to early GAs.
"""
import numpy as np
from src.moo_utils import archive, non_dominated_sort, crowding_distance, dominates
from src.project_config import DEFAULT_OPTIMIZER_SEED

class State:
    def __init__(self,problem,budget=10000,seed=DEFAULT_OPTIMIZER_SEED,population=40,**params):
        self.p=problem; self.budget=budget; self.rng=np.random.default_rng(seed)
        self.n=min(population,budget); self.params=params; self.used=0; self.generation=0
        self.x=problem.sample(self.rng,self.n); self.f,self.cv=self.evaluate(self.x)
        self.ax,self.af,self.ac=archive(self.x,self.f,self.cv,self.n)
        self.extra={}; self.history=[]
    def evaluate(self,x):
        if self.used+len(x)>self.budget: raise ValueError('Evaluation budget exceeded')
        f,cv=self.p.evaluate(x); self.used+=len(x); return f,cv
    def record(self,x,f,cv):
        self.ax,self.af,self.ac=archive(np.r_[self.ax,x],np.r_[self.af,f],np.r_[self.ac,cv],self.n)
    def finish(self):
        ok=self.ac<=1e-10
        return {'x':self.ax[ok], 'f':self.af[ok], 'cv':self.ac[ok], 'evaluations':self.used,
                'final_x':self.x,'final_f':self.f,'history':self.history}

def evaluate(state,x): return state.evaluate(x)

def mutate(p,x,rng,scale=.1):
    y=x.copy()
    if p.kind=='permutation':
        i,j=np.sort(rng.choice(len(x),2,replace=False))
        if rng.random()<.5: y[i:j+1]=y[i:j+1][::-1]
        else: y[i],y[j]=y[j],y[i]
    elif p.kind=='binary':
        flips=rng.random(len(x))<1/len(x); y[flips]=1-y[flips]
    else:
        mask=rng.random(len(x))<1/len(x)
        if not mask.any(): mask[rng.integers(len(x))]=True
        y[mask]+=rng.normal(0,scale,mask.sum())*(p.upper-p.lower)[mask]
    return p.repair(y)

def crossover(p,a,b,rng):
    if p.kind=='permutation':
        i,j=np.sort(rng.choice(len(a),2,replace=False)); y=np.full(len(a),-1,int); y[i:j+1]=a[i:j+1]
        remaining=[v for v in np.roll(b,-j-1) if v not in y]
        positions=list(range(j+1,len(a)))+list(range(i))
        y[positions]=remaining; return y
    if p.kind=='binary': return np.where(rng.random(len(a))<.5,a,b)
    # SBX with eta=15.
    u=rng.random(len(a)); beta=np.where(u<=.5,(2*u)**(1/16),(1/(2*(1-u)))**(1/16))
    beta*=rng.choice([-1,1],len(a)); return p.repair(.5*((1+beta)*a+(1-beta)*b))

def offspring(s,parents=None,count=None):
    parents=np.arange(s.n) if parents is None else np.asarray(parents)
    count=min(s.n,s.budget-s.used) if count is None else count
    return np.array([mutate(s.p,crossover(s.p,s.x[s.rng.choice(parents)],s.x[s.rng.choice(parents)],s.rng),s.rng) for _ in range(count)])

def environmental(f,cv,n):
    chosen=[]
    for front in non_dominated_sort(f,cv):
        if len(chosen)+len(front)<=n: chosen.extend(front)
        else:
            chosen.extend(front[np.argsort(-crowding_distance(f[front]),kind='stable')[:n-len(chosen)]]); break
    return np.array(chosen,int)

def rank_crowding(f,cv):
    rank=np.zeros(len(f),int); crowd=np.zeros(len(f))
    for r,front in enumerate(non_dominated_sort(f,cv)): rank[front]=r; crowd[front]=crowding_distance(f[front])
    return rank,crowd

def tournament(s):
    rank,c=rank_crowding(s.f,s.cv); pairs=s.rng.integers(s.n,size=(s.n,2))
    return np.array([a if (rank[a],-c[a])<(rank[b],-c[b]) else b for a,b in pairs])

def merge(s,y,f,cv,selector=environmental):
    x=np.r_[s.x,y]; ff=np.r_[s.f,f]; cc=np.r_[s.cv,cv]; idx=selector(ff,cc,s.n)
    s.x,s.f,s.cv=x[idx],ff[idx],cc[idx]

def execute(initialize,iterate,problem,budget=10000,seed=DEFAULT_OPTIMIZER_SEED,**params):
    s=initialize(problem,budget,seed,**params)
    while s.used<s.budget:
        old=s.used; iterate(s); s.generation+=1
        if s.used==old: raise RuntimeError('Iteration consumed no evaluations')
    return s.finish()


def archive_leader(s,count=1):
    crowd=crowding_distance(s.af); weights=np.where(np.isinf(crowd),2.,crowd+1e-6)
    weights/=weights.sum()
    ids=s.rng.choice(len(s.ax),count,replace=count>len(s.ax),p=weights)
    return s.ax[ids]
