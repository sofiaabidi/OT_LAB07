# Requirements and evidence map

The attached assignment and project instructions are preserved verbatim in this directory.
Roll R=63: ((62)%37)+1=26; ((74)%37)+1=1; ((86)%37)+1=13.

| Requirement | Evidence location | Verification |
|---|---|---|
| Python, permitted dependencies only | requirements.txt; src/ | import audit; NumPy and standard library, SciPy in 1-7 only; sklearn dataset loader only |
| Shared dominance, Deb rules, sorting, crowding, HV, IGD, Spacing, normalization | src/moo_utils.py | tests/test_lab.py Utilities |
| P1-P14 exact objectives and constraints | src/problems/__init__.py | sanity checks; formulations in report |
| P8 seed 7 data and valid tours | data/p8_*.csv; common.py | symmetric matrices and OX/mutation tests |
| P9 hand-coded 5-NN, five folds | src/problems/__init__.py | loader/baseline test; reduced-budget runs explicitly labelled |
| P13 handwritten network | src/problems/network.py | finite-difference tests; network CSVs |
| All 37 separate modules | src/algorithms/ | numbered defining-mechanism tests |
| A: designated problems, fronts and metrics | results/csv/*.npz; summary.csv; figures/ | stored raw decisions/objectives and manifest |
| A: implementation log | results/implementation_log.csv | generated from actual rows |
| B: 4 advantages/disadvantages, evidence | results/tables/comparison.csv; docs/algorithm_notes.md | measured vs reasoned claims distinguished |
| C: MOSA, Weighted Sum, NPGA study cards | docs/study_cards.md | bibliography, formulas, flowcharts, parameters |
| C: two iterations/population 4 or two weights | results/csv/hand_traces.json; tests/test_traces.py | independent analytical assertions |
| C: three sensitivity values x 10 seeds | summary.csv sensitivity rows | counts and raw files |
| D: applicable P3/P5, 10 trials | summary.csv D rows; figures/D_*.png | equal budget caps; actual calls disclosed |
| D: P10 M=5 five methods | summary.csv D rows | normalized HV Monte Carlo and sampled sphere IGD |
| D: P8 four methods and two baselines | routing_baselines.csv; D rows | valid permutations |
| D: ranking input/front and changed weights | rankings.csv; P4_nsga2_ranking_input.csv | TOPSIS/VIKOR tests |
| D: gradient methods vs equal weights | network_*.csv; toy_equal.csv | ten network seeds |
| E: six cases including constraints/many objectives | docs/case_studies.md | references to summary rows |
| F: eight specified + all 37 mechanism questions | docs/viva_questions.md | aligned with actual implementation |
| Editable DOCX, all tasks and real figures | Lab_Assignment_7_Report.docx | rendered page visual QA and text extraction |
| Runnable instructions and code | README.md; run_all.py | tests and manifest audit; ZIP cancelled by user |

## Explicit ambiguities and interpretation decisions

- Five Chapter 5 lecture PDFs were later supplied and audited. Exact car and Deb examples now pass; see lecture_alignment.md. Labelled substitute tests remain as additional independent checks.
- P3 is the specified n=10 formula g=1+sum(x2..x10), which equals the stated ZDT2 factor at n=10. It is retained exactly.
- P6 sanity endpoints are correct; its second constraint is inactive over the whole stated box (minimum expression is 18 > 7.7). This is documented rather than replaced with another benchmark.
- P8 says 15 customers but explicitly encodes a permutation of 15 cities. We use 15 total cities, city 0 as the baseline start. Symmetric traffic uses independent upper-triangle draws after coordinates; this draw order was unspecified and is documented.
- Benson matches the explicit teaching reference-improvement definition in Foundations slide 35. A full polyhedral Benson implementation is outside that lecture definition.
- NSGA-III uses the range normalization explicitly permitted by Bonus 5E slide 5; reference-vector counts are subsampled to population size. These resolution limitations are explicit.
- MOSA uses the lecture acceptance rule: incomparable neighbours always accepted, dominated neighbours face Boltzmann acceptance using summed worsened normalized objectives. Forty parallel chains extend the lecture single-agent illustration.
- MO-TLBO uses TF=2-used/budget, honoring the catalogue's shrinking factor rather than the conventional random integer factor.
- Many-objective HV uses fixed seed 991, 8192 uniform points in [0,1.1]^M; it is an estimate. Samples are identical across methods; reference and normalization are fixed by problem, not by each run.
- Unknown exact fronts P4/P8/P9 are not assigned invented IGD values. P4 ideal risk 0 is a conservative scaling lower bound rather than the attainable ideal; normalizations are shared across every method.
- Output archives for non-elitist methods are passive logs; final populations are saved too. Recording nondominated observations does not grant elitism to VEGA/MOGA/NSGA/NPGA.
- P9 runs use 200 evaluations instead of 10000 due to five-fold pairwise distance computation. This requirement remains incomplete at the full suggested budget; reduced counts are never relabelled.
- Classical solvers share a 10000 cap but terminate naturally; actual calls differ. This is not strict equal-consumed-budget comparison. Deterministic solves repeated across seeds give zero dispersion if identical.
- Academic integrity: this is AI-assisted draft code and writing. The student must understand each line, validate lecturer conventions and produce their own conclusions; the project does not attest authorship or mastery.
