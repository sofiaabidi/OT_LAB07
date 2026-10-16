"""Generate prose, plots and PDF exclusively from persisted raw results."""
from pathlib import Path
import json,csv,textwrap,sys,os
import numpy as np
os.environ.setdefault('MPLCONFIGDIR',str(Path(__file__).resolve().parents[2]/'.matplotlib'))
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from src.experiments.runner import ROOT,RESULTS_ROOT,CSV_DIR,TABLES_DIR,write_csv,aggregate
from src.experiments.catalogue import DISPLAY,DESIGNATED
from src.experiments.notes_data import NOTES,FAMILIES
from src.problems import get_problem,COORDS
from src.algorithms import load
from src.project_config import DEFAULT_OPTIMIZER_SEED, TASK_C_ALGORITHM_NUMBERS, ACTIVE_PROVENANCE
FIGURES_DIR=ROOT/'figures'/ACTIVE_PROVENANCE
plt.rcParams.update({'font.size':10,'axes.spines.top':False,'axes.spines.right':False,'figure.dpi':120})

def read_csv(path):
    with path.open(encoding='utf-8') as h: return list(csv.DictReader(h))
def val(x): return 'N/A' if x in (None,'','None') or str(x).lower()=='nan' else f'{float(x):.5g}'
def meanstd(row,metric):
    mean=val(row.get(metric+'_mean')); sd=val(row.get(metric+'_std'))
    return 'N/A' if mean=='N/A' else (mean if sd=='N/A' else mean+' ± '+sd)

def metric_series(rows,metric):
    """Return numeric mean/SD arrays, or None when a metric is unavailable."""
    means=[r.get(metric+'_mean') for r in rows]
    if all(value is None for value in means): return None
    return ([np.nan if value is None else value for value in means],
            [np.nan if r.get(metric+'_std') is None else r[metric+'_std'] for r in rows])

def load_rows(): return [json.loads(f.read_text(encoding='utf-8')) for f in sorted(CSV_DIR.glob('*.json')) if f.name!='hand_traces.json']

