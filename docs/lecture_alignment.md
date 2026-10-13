# Lecture alignment and resolved inconsistencies

Five supplied PDFs were parsed: Foundations/Classical (53 pages), Non-Elitist (42), Elitist (64), Part 4 (98), Bonus 5E (46). Their extracted text is retained in docs/lectures for reproducibility. The assignment takes precedence for problem constants and submission requirements. Lecture slides define teaching mechanisms; their numerical claims are independently checked.

1. Foundations slide 8 car table: A=(5,15), B=(8,22), C=(6,18), D=(10,25), E=(7,12), F=(9,20), cost minimized/mileage maximized. Correct front A,B,C,D. Exact unit test added.
2. Foundations slide 22 Deb table: A=(3,6),D=(4,5), both feasible; B=(1,2),CV=2; C=(.5,1),CV=5. Correct layers [A,D],[B],[C]. Exact unit test added.
3. Benson Foundations slide 35 is precisely weighted reference achievement with nonnegative deviations. The code matches this teaching definition; it is not the polyhedral outer-approximation algorithm. Its reference and direction weights are expressed in normalized coordinates; natural-unit targets are recovered using the fixed affine scales. This is a declared preference reparameterization. Its nonconvex-region ability requires restrictive reference bounds; sweeping only weights against an unrestricted reference still inherits a weighted-sum limitation.
4. Non-Elitist slide 6 sharing is quadratic, 1-(d/sigma)^2, not linear. MOGA, NSGA and NPGA corrected; associated runs regenerated.
5. NPGA slide 27 compares contestants directly, comparison set used only for niche count. The catalogue and original NPGA literature can suggest comparison-set dominance; we follow the explicit lecture teaching variant. Default comparison_size=2, excluding contestants. Exact two-round telecom example added with fixed lecture scales. Correct arithmetic yields NC=(.59,.78) and (.98,.39), rather than slide-rounded (.590,.778)/(.979,.389); winners remain A,D.
6. Part 4 slide 41 MOSA accepts any neighbour not dominated by the current state; only a dominated neighbour receives exp(-sum positive objective differences/T). Corrected from weighted-energy variant, results regenerated. Experiment version uses 40 parallel chains and normalized T0=.1; lecture example uses one raw-unit chain T0=100. Both are explicit; trace reproduces 100->90->81 and x=10->13->15. Part 4 slide 46 wrongly labels its line f2=5+.5*f1: eliminating x gives f2=20-.5*f1. Objective values are retained.
7. Bonus 5E slide 5 explicitly permits per-objective range normalization for NSGA-III; our normalization matches that teaching simplification. Reference simplex count is subsampled to N=40 if necessary while retaining axes, a documented resolution limit.
8. Bonus 5E slide 8 RVEA uses APD=d*(1+alpha*(t/tmax)*theta/gamma), with fixed alpha=2. Code corrected from the canonical alternative M*(t/tmax)^alpha. Per-generation range normalization and periodic vector adaptation retained; results regenerated.
9. Bonus 5E slide 17 HypE uses equal sample sharing among all dominators. Code corrected from canonical k-order exclusive-removal credits; all runs regenerated. Selection uses 256 samples vs final evaluation 8192; approximation noise is a limitation.
10. Bonus 5E slide 11 IBEA uses outgoing indicator sums and deletes the largest fitness; implemented exactly. This differs from conventional incoming-indicator sums with the smallest fitness deleted. Results regenerated and convention explicit.
11. Foundations slide 37 finite p metric places weights outside absolute deviations raised to p. Code corrected for p=2. The literal p->infinity limit of this finite-p expression loses positive weights; the catalogue explicitly names weighted Tchebycheff, so infinity uses max(w*abs(f-ideal)). This convention discrepancy is recorded instead of silently treating the formulas as identical.
12. Part 4 archive leadership uses crowding; MOGWO, MO-TLBO and MOBA aligned. MOABC onlookers favour crowding; MOMA local moves target sparse children and accept normalized combined objective improvement. Converted minimization means score=sum(old_normalized-new_normalized), with feasibility protected. All changed runs regenerated.
13. Part 4 TLBO's shrinking teaching factor is retained as TF=2-used/budget, as required by the assignment. NSGA uses efficient shared sorting rather than reproducing the historical cubic sorter; its dummy fitness keeps lower fronts below upper fronts after sharing.
14. Bonus 5E MGDA expression O(n*k) contradicts prose saying independent of n; storage/gradient work depends on n. MGDA's convex mixing subproblem depends on task count, but gradients do not. Report uses the correct dependence.
15. Bonus 5E SMS-EMOA total initial HV=9.10 is correct. After the inserted midpoints, L1's exclusive contribution is .15, not .30; ties occur with C1 and C2. The code recomputes contributions from the current population and does not reproduce stale numbers.

The 37 implementations remain educational variants. Exact original-paper equivalence is not claimed. All optimization is hand-coded except permitted scalar SLSQP solves. Lecture default numbers used in hand examples are not necessarily good experimental defaults after normalization.

## Roll-72 Task C alignment

- VEGA follows the Part 2 objective-wise mating-pool mechanism. The code uses
  alternating objective-specific binary tournaments, which gives equal objective
  slot counts when the population is divisible by the objective count. This is
  closer to the slide's proportional-selection description than its simplified
  top-k hand example, but it is still a teaching variant. It is nonelitist; the
  passive result archive must not be described as VEGA survival.
- MOPSO follows the Part 4 velocity equation with configurable `w`, `c1` and `c2`,
  crowding-weighted archive guides and Deb dominance. Personal best is retained
  for incomparable trials, matching the slide's worked example; it changes only
  when the trial dominates it.
- R-NSGA-II follows Bonus 5E's normalized reference distance and epsilon-clearing
  description inside NSGA-II fronts. The caller may provide a natural-unit or
  already-normalized reference. This is the supplied teaching mechanism, not a
  claim of exact reproduction of every detail in the 2006 paper.
