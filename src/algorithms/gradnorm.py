"""GradNorm: adaptive weights minimizing sum |G_i-target_i|.
G_i=w_i*||gradient_i||; target=mean(G)*relative_training_rate**alpha,
stop-gradient target, weights renormalized to sum(tasks). Alpha=1.5,
weight_lr=.01, model_lr=.05. Hand-derived weight gradient uses sign.
This supports toy objectives and the handwritten shared network."""
import numpy as np

def update_weights(w,loss,initial,gradients,alpha=1.5,lr=.01):
    norms=np.linalg.norm(gradients,axis=1); G=w*norms
    rates=loss/np.maximum(initial,1e-12); rates/=max(rates.mean(),1e-12)
    target=G.mean()*rates**alpha
    w=np.maximum(w-lr*np.sign(G-target)*norms,1e-6)
    return w*len(w)/w.sum()
def initialize(problem,budget=10000,seed=63,**params):
    x=np.array([0.,5.]); f=None
    return {'p':problem,'x':x,'w':np.ones(2),'initial':f,'used':0,'budget':budget,'params':params,'history':[]}
def evaluate(s): return s['p'].evaluate(s['x'][None])[0][0]
def iterate(s):
    f=evaluate(s); g=np.array([2*(s['x']-3),2*(s['x']+3)]); p=s['params']
    if s['initial'] is None: s['initial']=f.copy()
    s['w']=update_weights(s['w'],f,s['initial'],g,p.get('alpha',1.5),p.get('weight_lr',.01))
    s['history'].append([s['used'],*f,*s['w'],*s['x']]); s['used']+=1
    s['x']-=p.get('lr',.05)*(s['w']@g)
def run(problem,budget=10000,seed=63,**params):
    s=initialize(problem,budget,seed,**params)
    while s['used']<budget: iterate(s)
    last=np.asarray(s['history'][-1]); x=last[-2:]; f=last[1:3]
    return {'x':x[None],'f':f[None],'cv':np.zeros(1),'evaluations':s['used'],'history':s['history']}