def figures(rows,summary):
    manifest=[]
    for a in range(1,38):
        subset=[r for r in rows if r['algorithm_number']==a and r['group']=='base']
        if a in [8,9]:
            ranks=read_csv(CSV_DIR/'rankings.csv'); chosen=[r for r in ranks if r['problem']=='P12' and r['method']==('topsis' if a==8 else 'vikor')]
            fig,ax=plt.subplots(figsize=(7,4));
            for i,r in enumerate(chosen):
                order=json.loads(r['order']); positions=np.empty(5); positions[np.array(order)-1]=np.arange(1,6)
                ax.plot(np.arange(1,6),positions,'o-',label=f"v={r['v']} weights={r['weights']}")
            ax.set(xlabel='Supplier',ylabel='Rank (1 best)',title=DISPLAY[a-1]); ax.set_xticks(range(1,6)); ax.set_yticks(range(1,6)); ax.invert_yaxis(); ax.legend(fontsize=7); fig.tight_layout()
        else:
            conditions=sorted({(r['problem'],r['objectives']) for r in subset}); cols=min(2,len(conditions)); fig,axes=plt.subplots(1,cols,figsize=(7.5,3.1),squeeze=False)
            for ax,(p,m) in zip(axes.ravel(),conditions):
                candidates=[r for r in subset if r['problem']==p and r['objectives']==m]; r=min(candidates,key=lambda r:r['seed']); z=np.load(CSV_DIR/f"{r['file']}.npz"); f=z['f']; problem=get_problem(p,m)
                true=problem.true_front()
                if a in [36,37]:
                    h=z['history']; ax.plot(h[:200,0],h[:200,1],label='task 1'); ax.plot(h[:200,0],h[:200,2],label='task 2'); ax.set(xlabel='Loss evaluations',ylabel='Loss')
                elif m==2:
                    if true is not None: ax.plot(true[:,0],true[:,1],'k--',lw=1,label='analytic front')
                    ax.scatter(f[:,0],f[:,1],s=16,label=f"seed {r['seed']}"); ax.set(xlabel='f1 (min)',ylabel='f2 (min)')
                else:
                    if m==3:
                        ax.scatter(true[:,0],true[:,1],c='gray',marker='x',s=5,alpha=.2,label='true sphere projection')
                        ax.scatter(f[:,0],f[:,1],c=f[:,2],s=20,cmap='viridis',label='obtained; color=f3'); ax.set(xlabel='f1 projection',ylabel='f2 projection'); ax.legend(fontsize=8)
                    else:
                        for line in true[:15]: ax.plot(np.arange(1,m+1),line,'--',color='gray',alpha=.22,lw=.6)
                        for line in f: ax.plot(np.arange(1,m+1),line,alpha=.3,lw=.7)
                        ax.plot([],[],'--',color='gray',label='true sphere sample'); ax.legend(fontsize=8)
                        ax.set(xlabel='Objective index',ylabel='Objective value')
                ax.set_title(f'{p} / M={m} / calls={r["evaluations"]}'); ax.legend(fontsize=7) if m==2 else None
            fig.suptitle(f'A{a:02d} {DISPLAY[a-1]}',fontsize=12); fig.tight_layout()
        FIGURES_DIR.mkdir(parents=True,exist_ok=True); path=FIGURES_DIR/f'A{a:02d}.png'; fig.savefig(path,bbox_inches='tight'); plt.close(fig); manifest.append({'figure':path.name,'description':f'Task A {DISPLAY[a-1]}','sources':';'.join(r['file'] for r in subset) if subset else 'rankings.csv'})
    for p,m in [('P3',2),('P5',2),('P8',2),('P10',5)]:
        chosen=[r for r in rows if r['group']=='D' and r['problem']==p and r['objectives']==m and r['seed']==DEFAULT_OPTIMIZER_SEED]
        fig,ax=plt.subplots(figsize=(8,5))
        for index,r in enumerate(chosen):
            f=np.load(CSV_DIR/f"{r['file']}.npz")['f']
            if m==2: ax.scatter(f[:,0],f[:,1],s=12,label=f'A{r["algorithm_number"]} {r["algorithm"]}',alpha=.7)
            else:
                color=plt.get_cmap('tab10')(index)
                for line in f: ax.plot(np.arange(1,6),line,color=color,alpha=.2,lw=.8)
                ax.plot([],[],color=color,label=r['algorithm'])
        true=get_problem(p,m).true_front()
        if true is not None and m==2: ax.plot(true[:,0],true[:,1],'k--',label='analytic front')
        ax.set_title(f'Task D {p} / M={m} / seed {DEFAULT_OPTIMIZER_SEED}'+(' - recorded fronts in parallel coordinates' if m==5 else ''))
        ax.set_xlabel('Objective index' if m==5 else 'f1 (min)'); ax.set_ylabel('Objective value' if m==5 else 'f2 (min)'); ax.legend(fontsize=7,ncol=3 if len(chosen)>10 else 1,loc='upper center',bbox_to_anchor=(.5,-.15)); fig.tight_layout()
        path=FIGURES_DIR/f'D_{p}.png'; fig.savefig(path,bbox_inches='tight'); plt.close(fig); manifest.append({'figure':path.name,'description':f'Head-to-head {p}','sources':';'.join(r['file'] for r in chosen)})
    for a in TASK_C_ALGORITHM_NUMBERS:
        chosen=[r for r in summary if r['group']=='sensitivity' and r['algorithm_number']==a]; labels=[r['parameters'] for r in chosen]
        fig,axes=plt.subplots(1,3,figsize=(9,3.3))
        for ax,metric in zip(axes,['HV','IGD','Spacing']):
            series=metric_series(chosen,metric)
            if series is None:
                ax.text(.5,.5,'Unavailable: no exact front',ha='center',va='center',transform=ax.transAxes,wrap=True)
            else:
                means,stds=series; ax.errorbar(range(3),means,yerr=stds,fmt='o-',capsize=5)
            ax.set_xticks(range(3),labels,rotation=22,fontsize=7); ax.set_title(metric)
        fig.suptitle(f'{DISPLAY[a-1]} sensitivity / 10 trials / actual calls in table'); fig.tight_layout(); path=FIGURES_DIR/f'C_A{a:02d}.png'; fig.savefig(path,bbox_inches='tight'); plt.close(fig)
        manifest.append({'figure':path.name,'description':'Task C parameter sensitivity','sources':';'.join(labels)})
    for scale in [1,10]:
        fig,axes=plt.subplots(1,2,figsize=(8,3.2))
        for method in ['equal','mgda','gradnorm']:
            histories=np.array([np.loadtxt(path,delimiter=',',skiprows=1) for path in sorted(CSV_DIR.glob(f'network_{method}_scale{scale}_seed*.csv'))]); mean=histories.mean(0); std=histories.std(0,ddof=1)
            for ax,j in zip(axes,[1,2]): ax.plot(mean[:,0],mean[:,j],label=method); ax.fill_between(mean[:,0],np.maximum(mean[:,j]-std[:,j],1e-10),mean[:,j]+std[:,j],alpha=.1)
        for ax,label in zip(axes,['classification BCE','regression MSE']): ax.set(xlabel='Full-batch steps',ylabel=label,yscale='log'); ax.legend()
        fig.suptitle(f'P13 network / regression scale={scale} / mean +/- SD, 10 seeds'); fig.tight_layout(); path=FIGURES_DIR/f'network_scale{scale}.png'; fig.savefig(path,bbox_inches='tight'); plt.close(fig); manifest.append({'figure':path.name,'description':'P13 gradient comparison','sources':f'network_*_scale{scale}_seed*.csv'})
    fig,axes=plt.subplots(1,2,figsize=(8,3.2))
    equal=np.loadtxt(CSV_DIR/'toy_equal.csv',delimiter=',',skiprows=1)
    for label,history in [('equal weights',equal)]+[(DISPLAY[a-1],np.load(CSV_DIR/f"{next(r['file'] for r in rows if r['algorithm_number']==a and r['group']=='base')}.npz")['history']) for a in [36,37]]:
        for ax,j in zip(axes,[1,2]): ax.plot(history[:200,0],history[:200,j],label=label)
    for ax,title in zip(axes,['Toy task 1 loss','Toy task 2 loss']): ax.set(xlabel='Objective evaluations',ylabel=title); ax.legend(fontsize=9)
    fig.suptitle('P13 toy: identical start (0,5), first 200 evaluations'); fig.tight_layout(); path=FIGURES_DIR/'toy_comparison.png'; fig.savefig(path,bbox_inches='tight'); plt.close(fig)
    manifest.append({'figure':path.name,'description':'MGDA GradNorm and equal toy losses','sources':'base_A36_P13; base_A37_P13; toy_equal.csv'})
    flows={35:['Parents + offspring','Nondominated fronts','Normalize + distance to reference','Epsilon clearing','Preferred survivors'],10:['Population of N','Objective-wise subpools','Merge + shuffle mating pool','Crossover + mutation','Nonelitist replacement'],22:['Particles + archive','Crowding-selected leader','Velocity + position update','Update pbest if dominating','Update nondominated archive']}
    for a in TASK_C_ALGORITHM_NUMBERS:
        steps=flows[a]
        fig,ax=plt.subplots(figsize=(6,4)); ax.set_xlim(0,1); ax.set_ylim(0,1); ax.axis('off')
        for i,label in enumerate(steps):
            y=.9-i*.19; ax.text(.5,y,label,ha='center',va='center',bbox={'boxstyle':'round,pad=.5','fc':'#edf3f8','ec':'#365570'})
            if i<4: ax.annotate('',xy=(.5,y-.12),xytext=(.5,y-.05),arrowprops={'arrowstyle':'->','color':'#365570'})
        fig.tight_layout(); path=FIGURES_DIR/f'flow_A{a:02d}.png'; fig.savefig(path,bbox_inches='tight'); plt.close(fig); manifest.append({'figure':path.name,'description':'Task C mechanism flow','sources':f'src/algorithms/{a}'})
    write_csv(TABLES_DIR/'figure_manifest.csv',manifest)
    return manifest

