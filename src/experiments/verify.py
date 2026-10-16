"""Independent consistency checks for submitted code and recorded outputs."""
from pathlib import Path
from collections import defaultdict
import csv,json,zipfile,xml.etree.ElementTree as ET
import numpy as np
from src.algorithms import NAMES
from src.experiments.runner import ROOT,RESULTS_ROOT,CSV_DIR,TABLES_DIR,tasks,job_key,aggregate
from src.experiments.catalogue import DESIGNATED
from src.project_config import ACTIVE_PROVENANCE, OPTIMIZER_SEEDS, ROLL_SUFFIX, STUDENT, TASK_C_ALGORITHMS
from src.problems import get_problem
from src.moo_utils import hypervolume,spacing,igd

def verify():
    problems=[]; counts=defaultdict(int); rows=[]; checked=0
    for name in NAMES: assert (ROOT/'src/algorithms'/f'{name}.py').is_file(),name
    expected={job_key(j) for j in tasks()}
    observed={p.stem for p in CSV_DIR.glob('*.json') if p.name!='hand_traces.json'}
    assert expected==observed,('missing/extra',len(expected-observed),len(observed-expected))
    for path in sorted(CSV_DIR.glob('*.json')):
        if path.name=='hand_traces.json': continue
        row=json.loads(path.read_text(encoding='utf-8'))
        assert row.get('provenance')==ACTIVE_PROVENANCE,path
        assert row.get('roll_suffix')==ROLL_SUFFIX,path
        assert row['seed'] in OPTIMIZER_SEEDS,path
        rows.append(row); counts[(row['algorithm_number'],row['problem'],row['objectives'],row['group'],row['parameters'])]+=1
        raw=np.load(path.with_suffix('.npz')); x,f,c=raw['x'],raw['f'],raw['cv']; p=get_problem(row['problem'],row['objectives'])
        assert row['evaluations']<=row['budget_cap']
        if row['algorithm_number'] in range(10,36): assert row['evaluations']==row['budget_cap']
        assert len(x)==len(f)==len(c)==row['front_size']; assert np.isfinite(f).all(); assert np.all(c<=1e-8)
        if len(x):
            assert np.all(x>=p.lower-1e-8) and np.all(x<=p.upper+1e-8)
            reevaluated,cv=p.evaluate(x)
            np.testing.assert_allclose(reevaluated,f,rtol=1e-10,atol=1e-10)
            if row['problem']=='P8':
                for tour in x: np.testing.assert_array_equal(np.sort(tour),np.arange(15))
        z=p.normalized(f); hv=hypervolume(z,np.full(p.m,1.1)); np.testing.assert_allclose(hv,row['HV'],rtol=1e-12,atol=1e-12)
        np.testing.assert_allclose(spacing(z),row['Spacing'],rtol=1e-12,atol=1e-12)
        if row['IGD'] is not None: np.testing.assert_allclose(igd(z,p.normalized(p.true_front())),row['IGD'],rtol=1e-12,atol=1e-12)
        checked+=1
    for (a,p,m,group,params),n in counts.items():
        if 10<=a<=35 or group in ['D','sensitivity']: assert n==10,(a,p,group,n)
    for a,designated in enumerate(DESIGNATED,1):
        if a in [8,9]: continue
        used={p for (aa,p,m,g,params) in counts if aa==a and g=='base'}
        assert set(designated[:2])<=used,(a,used)
    expected_summary=aggregate(rows)
    with (TABLES_DIR/'summary.csv').open(encoding='utf-8') as f: written=list(csv.DictReader(f))
    assert len(written)==len(expected_summary)
    for a,b in zip(expected_summary,written):
        for metric in ['HV','IGD','Spacing','runtime','front_size','evaluations']:
            for stat in ['mean','std']:
                k=metric+'_'+stat
                if a[k] is None: assert b[k]==''
                else: np.testing.assert_allclose(a[k],float(b[k]),rtol=1e-12)
    content=json.loads((RESULTS_ROOT/'report_content.json').read_text(encoding='utf-8')); assert content['summary']==expected_summary
    assert len(content['algorithms'])==37; assert len(content['formulations'])==14
    for alg in content['algorithms']:
        assert len(alg['advantages'].split(';'))>=4 and len(alg['disadvantages'].split(';'))>=4
        for key in ['evidence_supported_strengths','evidence_supported_limitations']:
            assert len(alg[key].split())>=20,(alg['algorithm_number'],key)
        assert (ROOT/'figures'/ACTIVE_PROVENANCE/alg['figure']).is_file()
    assert len(content['questions'])==8
    assert [name for name,_ in content['code_walkthrough']]==['A10 VEGA','A22 MOPSO','A35 R-NSGA-II']
    with (RESULTS_ROOT/'implementation_log.csv').open(encoding='utf-8') as f:
        log=list(csv.DictReader(f))
    assert {r['algorithm_number'] for r in log}=={str(i) for i in range(1,38)}
    assert all(r['problems_used'] and r['evaluation_budget'] and r['status'] for r in log)
    traces=json.loads((CSV_DIR/'hand_traces.json').read_text(encoding='utf-8'))
    assert traces['metadata']['provenance']==ACTIVE_PROVENANCE
    assert tuple(traces['metadata']['algorithms'])==tuple(number for number,_ in TASK_C_ALGORITHMS)
    for key in ['r_nsga2','vega','mopso']:
        assert len(traces[key])==2,key
        assert all(row['population_size']==4 for row in traces[key]),key
    assert all(np.allclose(row['normalized_reference'],[.25,.25]) for row in traces['r_nsga2'])
    assert all(row['problem_definition']=='independent scalar toy; not assignment P2' for row in traces['mopso'])
    with (TABLES_DIR/'figure_manifest.csv').open(encoding='utf-8') as f:
        for r in csv.DictReader(f): assert (ROOT/'figures'/ACTIVE_PROVENANCE/r['figure']).is_file()
    report=ROOT/'Lab_Assignment_7_Sofia_Abidi_241071072.docx'; report_status='not generated'
    if report.exists():
        with zipfile.ZipFile(report) as z:
            assert z.testzip() is None; xml=ET.fromstring(z.read('word/document.xml'))
            text=' '.join(el.text or '' for el in xml.iter() if el.tag.endswith('}t'))
            assert STUDENT.name in text and STUDENT.registration in text
            assert 'https://github.com/sofiaabidi/OT_LAB07' in text
            assert '[Paste your GitHub repository link here after uploading]' not in text
            assert 'seed=63' not in text
            for token in ['Task C','Task D','Task E','Task F','P14','GradNorm',*[name for _,name in TASK_C_ALGORITHMS]]:
                assert token in text,token
            media=[n for n in z.namelist() if n.startswith('word/media/')]
            assert len(media)>=len(content['figures']),(len(media),len(content['figures']))
        report_status='valid XML and embedded media'
    population=list((CSV_DIR/'population').glob('*.json'))
    assert len(population)==90
    for path in population:
        row=json.loads(path.read_text(encoding='utf-8'))
        assert row.get('provenance')==ACTIVE_PROVENANCE,path
        assert row.get('roll_suffix')==ROLL_SUFFIX,path
        assert row.get('optimizer_seed')==row.get('seed') in OPTIMIZER_SEEDS,path
        raw=np.load(path.with_suffix('.npz')); p=get_problem('P3')
        np.testing.assert_allclose(p.evaluate(raw['x'])[0],raw['f'],rtol=1e-10,atol=1e-10)
        np.testing.assert_allclose(igd(p.normalized(raw['f']),p.normalized(p.true_front())),row['IGD'],rtol=1e-12)
    result={'modules':37,'population_study_jobs_checked':90,'main_jobs_checked':checked,'summary_groups':len(written),'stochastic_trial_counts':'all 10','budgets':'verified','raw_objectives_and_metrics':'recomputed from stored decisions','figures':'exist','docx':report_status,'errors':[]}
    RESULTS_ROOT.mkdir(parents=True,exist_ok=True)
    (RESULTS_ROOT/'verification.json').write_text(json.dumps(result,indent=2),encoding='utf-8'); print(json.dumps(result,indent=2))
if __name__=='__main__': verify()
