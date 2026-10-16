# Task C study cards — roll suffix 72

The assignment formulas produce Algorithms 35, 10 and 22. These cards describe the implemented teaching variants and do not claim original-paper equivalence.

## 35. R-NSGA-II — Reference Point-Based NSGA-II

Historical context: the supplied Bonus 5E lecture identifies Kalyanmoy Deb, J. Sundar, N. Udaya Bhaskara Rao and Shamik Chaudhuri (2006). The method reduces the cost of approximating an entire front when a decision-maker already knows the preferred region.

Motivation and core principle: retain NSGA-II nondominated fronts, normalize objectives, measure Euclidean distance to a decision-maker reference point, and apply ε-clearing so selected points near that reference do not collapse. If clearing leaves too few survivors, backfill in increasing reference-distance order.

Flow: parents + offspring → Deb nondominated fronts → normalized objectives and reference → splitting-front reference distances → ε-clearing → preferred survivors.

Algorithm steps and equations:

1. Combine parents and offspring and form fronts F₁, F₂, … using Deb feasibility rules before objective dominance.
2. Normalize zᵢⱼ = (fᵢⱼ − idealⱼ)/(nadirⱼ − idealⱼ) using fixed assignment scales. Normalize a natural-unit reference with the same transformation.
3. Compute dᵢ = √[Σⱼ(zᵢⱼ − rⱼ)²].
4. Copy complete fronts. In the splitting front, inspect increasing dᵢ and accept i only when min ‖zᵢ − zq‖ ≥ ε for every already accepted q.
5. Backfill deferred points by increasing reference distance until the population contains N survivors.

Parameters: a wrong reference focuses on an irrelevant region. An ε that is too small permits crowding, whereas an ε that is too large clears useful neighbours and forces distance-only backfilling. Small N gives little preferred-region resolution; large N costs more evaluations per generation. Crossover and mutation control exploration.

Convergence, diversity and constraints: nondominated rank supplies convergence pressure before preference distance is used in the splitting front. ε-clearing supplies local diversity. Deb rules handle constraints. Nondominated sorting can follow nonconvex fronts, but an unreachable reference and finite population can bias coverage. A k-dimensional reference extends beyond three objectives, although distance concentration and ε tuning become harder.

Complexity: pairwise sorting is O(MN²) for M objectives and 2N candidates; reference-distance calculation and straightforward clearing add O(MN²).

Strengths and limitations: the method directs evaluations toward a decision-relevant region while retaining Pareto ranking and explicit local spacing. Its answer depends on reference scaling and ε, and it does not provide uniform whole-front coverage when preference pressure is strong.

Sensitivity evidence: ε = 0.02, 0.05 and 0.10 on P14, using ten independent optimizer seeds 720–729. Raw rows and aggregate statistics are stored under results/roll72/; the sensitivity figure is figures/roll72/C_A35.png.

## 10. VEGA — Vector Evaluated Genetic Algorithm

Historical context: David Schaffer proposed VEGA in 1985. It was an early extension of genetic algorithms to several objectives, but objective-wise selection can duplicate extreme solutions and discard balanced compromises.

Motivation and core principle: evaluate all objectives, allocate equal mating-pool slots to the objectives, select each slot using only its assigned objective, merge and shuffle the subpools, then apply crossover and mutation before nonelitist replacement.

Flow: population → objective-specific tournaments and subpools → merged mating pool → crossover and mutation → nonelitist offspring replacement.

Algorithm steps and equations:

1. Evaluate every objective fⱼ(xᵢ) and the constraint violation of each candidate.
2. For mating slot i, use objective j = i mod M; compare two candidates using Deb feasibility and then scalar value fⱼ when both are feasible.
3. Pool the N winners. Each objective receives equal slots when N is divisible by M.
4. Apply the shared real, binary or permutation-safe crossover and mutation operators appropriate to the problem encoding.
5. Replace the parents with the offspring. The passive output archive records discoveries but does not make the breeding algorithm elitist.

Parameters: small N increases genetic drift; large N improves instantaneous coverage but yields fewer generations under a fixed evaluation budget. Excessive mutation destroys selected structure, whereas insufficient mutation cannot restore lost regions. Strong crossover can mix extremes but provides no diversity guarantee.

Convergence, diversity and constraints: single-objective subpools create pressure toward extremes but provide no explicit Pareto-convergence or diversity pressure. Deb feasibility is used inside every tournament. Search operators can visit nonconvex fronts, but selection does not protect their interior. With many objectives, each subpool becomes small and balanced tradeoffs receive weaker selection pressure.

Complexity: objective-wise selection requires O(N) comparisons after O(MN) evaluation; variation is O(ND) for D variables. The implementation’s passive archive adds pairwise bookkeeping but does not affect parent selection.

Strengths and limitations: VEGA is simple, inexpensive and exposes objective conflicts clearly. Its nonelitist objective partitioning can overrepresent extremes, lose compromises and make final-population coverage unstable.

Sensitivity evidence: population N = 20, 40 and 80 on P3, using ten independent optimizer seeds 720–729. At a fixed budget, this tests simultaneous coverage against the number of generations; see figures/roll72/C_A10.png.

## 22. MOPSO — Multi-Objective Particle Swarm Optimization

Historical context: Carlos A. Coello Coello and Maximino Salazar Lechuga proposed MOPSO in 2002. It extends scalar PSO by replacing one global best with guides selected from an external nondominated archive.

Motivation and core principle: maintain particle positions, velocities and personal bests; retain a nondominated external archive; prefer leaders from sparse archive regions; move toward the personal best and leader; mutate selected particles; and update a personal best only when the new point dominates it.

Flow: particles + archive → crowding-weighted leader → bounded velocity and position update → evaluation and mutation → dominance-based personal best → nondominated archive.

Algorithm steps and equations:

1. Initialize x, set velocity v = 0 and pbest = x, then build the nondominated archive.
2. Select an archive leader using crowding-derived probabilities.
3. Update each coordinate using v′ = wv + c₁r₁(pbest − x) + c₂r₂(leader − x).
4. In the main implementation, clip velocity to 20% of the decision-variable range, set x′ = repair(x + v′), and apply occasional mutation. The separate hand-worked teaching trace explicitly uses fixed limits [−10,10].
5. Replace pbest only if x′ dominates it under Deb rules; merge x′ into the nondominated archive and continue until the evaluation budget is exhausted.

Parameters: small inertia w can stagnate quickly, whereas large w may overshoot and weaken exploitation. Small c₁ underuses personal experience; large c₁ can cause oscillation around pbest. Small c₂ underuses the front; large c₂ can crowd particles around leaders. A small archive loses coverage; an oversized archive increases maintenance cost.

Convergence, diversity and constraints: personal bests and archive leaders supply convergence pressure, while crowding-weighted leader choice and mutation support diversity. Deb dominance handles constraints. The swarm can sample nonconvex fronts because it does not scalarize them, but its continuous velocity model is a poor natural fit for permutations. In many objectives, dominance and crowding lose discrimination and archive maintenance becomes costly.

Complexity: velocity updates cost O(ND); straightforward archive dominance and crowding cost O(MA²) for archive size A, plus problem-evaluation cost.

Strengths and limitations: MOPSO combines memory, an external Pareto archive and gradient-free movement. Performance is sensitive to inertia, acceleration coefficients, velocity limits, mutation and archive-leader pressure.

Sensitivity evidence: inertia w = 0.2, 0.4 and 0.8 on P4, using ten independent optimizer seeds 720–729; see figures/roll72/C_A22.png. IGD is unavailable because P4 has no exact reference front, and the plot states that limitation.
