# Lab Assignment 7 Multiobjective Optimization

Educational Python implementations of all 37 catalogue mechanisms with P1-P14, tests, measured results and an editable Word report. Roll suffix 63 assigns MOSA (26), Weighted Sum (1), and NPGA (13). No optimizer libraries are used: NumPy and standard-library search code, permitted SciPy scalar solves for 1-7, sklearn dataset loader only. Five supplied Chapter 5 lecture PDFs were checked; teaching conventions and numerical discrepancies are in `docs/lecture_alignment.md`.

The final requested report is **Lab_Assignment_7_Report.docx**. Paste your GitHub repository URL into its editable field and add your student details. You can export it to PDF yourself. No submission ZIP is generated, as requested. Nothing has been pushed to GitHub.

## Install

Python 3.10 or later:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

On Windows activate with `.venv\Scripts\activate`. Development was tested with Python 3.12. Versions used in the recorded experiment environment are saved in `results/environment.json`. Newer dependency versions can affect exact floating-point last digits; use the recorded versions for close reproduction.

## Structure

- `src/moo_utils.py`: dominance, Deb rules, sorting, crowding, HV, IGD, Spacing and archives.
- `src/problems/`: all 14 assignment definitions, exact P8 data generator, hand-coded five-fold 5NN, NumPy network.
- `src/algorithms/`: 37 separate modules, plus shared variation/bookkeeping.
- `src/experiments/`: checkpoint runner, reports, investigations and verification.
- `tests/`: utility, problem, 37 mechanism, reproducibility, hand-trace and exact lecture tests.
- `results/csv/`: job JSON/NPZ, aggregated raw CSV, traces, rankings and learning curves.
- `results/tables/`: summary, comparison, case studies, completion status and figure provenance.
- `figures/`: real-result plots and mechanism flows.
- `docs/`: original specification, lecture extractions, requirement map, study cards, viva and bibliography.
- `data/`: routing coordinates, distance and traffic matrices.

## Run tests

```bash
python run_all.py test
```

59 tests currently pass. Each of 37 modules has a defining-mechanism test. Stochastic reproducibility tests repeat all 26 population algorithms at identical seeds, check exact budgets and output bounds. Lecture tests reproduce the car front, Deb table, NPGA two rounds, MOSA two iterations and Benson achievement signs. Network gradients pass central finite-difference checks.

## Run one algorithm

```bash
python run_all.py one --algorithm 26 --problem P3 --budget 10000 --seed 630
python run_all.py one --algorithm 13 --problem P5 --budget 10000 --seed 630
python run_all.py one --algorithm 1 --problem P1
python run_all.py one --algorithm 15 --problem P10 --objectives 5
python run_all.py one --algorithm 25 --problem P8
python run_all.py one --algorithm 8 --problem P12
```

Output includes decisions, objectives and evaluation count, or ranking arrays for 8-9. Python API: `load(number).run(get_problem('P3'), budget=10000, seed=630, population=40)`. Parameters are documented in each module. Ant methods require P8; gradient methods require P13; the MODE donor is real-coded; SMS-EMOA here is two-objective.

## Run all experiments

```bash
python run_all.py experiments --workers 4
```

Seeds 630-639, population 40, 10000 candidate calls for stochastic comparisons. Classical methods share a cap but terminate naturally and may use fewer actual calls. P9 deliberately uses 200 calls because five-fold distance computation is costly; these are exploratory reduced-budget experiments. Network uses 1000 full-batch steps at fixed data seed 63 with ten initialization seeds. Evaluation of M-objective quality uses fixed normalization and HV reference 1.1 in every coordinate. MC HV uses 8192 identical points, seed 991; IGD uses 301 exact-front samples. SLSQP default maxiter 120, ftol 1e-10.

An additional P3 study compares populations 20, 40 and 80 at budgets 1000, 5000 and 10000 with ten seeds per condition; its 90 raw jobs are under `results/csv/population/`.

Jobs checkpoint under `results/csv/`. Existing files are reused; selective rerun:

```bash
python -m src.experiments.runner --algorithms 13 26 --force --skip-extras --workers 4
```

The current implementation deliberately caps P9 to 200 even when `--budget 10000` is supplied. To pursue full-budget feature runs, change that explicit P9 cap in `runner.tasks`, clear the affected checkpoints with `--force`, and allow sufficient time. Do not relabel existing reduced runs as 10000 evaluations.

## Regenerate figures tables and Word report

```bash
python run_all.py report
```

This reads the saved raw outputs, generates figures/tables/prose and builds the DOCX. Source fixtures should first be regenerated with `python -m src.experiments.traces` if code changed. The report builder embeds actual plots; editable prose/tables contain no fabricated numbers. Equations are high-resolution display images while code notation remains editable.

The standard `.docx` opens in Word or compatible editors. Update your repository field and export PDF using Word. Renderer scripts used during development are environment-specific QA tools and not needed to regenerate the DOCX itself.

## Verify stored artifacts

```bash
python run_all.py verify
```

Checks 37 modules, designated experiments, ten-trial stochastic groups, per-run budgets, feasible stored fronts, valid tours, aggregate consistency, figures and DOCX ZIP/XML structure. Verification does not certify original-paper equivalence or global optimality.

## Assigned deep dives

- **Weighted Sum:** fixed-scale scalarization and a 21-direction sweep; analytical P1 trace gives x=6 and x=4. Nonconvex P3 geometry explains why more weights cannot recover unsupported points.
- **NPGA:** supplied lecture variant: direct contestant dominance, then quadratic sharing against a separate two-member comparison set. Exact telecom rounds and two full four-member generations are checked.
- **MOSA:** supplied lecture acceptance: incomparable moves always accepted; dominated moves use summed worsened-objective Boltzmann energy. Experiments use forty parallel chains with normalized T0=.1; exact single-chain lecture trace uses raw T0=100.

## Honest status and limitations

All 37 mechanisms are implemented and tested; P9 runs for MOGWO/MOMA remain at 200 evaluations, so their assignment-level status is partly works. Targeted experimental ablations do not yet establish two experimentally supported advantages and two experimentally supported disadvantages for **every** method: the report provides actual quality/runtime measurements and separately labels mechanism-based reasoning. This stricter Task B evidence requirement remains partly satisfied. No global-optimality claims are made. These are teaching variants, and the original NPGA/IBEA/HypE conventions differ from some course slides; all choices are documented.

The final report includes Tasks A-F, not a claim that the student has mastered them. Read the implementations and `docs/viva_questions.md`; rewrite personal conclusions in your own words before submitting, consistent with the assignment's integrity requirement.
