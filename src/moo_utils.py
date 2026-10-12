"""Minimization, Deb feasibility rules, fronts and normalized quality metrics.

No optimizer libraries are used. Pairwise dominance costs O(M*N**2).
"""
import numpy as np

def dominates(a, b, ca=0., cb=0.):
    if ca <= 1e-10 < cb: return True
    if cb <= 1e-10 < ca: return False
    if ca > 1e-10 and cb > 1e-10: return ca < cb
    return bool(np.all(np.asarray(a) <= b) and np.any(np.asarray(a) < b))

def dominance_matrix(f, cv=None):
    f = np.asarray(f); n = len(f)
    d = np.all(f[:, None] <= f[None, :], axis=2) & np.any(f[:, None] < f[None, :], axis=2)
    if cv is not None:
        c = np.asarray(cv); feasible = c <= 1e-10
        d = np.where(feasible[:, None] & feasible[None, :], d,
             np.where(feasible[:, None], True,
             np.where(feasible[None, :], False, c[:, None] < c[None, :])))
    np.fill_diagonal(d, False)
    return d

def non_dominated_sort(f, cv=None):
    d = dominance_matrix(f, cv); count = d.sum(axis=0); fronts=[]
    remaining = np.ones(len(f), bool)
    while remaining.any():
        front = np.flatnonzero(remaining & (count == 0))
        if not len(front): raise RuntimeError('Dominance relation is cyclic')
        fronts.append(front); remaining[front]=False
        count -= d[front].sum(axis=0)
    return fronts

def crowding_distance(f):
    f=np.asarray(f); n=len(f); out=np.zeros(n)
    if n <= 2: return np.full(n, np.inf)
    for j in range(f.shape[1]):
        order=np.argsort(f[:,j], kind='stable'); span=np.ptp(f[:,j])
        if span <= 1e-15: continue
        out[order[[0,-1]]]=np.inf
        out[order[1:-1]] += (f[order[2:],j]-f[order[:-2],j])/span
    return out

def normalize(f, ideal, nadir):
    return (np.asarray(f)-ideal)/np.maximum(np.asarray(nadir)-ideal, 1e-12)

def violation(g):
    return np.maximum(np.asarray(g),0).sum(axis=-1)

def nondominated(f, cv=None):
    return np.flatnonzero(~dominance_matrix(f,cv).any(axis=0))

def archive(x, f, cv, limit=100):
    idx=nondominated(f,cv)
    # Exact duplicate objectives do not add hypervolume.
    _, unique=np.unique(np.round(f[idx],12),axis=0,return_index=True); idx=idx[unique]
    if len(idx)>limit: idx=idx[np.argsort(-crowding_distance(f[idx]),kind='stable')[:limit]]
    return x[idx].copy(), f[idx].copy(), cv[idx].copy()

def hypervolume(f, reference, samples=8192, seed=991, lower=None):
    f=np.asarray(f); r=np.asarray(reference)
    f=f[np.all(f<r,axis=1)]
    if not len(f): return 0.
    f=f[nondominated(f)]
    if f.shape[1]==2:
        f=f[np.argsort(f[:,0])]; last=r[1]; area=0.
        for a,b in f:
            if b<last: area+=(r[0]-a)*(last-b); last=b
        return float(area)
    low=np.zeros(len(r)) if lower is None else np.asarray(lower)
    if np.any(f<low): raise ValueError('Monte Carlo lower bound does not enclose front')
    pts=np.random.default_rng(seed).uniform(low,r,(samples,len(r)))
    covered=np.zeros(samples,bool)
    for point in f: covered |= np.all(pts>=point,axis=1)
    return float(np.prod(r-low)*covered.mean())

def igd(f, true_front):
    if len(f)==0: return float('inf')
    return float(np.sqrt(((np.asarray(true_front)[:,None]-f[None,:])**2).sum(axis=2)).min(axis=1).mean())

def spacing(f):
    if len(f)<2: return 0.
    d=np.abs(np.asarray(f,dtype=float)[:,None]-f[None,:]).sum(axis=2); np.fill_diagonal(d,np.inf)
    return float(np.std(d.min(axis=1),ddof=1))

def reference_vectors(n,m,seed=19):
    if m==2:
        t=np.linspace(0,1,n); return np.column_stack([t,1-t])
    # Simplex-lattice directions, deterministic subsampling if too numerous.
    import itertools, math
    h=1
    while math.comb(h+m-1,m-1)<n: h+=1
    def compositions(total,k):
        if k==1: yield (total,); return
        for i in range(total+1):
            for tail in compositions(total-i,k-1): yield (i,)+tail
    v=np.array(list(compositions(h,m)),float)/h
    if len(v)>n:
        extremes=np.argmax(v,axis=0); rest=np.setdiff1d(np.arange(len(v)),extremes)
        idx=np.r_[extremes,np.random.default_rng(seed).choice(rest,n-len(extremes),replace=False)]
        v=v[idx]
    return v
