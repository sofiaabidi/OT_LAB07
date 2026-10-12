"""VIKOR compromise ranking with S=sum weighted regret, R=max regret,
Q=v*(S-Sbest)/(Sworst-Sbest)+(1-v)*(R-Rbest)/(Rworst-Rbest).
Default v=.5. Report acceptable advantage 1/(N-1) and stability; never
force a unique compromise when the conditions fail."""
import numpy as np

def initialize(table,weights=None,benefit=None):
    a=np.asarray(table,float); w=np.ones(a.shape[1])/a.shape[1] if weights is None else np.asarray(weights,float)
    return a,w,np.zeros(a.shape[1],bool) if benefit is None else np.asarray(benefit,bool)
def evaluate(table): return np.asarray(table,float)
def iterate(table,weights=None,benefit=None,v=.5):
    a,w,b=initialize(table,weights,benefit); cost=a*np.where(b,-1,1)
    regret=(cost-cost.min(0))/np.maximum(np.ptp(cost,axis=0),1e-12)*w
    S=regret.sum(1); R=regret.max(1)
    Q=v*(S-S.min())/max(np.ptp(S),1e-12)+(1-v)*(R-R.min())/max(np.ptp(R),1e-12)
    order=np.argsort(Q,kind='stable'); best=order[0]
    advantage=len(a)<2 or Q[order[1]]-Q[best]>=1/max(len(a)-1,1)
    stability=best==np.argmin(S) or best==np.argmin(R)
    compromise=[int(best)]
    if not advantage: compromise=[int(i) for i in order if Q[i]-Q[best]<1/max(len(a)-1,1)]
    elif not stability and len(a)>1: compromise.append(int(order[1]))
    return {'S':S,'R':R,'Q':Q,'order':order,'advantage':advantage,'stability':stability,'compromise':compromise}
def run(table,weights=None,benefit=None,v=.5,**params): return iterate(table,weights,benefit,v)
