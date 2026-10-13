"""Deterministic two-iteration Task C traces for Sofia's roll-72 methods.

All choices are explicit fixtures. These traces validate mechanisms; they are
not stochastic optimizer trials or convergence proofs.
"""
import json
import numpy as np

from src.algorithms import mopso, r_nsga2
from src.experiments.runner import CSV_DIR
from src.problems import get_problem
from src.project_config import ACTIVE_PROVENANCE, ROLL_SUFFIX, TASK_C_ALGORITHM_NUMBERS


def _r_nsga2_trace():
    p=get_problem('P1'); reference=np.array([4.,4.]); epsilon=.20
    populations=[
        np.array([3.,4.,6.,7.,3.5,4.5,5.5,6.5]),
        np.array([4.5,5.5,4.,6.,4.25,4.75,5.25,5.75]),
    ]
    rows=[]
    for iteration,x in enumerate(populations,1):
        f,cv=p.evaluate(x[:,None]); z=p.normalized(f); ref=p.normalized(reference)
        distances=np.linalg.norm(z-ref,axis=1)
        selected=r_nsga2.preference_select(f,cv,4,p,epsilon,reference)
        rows.append({
            'iteration':iteration,'population_size':4,
            'parents_x':x[:4].tolist(),'offspring_x':x[4:].tolist(),
            'candidates_x':x.tolist(),'F':f.tolist(),
            'normalized_F':z.tolist(),'normalized_reference':ref.tolist(),
            'distance_to_reference':distances.tolist(),'epsilon':epsilon,
            'distance_order':np.argsort(distances,kind='stable').tolist(),
            'selected_indices':selected.tolist(),'selected_x':x[selected].tolist(),
        })
    return rows


def _vega_trace():
    # Supplied lecture example uses f1 minimization and f2 maximization.
    populations=[np.array([10.,20.,30.,40.]),np.array([40.,40.,30.,30.])]
    rows=[]
    for iteration,x in enumerate(populations,1):
        f1=1000/x; f2=x*x/100
        by_f1=np.argsort(f1,kind='stable')[:2]
        by_f2=np.argsort(-f2,kind='stable')[:2]
        selected=np.r_[by_f1,by_f2]
        rows.append({
            'iteration':iteration,'population_size':4,
            'population':x.tolist(),'f1_min':f1.tolist(),
            'f2_max':f2.tolist(),'f1_selected_indices':by_f1.tolist(),
            'f2_selected_indices':by_f2.tolist(),
            'mating_pool':x[selected].tolist(),
            'variation_rule':'copy parents; no mutation in lecture fixture',
        })
    return rows


def _mopso_trace():
    x=np.array([5.,10.,15.,12.]); v=np.zeros(4); pbest=x.copy()
    guides=[np.array([15.,15.,5.,5.]),np.array([15.,15.,5.,5.])]
    rows=[]
    for iteration,leader in enumerate(guides,1):
        old=x.copy(); old_v=v.copy()
        v=mopso.velocity(v,x,pbest,leader,np.full(4,.5),np.full(4,.5),
                         inertia=.7,c1=1.5,c2=1.5)
        x=x+v; f=np.c_[100/x,x*x]
        rows.append({
            'iteration':iteration,'population_size':4,
            'old_x':old.tolist(),'old_velocity':old_v.tolist(),
            'pbest':pbest.tolist(),'leader':leader.tolist(),'r1':[.5]*4,
            'r2':[.5]*4,'inertia':.7,'c1':1.5,'c2':1.5,
            'new_velocity':v.tolist(),'new_x':x.tolist(),'F':f.tolist(),
            'pbest_after':pbest.tolist(),
            'pbest_rule':'incomparable trial does not replace personal best',
            'archive_size_after':4+4*iteration,
        })
    return rows


def build():
    output={
        'metadata':{'provenance':ACTIVE_PROVENANCE,'roll_suffix':ROLL_SUFFIX,
                    'algorithms':list(TASK_C_ALGORITHM_NUMBERS)},
        'r_nsga2':_r_nsga2_trace(),'vega':_vega_trace(),'mopso':_mopso_trace(),
    }
    CSV_DIR.mkdir(parents=True,exist_ok=True)
    (CSV_DIR/'hand_traces.json').write_text(json.dumps(output,indent=2))
    return output


if __name__=='__main__': build()