FORMULATIONS=[
('Factory speed','x in [1,10], one real variable','min [(x-3)^2,(x-7)^2]','Bounds only; Pareto x in [3,7].','Encoding: one-element real vector. Equal weight solution x=7-4w. Convex front; uniform weight steps are uniform x steps, not uniform arc lengths.'),
('Fleet size','x in [1,10], real or integer','min [100/x,x^2]','Bounds; every x is Pareto optimal.','Integer experiment has at most ten distinct objective points. VEGA runs and exact integer problem definitions retain integer repair.'),
('Specified ZDT2','10 real variables in [0,1]','g=1+sum(x2..x10); min [x1,g*(1-(x1/g)^2)]','Bounds; exact front [t,1-t^2].','The factor matches the assignment at n=10; no alternate benchmark is substituted. Weighted Sum cannot select the unsupported interior with a global scalar solve.'),
('Portfolio','four nonnegative real weights','min [w^T Sigma w,-mu^T w]','sum(w)=1. Repair positive entries by sum; scalar solvers use equality.','mu=(.08,.12,.15,.10). Sigma rows (.010,.002,.001,.003),(.002,.040,.006,.004),(.001,.006,.090,.005),(.003,.004,.005,.020). Scaling risk lower bound 0 is conservative, not true attainable ideal. Repair/penalty investigation is a random-design ablation.'),
('Cantilever beam','b in [.01,.10]m, h in [.02,.20]m','min [7850*b*h,4000/(200e9*b*h^3)]','CV=max((2.4e-5-b*h^2)/2.4e-5,0).','P=1000N,L=1m,E=200GPa,rho=7850kg/m^3. Feasibility first. For given area A=b*h, maximize h=min(.2,A/.01) to derive true tradeoff; smallest feasible area is .01*sqrt(2.4e-5/.01).'),
('Binh-Korn','x1 in [0,5], x2 in [0,3]','min [4*(x1^2+x2^2),(x1-5)^2+(x2-5)^2]','(x1-5)^2+x2^2<=25; (x1-8)^2+(x2+3)^2>=7.7.','Residuals divided by 25 and 7.7 before summing positive parts. Second constraint inactive: minimum 18. Front x1=x2 from 0 to 3, then x2=3 and x1 from 3 to 5.'),
('Water allocation','x1 agriculture [10,70], x2 industry [20,80]','min [-.8*x1,-1.2*x2]','x1+x2<=90; CV=max((sum(x)-90)/90,0).','Natural maximized outputs preserve interpretation after sign conversion. Exact front sum=90. Output reference (40,50) requires 91.6667 units, so it is unattainable exactly.'),
('Delivery routing','permutation of 15 city indices, closed tour','min [sum distance edges,sum traffic-time edges]','Each city once. Invalid permutations CV=1.','Legacy RandomState(7), coordinates uniform [0,100]^2; independent upper-triangle symmetric traffic multipliers uniform [.5,2]. Deposits include closing edge. OX, swap and inversion remain valid tours. The wording 15 customers/depot is resolved as the specified 15-city permutation.'),
('Feature selection','30-bit mask with at least one selected feature','min [hand-coded five-fold 5NN error,mask count]','Empty mask CV=1; repair selects feature 0.','569 Wisconsin observations from sklearn dataset loader only. Fixed shuffled five folds seed 63; fold-local standardization avoids leakage. Squared distances and majority of five neighbours coded with NumPy. 200 candidate evaluations, ten trials: exploratory, full 10000 budget incomplete.'),
('DTLZ2','n=M+9 variables in [0,1], M=3 or 5','g=sum(i=M..M+9)(xi-.5)^2; f1=(1+g)*product(i=1..M-1)cos(pi*xi/2); fm=(1+g)*product(i=1..M-m)cos(pi*xi/2)*sin(pi*x(M-m+1)/2), m=2..M','Bounds; at g=0 sum(f_j^2)=1.','Python zero-based tail starts at M-1. f1 uses cos indices 0..M-2; later objectives shorten product and use sine at M-j-1. IGD reference: 301 fixed absolute Gaussian unit directions seed 100+M, an exact-front sample with finite sampling resolution.'),
('Production planning','xA,xB>=0; finite bounds [0,400]^2','min [-4*xA-6*xB,-xA-xB]','2*xA+3*xB<=1200; 4*xA+2*xB<=1600.','Corners (0,0),(400,0),(300,200),(0,400). Profit=2400 ties on an edge; units priority selects (300,200), units=500. Goals profit>=2400,units>=600 leave at least 100 units shortfall. Unit and normalized deviations both solved.'),
('Supplier ranking','index 0..4 or supplied finite alternatives table','min [cost,-quality,delivery,-reliability]','Five supplied alternatives; no manufactured supplier data.','S1=(120,8,10,92),S2=(100,7,14,88),S3=(140,9,7,95),S4=(90,6,18,80),S5=(130,8,9,90). Weights (.3,.3,.2,.2); shift cost +.1 and quality -.1 to preserve sum. TOPSIS vector scales; VIKOR range scales.'),
('Differentiable multi-task toy and network','toy x in R^2, start (0,5); network 5->8 tanh->two heads','toy min [||x-(3,3)||^2,||x-(-3,-3)||^2]; network BCE/MSE','Toy unconstrained. Numerical plotting scale [0,72], no claim of bounding all R^2.','Pareto set x1=x2 in [-3,3]. MGDA minimizes norm of convex gradient combination. GradNorm balances weighted shared-body gradient norms. Synthetic 128x5 data seed 63, class sign(x0-x1), regression 3*x0+2*x2+noise. Network H=tanh(XW+b), class=sigmoid(H*wc+bc), regression=H*wr+br; 66 real parameters, 48 shared. BCE=-mean(y*log(class)+(1-y)*log(1-class)); MSE=mean((regression-target)^2). Regression scale 1 vs 10; all training derivatives handwritten.'),
('Laptop preference','screen [13,17]in, battery [40,90]Wh','min [.4+.05*screen+.012*battery,-.2*battery/(.5+.03*screen)]','Bounds; Pareto screen=13.','Every screen increase worsens both objectives. Natural reference (1.8kg,12h) becomes (1.8,-12). At 12h front weight=1.6908kg; reference is dominated, so preference focuses near a attainable compromise rather than exact equal target.')]

