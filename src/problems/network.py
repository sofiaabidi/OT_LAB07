"""P13(b): NumPy-only forward/backward shared tanh body, two heads.
Synthetic 128x5 inputs seed 63, binary class sign(X0-X1), regression
3*X0+2*X2 plus N(0,.1). Regression scale stress multiplies target by 10.
Full-batch training, BCE and MSE; no autograd, no ML training library.
"""
import numpy as np
from src.project_config import NETWORK_DATA_SEED

def data(seed=NETWORK_DATA_SEED,scale=1):
    rng=np.random.default_rng(seed); x=rng.normal(size=(128,5))
    yc=(x[:,0]-x[:,1]>0).astype(float); yr=scale*(3*x[:,0]+2*x[:,2]+rng.normal(0,.1,128))
    return x,yc,yr

def initialize(seed=63):
    rng=np.random.default_rng(seed)
    return [rng.normal(0,.1,(5,8)),np.zeros(8),rng.normal(0,.1,8),np.zeros(1),rng.normal(0,.1,8),np.zeros(1)]

def forward_backward(params,batch):
    W,b,wc,bc,wr,br=params; X,yc,yr=batch; n=len(X)
    H=np.tanh(X@W+b); logits=H@wc+bc[0]; pred=1/(1+np.exp(-np.clip(logits,-50,50)))
    reg=H@wr+br[0]; loss=np.array([np.mean(np.logaddexp(0,logits)-yc*logits),np.mean((reg-yr)**2)])
    dc=(pred-yc)/n; dr=2*(reg-yr)/n
    gc=dc[:,None]*wc*(1-H*H); gr=dr[:,None]*wr*(1-H*H)
    zero=np.zeros(8)
    gradients=[ [X.T@gc,gc.sum(0),H.T@dc,np.array([dc.sum()]),zero.copy(),np.zeros(1)],
                [X.T@gr,gr.sum(0),zero.copy(),np.zeros(1),H.T@dr,np.array([dr.sum()])] ]
    shared=np.array([np.r_[g[0].ravel(),g[1]] for g in gradients])
    return loss,gradients,shared

def train(method='equal',seed=NETWORK_DATA_SEED,steps=1000,scale=1,lr=.01):
    from src.algorithms.mgda import weights as mgda_weights
    from src.algorithms.gradnorm import update_weights
    params=initialize(seed); batch=data(NETWORK_DATA_SEED,scale); w=np.ones(2); history=[]; initial=None
    for t in range(steps):
        loss,g,shared=forward_backward(params,batch)
        if initial is None: initial=loss.copy()
        if method=='mgda': w=mgda_weights(shared)
        elif method=='gradnorm': w=update_weights(w,loss,initial,shared,lr=.001)
        else: w=np.array([.5,.5])
        history.append([t,*loss,*w])
        for j in range(6): params[j]-=lr*(w[0]*g[0][j]+w[1]*g[1][j])
    return np.array(history)
