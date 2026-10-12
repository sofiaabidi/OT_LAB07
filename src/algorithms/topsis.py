"""TOPSIS ranking, not an optimizer. Vector normalization, weights,
benefit/cost ideal, Euclidean ideal and anti-ideal distance. Default equal
weights if not supplied; P12 uses [.3,.3,.2,.2]. Zero columns protected."""
import numpy as np

def initialize(table,weights=None,benefit=None):
    return np.asarray(table,float),np.ones(np.shape(table)[1])/np.shape(table)[1] if weights is None else np.asarray(weights,float),benefit

def evaluate(table): return np.asarray(table,float)

def iterate(table,weights=None,benefit=None):
    a,w,benefit=initialize(table,weights,benefit); benefit=np.zeros(a.shape[1],bool) if benefit is None else np.asarray(benefit,bool)
    z=a/np.maximum(np.linalg.norm(a,axis=0),1e-12)*w
    ideal=np.where(benefit,z.max(0),z.min(0)); anti=np.where(benefit,z.min(0),z.max(0))
    dp=np.linalg.norm(z-ideal,axis=1); dm=np.linalg.norm(z-anti,axis=1)
    score=dm/np.maximum(dp+dm,1e-12)
    return {'score':score,'order':np.argsort(-score,kind='stable'),'ideal':ideal,'anti':anti,'dplus':dp,'dminus':dm}

def run(table,weights=None,benefit=None,**params): return iterate(table,weights,benefit)
