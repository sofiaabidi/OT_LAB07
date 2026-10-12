"""Independent consistency checks for submitted code and recorded outputs."""
from pathlib import Path
from collections import defaultdict
import csv,json,zipfile,xml.etree.ElementTree as ET
import numpy as np
from src.algorithms import NAMES
from src.experiments.runner import ROOT,tasks,job_key,aggregate
from src.experiments.catalogue import DESIGNATED
from src.problems import get_problem
from src.moo_utils import hypervolume,spacing,igd

def verify():
    problems=[]; counts=defaultdict(int); rows=[]; checked=0
    for name in NAMES: assert (ROOT/'src/algorithms'/f'{name}.py').is_file(),name
    expected={job_key(j) for j in tasks()}
    observed={p.stem for p in (ROOT/'results/csv').glob('*.json') if p.name!='hand_traces.json'}
    assert expected==observed,('missing/extra',len(expected-observed),len(observed-expected))
    for path in sorted((ROOT/'results/csv').glob('*.json')):
        if path.name=='hand_traces.json': continue
        row=json.loads(path.read_text()); rows.append(row); counts[(row['algorithm_number'],row['problem'],row['objectives'],row['group'],row['parameters'])]+=1
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
    with (ROOT/'results/tables/summary.csv').open() as f: written=list(csv.DictReader(f))
    assert len(written)==len(expected_summary)
    for a,b in zip(expected_summary,written):
        for metric in ['HV','IGD','Spacing','runtime','front_size','evaluations']:
            for stat in ['mean','std']:
                k=metric+'_'+stat
                if a[k] is None: assert b[k]==''
                else: np.testing.assert_allclose(a[k],float(b[k]),rtol=1e-12)
    content=json.loads((ROOT/'docs/report_content.json').read_text()); assert content['summary']==expected_summary
    assert len(content['algorithms'])==37; assert len(content['formulations'])==14
    for alg in content['algorithms']:
        assert len(alg['advantages'].split(';'))>=4 and len(alg['disadvantages'].split(';'))>=4
        assert (ROOT/'figures'/alg['figure']).is_file()
    with (ROOT/'results/tables/figure_manifest.csv').open() as f:
        for r in csv.DictReader(f): assert (ROOT/'figures'/r['figure']).is_file()
    report=ROOT/'Lab_Assignment_7_Report.docx'
    with zipfile.ZipFile(report) as z:
        assert z.testzip() is None; xml=ET.fromstring(z.read('word/document.xml'))
        text=' '.join(el.text or '' for el in xml.iter() if el.tag.endswith('}t'))
        assert 'GitHub repository' in text; assert 'Paste your GitHub repository link here' in text
        for token in ['Task C','Task D','Task E','Task F','P14','NPGA','GradNorm']:
            assert token in text,token
        media=[n for n in z.namelist() if n.startswith('word/media/')]; assert len(media)>=60,len(media)
    population=list((ROOT/'results/csv/population').glob('*.json'))
    assert len(population)==90
    for path in population:
        row=json.loads(path.read_text()); raw=np.load(path.with_suffix('.npz')); p=get_problem('P3')
        np.testing.assert_allclose(p.evaluate(raw['x'])[0],raw['f'],rtol=1e-10,atol=1e-10)
        np.testing.assert_allclose(igd(p.normalized(raw['f']),p.normalized(p.true_front())),row['IGD'],rtol=1e-12)
    result={'modules':37,'population_study_jobs_checked':90,'main_jobs_checked':checked,'summary_groups':len(written),'stochastic_trial_counts':'all 10','budgets':'verified','raw_objectives_and_metrics':'recomputed from stored decisions','figures':'exist','docx':'valid XML and embedded media','errors':[]}
    (ROOT/'results/verification.json').write_text(json.dumps(result,indent=2)); print(json.dumps(result,indent=2))
if __name__=='__main__': verify()
