# Roll-72 requirements audit

Student: Sofia Abidi (241071072). Audit updated: 16 October 2026.

Functional correctness means the implementation satisfies its executable checks. Assignment compliance additionally requires the specified methods/problems, valid budgets, independent trials, reproducible provenance, and evidence that supports each written claim.

## Recorded baseline

| Command | Actual result before correction | Meaning |
|---|---|---|
| `python run_all.py test` | Could not start because `python` was absent from PATH | Environment failure, not a test failure |
| Repository-local Python: `run_all.py test` | 59 tests passed in 10.987 s | Existing functional baseline passed |
| Repository-local Python: `run_all.py verify` | Passed its then-current checks: 37 modules, 1,196 main jobs, 90 population jobs, 134 summary groups | Internally consistent, but identity, Task C, seed, and provenance assumptions did not match the current student assignment |

The local Python 3.12 runtime used to execute the repository is ignored by Git.

## Findings and disposition

| Area | Gap found | Affected files | Severity | Correction or remaining action |
|---|---|---|---|---|
| Identity and Task C | Student fields and assigned methods were duplicated and inconsistent | `run_all.py`; experiment/report generators; active docs | Critical | Centralized metadata and formula in `src/project_config.py`; tests assert `(35, 10, 22)` |
| Seed namespaces | Optimizer, problem-data, and metric seeds were conceptually mixed | catalogue, runner, supplementary studies, problems, metrics | High | Optimizers use 720-729; P8 remains 7; P9/network data remain 63; HV remains 991 |
| Result provenance | Aggregation could silently accept incompatible checkpoints | runner, builder, verifier, result layout | Critical | Active paths are isolated; every job records roll/provenance/optimizer seed; verifier rejects mismatches |
| Task A algorithms | Module presence and narrow mechanism tests are weaker than paper-level validation | `src/algorithms/`; `tests/test_lab.py` | High | All 37 mechanisms execute and active evidence was regenerated; no convergence or original-paper equivalence is claimed |
| Task A interface | Classical/ranking modules do not uniformly expose the requested four-function teaching interface | `src/algorithms/*.py` | Medium | Remains a structural compliance gap; a broad speculative rewrite was avoided |
| MOPSO | Incomparable trials could randomly replace personal best; coefficients were fixed | `mopso.py`; trace tests | High | Personal best now changes only on dominance; `c1`/`c2` are configurable; four-particle arithmetic is tested |
| VEGA | Raw violation tuples could let tiny feasible residual differences override the selected objective | `vega.py` | Medium | Uses the shared Deb feasibility threshold before objective comparison |
| R-NSGA-II | The preference reference was not caller-configurable | `r_nsga2.py` | High | Added validated natural-unit or normalized references while preserving defaults |
| Task B | Generic mechanism claims beside metrics do not prove causal advantages/disadvantages | builder; `algorithm_notes.md`; comparison table | Critical | Measured outcomes and reasoned properties are explicitly separated; method-specific ablations remain necessary for full claim-level evidence |
| Task C | Study materials, traces, flows, and sensitivities did not match the computed assignment | study cards, traces, tests, builder, report generator | Critical | Replaced with R-NSGA-II, VEGA, and MOPSO; each has two iterations, four individuals, a flowchart, and three-setting/ten-seed sensitivity evidence |
| Task D | Equal caps were sometimes described as equal consumed budgets | runner; generated discussion | High | Actual evaluation counts are retained and disclosed; all active Task D evidence was regenerated |
| Task E/F | Existing prose could outlive the evidence it cited | builders; case studies; viva material | Medium | Rebuilt from active summaries; student understanding remains outside automated verification |
| P9 | Suggested 10,000-evaluation evidence is impractical in the current five-fold implementation | runner; README; tables | High | Runs remain explicitly capped at 200 and are never relabelled; full-budget compliance is open |
| Dependency policy | Needed confirmation that optimizers do not use external optimization libraries | `requirements.txt`; `src/` | High | Static audit finds SciPy only in methods 1-7 and scikit-learn only in the P9 loader |
| Text encoding | Five generated Markdown/CSV evidence files used the Windows-1252 encoding | evidence builders; generated docs/tables; tests | Medium | Converted the files to UTF-8, made relevant readers/writers explicit, and added a regression test |
| Final report | Report metadata and Task C sections required correction | `docx_report.py`; verifier | High | The approved editable report is `Lab_Assignment_7_Sofia_Abidi_241071072.docx`; verifier checks identity, required sections, XML, and current manifest media without modifying it |

## Current evidence state

- Final `run_all.py test`: 63 tests passed in 8.752 s.
- Final `run_all.py verify`: no errors; 37 modules, 1,196 main jobs, 90
  population-study jobs, 134 summary groups, budgets, stored objectives/metrics,
  figures, and the approved DOCX structure verified.
- 1,196 main experiment jobs, 90 population-study jobs, and 134 summary groups are present under `results/roll72/`.
- Active results use optimizer seeds 720-729 and carry provenance metadata.
- Tables, algorithm notes, six case studies, viva material, 37 algorithm plots, Task D plots, three Task C sensitivity plots, and three Task C flowcharts were regenerated.
- Unknown exact fronts are not given invented IGD values; unavailable panels say why.
- A strict UTF-8 scan passed for all 1,450 active text files; inherited roll-63 reference data was excluded from that active scan.
- Remaining assignment-level gaps are the P9 full budget, universal claim-level Task B ablations, and the non-uniform four-function module interface.

The final editable DOCX exists under its student-specific filename. No submission ZIP is retained.
