# Requirements and evidence map

Student and experiment metadata are centralized in `src/project_config.py`.
For roll suffix 72, the formulas compute `(35, 10, 22)`.

| Requirement | Evidence | Status |
|---|---|---|
| Permitted dependencies | `requirements.txt`; static import audit of `src/` | Compliant: SciPy only in methods 1-7; scikit-learn only loads P9 data |
| Shared MO utilities | `src/moo_utils.py`; utility tests | Implemented and tested |
| P1-P14 objectives and constraints | `src/problems/`; problem tests | Implemented; P6's stated second constraint is inactive and documented |
| P8 seed 7 and valid permutations | `data/p8_*.csv`; operator and result checks | Verified |
| P9 hand-coded five-fold 5-NN | `src/problems/__init__.py`; tests | Functional; experiment budget reduced to 200, so full-budget compliance remains open |
| P13 handwritten network | `src/problems/network.py`; gradient checks | Verified against central finite differences |
| 37 separate methods | `src/algorithms/`; mechanism tests | Functionally covered; tests do not prove paper-level equivalence or convergence |
| Task A designated runs, metrics, and figures | `results/roll72/`; `figures/roll72/A*.png` | 1,196 main jobs complete; active summaries and plots generated |
| Task A implementation log | `results/roll72/implementation_log.csv` | Generated from active rows |
| Task B advantages/disadvantages | `docs/algorithm_notes.md`; `results/roll72/tables/comparison.csv` | Measured outcomes and mechanism reasoning are separated; universal claim-level causal evidence remains partial |
| Task C assignment | `src/project_config.py`; configuration tests | R-NSGA-II (35), VEGA (10), MOPSO (22) computed and asserted |
| Task C study cards and flowcharts | `docs/study_cards.md`; `figures/roll72/flow_A*.png` | Complete for the three assigned methods |
| Task C two iterations with four individuals | `results/roll72/csv/hand_traces.json`; `tests/test_traces.py` | Deterministic arithmetic and selections asserted |
| Task C sensitivities | sensitivity rows in `results/roll72/` | Three settings x ten seeds x three methods complete |
| Task D P3/P5 comparisons | Task D rows and `figures/roll72/D_*.png` | Complete under equal caps; actual evaluation counts disclosed |
| Task D P10, P8, ranking, and gradient studies | active summary/supplementary tables and CSVs | Generated and verified; HV is a common-sample Monte Carlo estimate |
| Task E six cases | `docs/case_studies.md`; `case_studies.csv` | Rebuilt from active summaries |
| Task F viva preparation | `docs/viva_questions.md` | Covers specified and implementation-specific questions; student mastery is not machine-verifiable |
| Editable DOCX | `src/experiments/docx_report.py` | Generator updated; output intentionally deferred |
| Runnable CLI and verification | `run_all.py`; `src/experiments/verify.py` | Test and verify commands are the acceptance checks |

## Interpretation decisions

- P3 uses the stated ten-variable formula.
- P8 uses 15 total cities with city 0 as the baseline start; fixed instance seed 7 is not an optimizer seed.
- Benson follows the supplied teaching reference-improvement definition.
- NSGA-III uses the range normalization permitted by the lecture material.
- MOSA uses the supplied incomparable/dominated acceptance convention.
- MO-TLBO retains the catalogue's shrinking teaching factor.
- Unknown exact fronts P4, P8, and P9 are not assigned fabricated IGD values.
- Non-elitist methods may keep passive output archives; those archives do not affect breeding.
- Classical methods are equal-cap rather than equal-consumed-budget comparisons.
- Academic integrity still requires the student to understand, validate, and present the work in their own words.
