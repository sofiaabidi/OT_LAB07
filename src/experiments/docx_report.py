"""Editable academic DOCX report, created from saved outputs only.

Use python-docx; plots/equation displays are embedded raster figures. Text,
headings, numeric tables, captions and repository placeholder remain editable.
"""
from pathlib import Path
import csv,json,re
from docx import Document
from docx.shared import Inches,Pt,RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT,WD_CELL_VERTICAL_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
ROOT=Path(__file__).resolve().parents[2]

def read_csv(name):
    with (ROOT/name).open() as f: return list(csv.DictReader(f))
def number(value):
    if value is None or str(value) in ('None',''): return 'N/A'
    try: return f'{float(value):.4g}'
    except ValueError: return str(value)
def ms(r,k): return number(r[k+'_mean'])+' +/- '+number(r[k+'_std'])

def generate():
    content=json.loads((ROOT/'docs/report_content.json').read_text()); doc=Document()
    section=doc.sections[0]; section.page_width=Inches(8.27); section.page_height=Inches(11.69)
    section.top_margin=section.bottom_margin=Inches(.7); section.left_margin=section.right_margin=Inches(.75)
    section.header_distance=section.footer_distance=Inches(.3)
    for name in ['Normal','Title','Subtitle','Heading 1','Heading 2','Heading 3','Caption']:
        style=doc.styles[name]; style.font.name='Calibri'; style.font.color.rgb=RGBColor(0,0,0)
    doc.styles['Normal'].font.size=Pt(10.5); doc.styles['Normal'].paragraph_format.line_spacing=1.05; doc.styles['Normal'].paragraph_format.space_after=Pt(6)
    doc.styles['Title'].font.size=Pt(26); doc.styles['Subtitle'].font.size=Pt(13)
    for name,size in [('Heading 1',17),('Heading 2',14),('Heading 3',11)]:
        doc.styles[name].font.size=Pt(size); doc.styles[name].paragraph_format.keep_with_next=True
    doc.styles['Caption'].font.size=Pt(9); doc.styles['Caption'].font.italic=True
    footer=section.footer.paragraphs[0]; footer.alignment=WD_ALIGN_PARAGRAPH.RIGHT
    footer.add_run('Lab Assignment 7 | ')
    field=OxmlElement('w:fldSimple'); field.set(qn('w:instr'),'PAGE'); footer._p.append(field)
    doc.core_properties.title='Lab Assignment 7 Multiobjective Optimization'; doc.core_properties.subject='37 algorithms and Tasks A to F'; doc.core_properties.author=''
    def para(text,bold_label=None):
        p=doc.add_paragraph()
        if bold_label: p.add_run(bold_label+' ').bold=True
        p.add_run(str(text)); return p
    def heading(text,level=1,newpage=False):
        p=doc.add_heading(re.sub(r'[^\w\s]',' ',text),level)
        if newpage: p.paragraph_format.page_break_before=True
    def table(headers,rows,widths=None):
        t=doc.add_table(rows=1,cols=len(headers)); t.alignment=WD_TABLE_ALIGNMENT.CENTER; t.autofit=False
        widths=widths or [6.77/len(headers)]*len(headers)
        for i,w in enumerate(widths): t.columns[i].width=Inches(w)
        for i,text in enumerate(headers): t.rows[0].cells[i].text=str(text)
        for row in rows:
            cells=t.add_row().cells
            for i,value in enumerate(row): cells[i].text=str(value)
        for ri,row in enumerate(t.rows):
            pr=row._tr.get_or_add_trPr(); keep=OxmlElement('w:cantSplit'); pr.append(keep)
            if ri==0: repeat=OxmlElement('w:tblHeader'); pr.append(repeat)
            for ci,cell in enumerate(row.cells):
                cell.width=Inches(widths[ci]); cell.vertical_alignment=WD_CELL_VERTICAL_ALIGNMENT.CENTER
                tcpr=cell._tc.get_or_add_tcPr(); margins=OxmlElement('w:tcMar')
                for side in ['top','left','bottom','right']:
                    el=OxmlElement('w:'+side); el.set(qn('w:w'),'70'); el.set(qn('w:type'),'dxa'); margins.append(el)
                tcpr.append(margins); borders=OxmlElement('w:tcBorders')
                for side in ['top','left','bottom','right']:
                    el=OxmlElement('w:'+side); el.set(qn('w:val'),'single'); el.set(qn('w:sz'),'4'); el.set(qn('w:color'),'D9D9D9'); borders.append(el)
                tcpr.append(borders)
                shade=OxmlElement('w:shd'); shade.set(qn('w:fill'),'DCE6EF' if ri==0 else ('F6F8FA' if ri%2==0 else 'FFFFFF')); tcpr.append(shade)
                for p in cell.paragraphs:
                    p.paragraph_format.space_after=Pt(2); p.paragraph_format.space_before=Pt(2); p.paragraph_format.line_spacing=1.
                    p.alignment=WD_ALIGN_PARAGRAPH.LEFT if ci==0 else WD_ALIGN_PARAGRAPH.CENTER
                    for run in p.runs: run.font.size=Pt(9); run.bold=ri==0
        doc.add_paragraph().paragraph_format.space_after=Pt(3); return t
    def figure(name,caption,width=6.3):
        p=doc.add_paragraph(); p.alignment=WD_ALIGN_PARAGRAPH.CENTER; p.paragraph_format.keep_with_next=True
        p.add_run().add_picture(str(ROOT/'figures'/name),width=Inches(width))
        doc.add_paragraph(caption,style='Caption')
    def markdown(path,exclude_title=False):
        for block in (ROOT/path).read_text().split('\n\n'):
            block=block.strip()
            if not block: continue
            if block.startswith('#'):
                line=block.splitlines()[0]; hashes=len(line)-len(line.lstrip('#'))
                if not (exclude_title and hashes==1): heading(line.lstrip('# ').strip(),min(hashes,3))
                rest='\n'.join(block.splitlines()[1:])
                if rest: para(rest)
            else: para(block)
    # Title page
    doc.add_paragraph('Lab Assignment 7\nMultiobjective Optimization',style='Title')
    doc.add_paragraph('Algorithms tradeoffs and applications',style='Subtitle')
    para('Optimization Techniques Lab | Department of Artificial Intelligence and Data Science | MTech')
    para('Roll number suffix 63 | Assigned deep dives 26 MOSA 1 Weighted Sum 13 NPGA')
    para('Assignment issued 5 October 2026 | Experiments and report prepared 12 October 2026')
    para('Student name and registration number: [Enter details]')
    para('GitHub repository: [Paste your GitHub repository link here after uploading]')
    para('This report presents tested Python implementations of all 37 catalogue mechanisms, their measured tradeoffs on the assignment problems, and the three assigned study cards. It includes Tasks A to F, raw-result references and reproducible commands. The main finding is that selection geometry, constraints and preferences determine useful choices: no algorithm leads across every problem and metric.')
    para('Ten-trial stochastic studies use a 10000-evaluation cap, with P9 feature-selection experiments explicitly reduced to 200. Classical scalar solvers often consume fewer calls. Measured quality is separated from theoretical mechanism claims; some advantages and disadvantages needing direct experimental support still need targeted ablations.')
    heading('Contents',newpage=True)
    titles=['1 Overview and completion status','2 Methodology and reproducibility','3 Problem formulations','4 Shared tools and verification','5 Tasks A and B algorithm implementations and comparison','6 Task C assigned study cards and hand traces','7 Task D head to head comparisons','8 Task E algorithm selection cases','9 Task F viva preparation','10 Findings and limitations','11 Reproducibility and repository instructions','12 References','13 Appendix evidence files and lecture alignment']
    for title in titles: para(title)
    para('All sections and subsections use Word heading styles. Page numbers appear in the footer. Use Word References > Table of Contents to insert or refresh a paginated index after your edits.')
    heading(titles[0],newpage=True)
    para(f"The project has 37 separately named algorithm modules, 37 defining-mechanism tests and 59 passing automated tests in total. The main manifest contains {content['rows_count']} optimizer experiment rows and 60 additional network learning curves. Every front figure is drawn from persisted arrays of decisions, objectives and violations, not mock data.")
    para('Roll assignment calculation: ((63-1) mod 37)+1=26; ((63+11) mod 37)+1=1; ((63+23) mod 37)+1=13.')
    table(['Area','Verified outcome'],[['Implementations','All 37 modules have core-mechanism tests'],['Problem bank','P1 to P14 definitions plus NumPy network'],['Task A','Designated problem runs and figures for all methods'],['Task B','Four reasoned strengths and four risks per method, measured metrics; causal evidence requirement remains partly supported'],['Task C','Three study cards, deterministic traces, three settings x ten trials'],['Task D','P3 P5 P10 M5 P8 comparisons plus ranking and gradient studies'],['Task E','Six cases including constraints and five objectives'],['Task F','Eight required questions and further code walkthrough questions'],['Remaining','P9 at full suggested budget and further mechanism-specific causal ablations']],widths=[1.05,5.72])
    heading(titles[1],newpage=True)
    para('Implementations use NumPy and the standard library. Matplotlib creates plots. SciPy SLSQP is used only in algorithms 1 to 7 for permitted scalar subproblems; scalarization, reference/epsilon sweeps, deviation elimination and priorities are handwritten. Scikit-learn loads only the Wisconsin dataset; five-neighbour classification and five-fold evaluation are handwritten. Neural-network forward and backward passes use NumPy without autograd.')
    para('Stochastic seeds are 630 to 639, ten independent streams. Population and output archive cap are 40 except methods whose archive naturally shrinks. Candidate evaluation budgets include local-search proposals. Objective-vector evaluation counts one candidate irrespective of objective count. Finite-difference solver probes count in classical methods, including objective evaluations invoked by constraints. Reported runtime is wall-clock per job under a six-process experiment pool and should not be treated as a machine-independent algorithm complexity.')
    para('All natural maximization objectives are negated before dominance. Feasible candidates beat infeasible ones; smaller normalized positive constraint residual wins among infeasible candidates. Feasibility threshold is 1e-10, with a 1e-8 numerical verification tolerance on scalar-solver outputs. This prevents roundoff from being confused with a materially infeasible design.')
    para('Quality normalization uses fixed problem constants listed in Section 3. Two-objective HV is an exact staircase area. Higher-dimensional HV uses 8192 identical uniform samples per comparison, seed 991, in [0,1.1]^M. Its absolute Monte Carlo uncertainty is bounded by box_volume/(2*sqrt(8192)), about 0.00735 for M=3 and 0.00890 for M=5; differences smaller than that require cautious interpretation. SD across ten optimizer seeds is distinct from HV sampling error. IGD uses 301 exact-front samples where an analytic front is available; no true-front IGD is invented for P4 P8 or P9. Spacing is the sample SD of nearest L1 distances; a singleton scores zero without offering coverage.')
    para('Early nonelitist algorithms use a passive recording archive for comparable outputs. The final breeding population is saved separately in NPZ files. Thus a good recorded front does not prove that VEGA MOGA NSGA or NPGA preserved its parents. Classical algorithms use a common cap but naturally different consumed counts, so these are equal-cap rather than equal-consumed-budget studies.')
    para('The five supplied lecture decks were checked against the code. The teaching NPGA, MOSA, IBEA, RVEA and HypE conventions are stated in the appendix. Algorithms changed during that check were rerun; current figures and tables use refreshed rows.')
    heading(titles[2],newpage=True)
    for spec in content['formulations']:
        heading(spec['key']+' '+spec['title'],2,newpage=spec['key']!='P1')
        para(spec['variables'],bold_label='Decision variables and encoding')
        figure('equation_'+spec['key']+'.png','Standard form objectives in minimization convention',6.25)
        para(spec['formula'],bold_label='Formula in code notation')
        para(spec['constraints'],bold_label='Constraints and handling')
        para(spec['interpretation'])
        para('Normalized objectives are (F-ideal)/(nadir-ideal). Fixed ideal='+str(spec['ideal'])+'; fixed nadir='+str(spec['nadir'])+'. Quality HV reference='+str(spec['reference'])+' in normalized coordinates. These are declared scaling constants; conservative lower bounds are used where the attainable ideal is unavailable.')
        para(spec['termination'],bold_label='Termination')
        relevant=[r for r in content['summary'] if r['problem']==spec['key'] and r['group']=='base']
        para('Evaluated methods: '+(', '.join(sorted(set(r['algorithm'] for r in relevant))) if relevant else ('TOPSIS and VIKOR on supplier data' if spec['key']=='P12' else 'See supplementary investigations'))+'. See the corresponding Task A pages and raw files.')
        if spec['key']=='P6':
            table(['Point','Decision','f1','f2','Circle lhs','CV'],[['A','(0,0)',0,50,25,0],['B','(1,1)',8,32,17,0],['C','(0,3)',36,29,34,.36],['D','(.2,3)',36.16,27.04,32.04,.2816]])
            para('Manual Deb comparison: A and B are feasible and trade off objectives; both outrank C and D. D outranks C because .2816 < .36. The layers are [A,B], [D], [C]. The second constraint is inactive for all four points; infeasible objective values do not override violation order.')
        if spec['key']=='P9':
            freq=sorted(read_csv('results/csv/feature_frequencies.csv'),key=lambda r:-float(r['front_frequency']))[:10]
            para('Most frequent features in the pooled retained feature-selection fronts are listed below. Frequencies pool the two methods and ten seeds; the reduced budget does not establish globally optimal masks.')
            table(['Feature','Front frequency'],[[r['feature'],number(r['front_frequency'])] for r in freq],widths=[4.8,1.97])
        if spec['key']=='P12': para('All five supplied suppliers are nondominated under cost minimization and quality delivery reliability directions. Ranking imposes an additional preference order on these tradeoffs.')
        if spec['key']=='P8': table(['City','x','y'],[[i,number(x),number(y)] for i,(x,y) in enumerate(json.loads((ROOT/'docs/p8_coords.json').read_text()))],widths=[.7,3.035,3.035])
    heading(titles[3],newpage=True)
    para('moo_utils.py centralizes dominance, pairwise front sorting, crowding distance, archive filtering, normalization, positive-residual violation, exact 2D HV, Monte Carlo HV, IGD, Spacing and reproducible reference directions. Pairwise arrays expose the calculations directly and cost O(M*N^2); vectorization improves execution time without changing asymptotic work.')
    table(['Check','Input','Expected'],[['Dominance','(1,2) versus (2,3)','First dominates'],['Tradeoff','(1,3) versus (2,2)','Neither dominates'],['HV','(1,3) (2,2) (3,1); reference (4,4)','6'],['IGD identical fronts','same point sets','0'],['Crowding','(0,2) (1,1) (2,0)','infinity 2 infinity'],['Lecture car front','A B C D E F table','A B C D'],['Lecture Deb layers','A D feasible; B CV2; C CV5','A,D then B then C'],['DTLZ2 g0','tail variables all .5','squared objective sum 1'],['Network derivatives','central finite difference +/-1e-6','analytical match to 5 decimal places']],widths=[1.3,3.5,1.97])
    para('Final automated result: 59 tests passed. Tests include seed reproducibility for all 26 stochastic modules and bounds for recorded solutions. For P8 the crossover and both mutation variants are checked across 20 seeds; cities occur exactly once. See results/test_output.txt for the named checks. Tests verify defining mechanisms, not a global-optimality guarantee.')
    heading(titles[4],newpage=True)
    para('Each algorithm page combines its Task A implementation and measured results with its Task B comparison. Four strengths and four weaknesses below are reasoned from the code, while the numerical evidence describes what these runs achieved. Metrics alone do not prove every causal mechanism claim; the stricter requirement for two advantages and two disadvantages per method individually supported by experimental results remains only partly met. No unsupported causal conclusion is relabelled as experimental evidence.')
    para(content['family_discussion'])
    for alg in content['algorithms']:
        a=alg['algorithm_number']; heading(f'{a} {alg["algorithm"]}',2,newpage=True)
        para(alg['what_it_does']+'. Module '+alg['module']+'. Status '+alg['status']+'. Defining test test_'+f'{a:02d}'+'_mechanism passes.')
        para(alg['docstring'].replace('Lecture decks supplied on 12 October 2026; teaching variants documented in docs/lecture_alignment.md.','').replace('\n',' '),bold_label='Implementation and defaults')
        if alg['results']:
            table(['Problem','Trials','HV','IGD','Spacing','Time s'],[[r['problem']+(' M'+str(r['objectives']) if r['problem']=='P10' else ''),r['trials'],ms(r,'HV'),ms(r,'IGD'),ms(r,'Spacing'),ms(r,'runtime')] for r in alg['results']],widths=[.8,.45,1.35,1.35,1.35,1.47])
            para('Actual mean evaluations: '+'; '.join(r['problem']+' '+number(r['evaluations_mean'])+' of cap '+str(r['budget_cap']) for r in alg['results'])+'.')
        para('; '.join(f'{i+1}. {x}' for i,x in enumerate(alg['advantages'].split(';'))),bold_label='Advantages with mechanism reasoning')
        para('; '.join(f'{i+1}. {x}' for i,x in enumerate(alg['disadvantages'].split(';'))),bold_label='Disadvantages with mechanism reasoning')
        para(alg['suitable']+'. Avoid: '+alg['avoid']+'.',bold_label='Suitable use')
        para(alg['measured_limitations'],bold_label='Measured limits')
        if a in [8,9]: para(alg['measured_evidence'],bold_label='Measured rankings')
        figure(alg['figure'],f'Figure A{a:02d} Recorded output on designated problems. Plotted seed and actual calls appear in the panel. The full ten-trial metrics are in the table.',6.25)
    heading(titles[5],newpage=True)
    markdown(Path('docs/study_cards.md'),exclude_title=True)
    for a in [26,1,13]:
        heading(f'Flow diagram A{a} {content["algorithms"][a-1]["algorithm"]}',3)
        figure(f'flow_A{a:02d}.png',f'Figure C{a} Current implementation control flow',5.6)
    traces=json.loads((ROOT/'results/csv/hand_traces.json').read_text())
    heading('Weighted Sum two settings',2,newpage=True)
    table(['w1','w2','x','f1','f2','Scalar'],[[r['w'][0],r['w'][1],r['x'],r['objectives'][0],r['objectives'][1],r['raw_scalar']] for r in traces['weighted_sum']])
    para('Stationarity gives 2*w*(x-3)+2*(1-w)*(x-7)=0, hence x=7-4*w; second derivative=2. Both solutions satisfy [1,10] and lie in the Pareto set [3,7]. No random choices enter this trace.')
    heading('MOSA lecture and population four trace',2,newpage=True)
    table(['Step','Current x','Next x','Current F','Next F','T next','Rule'],[[1,10,13,'(20,10)','(17,11.5)',90,'incomparable accept'],[2,13,15,'(17,11.5)','(15,12.5)',81,'incomparable accept']],widths=[.4,.65,.65,1.1,1.1,.7,2.17])
    para('Raw-unit dominated example (20,10)->(23,12): deltaE=3+2=5; p=exp(-5/100)=0.951229. At T=1, p=0.006738. The displayed lecture curve is corrected to f2=20-.5*f1.')
    for r in traces['mosa']:
        heading('Population iteration '+str(r['iteration']),3)
        para('T='+number(r['T'])+'. The draws and proposals are fixed. Normalized objectives use division by 16; no preference weights enter acceptance.')
        table(['Chain','x','Proposal','Old norm F','New norm F','Delta positive','p','u','Accept'],[[i,number(r['x'][i]),number(r['proposal'][i]),','.join(number(x) for x in r['normalized_old'][i]),','.join(number(x) for x in r['normalized_new'][i]),number(r['worsened_sum'][i]),number(r['probability'][i]),r['uniform'][i],str(r['accepted'][i])] for i in range(4)],widths=[.4,.45,.6,1.1,1.1,.85,.6,.5,.67])
        para('Next population '+str(r['next_x'])+'. All proposals are recorded by the passive Pareto archive, independently of chain acceptance.')
    heading('NPGA exact lecture tournament rounds',2,newpage=True)
    table(['Topology','Cost','Reliability','Normalized cost','Normalized reliability'],[['A',10,.80,0,0],['B',15,.90,.5,.5],['C',12,.85,.2,.25],['D',18,.95,.8,.75]],widths=[.65,.8,.9,2.21,2.21])
    table(['Round','Candidates','Comparison','Niche counts exact','Winner'],[[1,'A versus B','C D','.59 versus .78','A'],[2,'C versus D','A B','.98 versus .39','D']],widths=[.55,1.25,1.1,2.67,1.2])
    para('Sharing sigma=.5 and sh(d)=max(0,1-(d/.5)^2). Distances A-C=.320156, A-D=1.096586, B-C=B-D=.390512. Shares are .59,0,.39,.39. The two contestants trade cost against reliability, so direct dominance does not decide. Exact counts differ slightly from slide-rounded figures but give identical winners.')
    heading('NPGA two complete population four generations',2,newpage=True)
    for r in traces['npga']:
        heading('Generation '+str(r['iteration']),3,newpage=r['iteration']>1)
        table(['Member','x','f1','f2','Norm f1','Norm f2'],[[i,number(r['population'][i]),number(r['F'][i][0]),number(r['F'][i][1]),number(r['normalized_F'][i][0]),number(r['normalized_F'][i][1])] for i in range(4)])
        para('All distances and quadratic sharing terms follow. Sigma=.8; normalization is recomputed from the four current objective rows. Pair-specific comparison sets exclude contestants.')
        table(['Distance','0','1','2','3'],[[i,*[number(x) for x in r['distances'][i]]] for i in range(4)])
        table(['Share','0','1','2','3'],[[i,*[number(x) for x in r['sharing'][i]]] for i in range(4)])
        table(['Pair','Compare set','NC first','NC second','Winner','Parent x','Normal z','Increment','Child x'],[[str(pair),str(C),number(sum(r['sharing'][pair[0]][j] for j in C)),number(sum(r['sharing'][pair[1]][j] for j in C)),winner,number(r['population'][winner]),number(z),number(inc),number(child)] for pair,C,winner,z,inc,child in zip(r['pairs'],r['comparison_sets'],r['winners'],r['mutation_z'],r['increments'],r['offspring'])],widths=[.8,.9,.6,.6,.5,.7,.7,.7,1.27])
        para('Direct dominance decides pair (0,3) in generation 2: member 0 has equal f1 and smaller f2. Every other listed pair is incomparable, so its comparison-set niche totals determine the winner. Equal totals select the first contestant.')
        para('SBX u=.5 and positive beta sign imply beta=1, so each child copies its selected first parent; coordinate mutation adds .1*9*z=.9*z. Bounds are clipped to [1,10]. Offspring objectives '+str(r['offspring_F'])+'. This offspring becomes the entire next nonelitist population.')
    heading('Ten trial sensitivity studies',2,newpage=True)
    for a in [26,1,13]:
        selected=[r for r in content['summary'] if r['group']=='sensitivity' and r['algorithm_number']==a]
        heading(content['algorithms'][a-1]['algorithm'],3)
        table(['Setting','Trials','HV','IGD','Spacing','Calls'],[[r['parameters'],r['trials'],ms(r,'HV'),ms(r,'IGD'),ms(r,'Spacing'),number(r['evaluations_mean'])] for r in selected],widths=[1.6,.45,1.2,1.2,1.2,1.12])
        best=max(selected,key=lambda r:r['HV_mean']); worst=min(selected,key=lambda r:r['HV_mean'])
        para('Largest mean HV occurred at '+best['parameters']+' ('+ms(best,'HV')+'); smallest at '+worst['parameters']+' ('+ms(worst,'HV')+'). These three settings and ten trials provide a finite comparison, not an optimum parameter search. Overlapping uncertainty requires caution.'+(' More scalar settings change consumed evaluations and cannot remove the P3 supporting-hyperplane barrier.' if a==1 else ''))
        figure(f'C_A{a:02d}.png',f'Figure S{a} Sensitivity metrics with sample SD across ten seeds',6.25)
    heading(titles[6],newpage=True)
    para('The continuous comparison includes 25 applicable two-objective optimizer mechanisms. Ranking methods are evaluated separately; ant construction requires tours, gradient methods require differentiability, and many-objective-specific methods are compared on P10. Algorithms 5 to 7 retain their designated utility goals and priorities rather than receiving invented P3/P5 goals. Algorithms 1 to 4 use at least 21 sweep settings, with metric p variants combined.')
    for p,m in [('P3',2),('P5',2),('P10',5),('P8',2)]:
        heading(p+' comparison',2,newpage=True)
        selected=sorted([r for r in content['summary'] if r['group']=='D' and r['problem']==p and r['objectives']==m],key=lambda r:-r['HV_mean'])
        table(['Rank','Algorithm','HV','IGD','Spacing','Runtime s'],[[i+1,r['algorithm'],ms(r,'HV'),ms(r,'IGD'),ms(r,'Spacing'),ms(r,'runtime')] for i,r in enumerate(selected)],widths=[.4,1.7,1.15,1.15,1.15,1.22])
        best=selected[0]; low=selected[-1]
        para('Ranked by mean HV: '+best['algorithm']+' leads at '+ms(best,'HV')+', compared with '+low['algorithm']+' at '+ms(low,'HV')+'. HV and IGD judge different aspects; this ranking is specific to the fixed scales and reference. All rows have ten trials. '+('Classical actual calls differ despite the common 10000 cap; see raw_experiments.csv.' if p in ['P3','P5'] else 'All candidate budgets are 10000.'))
        figure('D_'+p+'.png','Figure D'+p+' Combined seed 630 results. For five objectives the overlaid parallel-coordinate lines show every recorded front vector; this projection is descriptive rather than a dominance ordering.',6.25)
        if p=='P10':
            pressure=read_csv('results/csv/dominance_pressure.csv')
            for M in [3,5]:
                z=[float(r['nondominated_fraction']) for r in pressure if int(r['M'])==M]; para('M='+str(M)+' random population nondominated fraction mean='+number(sum(z)/len(z))+'. Increasing nondomination reduces rank discrimination, while vector association adds a directional criterion.')
        if p=='P8':
            bases=read_csv('results/csv/routing_baselines.csv'); table(['Nearest neighbour','Distance','Time','Tour'],[[r['baseline'],number(r['distance']),number(r['time']),r['tour']] for r in bases],widths=[1.1,.9,.9,3.87])
            para('Distance/time baselines use different edge metrics and retain valid 15-city permutations. A good optimized archive can improve one objective while worsening the other, so neither baseline should be assumed to dominate the entire tradeoff set.')
    heading('P3 population and generation budget investigation',2,newpage=True)
    population=read_csv('results/tables/population_study_summary.csv')
    table(['Population','Budget','Full generations','HV','IGD','Spacing'],[[r['population'],r['budget'],r['full_generations'],ms(r,'HV'),ms(r,'IGD'),ms(r,'Spacing')] for r in population],widths=[.75,.7,1.1,1.4,1.4,1.42])
    para('This additional NSGA-II study uses ten seeds for each of nine population and budget settings. At fixed budget, larger populations receive fewer generations; improving population coverage can compete with convergence. More evaluations generally allow more refinement, but the measured IGD values determine the conclusion for each setting rather than an assumed universal trend. Ninety raw fronts and objective metrics are stored under results/csv/population/.')
    heading('Ranking existing alternatives and preferred scalar solutions',2,newpage=True)
    rankings=read_csv('results/csv/rankings.csv')
    table(['Input','Method','Weights','v','Top three'],[[r['problem'],r['method'],r['weights'],r['v'],r['top_three']] for r in rankings],widths=[1.2,.7,1.5,.4,2.97])
    para('P12 supplier identifiers are 1-based. P4 front identifiers are 0-based rows in P4_nsga2_ranking_input.csv. Moving .1 weight to the first criterion and subtracting .1 from the second preserves the simplex. VIKOR v=.25,.5,.75 and its compromise-set flags remain in rankings.csv.')
    for method in ['topsis','vikor']:
        subset=[r for r in rankings if r['problem']=='P12' and r['method']==method and float(r['v'])==.5]
        para(method.upper()+' top-three order '+('changes' if subset[0]['top_three']!=subset[1]['top_three'] else 'is unchanged')+' under the .1 weight shift: '+subset[0]['top_three']+' -> '+subset[1]['top_three']+'. This measured local response is not universal preference stability.')
    para('Value Function returns declared portfolio profiles or the laptop aspiration. Goal Programming uses production targets 2400 profit and 600 units, and normalized versus unit deviations. Lexicographic profit-first then units selects the profit tie with maximum units, approximately (300,200). Exact decisions and solver success messages are retained in the classical job JSON records; a solver failure is not silently treated as proof of optimality.')
    heading('P13 gradient methods and equal weights',2,newpage=True)
    table(['Method','Scale','BCE initial','BCE final','MSE initial','MSE final'],[[r['method'],r['regression_scale'],number(r['classification_initial']),number(r['classification_final_mean'])+' +/- '+number(r['classification_final_std']),number(r['regression_initial']),number(r['regression_final_mean'])+' +/- '+number(r['regression_final_std'])] for r in content['network']],widths=[.85,.45,1.1,1.65,1.1,1.62])
    para('The network has a five-input shared tanh layer of width eight and separate classification and regression heads. Ten seeds vary initialization while synthetic observations remain fixed. Regression target scale 10 creates larger gradient norms. Equal weights and MGDA sum to one; GradNorm weights sum to two by definition. Their model learning rates are explicitly recorded, so weight normalization changes effective step size and must be considered when interpreting loss differences.')
    for scale in [1,10]: figure(f'network_scale{scale}.png',f'Figure N{scale} Network task losses with mean and SD from ten initializations',6.25)
    para('On the toy, fixed equal weights converge to (0,0), while MGDA generally stops at a different Pareto-stationary point and GradNorm changes the task weighting. Individual losses need not both approach zero: the two target points conflict. The saved 10000-step histories and toy_equal.csv expose this trajectory rather than claiming full-front coverage from one initial point.')
    heading('Toy task losses against equal weights',2,newpage=True)
    figure('toy_comparison.png','Figure T13 Hand-coded toy loss trajectories against fixed equal weights, with identical starting point and learning rate',6.25)
    para('The equal-weight toy baseline tends to x=(0,0), giving losses (18,18). MGDA tends to a different point on the Pareto segment, while GradNorm adapts its loss weights. A smaller task 1 loss can coexist with a larger task 2 loss at a Pareto-stationary tradeoff; neither method is expected to make both target distances zero.')
    heading(titles[7],newpage=True)
    for c in content['cases']:
        heading(c['problem'],2); para('Suitable: '+c['suitable_algorithms']+'. Poor choice: '+c['poor_algorithm']+'. '+c['reason']); para(c['evidence']); para(c['interpretation'])
    heading(titles[8],newpage=True)
    for i,(q,answer) in enumerate(content['questions']):
        heading(str(i+1)+' '+q,3); para(answer)
    heading(titles[9],newpage=True)
    para('The numerical comparison shows meaningful differences in convergence, coverage and computation across methods, but finite outputs do not establish global optima. Weighted Sum on P3 illustrates a structural unsupported-region limit. Many-objective methods preserve directional niches when ranks tie. Routing methods require valid edge/tour operations. Preference and gradient methods should be judged by their declared decision or learning task rather than by full-front HV alone.')
    para('Remaining work is explicit: P9 uses 200 evaluations per run rather than the suggested 10000, and its smallest observed feature set is an exploratory result. The Task B table contains four argued advantages and disadvantages plus traceable measured metrics, but targeted ablations do not yet establish two experiment-supported benefits and drawbacks for every method. This report does not claim that stricter evidence requirement is fully satisfied. Student explanation and personal conclusions remain necessary for the viva.')
    investigations=read_csv('results/csv/problem_investigations.csv'); table(['Problem','Investigation','Measured value','Interpretation'],[[r['problem'],r['investigation'],number(r['value']),r['notes']] for r in investigations],widths=[.55,2.15,.9,3.17])
    para('Additional limitations: fixed population 40 limits front resolution; sparse grids and reference lattices can bias irregular fronts; Monte Carlo selection noise is larger than final HV evaluation noise; runtimes measured in a process pool are environment specific; IGD depends on reference sample density; exact fronts for P4 P8 P9 remain unknown here. The shared output archive can mask nonelitist final-population losses, so saved final_f is essential for diagnosing collapse.')
    heading(titles[10],newpage=True)
    para('Keep src tests results figures docs and data together. From the project root create a Python 3.10+ virtual environment, install requirements.txt, run python -m unittest discover -s tests -v, and execute python run_all.py experiments --workers 4. Jobs checkpoint per algorithm/problem/seed; an existing JSON row is reused unless --force is requested. Use python run_all.py report to rebuild figures and the Word document from saved arrays.')
    para('GitHub repository: [Paste your GitHub repository link here after uploading]. No GitHub credentials or publication actions were used. The README gives individual algorithm commands and selective reruns. No submission ZIP is required, as requested. You can edit this DOCX and export it to PDF in Word after inserting your details and repository link.')
    heading(titles[11],newpage=True); markdown(Path('docs/references.md'),exclude_title=True)
    heading(titles[12],newpage=True)
    table(['Evidence','Location'],[['Raw fronts and decisions','results/csv/job_name.npz'],['Job metrics and scalar solver messages','results/csv/job_name.json'],['All raw experiment rows','results/csv/raw_experiments.csv'],['Mean and sample SD tables','results/tables/summary.csv'],['37 method comparison','results/tables/comparison.csv'],['Implementation log','results/implementation_log.csv'],['Deterministic full traces','results/csv/hand_traces.json'],['Feature frequencies','results/csv/feature_frequencies.csv'],['Network loss histories','results/csv/network_method_scale_seed.csv'],['Figure provenance','results/tables/figure_manifest.csv'],['Tests','results/test_output.txt'],['Requirement map','docs/requirements_checklist.md']],widths=[2.6,4.17])
    markdown(Path('docs/lecture_alignment.md'),exclude_title=True)
    heading('Consolidated Task B comparison table',2,newpage=True)
    para('This table provides the required six comparison fields for all 37 methods. Advantages and disadvantages are numbered mechanism-based arguments; the detailed method pages provide measured metrics and recorded limitations. The remaining experimental evidence gap remains explicit in Sections 1 and 10.')
    table(['Algorithm','Main mechanism','Four advantages','Four disadvantages','Suitable','Avoid'],[[str(a['algorithm_number'])+' '+a['algorithm'],a['what_it_does'],'; '.join(str(i+1)+'. '+x for i,x in enumerate(a['advantages'].split(';'))),'; '.join(str(i+1)+'. '+x for i,x in enumerate(a['disadvantages'].split(';'))),a['suitable'],a['avoid']] for a in content['algorithms']],widths=[.95,1.1,1.5,1.5,.86,.86])
    # python-docx's bundled template can carry paragraph borders; strip them.
    for tree in [doc._element,doc.styles.element]:
        for border in list(tree.iter(qn('w:pBdr'))): border.getparent().remove(border)
    doc.save(ROOT/'Lab_Assignment_7_Report.docx')
    print('Saved editable report')
if __name__=='__main__': generate()
