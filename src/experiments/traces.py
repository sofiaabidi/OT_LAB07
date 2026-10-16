"""Deterministic two-iteration Task C traces for Sofia's roll-72 methods.

All choices are explicit fixtures. These traces validate mechanisms; they are
not stochastic optimizer trials or convergence proofs.
"""
import json
import numpy as np

from src.algorithms import mopso, r_nsga2, vega
from src.experiments.runner import CSV_DIR
from src.moo_utils import dominates
from src.problems import get_problem
from src.project_config import ACTIVE_PROVENANCE, ROLL_SUFFIX, TASK_C_ALGORITHM_NUMBERS


def _r_nsga2_trace():
    p=get_problem('P1'); reference=np.array([4.,4.]); epsilon=.20
    parents=np.array([3.,4.,6.,7.])
    offspring_sets=[np.array([3.5,4.5,5.5,6.5]),
                    np.array([4.25,4.75,5.25,5.75])]
    rows=[]
    for iteration,offspring in enumerate(offspring_sets,1):
        x=np.r_[parents,offspring]
        f,cv=p.evaluate(x[:,None]); z=p.normalized(f); ref=p.normalized(reference)
        distances=np.linalg.norm(z-ref,axis=1)
        details=r_nsga2.preference_select_details(f,cv,4,p,epsilon,reference)
        selected=details['selected_indices']
        rows.append({
            'iteration':iteration,'population_size':4,
            'reference_natural':reference.tolist(),
            'normalization_ideal':p.ideal.tolist(),
            'normalization_nadir':p.nadir.tolist(),
            'parents_x':parents.tolist(),'offspring_x':offspring.tolist(),
            'candidates_x':x.tolist(),'F':f.tolist(),
            'normalized_F':z.tolist(),'normalized_reference':ref.tolist(),
            'distance_to_reference':distances.tolist(),'epsilon':epsilon,
            'distance_order':np.argsort(distances,kind='stable').tolist(),
            'fronts':details['fronts'],'clearing_decisions':details['decisions'],
            'selected_indices':selected.tolist(),'selected_x':x[selected].tolist(),
        })
        parents=x[selected]
    return rows


def _vega_trace():
    p=get_problem('P1'); population=np.array([3.,4.,6.,7.])
    tournament_pairs=[[(0,2),(1,3),(1,2),(0,2)],
                      [(0,2),(1,3),(2,3),(2,3)]]
    objectives=[0,1,0,1]; u=.25; beta=(2*u)**(1/16)
    rows=[]
    for iteration,pairs in enumerate(tournament_pairs,1):
        f,cv=p.evaluate(population[:,None])
        winners=[vega.objective_winner(f,cv,a,b,j)
                 for (a,b),j in zip(pairs,objectives)]
        mating=population[winners]
        parent_pairs=[mating[:2].tolist(),mating[2:].tolist()]
        children=[]
        for left,right in parent_pairs:
            children.extend([.5*((1+beta)*left+(1-beta)*right),
                             .5*((1-beta)*left+(1+beta)*right)])
        children=np.asarray(children); child_f,_=p.evaluate(children[:,None])
        rows.append({
            'iteration':iteration,'population_size':4,
            'population':population.tolist(),'F':f.tolist(),
            'slot_objectives':objectives,
            'tournament_pairs':[list(v) for v in pairs],
            'winner_indices':winners,'mating_pool':mating.tolist(),
            'parent_pairs':parent_pairs,'sbx_u':u,'sbx_beta':beta,
            'mutation_increments':[0.,0.,0.,0.],
            'offspring':children.tolist(),'offspring_F':child_f.tolist(),
            'next_population':children.tolist(),
            'variation_rule':'SBX fixture u=0.25 and positive beta; swapped parents produce the paired child; mutation increment is zero',
        })
        population=children
    return rows


def _mopso_trace():
    # This deliberately isolates the MOPSO mechanics from assignment problem P2.
    # The wider toy interval keeps all stated particles and updates feasible, while
    # the explicit velocity limit makes the hand calculation independently checkable.
    toy_bounds=np.array([1.,20.]); velocity_limits=np.array([-10.,10.])
    x=np.array([5.,10.,15.,12.]); v=np.zeros(4); pbest=x.copy()
    guides=[np.array([15.,15.,5.,5.]),np.array([15.,15.,5.,5.])]
    rows=[]; archive_positions=x.copy().tolist()
    for iteration,leader in enumerate(guides,1):
        old=x.copy(); old_v=v.copy()
        old_f=np.c_[100/old,old*old]
        inertia_term=.7*v
        cognitive_term=1.5*.5*(pbest-x)
        social_term=1.5*.5*(leader-x)
        v=mopso.velocity(v,x,pbest,leader,np.full(4,.5),np.full(4,.5),
                         inertia=.7,c1=1.5,c2=1.5)
        v=np.clip(v,*velocity_limits)
        x=x+v; f=np.c_[100/x,x*x]
        outcomes=[]
        for i in range(4):
            pf=np.array([100/pbest[i],pbest[i]*pbest[i]])
            outcomes.append('replace' if dominates(f[i],pf) else
                            ('retain: pbest dominates' if dominates(pf,f[i]) else
                             'retain: incomparable'))
        archive_before=list(archive_positions); archive_positions.extend(x.tolist())
        rows.append({
            'iteration':iteration,'population_size':4,
            'problem_definition':'independent scalar toy; not assignment P2',
            'position_bounds':toy_bounds.tolist(),
            'velocity_limits':velocity_limits.tolist(),
            'old_x':old.tolist(),'old_velocity':old_v.tolist(),
            'old_F':old_f.tolist(),
            'pbest':pbest.tolist(),'leader':leader.tolist(),'r1':[.5]*4,
            'r2':[.5]*4,'inertia':.7,'c1':1.5,'c2':1.5,
            'inertia_term':inertia_term.tolist(),
            'cognitive_term':cognitive_term.tolist(),
            'social_term':social_term.tolist(),
            'new_velocity':v.tolist(),'new_x':x.tolist(),'F':f.tolist(),
            'pbest_after':pbest.tolist(),
            'pbest_decisions':outcomes,
            'pbest_rule':'replace only when the trial dominates; all four trials here are incomparable',
            'archive_before':archive_before,'archive_after':list(archive_positions),
            'archive_size_after':len(archive_positions),
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
