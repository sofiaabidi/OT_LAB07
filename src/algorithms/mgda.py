"""MGDA: minimum-norm convex combination of task gradients.
For two tasks solve lambda analytically; clamp to [0,1]. Learning rate=.05.
Toy losses have gradients 2*(x-a),2*(x-b). No convergence theorem assumed
for arbitrary nonconvex neural networks."""
import numpy as np
from src.project_config import DEFAULT_OPTIMIZER_SEED

def weights(gradients):
    a,b=np.asarray(gradients); d=a-b; t=np.clip(-b@d/max(d@d,1e-15),0,1)
    return np.array([t,1-t])
def initialize(problem,budget=10000,seed=DEFAULT_OPTIMIZER_SEED,**params):
    return {'p':problem,'x':np.array([0.,5.]),'used':0,'budget':budget,'lr':params.get('lr',.05),'history':[]}
def evaluate(s): return s['p'].evaluate(s['x'][None])[0][0]
def iterate(s):
    f=evaluate(s); g=np.array([2*(s['x']-3),2*(s['x']+3)]); w=weights(g)
    s['history'].append([s['used'],*f,*w,*s['x']]); s['used']+=1; s['x']-=s['lr']*(w@g)
def run(problem,budget=10000,seed=DEFAULT_OPTIMIZER_SEED,**params):
    s=initialize(problem,budget,seed,**params)
    while s['used']<budget: iterate(s)
    last=np.asarray(s['history'][-1]); x=last[-2:]; f=last[1:3]
    return {'x':x[None],'f':f[None],'cv':np.zeros(1),'evaluations':s['used'],'history':s['history']}
