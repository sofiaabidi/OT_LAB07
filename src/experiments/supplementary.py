"""Problem-bank investigations, with explicit actual and reduced budgets."""
from pathlib import Path
import csv,json
import numpy as np
from src.problems import get_problem,knn_error,cancer_data,nearest_neighbour,DIST,TIME
from src.algorithms import load
from src.moo_utils import nondominated
from src.experiments.runner import write_csv,ROOT

def run():
    rows=[]
    for integer in [False,True]:
        p=get_problem('P2',integer=integer); result=load(10).run(p,10000,630)
        rows.append({'problem':'P2','investigation':'VEGA integer' if integer else 'VEGA real','value':len(result['f']),'notes':'distinct recorded Pareto points at 10000 evaluations'})
        np.savetxt(ROOT/'results/csv'/f'p2_vega_integer{integer}.csv',np.c_[result['x'],result['f']],delimiter=',',header='x,cost,delay',comments='')
    rng=np.random.default_rng(630); p=get_problem('P5'); X=p.sample(rng,10000); f,c=p.evaluate(X)
    rows.append({'problem':'P5','investigation':'random infeasible fraction','value':float((c>0).mean()),'notes':'10000 independent uniform box designs; same formulas'})
    feasible=nondominated(f,c); ignore=nondominated(f)
    np.savetxt(ROOT/'results/csv/beam_constraint_ablation.csv',np.c_[X,f,c],delimiter=',',header='b,h,mass,deflection,violation',comments='')
    rows.append({'problem':'P5','investigation':'ignore stress minimum mass','value':float(f[ignore,0].min()),'notes':f'feasible-front minimum {f[feasible,0].min():.6g}; random-design ablation, not an optimizer run'})
    # Repair vs penalty on identical random portfolio draws. This measures
    # feasibility and score changes, not a causal full optimizer comparison.
    p=get_problem('P4'); X=rng.uniform(0,1,(10000,4)); rawf,c=p.evaluate(X); repaired=np.array([p.repair(x) for x in X]); ff,cc=p.evaluate(repaired)
    rows.append({'problem':'P4','investigation':'raw equality feasible fraction','value':float((c<=1e-10).mean()),'notes':f'repair feasible fraction={(cc<=1e-10).mean():.3f}; penalty=z1+z2+100*violation'})
    np.savetxt(ROOT/'results/csv/portfolio_repair_penalty.csv',np.c_[rawf,c,ff,cc],delimiter=',',header='raw_risk,raw_negative_return,raw_violation,repaired_risk,repaired_negative_return,repaired_violation',comments='')
    ds,folds=cancer_data(); baseline=knn_error((True,)*30)
    masks=[]; objectives=[]
    for path in (ROOT/'results/csv').glob('base_A*_P9_*.npz'):
        z=np.load(path); masks.extend(z['x']); objectives.extend(z['f'])
    f=np.array(objectives); X=np.array(masks); idx=nondominated(f); X,f=X[idx],f[idx]
    eligible=f[:,0]<=baseline+.01; minimum=int(f[eligible,1].min()) if eligible.any() else None
    rows.append({'problem':'P9','investigation':'all-features 5NN baseline error','value':baseline,'notes':f'smallest observed mask within +.01 error: {minimum}; exploratory 200-evaluation runs, not global optimum'})
    write_csv(ROOT/'results/csv/feature_frequencies.csv',[{'feature':name,'front_frequency':float(freq)} for name,freq in zip(ds.feature_names,X.mean(0))])
    rows.append({'problem':'P14','investigation':'aspiration at 12h analytic front weight','value':.4+.05*13+.012*(12*.89/.2),'notes':'at x1=13, battery=53.4Wh yields 1.6908kg; aspiration (1.8,12h) is dominated'})
    rows.append({'problem':'P6','investigation':'second-constraint minimum left side','value':18.,'notes':'at (5,0), 9+9=18>7.7; inactive across full box'})
    rows.append({'problem':'P7','investigation':'reference feasible allocation','value':(40/.8)+(50/1.2),'notes':'91.6667>90; exact (40,50) output unattainable'})
    write_csv(ROOT/'results/csv/problem_investigations.csv',rows)
if __name__=='__main__': run()

def population_job(job):
    import time
    from src.moo_utils import hypervolume,igd,spacing
    N,budget,seed=job; folder=ROOT/'results/csv/population'; folder.mkdir(exist_ok=True)
    key=f'N{N}_B{budget}_S{seed}'; checkpoint=folder/f'{key}.json'
    if checkpoint.exists(): return json.loads(checkpoint.read_text())
    p=get_problem('P3'); t=time.perf_counter(); r=load(14).run(p,budget,seed,population=N); duration=time.perf_counter()-t
    z=p.normalized(r['f']); row={'population':N,'budget':budget,'seed':seed,'full_generations':(budget-N)//N,'HV':hypervolume(z,[1.1,1.1]),'IGD':igd(z,p.normalized(p.true_front())),'Spacing':spacing(z),'runtime':duration}
    np.savez_compressed(folder/f'{key}.npz',x=r['x'],f=r['f'],cv=r['cv']); checkpoint.write_text(json.dumps(row,indent=2)); return row

def population_study():
    from concurrent.futures import ProcessPoolExecutor
    jobs=[(N,B,S) for N in [20,40,80] for B in [1000,5000,10000] for S in range(630,640)]
    with ProcessPoolExecutor(max_workers=6) as pool: rows=list(pool.map(population_job,jobs))
    write_csv(ROOT/'results/csv/population_study.csv',rows); summary=[]
    for N in [20,40,80]:
        for B in [1000,5000,10000]:
            r=[z for z in rows if z['population']==N and z['budget']==B]; row={'population':N,'budget':B,'trials':10,'full_generations':r[0]['full_generations']}
            for metric in ['HV','IGD','Spacing','runtime']:
                a=[z[metric] for z in r]; row[metric+'_mean']=float(np.mean(a)); row[metric+'_std']=float(np.std(a,ddof=1))
            summary.append(row)
    write_csv(ROOT/'results/tables/population_study_summary.csv',summary)
