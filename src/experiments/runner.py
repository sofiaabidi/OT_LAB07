"""Checkpointable Task A/C/D experiments. All CSVs are actual evaluations.
One job per algorithm/problem/seed; no source copying or optimizer libraries.
"""
from pathlib import Path
import csv,json,time,importlib
import numpy as np
from src.algorithms import load
from src.problems import get_problem,SUPPLIERS,COORDS,DIST,TIME,nearest_neighbour
from src.moo_utils import hypervolume,igd,spacing,nondominated
from src.experiments.catalogue import DISPLAY,DESIGNATED,SEEDS
from src.project_config import (
    ACTIVE_PROVENANCE, DEFAULT_OPTIMIZER_SEED, NETWORK_DATA_SEED,
    ROLL_SUFFIX, TASK_C_ALGORITHM_NUMBERS,
)
ROOT=Path(__file__).resolve().parents[2]
RESULTS_ROOT=ROOT/'results'/ACTIVE_PROVENANCE
CSV_DIR=RESULTS_ROOT/'csv'
TABLES_DIR=RESULTS_ROOT/'tables'

def tasks(budget=10000):
    jobs=set()
    for a,plist in enumerate(DESIGNATED,1):
        if a in [8,9]: continue
        for p in plist[:2]:
            for seed in (SEEDS if 10<=a<=35 else [DEFAULT_OPTIMIZER_SEED]):
                jobs.add((a,p,5 if p=='P10' else 2,seed,'base','',budget if p!='P9' else min(budget,200)))
    # NSGA-III Task A explicitly includes M=3 and M=5.
    for a in [15,31,34]:
        for seed in SEEDS: jobs.add((a,'P10',3,seed,'base','',budget))
    # Continuous head-to-head: every applicable optimizer (exclude ranking,
    # permutation, gradient and many-objective specific implementations).
    continuous=[1,2,3,4,*range(10,15),16,17,18,19,21,22,23,24,26,27,28,29,30,32,33,35]
    for p in ['P3','P5']:
        for a in continuous:
            for seed in SEEDS: jobs.add((a,p,2,seed,'D','',budget))
    for a in [14,15,18,31,34]:
        for seed in SEEDS: jobs.add((a,'P10',5,seed,'D','',budget))
    for a in [20,25,14,30]:
        for seed in SEEDS: jobs.add((a,'P8',2,seed,'D','',budget))
    # Task C sensitivity: one primary parameter, three settings, ten seeds.
    for a,parameter,values,p in [
        (35,'epsilon',[.02,.05,.10],'P14'),
        (10,'population',[20,40,80],'P3'),
        (22,'inertia',[.2,.4,.8],'P4'),
    ]:
        for value in values:
            for seed in SEEDS: jobs.add((a,p,2,seed,'sensitivity',json.dumps({parameter:value}),budget))
    return sorted(jobs)

def job_key(job):
    a,p,m,seed,group,params,b=job
    suffix=params.replace(' ','').replace('"','').replace(':','_').replace('{','').replace('}','')
    return f'{group}_A{a:02d}_{p}_M{m}_S{seed}_B{b}_{suffix}'

def run_job(job):
    a,p,m,seed,group,params,b=job
    key=job_key(job); target=CSV_DIR/f'{key}.json'; target.parent.mkdir(parents=True,exist_ok=True)
    if target.exists():
        saved=json.loads(target.read_text())
        if (saved.get('provenance')!=ACTIVE_PROVENANCE or
                saved.get('roll_suffix')!=ROLL_SUFFIX or
                saved.get('optimizer_seed')!=seed):
            raise ValueError(f'{target} has incompatible provenance')
        return saved
    problem=get_problem(p,m=m); t=time.perf_counter()
    options=json.loads(params) if params else {}; options.setdefault('population',40)
    result=load(a).run(problem,budget=b,seed=seed,**options)
    elapsed=time.perf_counter()-t; f=result['f']; z=problem.normalized(f); true=problem.true_front()
    # IGD only against exact analytic/sphere reference; no invented P4/P8/P9 front.
    hv=hypervolume(z,np.full(problem.m,1.1)) if len(z) else 0.
    row={'algorithm_number':a,'algorithm':DISPLAY[a-1],'problem':p,'objectives':problem.m,'seed':seed,
        'group':group,'parameters':params,'budget_cap':b,'evaluations':result['evaluations'],'HV':hv,
        'IGD':igd(z,problem.normalized(true)) if true is not None else None,'Spacing':spacing(z),
        'runtime':elapsed,'front_size':len(f),'feasible_fraction':float(np.mean(result['cv']<=1e-10)) if len(f) else 0.,'file':key,
        'provenance':ACTIVE_PROVENANCE,'roll_suffix':ROLL_SUFFIX,'optimizer_seed':seed}
    # Retain both decisions and objectives for every front, even if empty.
    np.savez_compressed(CSV_DIR/f'{key}.npz',x=result['x'],f=f,cv=result['cv'],history=np.asarray(result.get('history',[])),final_f=result.get('final_f',f))
    if 'solves' in result: row['solves']=result['solves']
    target.write_text(json.dumps(row,indent=2)); return row

def write_csv(path,rows,columns=None):
    if not rows: return
    columns=columns or list(rows[0]); path.parent.mkdir(parents=True,exist_ok=True)
    with path.open('w',newline='') as handle:
        writer=csv.DictWriter(handle,fieldnames=columns,extrasaction='ignore'); writer.writeheader(); writer.writerows(rows)

