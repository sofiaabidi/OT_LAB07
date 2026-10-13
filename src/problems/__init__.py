"""Assignment P1-P14, with natural maximizations negated.

Constraints are dimensionless positive residuals; zero means feasible.
P8 follows legacy NumPy RandomState(7), not default_rng(7).
P9 standardization is fit on training folds only; folds fixed with seed 63.
"""
from dataclasses import dataclass
from functools import lru_cache
import numpy as np
from src.moo_utils import normalize, nondominated
from src.project_config import (
    DTLZ_REFERENCE_SEED_OFFSET, P8_INSTANCE_SEED, P9_FOLD_SEED,
)

MU=np.array([.08,.12,.15,.10])
COV=np.array([[.010,.002,.001,.003],[.002,.040,.006,.004],[.001,.006,.090,.005],[.003,.004,.005,.020]])
SUPPLIERS=np.array([[120,8,10,92],[100,7,14,88],[140,9,7,95],[90,6,18,80],[130,8,9,90]],float)
rs=np.random.RandomState(P8_INSTANCE_SEED)
COORDS=rs.uniform(0,100,(15,2))
DIST=np.linalg.norm(COORDS[:,None]-COORDS[None,:],axis=2)
U=np.ones((15,15))
for i in range(15):
    for j in range(i+1,15): U[i,j]=U[j,i]=rs.uniform(.5,2.)
TIME=DIST*U

@lru_cache(None)
def cancer_data():
    # Dataset loader only. No sklearn classifier or cross-validation tools.
    from sklearn.datasets import load_breast_cancer
    ds=load_breast_cancer(); folds=np.array_split(np.random.default_rng(P9_FOLD_SEED).permutation(len(ds.target)),5)
    matrices=[]
    for test in folds:
        train=np.setdiff1d(np.arange(len(ds.target)),test)
        mean=ds.data[train].mean(0); std=np.maximum(ds.data[train].std(0),1e-12)
        a=(ds.data[test]-mean)/std; b=(ds.data[train]-mean)/std
        matrices.append(((a[:,None,:]-b[None,:,:])**2,ds.target[train],ds.target[test]))
    return ds,matrices

@lru_cache(8192)
def knn_error(mask):
    if not any(mask): return 1.
    ds,folds=cancer_data(); correct=0
    for square,train_y,test_y in folds:
        d=square[:,:,np.asarray(mask,bool)].sum(2)
        ids=np.argpartition(d,4,axis=1)[:,:5]
        pred=(train_y[ids].sum(1)>=3).astype(int)
        correct+=int((pred==test_y).sum())
    return 1-correct/len(ds.target)

