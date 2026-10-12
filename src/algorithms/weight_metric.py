"""Weight Metric: distance from fixed ideal, weighted p=1,2,infinity.
Sweep weights for all three p values. p=infinity uses epigraph-free max.
Default SLSQP ftol=1e-10, maxiter=120; sweep=21; seed=63.
Bounds and explicit constraints handled by SLSQP. Only scalar subproblems use SciPy.
Local solves are not a global optimality certificate.
"""
import numpy as np
from scipy.optimize import minimize
from src.moo_utils import archive

def initialize(problem,budget=10000,seed=63,**params):
    return {'p':problem,'budget':budget,'seed':seed,'params':params,'used':0,'x':[],'f':[],'cv':[],'solves':[]}

def evaluate(s,x):
    if s['used']>=s['budget']: raise StopIteration
    f,c=s['p'].evaluate(np.asarray(x)[None]); s['used']+=1
    s['x'].append(np.array(x)); s['f'].append(f[0]); s['cv'].append(c[0])
    return s['p'].normalized(f[0]),c[0]

def solve(s,objective,extra_constraints=(),start=None):
    p=s['p']; rng=np.random.default_rng(s['seed'])
    start=p.sample(rng,1)[0] if start is None else start
    constraints=[{'type':'ineq','fun':lambda x:-p.evaluate(x[None])[1][0]}]
    if p.key=='P4': constraints=[{'type':'eq','fun':lambda x:x.sum()-1}]
    constraints.extend({'type':'ineq','fun':g} for g in extra_constraints)
    # Constraint objective evaluations count as calls too; for reproducibility all
    # evaluations are routed through the same cache, indexed by exact vector.
    cache={}
    def get(x):
        key=tuple(x)
        if key not in cache: cache[key]=evaluate(s,x)
        return cache[key]
    constraints[0]['fun']=(lambda x:x.sum()-1) if p.key=='P4' else (lambda x:-get(x)[1])
    result=minimize(lambda x:objective(get(x)[0]),start,method='SLSQP',bounds=list(zip(p.lower,p.upper)),constraints=constraints,
        options={'maxiter':120,'ftol':1e-10})
    s['solves'].append({'success':bool(result.success),'message':str(result.message),'x':result.x.tolist(),'f':(get(result.x)[0]*(p.nadir-p.ideal)+p.ideal).tolist(),'cv':float(get(result.x)[1])})
    return result.x,get(result.x)[0]

def finish(s):
    p=s['p']; x=np.array(s['x']); f=np.array(s['f']); c=np.array(s['cv'])
    # Classical sweep results are solver solutions, not its intermediate probes.
    if s['solves']:
        x=np.array([v['x'] for v in s['solves']]); f=np.array([v['f'] for v in s['solves']]); c=np.array([v['cv'] for v in s['solves']])
    if len(x): x,f,c=archive(x,f,c,1000)
    good=c<=1e-8
    return {'x':x[good],'f':f[good],'cv':c[good],'evaluations':s['used'],'solves':s['solves']}

def run(problem,budget=10000,seed=63,**params):
    s=initialize(problem,budget,seed,**params)
    try: iterate(s)
    except StopIteration: pass
    return finish(s)

def metric(f,w,p):
    z=np.maximum(w,1e-6)*np.abs(f)
    return float(z.max() if np.isinf(p) else (np.maximum(w,1e-6)*np.abs(f)**p).sum()**(1/p))
def iterate(s):
    for p in s['params'].get('powers',[1,2,np.inf]):
        for t in np.linspace(0,1,s['params'].get('settings',21)):
            w=np.array([t,1-t]); solve(s,lambda f:metric(f,w,p))