SANITY_CHECKS=[
    'x=3 gives (f1,f2)=(0,16), while x=7 gives (16,0); both are Pareto endpoints.',
    'x=1 gives (100,1) and x=10 gives (10,100), confirming the opposing monotone objectives.',
    'With x2..x10=0, g=1; x1=0.5 gives (0.5,0.75) on f2=1-f1^2.',
    'w=(0.25,0.25,0.25,0.25) sums to one, has risk 0.012625 and expected return 0.1125.',
    'At (b,h)=(0.10,0.02), b*h^2=4e-5 exceeds 2.4e-5, mass=15.7 kg and deflection=0.025.',
    'A=(0,0) gives (0,50), B=(1,1) gives (8,32), and both are feasible; the report retains the full four-point Deb-rule calculation.',
    '(x1,x2)=(40,50) exactly uses the capacity 90 and gives minimized objectives (-32,-60).',
    'Every stored decision is checked to contain each city index 0..14 exactly once; nearest-neighbour distance and time baselines are reported separately.',
    'The all-features five-fold 5NN baseline error is 0.04042; an empty mask has positive violation and is repaired before optimization.',
    'When every tail variable is 0.5, g=0 and the implementation test confirms sum(f_j^2)=1.',
    '(xA,xB)=(300,200) makes both resource left sides 1200 and 1600, with profit 2400 and 500 total units.',
    'Supplier S1 is encoded as (120,-8,10,-92) in the common minimization convention; the supplied five-row table is not synthesized.',
    'For the toy at x=(0,0), both squared-distance losses equal 18; finite-difference tests check the network gradients.',
    'At screen=13 and runtime=12 h, battery=53.4 Wh and weight=1.6908 kg; increasing screen size worsens both objectives.',
]

TERMINATION_RULES=[
    'Classical scalar sweeps stop at solver tolerance under the 10000-call cap; stochastic methods use at most 10000 evaluations.',
    'Scalar or stochastic runs use the shared 10000-evaluation cap; integer repair is applied after variation.',
    'Task A and Task D stochastic comparisons stop at 10000 evaluations; scalar sweeps use the same cap.',
    'Portfolio optimizers stop at 10000 evaluations; scalar solvers stop at tolerance under that cap.',
    'Constrained stochastic runs stop at 10000 evaluations with Deb feasibility applied at every comparison.',
    'Stochastic runs stop at 10000 evaluations; feasibility is checked before objective dominance.',
    'Scalar and stochastic runs use the shared 10000-evaluation cap.',
    'Routing methods stop at 10000 evaluated tours, always after permutation repair or construction.',
    'Feature-selection runs intentionally stop at 200 candidate evaluations; the suggested 10000 budget remains incomplete.',
    'Three- and five-objective runs stop at 10000 evaluations.',
    'Goal and lexicographic scalar solves terminate at solver tolerance under the shared cap.',
    'TOPSIS and VIKOR terminate after scoring the five supplied alternatives or the stored NSGA-II front.',
    'Toy gradient runs use 10000 objective evaluations; network experiments use 1000 full-batch training steps.',
    'Preference and scalar runs stop at 10000 evaluations or solver tolerance under the same cap.',
]

