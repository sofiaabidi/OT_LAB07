# Lab Assignment 7: Multiobjective Optimization

Educational Python implementations of all 37 catalogue methods and problems P1-P14, configured for **Sofia Abidi** (registration **241071072**, roll suffix **72**), B.Tech Computer Engineering, Veermata Jijabai Technological Institute.

The Task C formulas are evaluated in `src/project_config.py` and select **Algorithm 35 — R-NSGA-II**, **Algorithm 10 — VEGA**, and **Algorithm 22 — MOPSO**. That module is also the source of truth for student metadata, optimizer seeds, fixed problem-data seeds, and Monte Carlo hypervolume settings.

## Install and test

Python 3.10 or later is required.

```bash
python -m venv .venv
.venv\Scripts\activate
python -m pip install -r requirements.txt
python run_all.py test
python run_all.py verify
```

Linux/macOS activation is `source .venv/bin/activate`. The project uses NumPy and hand-written optimization code. SciPy is limited to permitted classical methods 1-7; scikit-learn is used only to load the P9 dataset.

## Repository map

- `src/project_config.py`: identity, Task C computation, seed namespaces, and report metadata.
- `src/problems/`: all 14 problem definitions, P8 routing data, hand-coded P9 five-fold 5-NN, and the NumPy P13 network.
- `src/algorithms/`: 37 separate algorithm modules and shared operators.
- `src/experiments/`: checkpoint runner, traces, evidence builders, report generator, and verifier.
- `results/roll72/`: active job records, arrays, traces, tables, logs, and verification evidence.
- `figures/roll72/`: active result plots, sensitivity plots, and Task C flowcharts.
- `docs/`: specification, lecture extracts, alignment notes, study cards, audit, case studies, and viva material.

## Run one method

```bash
python run_all.py one --algorithm 35 --problem P14 --budget 10000 --seed 720
python run_all.py one --algorithm 10 --problem P3 --budget 10000 --seed 720
python run_all.py one --algorithm 22 --problem P4 --budget 10000 --seed 720
```

The default optimizer seed is 720. Ranking methods 8-9 use the supplier fixture; ant methods require P8; gradient methods require P13; SMS-EMOA is implemented for two objectives.

## Experiments and reproducibility

```bash
python run_all.py experiments --workers 4
```

Independent optimizer trials use seeds **720-729**. Stochastic comparisons use population 40 and a 10,000-evaluation cap. Classical solvers share the cap but may terminate earlier. P9 is explicitly limited to 200 evaluations because its five-fold distance evaluation is expensive; it must not be described as a full-budget run.

Problem construction and measurement randomness are separate from optimizer trials: P8 retains instance seed 7, P9 folds and P13 network data retain fixed seed 63, and Monte Carlo HV uses 8,192 common samples with seed 991. Checkpoints are reused only when their roll and provenance metadata match the active configuration.

The completed active campaign contains 1,196 main jobs, 90 population-study jobs, and 134 summary groups. A selective Task C rerun is:

```bash
python -m src.experiments.runner --algorithms 10 22 35 --force --skip-extras --workers 4
python -m src.experiments.traces
python -m src.experiments.build_deliverables
```

## Evidence and report generation

`python -m src.experiments.build_deliverables` rebuilds tables, figures, algorithm notes, case studies, and viva material from active checkpoints. Task C has two deterministic hand-worked iterations and three-value, ten-seed sensitivity studies for each assigned method.

`python run_all.py report` additionally creates the editable `Lab_Assignment_7_Sofia_Abidi_241071072.docx`. The verifier checks its structure, identity, Task C content, and embedded media when it is present.

## Scope and limitations

The tests establish implemented mechanisms, reproducibility, accounting, constraints, and stored-result consistency; they do not prove global optimality or exact reproduction of every original paper. Task B includes measured quality/runtime evidence plus clearly separated mechanism-based reasoning, but the stronger requirement for two causal, experimentally supported advantages and disadvantages for every one of 37 algorithms would require additional method-specific ablations. P9 full-budget evidence remains incomplete. The student must validate and be able to explain all conclusions before submission.

No submission ZIP is produced and no repository operation is performed by these commands.