def aggregate(rows):
    groups={}
    for r in rows: groups.setdefault((r['group'],r['algorithm_number'],r['problem'],r['objectives'],r['parameters']),[]).append(r)
    out=[]
    for (group,a,p,m,params),values in sorted(groups.items()):
        row={'group':group,'algorithm_number':a,'algorithm':DISPLAY[a-1],'problem':p,'objectives':m,'parameters':params,'trials':len(values),'budget_cap':values[0]['budget_cap']}
        for metric in ['HV','IGD','Spacing','runtime','front_size','evaluations']:
            z=[v[metric] for v in values if v[metric] is not None]
            row[metric+'_mean']=float(np.mean(z)) if z else None; row[metric+'_std']=float(np.std(z,ddof=1)) if len(z)>1 else (0. if z else None)
        out.append(row)
    return out

def extras():
    from src.problems.network import train
    from src.algorithms import topsis,vikor
    rankings=[]
    for method in ['topsis','vikor']:
        for v in ([.5] if method=='topsis' else [.25,.5,.75]):
            for weights in [[.3,.3,.2,.2],[.4,.2,.2,.2]]:
                result=(topsis.run(SUPPLIERS,weights,[False,True,False,True]) if method=='topsis' else vikor.run(SUPPLIERS,weights,[False,True,False,True],v))
                rankings.append({'problem':'P12','method':method,'weights':str(weights),'v':v,'order':str((result['order']+1).tolist()),'top_three':str((result['order'][:3]+1).tolist()),'compromise':str(result.get('compromise',[]))})
    p=get_problem('P4'); front=load(14).run(p,budget=10000,seed=DEFAULT_OPTIMIZER_SEED)
    write_csv(CSV_DIR/'P4_nsga2_ranking_input.csv',[{'id':i,**{f'f{j+1}':v for j,v in enumerate(f)}} for i,f in enumerate(front['f'])])
    for weights in [[.5,.5],[.6,.4]]:
        for method in ['topsis','vikor']:
            result=load(8 if method=='topsis' else 9).run(p.normalized(front['f']),weights)
            rankings.append({'problem':'P4 NSGA-II front','method':method,'weights':str(weights),'v':.5,'order':str(result['order'].tolist()),'top_three':str(result['order'][:3].tolist()),'compromise':str(result.get('compromise',[]))})
    write_csv(CSV_DIR/'rankings.csv',rankings)
    np.savetxt(ROOT/'data/p8_coordinates.csv',COORDS,delimiter=',',header='x,y',comments='')
    np.savetxt(ROOT/'data/p8_distance.csv',DIST,delimiter=','); np.savetxt(ROOT/'data/p8_time.csv',TIME,delimiter=',')
    bases=[]
    for label,matrix in [('distance',DIST),('time',TIME)]:
        tour=nearest_neighbour(matrix); f,c=get_problem('P8').evaluate(tour[None]); bases.append({'baseline':label,'tour':str(tour.tolist()),'distance':f[0,0],'time':f[0,1]})
    write_csv(CSV_DIR/'routing_baselines.csv',bases)
    for scale in [1,10]:
        for seed in SEEDS:
            for method in ['equal','mgda','gradnorm']:
                h=train(method,seed,1000,scale=scale,lr=.001 if scale==10 else .01)
                np.savetxt(CSV_DIR/f'network_{method}_scale{scale}_seed{seed}.csv',h,delimiter=',',header='step,classification,regression,w1,w2',comments='')
    for method in ['equal']:
        x=np.array([0.,5.]); p=get_problem('P13'); h=[]
        for t in range(10000):
            f,c=p.evaluate(x[None]); h.append([t,*f[0],.5,.5,*x]); x-=.05*(2*x)
        np.savetxt(CSV_DIR/'toy_equal.csv',h,delimiter=',',header='step,f1,f2,w1,w2,x1,x2',comments='')
    # Random dominance fraction to quantify many-objective selection pressure.
    rows=[]
    for m in [3,5]:
        p=get_problem('P10',m)
        for seed in SEEDS:
            x=p.sample(np.random.default_rng(seed),100); f,c=p.evaluate(x)
            rows.append({'M':m,'seed':seed,'nondominated_fraction':len(nondominated(f))/100})
    write_csv(CSV_DIR/'dominance_pressure.csv',rows)

if __name__=='__main__':
    import argparse,concurrent.futures,os
    parser=argparse.ArgumentParser(); parser.add_argument('--budget',type=int,default=10000); parser.add_argument('--workers',type=int,default=4); parser.add_argument('--limit',type=int); parser.add_argument('--algorithms',type=int,nargs='+'); parser.add_argument('--force',action='store_true'); parser.add_argument('--skip-extras',action='store_true')
    args=parser.parse_args(); jobs=tasks(args.budget)
    if args.algorithms: jobs=[j for j in jobs if j[0] in args.algorithms]
    if args.limit: jobs=jobs[:args.limit]
    if args.force:
        for job in jobs:
            path=CSV_DIR/f'{job_key(job)}.json'
            if path.exists(): path.unlink()
    with concurrent.futures.ProcessPoolExecutor(max_workers=args.workers) as pool:
        for i,row in enumerate(pool.map(run_job,jobs),1):
            if i%10==0 or i==len(jobs): print(f'{i}/{len(jobs)} {row["algorithm"]} {row["problem"]}',flush=True)
    rows=[json.loads(f.read_text()) for f in CSV_DIR.glob('*.json') if f.name!='hand_traces.json']
    write_csv(CSV_DIR/'raw_experiments.csv',rows,[k for k in rows[0] if k!='solves'])
    summary=aggregate(rows); write_csv(TABLES_DIR/'summary.csv',summary)
    if not args.skip_extras: extras()