@dataclass
class Problem:
    key: str
    lower: np.ndarray
    upper: np.ndarray
    ideal: np.ndarray
    nadir: np.ndarray
    kind: str='real'
    m: int=2

    def repair(self,x):
        x=np.clip(np.asarray(x,float),self.lower,self.upper)
        if self.key=='P4':
            x=np.maximum(x,1e-15); x=x/x.sum(axis=-1,keepdims=True)
        if self.kind in ('binary','integer'): x=np.rint(x)
        if self.kind=='binary' and x.sum()==0: x.flat[0]=1
        if self.kind=='permutation':
            # Random keys may be used by swarm moves; direct tours stay unchanged.
            if not np.array_equal(np.sort(x.astype(int)),np.arange(15)) or not np.all(x==np.rint(x)):
                x=np.argsort(x)
            x=x.astype(int)
        return x

    def sample(self,rng,n):
        if self.key=='P13': return rng.normal(size=(n,2))
        if self.kind=='permutation': return np.array([rng.permutation(15) for _ in range(n)])
        return np.array([self.repair(z) for z in rng.uniform(self.lower,self.upper,(n,len(self.lower)))])

    def evaluate(self,x):
        x=np.atleast_2d(x); k=self.key; a=x[:,0]; g=[]
        if k=='P1': f=np.c_[(a-3)**2,(a-7)**2]
        elif k=='P2': f=np.c_[100/a,a*a]
        elif k=='P3':
            z=1+x[:,1:].sum(1); f=np.c_[a,z*(1-(a/z)**2)]
        elif k=='P4':
            f=np.c_[np.einsum('ni,ij,nj->n',x,COV,x),-x@MU]
            g=[np.abs(x.sum(1)-1)-1e-8]
        elif k=='P5':
            b=a; h=x[:,1]; f=np.c_[7850*b*h,4*1000/(200e9*b*h**3)]
            g=[(2.4e-5-b*h*h)/2.4e-5]
        elif k=='P6':
            b=x[:,1]; f=np.c_[4*(a*a+b*b),(a-5)**2+(b-5)**2]
            g=[((a-5)**2+b*b-25)/25,(7.7-(a-8)**2-(b+3)**2)/7.7]
        elif k=='P7':
            f=np.c_[-.8*a,-1.2*x[:,1]]; g=[(x.sum(1)-90)/90]
        elif k=='P8':
            tours=x.astype(int); nxt=np.roll(tours,-1,axis=1)
            f=np.c_[DIST[tours,nxt].sum(1),TIME[tours,nxt].sum(1)]
            g=[np.array([0 if np.array_equal(np.sort(t),np.arange(15)) else 1 for t in tours])]
        elif k=='P9':
            f=np.array([[knn_error(tuple(z.astype(bool))),z.sum()] for z in x]); g=[(x.sum(1)<1).astype(float)]
        elif k=='P10':
            z=1+((x[:,self.m-1:]-.5)**2).sum(1); cols=[]
            for j in range(self.m):
                v=z*np.cos(x[:,:self.m-j-1]*np.pi/2).prod(1)
                if j: v*=np.sin(x[:,self.m-j-1]*np.pi/2)
                cols.append(v)
            f=np.column_stack(cols)
        elif k=='P11':
            b=x[:,1]; f=np.c_[-4*a-6*b,-a-b]
            g=[(2*a+3*b-1200)/1200,(4*a+2*b-1600)/1600]
        elif k=='P12':
            f=SUPPLIERS[x[:,0].astype(int)]*np.array([1,-1,1,-1])
        elif k=='P13': f=np.c_[((x-3)**2).sum(1),((x+3)**2).sum(1)]
        elif k=='P14': f=np.c_[.4+.05*a+.012*x[:,1],-.2*x[:,1]/(.5+.03*a)]
        else: raise KeyError(k)
        cv=np.maximum(np.column_stack(g),0).sum(1) if g else np.zeros(len(x))
        return f,cv

    def normalized(self,f): return normalize(f,self.ideal,self.nadir)

    def true_front(self,n=301):
        t=np.linspace(0,1,n)
        if self.key=='P1': return self.evaluate((3+4*t)[:,None])[0]
        if self.key=='P2': return self.evaluate((np.arange(1,11) if self.kind=='integer' else 1+9*t)[:,None])[0]
        if self.key=='P3': return np.c_[t,1-t*t]
        if self.key=='P5':
            # Analytic front: maximal height for each cross-section area.
            area=np.linspace(.01*np.sqrt(2.4e-5/.01),.1*.2,n)
            h=np.minimum(.2,area/.01); b=area/h
            return self.evaluate(np.c_[b,h])[0]
        if self.key=='P6':
            # Until (3,3), the unconstrained radial optimum is x1=x2.
            u=np.linspace(0,3,n//2); v=np.linspace(3,5,n-n//2)
            return self.evaluate(np.r_[np.c_[u,u],np.c_[v,np.full(len(v),3)]])[0]
        if self.key=='P7': return self.evaluate(np.c_[10+60*t,80-60*t])[0]
        if self.key=='P10':
            z=np.abs(np.random.default_rng(DTLZ_REFERENCE_SEED_OFFSET+self.m).normal(size=(n,self.m)))
            return z/np.linalg.norm(z,axis=1,keepdims=True)
        if self.key=='P11': return np.array([[-2400.,-500.]])
        if self.key=='P13': return self.evaluate(np.c_[-3+6*t,-3+6*t])[0]
        if self.key=='P14': return self.evaluate(np.c_[np.full(n,13),40+50*t])[0]
        return None

def get_problem(key,m=3,integer=False):
    definitions={
      'P1':([1],[10],[0,0],[16,16]),'P2':([1],[10],[10,1],[100,100]),
      'P3':([0]*10,[1]*10,[0,0],[1,1]),
      'P4':([0]*4,[1]*4,[0,-.15],[.09,-.08]),
      'P5':([.01,.02],[.1,.2],[0,0],[157,.25]),
      'P6':([0,0],[5,3],[0,4],[136,50]),
      'P7':([10,20],[70,80],[-56,-96],[-8,-24]),
      'P8':([0]*15,[14]*15,[0,0],[2200,3300]),
      'P9':([0]*30,[1]*30,[0,1],[.2,30]),
      'P10':([0]*(m+9),[1]*(m+9),[0]*m,[1]*m),
      'P11':([0,0],[400,400],[-2400,-500],[0,0]),
      'P12':([0],[4],[90,-9,7,-95],[140,-6,18,-80]),
      'P13':([-np.inf,-np.inf],[np.inf,np.inf],[0,0],[72,72]),
      'P14':([13,40],[17,90],[1.53,-.2*90/.89],[2.33,-.2*40/1.01])}
    lo,hi,ideal,nadir=map(lambda a:np.array(a,float),definitions[key])
    kind={'P8':'permutation','P9':'binary','P12':'integer'}.get(key,'real')
    if key=='P2' and integer: kind='integer'
    return Problem(key,lo,hi,ideal,nadir,kind,m if key=='P10' else len(ideal))

def nearest_neighbour(matrix,start=0):
    tour=[start]; remaining=set(range(len(matrix)))-{start}
    while remaining:
        city=min(remaining,key=lambda c:(matrix[tour[-1],c],c)); tour.append(city); remaining.remove(city)
    return np.array(tour)