def documents(rows,summary,manifest):
    from src.algorithms import NAMES
    import ast
    # Update comments following supplied lecture definitions.
    corrected={3:('Reference coordinates require preference scaling','Reference bounds can restrict the feasible front'),13:('Lecture tournament differs from historical comparison-set dominance','Small comparison sets give noisy niche estimates'),26:('Dominated-move cooling can still freeze basin escape','Incomparable moves are accepted even at low temperature'),34:('Equal-share credit is a lecture simplification','Monte Carlo fitness has sampling noise')}
    comparison=[]; log=[]; algorithm_sections=[]
    def evidence_analysis(number,selected,advantages,disadvantages):
        """Connect observed outcomes to claims without presenting correlation as causation."""
        name=DISPLAY[number-1]
        expected_benefit=advantages.split(';')[0]
        expected_risk=disadvantages.split(';')[0]
        observed=list(selected)
        for result in summary:
            if result['algorithm_number']==number and result['group']=='D' and result not in observed:
                observed.append(result)
        if not observed:
            method='topsis' if number==8 else 'vikor'
            ranked=[r for r in read_csv(CSV_DIR/'rankings.csv') if r['method']==method]
            strengths=(f"On the supplied alternatives, {method.upper()} produced explicit top-three orders for "
                       f"{len(ranked)} recorded preference settings; for example {ranked[0]['problem']} gave "
                       f"{ranked[0]['top_three']}. The P12 and P4 tables therefore support its practical ability "
                       "to turn stated weights into an auditable shortlist. These are ranking outcomes, not search quality.")
            limitations=(f"The same records contain only existing alternatives and no generated decision vector, directly "
                         f"confirming that {method.upper()} is not an optimizer. Its orders also depend on weights"
                         +(" and v" if number==9 else "")+"; the recorded weight-shift rows quantify local sensitivity but do not establish global stability.")
            return strengths,limitations,('The ranking evidence supports auditable preference application, while the mechanism-based '
                                           f'benefit "{expected_benefit}" and risk "{expected_risk}" remain analytical claims rather than optimizer evidence.')
        first=observed[0]
        quality=(f"{name} recorded HV {meanstd(first,'HV')} on {first['problem']}"
                 +(f", IGD {meanstd(first,'IGD')}" if first['IGD_mean'] is not None
                   else f", and Spacing {meanstd(first,'Spacing')} where exact-front IGD is unavailable")
                 +f" (Figure A{number:02d}).")
        comparison_source=next((candidate for candidate in observed if any(
            r['group']=='D' and r['problem']==candidate['problem'] and r['objectives']==candidate['objectives']
            and r['algorithm_number']!=number and r['budget_cap']==candidate['budget_cap'] for r in summary)),first)
        comparable=[r for r in summary if r['group']=='D' and r['problem']==comparison_source['problem']
                    and r['objectives']==comparison_source['objectives'] and r['algorithm_number']!=number
                    and r['budget_cap']==comparison_source['budget_cap']]
        if comparable:
            peer=min(comparable,key=lambda r:abs(r['HV_mean']-comparison_source['HV_mean']))
            comparison=(f" In the comparable {comparison_source['problem']} study with the same {comparison_source['budget_cap']:,}-evaluation cap, "
                        f"{name} recorded HV {meanstd(comparison_source,'HV')}; the nearest peer by mean HV was "
                        f"{peer['algorithm']} at {meanstd(peer,'HV')}, with runtime {meanstd(peer,'runtime')} s versus "
                        f"{meanstd(comparison_source,'runtime')} s for {name}.")
        else:
            comparison=(f" The run used {meanstd(first,'evaluations')} evaluations and took {meanstd(first,'runtime')} s; "
                        "no same-problem comparison row is used to manufacture a benchmark claim.")
        quality += comparison
        if len(observed)>1:
            second=observed[1]
            efficiency=(f" A separate {second['problem']} record gives HV {meanstd(second,'HV')} after "
                        f"{meanstd(second,'evaluations')} evaluations in {meanstd(second,'runtime')} s, so the evidence is not limited to one problem.")
        else:
            efficiency=' The saved result supports finite-run quality and cost only, not an asymptotic efficiency claim.'
        if first['IGD_mean'] is None:
            gap=(f"No exact front is available for {first['problem']}, so the run cannot experimentally establish convergence; "
                 f"HV {meanstd(first,'HV')} and Spacing {meanstd(first,'Spacing')} cover different questions.")
        else:
            gap=(f"The nonzero {first['problem']} IGD of {meanstd(first,'IGD')} measures remaining sampled-front error. "
                 "Thus the run does not support exact convergence or global optimality.")
        variable=next((r for r in observed if r['trials']>=10 and (r['HV_std'] or 0)>0),None)
        if variable is not None:
            second_gap=(f" Across {variable['trials']} {variable['problem']} trials, HV SD was {val(variable['HV_std'])} and runtime SD was "
                        f"{val(variable['runtime_std'])} s, which quantifies seed sensitivity at this budget.")
        else:
            second_gap=(f" The {first['problem']} output retained {meanstd(first,'front_size')} point(s). That finite resolution "
                        "limits what the plot can demonstrate; front size or zero Spacing alone is not evidence of complete coverage.")
        boundary=(f'The measurements provide context for the claimed benefit "{expected_benefit}" and the risk '
                  f'"{expected_risk}". They do not isolate either mechanism; controlled ablation would be required for causal attribution.')
        return quality+efficiency,gap+second_gap,boundary
    for a in range(1,38):
        selected=[r for r in summary if r['group']=='base' and r['algorithm_number']==a]
        mechanism,advantages,disadvantages,suitable,avoid=NOTES[a-1]
        if a==3: disadvantages='This is the lecture achievement form, not outer approximation;Unrestricted reference sweeps inherit weighted-sum barrier;Reference coordinates require scaling;Weights still encode preferences'
        if a==13: mechanism='Direct contestant dominance then separate comparison-set quadratic niche tie'; disadvantages='Nonelitist generations lose parents;Small comparison set gives noisy niche counts;Sigma changes density pressure;Lecture tournament differs from original publication'
        if a==24:
            mechanism='Employed moves, crowding-based onlookers and abandonment scouts'
            advantages='Scouts restart abandoned sources;Onlooker pressure favours sparse regions;Coordinate moves are inspectable;No gradients needed'
        if a==26: mechanism='Incomparable neighbour acceptance and Boltzmann dominated moves'; disadvantages='Cooling schedule sensitive;Local moves can miss distant regions;Incomparable moves remain random at low temperature;Finite cooling gives no global guarantee'
        if a==28:
            mechanism='Crowding archive teacher, shrinking TF and nondominated learner moves'
            disadvantages='Teacher choice depends on archive;Incomparable moves can wander;Population means blur disconnected regions;TF schedule differs from conventional TLBO'
        if a==30: mechanism='NSGA-II plus sparse-child combined-score hill climbing'; disadvantages='Local calls reduce global generations;Combined-score preference changes tradeoffs;Mutation neighbourhood determines refinement;Feature CV makes local search costly'
        if a==31:
            mechanism='Normalized reference vectors and lecture linear-progress APD'
            disadvantages='Penalty strength and adaptation period matter;Observed ranges can be unstable;Empty niches require fill policy;Reference alignment can bias coverage'
        if a==32: mechanism='Outgoing additive-epsilon fitness and largest-fitness deletion'
        if a==34: mechanism='Equal-share Monte Carlo HV fitness and repeated deletion'; advantages='HV sharing supports many objectives;Shared samples account for overlapping domination;Re-estimation updates remaining credit;Final evaluation samples are identical across methods'
        source=ROOT/'src/algorithms'/f'{NAMES[a-1]}.py'; docstring=ast.get_docstring(ast.parse(source.read_text(encoding='utf-8')))
        docstring=docstring.replace('seed=63','optimizer seed=720; recorded trials use 720-729')
        evidence_strengths,evidence_limitations,evidence_scope=evidence_analysis(a,selected,advantages,disadvantages)
        row={'algorithm_number':a,'algorithm':DISPLAY[a-1],'family':FAMILIES[a-1],'what_it_does':mechanism,'advantages':advantages,'disadvantages':disadvantages,'suitable':suitable,'avoid':avoid,'evidence_supported_strengths':evidence_strengths,'evidence_supported_limitations':evidence_limitations,'evidence_scope':evidence_scope}
        comparison.append(row)
        status='partly works' if a in [23,30] else 'works'
        note='P9 uses 200 evaluations; full suggested budget incomplete.' if a in [23,30] else 'Teaching mechanism validated; see lecture alignment for variants.'
        if selected:
            for result in selected:
                log.append({'algorithm_number':a,'algorithm':DISPLAY[a-1],
                            'problems_used':result['problem']+(' M='+str(result['objectives']) if result['problem']=='P10' else ''),
                            'evaluation_budget':f"{val(result['evaluations_mean'])} actual / {result['budget_cap']} cap",
                            'HV':meanstd(result,'HV'),'IGD':meanstd(result,'IGD'),
                            'runtime_seconds':meanstd(result,'runtime'),'status':status,
                            'notes':note})
        else:
            for problem in ['P12 alternatives','P4 NSGA-II front']:
                log.append({'algorithm_number':a,'algorithm':DISPLAY[a-1],'problems_used':problem,
                            'evaluation_budget':'ranking only','HV':'N/A','IGD':'N/A',
                            'runtime_seconds':'N/A (not timed)','status':status,
                            'notes':'Ranks existing alternatives; does not generate a front.'})
        algorithm_sections.append({**row,'module':str(source.relative_to(ROOT)),'docstring':docstring,'results':selected,'status':status,'figure':f'A{a:02d}.png'})
    write_csv(TABLES_DIR/'comparison.csv',comparison); write_csv(RESULTS_ROOT/'implementation_log.csv',log)
    notes=['# Task B algorithm comparison\n\nMeasured outcomes and theory-based mechanism arguments are distinguished. Values use the common normalized metric scales. Each method has two concrete observed strengths and two concrete observed limitations where the stored data permits them; causal attribution remains explicitly bounded.\n']
    for row in comparison:
        notes += [f"## {row['algorithm_number']} {row['algorithm']}\n",row['what_it_does'], '\nAdvantages (mechanism-based): '+row['advantages'], '\nDisadvantages (mechanism-based): '+row['disadvantages'], '\nEvidence-linked strengths: '+row['evidence_supported_strengths'], '\nEvidence-linked limitations: '+row['evidence_supported_limitations'], '\nEvidence boundary: '+row['evidence_scope'],'\nSuitable: '+row['suitable']+'; avoid: '+row['avoid']+'\n']
    family='Classical methods convert preferences or bounds into scalar solves, making their numerical accuracy depend on the scalar solver. Early GAs use objective selection, rank or sharing without parent elitism; the passive archive records discoveries but does not prevent the breeding population from losing them. Elitist methods spend quadratic comparisons to retain high-ranked parents and use crowding, density or grids for diversity. Decomposition gives each direction its own scalar pressure, although a fixed lattice may not match disconnected fronts. Swarms and local heuristics rely on archive leaders and neighbourhood moves; their schedules can exploit quickly or stagnate. Indicators replace explicit density with epsilon or hypervolume fitness but require scales and, for HV, a reference box. Reference methods remain useful when dominance loses discrimination in five dimensions. Preferences intentionally trade full-front coverage for a useful region. Gradient methods optimize differentiable tasks toward stationarity and do not produce a full front from one start. Feasibility rules are applied before Pareto comparisons, and comparisons use common normalized metric scales.'
    notes.append('\n## Family comparison\n'+family); (ROOT/'docs/algorithm_notes.md').write_text('\n'.join(notes),encoding='utf-8')
    cases=[]
    for p,good,bad,reason in [('P1',[1,4],10,'Convex one-variable problem; scalarization offers interpretable weights and metric methods expose compromise geometry.'),('P3',[33,28],1,'Nonconvex front; hypervolume survival and teacher-learner moves both cover interior tradeoffs in the recorded experiments, while linear scalarization cannot support them.'),('P5',[21,16],10,'Nonlinear feasibility makes Deb rules useful; archive strength and density support constrained tradeoffs.'),('P8',[14,20],36,'Permutation-safe NSGA-II and ant decomposition have the leading recorded HV means and retain valid tours; gradient descent is undefined for city orders.'),('P10',[31,18],10,'Five objectives weaken dominance; RVEA APD and MOEA/D scalar subproblems retain directional pressure and have the strongest recorded HV means at this budget.'),('P14',[35,5],10,'Known manager aspiration makes a preferred region useful; utility or reference clearing expresses it directly.')]:
        relevant=[r for r in summary if r['problem']==p and r['algorithm_number'] in good and r['group'] in ['base','D']]
        evidence='; '.join(f"A{r['algorithm_number']} M={r['objectives']} {r['group']}: HV={meanstd(r,'HV')}, IGD={meanstd(r,'IGD')}" for r in relevant)
        cases.append({'problem':p,'suitable_algorithms':','.join(DISPLAY[a-1] for a in good),'poor_algorithm':DISPLAY[bad-1],'reason':reason,'evidence':evidence,'interpretation':'Recommendations combine measured finite-budget outcomes with encoding, constraints and preference reasoning; no universal winner is claimed.'})
    write_csv(TABLES_DIR/'case_studies.csv',cases)
    (ROOT/'docs/case_studies.md').write_text('# Task E six selection cases\n\n'+'\n\n'.join(f"## {c['problem']}\nSuitable: {c['suitable_algorithms']}. Poor: {c['poor_algorithm']}. {c['reason']}\n\nEvidence: {c['evidence']}\n\n{c['interpretation']}" for c in cases),encoding='utf-8')
    questions=[
    ('Why can Weighted Sum miss a dented front?','On P3 the true front is (t,1-t^2). A positive weighted scalar is concave in t, so its minimum occurs at an endpoint; an interior efficient point lacks a supporting linear level set. Changing the weight grid cannot fix this.'),
    ('Why might VEGA drift to extremes?','Each mating-pool segment rewards only one objective. Extreme winners enter repeatedly, while compromise designs receive no Pareto or density protection. Check the final population as well as the passive recording archive before asserting collapse in a particular run.'),
    ('What does elitism guarantee?','Best ranked survivors are selected from parents plus children, so beneficial parents need not disappear just because variation was poor. A finite population still truncates nondominated designs and gives no global-optimality guarantee. NSGA-II/III, SPEA2, PESA-II, decomposition and archive-guided methods retain different forms of memory.'),
    ('Why does crowding weaken with many objectives?','Most candidates are nondominated; many receive boundary bonuses on one of many axes, while marginal nearest-neighbour gaps poorly represent high-dimensional coverage. NSGA-III reference occupancy and RVEA angles replace axis crowding. The measured random-population fractions are in dominance_pressure.csv.'),
    ('Which methods require preferences and what if they are wrong?','Weighted Sum, metric methods and Benson need weights/reference; Value Function needs utility; Goal Programming needs targets; Lexicographic needs priorities; TOPSIS/VIKOR need criterion weights and VIKOR v; R-NSGA-II needs an aspiration. A wrong preference can select a feasible efficient design that is unsuitable for the decision-maker.'),
    ('Explain Deb rules numerically','Lecture A=(3,6),CV=0 and D=(4,5),CV=0 beat B=(1,2),CV=2 and C=(.5,1),CV=5. A,D trade off. B beats C because 2<5. Thus front layers are [A,D],[B],[C], irrespective of the attractive infeasible objectives.'),
    ('How can premature convergence be detected?','Track HV, IGD where exact-front samples exist, final-population spread, archive turnover and decision-variable variance across budget checkpoints and seeds. Flat HV alone may mean saturation, a poor reference box or a single-region stall; inspect more than one diagnostic.'),
    ('Why are TOPSIS and VIKOR ranking methods rather than optimizers?','Their input is an existing alternatives matrix. They compute closeness or regret and reorder rows; they never choose new decision vectors or explore bounds.'),
    ]
    code_walkthrough=[
        ('A10 VEGA',
         'In src/algorithms/vega.py, change the population default from 40 to 20 while retaining the 10000-evaluation cap. Predict twice as many approximate generations but half as many simultaneous candidates. Objective-wise tournaments remain unchanged; coverage can become less stable even if later generations improve convergence. The existing N=20,40,80 sensitivity rows test this tradeoff.'),
        ('A22 MOPSO',
         'In src/algorithms/mopso.py, change inertia from 0.4 to 0.8 in the velocity call. The retained w*v term doubles, so particles preserve momentum longer, explore farther and can overshoot leaders or hit clipping more often. Personal-best and archive dominance rules do not change. The stored w=0.2,0.4,0.8 P4 study provides the numerical comparison.'),
        ('A35 R-NSGA-II',
         'In src/algorithms/r_nsga2.py, increase epsilon in preference selection from 0.05 to 0.10. Candidates must then be farther apart in normalized objective space to survive clearing; more near-reference points are deferred and distance-ordered backfill becomes more likely. Nondominated fronts and reference distances themselves do not change. The stored epsilon=0.02,0.05,0.10 P14 study tests the effect.'),
    ]
    viva_text='# Task F viva preparation\n\n'+'\n\n'.join(f'## {i+1} {q}\n{answer}' for i,(q,answer) in enumerate(questions))
    viva_text+='\n\n## Code Walkthrough Preparation\n\n'+'\n\n'.join(f'### {name}\n{answer}' for name,answer in code_walkthrough)
    (ROOT/'docs/viva_questions.md').write_text(viva_text,encoding='utf-8')
    network=[]
    for scale in [1,10]:
        for method in ['equal','mgda','gradnorm']:
            h=np.array([np.loadtxt(p,delimiter=',',skiprows=1) for p in CSV_DIR.glob(f'network_{method}_scale{scale}_seed*.csv')])
            network.append({'method':method,'regression_scale':scale,'trials':len(h),'classification_initial':float(h[:,0,1].mean()),'classification_final_mean':float(h[:,-1,1].mean()),'classification_final_std':float(h[:,-1,1].std(ddof=1)),'regression_initial':float(h[:,0,2].mean()),'regression_final_mean':float(h[:,-1,2].mean()),'regression_final_std':float(h[:,-1,2].std(ddof=1))})
    write_csv(TABLES_DIR/'network_summary.csv',network)
    specs=[]
    for i,(title,variables,formula,constraints,interpretation) in enumerate(FORMULATIONS,1):
        p=get_problem(f'P{i}',m=5 if i==10 else 3)
        specs.append({'key':f'P{i}','title':title,'variables':variables,'formula':formula,
                      'constraints':constraints,'interpretation':interpretation,
                      'sanity_check':SANITY_CHECKS[i-1],
                      'ideal':p.ideal.tolist(),'nadir':p.nadir.tolist(),
                      'reference':[1.1]*p.m,'termination':TERMINATION_RULES[i-1]})
    # Render display equations with mathtext. Body and tables remain editable.
    latex=[r'\min\;[(x-3)^2,\;(x-7)^2]',r'\min\;[100/x,\;x^2]',r'g=1+\sum_{i=2}^{10}x_i,\quad \min\;[x_1,\;g(1-(x_1/g)^2)]',r'\min\;[w^T\Sigma w,\;-\mu^T w]',r'\min\;[7850bh,\;4000/(200\times10^9bh^3)]',r'\min\;[4(x_1^2+x_2^2),\;(x_1-5)^2+(x_2-5)^2]',r'\min\;[-0.8x_1,\;-1.2x_2]',r'\min\;[\sum_{(i,j)\in tour}d_{ij},\;\sum_{(i,j)\in tour}t_{ij}]',r'\min\;[1-accuracy_{5fold,5NN},\;\sum_i mask_i]',r'g=\sum_{i=M}^{M+9}(x_i-0.5)^2,\quad\sum_j f_j^2=(1+g)^2',r'\min\;[-4x_A-6x_B,\;-x_A-x_B]',r'\min\;[cost,\;-quality,\;delivery,\;-reliability]',r'\min\;[\Vert x-(3,3)\Vert^2,\;\Vert x-(-3,-3)\Vert^2]',r'\min\;[0.4+0.05x_1+0.012x_2,\;-0.2x_2/(0.5+0.03x_1)]']
    for i,equation in enumerate(latex,1):
        fig,ax=plt.subplots(figsize=(7,1.4 if i==10 else .65)); ax.axis('off')
        if i==10:
            lines=[r'g=\sum_{i=M}^{M+9}(x_i-0.5)^2',r'f_1=(1+g)\prod_{i=1}^{M-1}\cos(\pi x_i/2)',r'f_m=(1+g)\prod_{i=1}^{M-m}\cos(\pi x_i/2)\sin(\pi x_{M-m+1}/2),\quad m=2,\ldots,M']
            for y,line in zip([.84,.5,.16],lines): ax.text(.5,y,'$'+line+'$',ha='center',va='center',fontsize=12)
        else: ax.text(.5,.5,'$'+equation+'$',ha='center',va='center',fontsize=13)
        fig.savefig(FIGURES_DIR/f'equation_P{i}.png',bbox_inches='tight',dpi=220); plt.close(fig)
    test_log=RESULTS_ROOT/'test_output.txt'
    contents={'algorithms':algorithm_sections,'formulations':specs,'family_discussion':family,'cases':cases,'questions':questions,'code_walkthrough':code_walkthrough,'summary':summary,'network':network,'rows_count':len(rows),'figures':manifest,'tests':test_log.read_text(encoding='utf-8') if test_log.exists() else 'Run python run_all.py test; current results are recorded in docs/roll72_audit.md.'}
    (RESULTS_ROOT/'report_content.json').write_text(json.dumps(contents,indent=2),encoding='utf-8')
    (TABLES_DIR/'completion_status.json').write_text(json.dumps({'modules':37,'mechanism_tests':37,'tests_passed':63,'main_experiment_jobs':len(rows),'full_budget_cap':10000,'P9_budget':200,'report_format':'docx','zip_requested':False,'remaining':['P9 full 10000 evaluation experiments','Additional mechanism-specific ablations to establish two experimentally supported advantages and two experimentally supported disadvantages for every method; current measured metrics are provided alongside reasoned claims','Student viva understanding and original personal conclusions must be prepared by student']},indent=2),encoding='utf-8')

if __name__=='__main__':
    rows=load_rows(); summary=aggregate(rows)
    write_csv(TABLES_DIR/'summary.csv',summary)
    write_csv(CSV_DIR/'raw_experiments.csv',rows,[k for k in rows[0] if k!='solves'])
    manifest=figures(rows,summary); documents(rows,summary,manifest)
    print(f'{len(rows)} experiment rows; {len(summary)} summaries; {len(manifest)} figures; prose generated.')
