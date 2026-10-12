"""Population-four hand traces with explicit choices; no hidden random stream.
The fixed variation draws are an instructional fixture, not experiment runs.
"""
from pathlib import Path
import json
import numpy as np
from src.problems import get_problem
from src.algorithms import weighted_sum,npga,mosa
ROOT=Path(__file__).resolve().parents[2]

def build():
    p=get_problem('P1'); output={}
    output['weighted_sum']=[]
    for w in [.25,.75]:
        x=weighted_sum.analytic_p1(w); f=p.evaluate(np.array([[x]]))[0][0]
        output['weighted_sum'].append({'w':[w,1-w],'derivative':'2*w*(x-3)+2*(1-w)*(x-7)=0','x':x,'objectives':f.tolist(),'raw_scalar':float(np.dot([w,1-w],f))})
    x=np.array([[3.],[4.],[6.],[7.]])
    output['npga']=[]
    pairs=[(0,1),(1,2),(2,3),(0,3)]
    for step in range(2):
        f,c=p.evaluate(x); sigma=.8; niches=npga.niche_count(f,sigma)
        comparison_sets=[[j for j in range(4) if j not in [a,b]] for a,b in pairs]
        winners=[int(npga.pareto_tournament(f,c,a,b,C,sigma)) for (a,b),C in zip(pairs,comparison_sets)]
        # SBX beta=1: uniform u=.5, positive sign; child copies first
        # selected parent. Mutations are explicitly fixed Gaussian draws
        # under scale=.1, bound range=9 (thus displacement=.9*z).
        increments=np.array([.5,-.25,.25,-.5]) if step==0 else np.array([.25,.5,-.5,-.25])
        child=np.clip(x[winners,0]+increments,1,10)[:,None]
        z=(f-f.min(0))/np.maximum(np.ptp(f,axis=0),1e-12)
        D=np.linalg.norm(z[:,None]-z[None,:],axis=2); shares=np.maximum(0,1-(D/sigma)**2)
        output['npga'].append({'iteration':step+1,'population':x.ravel().tolist(),'F':f.tolist(),'normalized_F':z.tolist(),'distances':D.tolist(),'sharing':shares.tolist(),'niche_counts':niches.tolist(),'pairs':pairs,'comparison_sets':comparison_sets,'dominated_flags':[any(np.all(f[j]<=f[i]) and np.any(f[j]<f[i]) for j in range(4)) for i in range(4)],'winners':winners,'SBX_u':.5,'SBX_sign':1,'beta':1.,'mutation_z':(increments/.9).tolist(),'increments':increments.tolist(),'offspring':child.ravel().tolist(),'offspring_F':p.evaluate(child)[0].tolist()})
        x=child
    x=np.array([3.,4.,6.,7.]); output['mosa']=[]
    proposals=[np.array([3.5,4.5,6.5,7.5]),np.array([4.,5.,7.,6.5])]
    uniforms=[np.array([.1,.2,.9,.1]),np.array([.2,.3,.7,.4])]
    for step in range(2):
        old=p.normalized(p.evaluate(x[:,None])[0]); new=p.normalized(p.evaluate(proposals[step][:,None])[0]); T=.1*.97**step
        prob=np.array([mosa.acceptance(a,b,T,[.5,.5]) for a,b in zip(old,new)])
        accepted=uniforms[step]<prob; final=np.where(accepted,proposals[step],x)
        output['mosa'].append({'iteration':step+1,'x':x.tolist(),'proposal':proposals[step].tolist(),'normalized_old':old.tolist(),'normalized_new':new.tolist(),'T':T,'worsened_sum':np.maximum(new-old,0).sum(1).tolist(),'probability':prob.tolist(),'uniform':uniforms[step].tolist(),'accepted':accepted.tolist(),'next_x':final.tolist()})
        x=final
    (ROOT/'results/csv/hand_traces.json').write_text(json.dumps(output,indent=2)); return output
if __name__=='__main__': build()
