# Task C study cards — roll suffix 72

The assignment formulas produce algorithms 35, 10 and 22. These cards describe
the implemented teaching variants and do not claim original-paper equivalence.

## 35. R-NSGA-II — Reference Point-Based NSGA-II

Historical context: the supplied Bonus 5E lecture identifies Kalyanmoy Deb,
J. Sundar, N. Udaya Bhaskara Rao and Shamik Chaudhuri (2006). It addresses the
cost of approximating an entire front when a decision-maker already knows the
region of interest.

Core idea (five lines): retain NSGA-II nondominated fronts; normalize objectives;
measure Euclidean distance to a decision-maker reference point; use epsilon
clearing so selected points near that reference do not collapse; backfill by
distance if clearing leaves too few survivors.

Flow: parents + offspring → Deb nondominated fronts → normalize objective values
and reference → sort the splitting front by reference distance → epsilon clearing
→ preferred survivors.

Steps and formulas:

1. Combine parents and offspring and form fronts F1, F2, ... using Deb feasibility
   rules before objective dominance.
2. Normalize `z_ij=(f_ij-ideal_j)/(nadir_j-ideal_j)` using the problem's fixed
   assignment scales. Normalize a natural-unit reference in the same way.
3. Compute `d_i=sqrt(sum_j (z_ij-r_j)^2)`.
4. Copy complete fronts. In the splitting front, inspect increasing `d_i` and
   accept i only when `min ||z_i-z_q|| >= epsilon` for already accepted q.
5. Backfill deferred points by reference distance until population size N.

Parameters: a wrong reference focuses on an irrelevant region; epsilon too small
permits crowding, while epsilon too large clears useful neighbours and forces
distance-only backfill. Small N gives little preferred-region resolution; large N
costs more evaluations per generation. Crossover and mutation control exploration.

Properties: convergence comes first from nondominated rank and then preference
distance in the splitting front. Epsilon clearing supplies local diversity.
Deb rules handle constraints. Nondominated sorting can follow nonconvex fronts,
but an unreachable reference and finite population can bias coverage. A k-D
reference works for more than three objectives, although distance concentration
and epsilon tuning become harder.

Cost: pairwise sorting is `O(M N^2)` for M objectives and 2N candidates;
reference distances and clearing add `O(M N^2)` in the straightforward code.

Sensitivity evidence: epsilon = 0.02, 0.05, 0.10 on P14, using ten independent
optimizer seeds 720-729. Raw rows and aggregate statistics are stored under
`results/roll72/`; the sensitivity figure is `figures/roll72/C_A35.png`.

## 10. VEGA — Vector Evaluated Genetic Algorithm

Historical context: David Schaffer proposed VEGA in 1985. It was an early way to
extend a genetic algorithm to several objectives, but objective-wise selection can
duplicate extreme solutions and discard balanced compromises.

Core idea (five lines): evaluate all objectives; allocate equal mating-pool slots
to the objectives; select each slot using one objective only; merge and shuffle the
subpools; apply crossover and mutation and replace the population without elitism.

Flow: population → objective-specific tournaments/subpools → merged mating pool →
crossover and mutation → nonelitist offspring replacement.

Steps and formulas:

1. Evaluate every `f_j(x_i)` and constraint violation.
2. For mating slot i use objective `j=i mod M`; compare two candidates using Deb
   feasibility, then the scalar value `f_j` when both are feasible.
3. Pool the N winners. Each objective receives equal slots when N is divisible by M.
4. Apply the shared real/binary/permutation-safe crossover and mutation operators.
5. The offspring replace the parents; the passive output archive records discoveries
   but does not make the breeding algorithm elitist.

Parameters: small N increases genetic drift; large N improves instantaneous
coverage but yields fewer generations at a fixed evaluation budget. Excessive
mutation destroys selected structure, while too little mutation cannot restore
lost regions. Strong crossover can mix extremes but provides no diversity guarantee.

Properties: single-objective subpools provide convergence pressure toward extremes
but no explicit Pareto convergence or diversity pressure. Deb feasibility is used
inside each tournament. The search operators can visit nonconvex fronts, but
selection does not protect their interior. With many objectives each subpool becomes
small and balanced tradeoffs receive even weaker selection pressure.

Cost: objective-wise selection is `O(N)` comparisons after `O(MN)` evaluation;
variation is `O(ND)` for D variables. The implementation's passive archive adds
pairwise bookkeeping but does not affect parent selection.

Sensitivity evidence: population N = 20, 40, 80 on P3, using ten independent
optimizer seeds 720-729. At a fixed budget this jointly tests coverage versus
number of generations; see `figures/roll72/C_A10.png`.

## 22. MOPSO — Multi-Objective Particle Swarm Optimization

Historical context: Carlos A. Coello Coello and Maximino Salazar Lechuga proposed
MOPSO in 2002. It extends scalar PSO by replacing one global best with guides from
an external nondominated archive.

Core idea (five lines): maintain particle positions, velocities and personal bests;
retain a nondominated external archive; choose leaders with preference for sparse
archive regions; update velocities toward personal best and leader; mutate some
particles and update personal best only when the new point dominates it.

Flow: particles + archive → crowding-weighted leader → velocity and bounded position
update → evaluate/mutate → dominance-based personal best → nondominated archive.

Steps and formulas:

1. Initialize x, set velocity v=0 and pbest=x, and build the archive.
2. Choose an archive leader using crowding-derived probabilities.
3. Update each coordinate:
   `v'=w v + c1 r1 (pbest-x) + c2 r2 (leader-x)`.
4. Clip velocity to 20% of the decision range, set `x'=repair(x+v')`, and apply
   occasional mutation.
5. Replace pbest only if x' dominates it under Deb rules; merge x' into the
   nondominated archive and continue to the evaluation budget.

Parameters: small inertia w can stagnate quickly, while large w overshoots and
weakens exploitation. Small c1 forgets personal experience; large c1 makes particles
oscillate around pbest. Small c2 underuses the front; large c2 crowds particles around
leaders. A small archive loses coverage; an oversized archive increases maintenance.

Properties: pbest and archive leaders supply convergence, while crowding-weighted
leader choice and mutation support diversity. Deb dominance handles constraints.
The swarm can sample nonconvex fronts because it does not scalarize them, but its
continuous velocity model is a poor natural fit for permutations. In many objectives,
dominance and crowding lose discrimination and archive maintenance becomes costly.

Cost: velocity updates cost `O(ND)`; straightforward archive dominance/crowding is
`O(M A^2)` for archive size A, plus problem evaluation cost.

Sensitivity evidence: inertia w = 0.2, 0.4, 0.8 on P4, using ten independent
optimizer seeds 720-729; see `figures/roll72/C_A22.png`. IGD is unavailable for
P4 because no exact reference front is known, so the plot states that limitation.
