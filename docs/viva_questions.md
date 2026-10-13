# Task F viva preparation

## 1 Why can Weighted Sum miss a dented front?
On P3 the true front is (t,1-t^2). A positive weighted scalar is concave in t, so its minimum occurs at an endpoint; an interior efficient point lacks a supporting linear level set. Changing the weight grid cannot fix this.

## 2 Why might VEGA drift to extremes?
Each mating-pool segment rewards only one objective. Extreme winners enter repeatedly, while compromise designs receive no Pareto or density protection. Check the final population as well as the passive recording archive before asserting collapse in a particular run.

## 3 What does elitism guarantee?
Best ranked survivors are selected from parents plus children, so beneficial parents need not disappear just because variation was poor. A finite population still truncates nondominated designs and gives no global-optimality guarantee. NSGA-II/III, SPEA2, PESA-II, decomposition and archive-guided methods retain different forms of memory.

## 4 Why does crowding weaken with many objectives?
Most candidates are nondominated; many receive boundary bonuses on one of many axes, while marginal nearest-neighbour gaps poorly represent high-dimensional coverage. NSGA-III reference occupancy and RVEA angles replace axis crowding. The measured random-population fractions are in dominance_pressure.csv.

## 5 Which methods require preferences and what if they are wrong?
Weighted Sum, metric methods and Benson need weights/reference; Value Function needs utility; Goal Programming needs targets; Lexicographic needs priorities; TOPSIS/VIKOR need criterion weights and VIKOR v; R-NSGA-II needs an aspiration. A wrong preference can select a feasible efficient design that is unsuitable for the decision-maker.

## 6 Explain Deb rules numerically
Lecture A=(3,6),CV=0 and D=(4,5),CV=0 beat B=(1,2),CV=2 and C=(.5,1),CV=5. A,D trade off. B beats C because 2<5. Thus front layers are [A,D],[B],[C], irrespective of the attractive infeasible objectives.

## 7 How can premature convergence be detected?
Track HV, IGD where exact-front samples exist, final-population spread, archive turnover and decision-variable variance across budget checkpoints and seeds. Flat HV alone may mean saturation, a poor reference box or a single-region stall; inspect more than one diagnostic.

## 8 Why are TOPSIS and VIKOR ranking methods rather than optimizers?
Their input is an existing alternatives matrix. They compute closeness or regret and reorder rows; they never choose new decision vectors or explore bounds.

## 9 What do HV IGD and Spacing measure?
HV is dominated volume within one fixed reference; for (1,3),(2,2),(3,1) and r=(4,4), HV=6. IGD averages true-front sample distance to the approximation. Spacing is sample SD of nearest L1 distances. A singleton has Spacing=0 but poor coverage. Normalize using the same constants across algorithms.

## 10 Why keep decisions as well as objective arrays?
Objectives rank tradeoffs, while decisions verify bounds, repair, feature masks and tours. NPZ files retain both and constraint residuals. Dense pairwise arrays permit vectorized dominance at O(M*N^2) storage/work; they do not remove quadratic complexity.

## 11 What does the hand trace prove?
R-NSGA-II reproduces reference-distance ordering and epsilon clearing, VEGA reproduces two objective-wise selections, and MOPSO reproduces two velocity/position updates with retained incomparable personal bests. These are mechanism checks, not proofs of global convergence.

## 12 How does changing a parameter affect behaviour?
Larger R-NSGA-II epsilon clears a wider preferred neighbourhood; VEGA population changes instantaneous coverage versus generations at fixed budget; larger MOPSO inertia preserves momentum and may overshoot. Inspect the three-value, ten-trial sensitivity rows before claiming numerical improvement.

## 13 Why does MGDA sometimes stop while task gradients remain nonzero?
At Pareto stationarity the minimum-norm convex combination is zero; individual gradients may oppose one another. For [1,0] and [-1,0], weights .5,.5 cancel. GradNorm instead controls magnitudes and need not choose a common descent direction.

## 14 How is network correctness verified?
Forward and backward BCE/MSE derivatives are handwritten. Tests perturb shared weights, biases and both heads by +/-1e-6 and compare finite differences to analytical task gradients. Standardization in feature selection is fitted only to training observations.

## 15 Explain A1 Weighted Sum and predict one change
Linear scalar solve and a sweep. Weighted Sum: minimize dot(w,F_normalized), sweep simplex weights.
Positive weights yield supported efficient points; zeros may give weak efficiency.
Default SLSQP ftol=1e-10, maxiter=120; sweep=21; seed=63.
Bounds and explicit constraints handled by SLSQP. Only scalar subproblems use SciPy.
Local solves are not a global optimality certificate. Inspect Weighted Sum in src\algorithms\weighted_sum.py and identify the test_01_mechanism assertion before editing.

## 16 Explain A2 Epsilon-Constraint and predict one change
One objective minimized and others bounded. Epsilon-Constraint: minimize F1 with normalized F2<=epsilon.
Default epsilon range=[0,1]. Extra constraint calls are explicitly counted.
Default SLSQP ftol=1e-10, maxiter=120; sweep=21; seed=63.
Bounds and explicit constraints handled by SLSQP. Only scalar subproblems use SciPy.
Local solves are not a global optimality certificate. Inspect Epsilon-Constraint in src\algorithms\epsilon_constraint.py and identify the test_02_mechanism assertion before editing.

## 17 Explain A3 Benson reference improvement and predict one change
Weighted improvement below a reference. Benson reference improvement: maximize weighted nonnegative improvements
from a dominated reference r=[1.1,1.1], require F<=r. This follows Foundations slide 35 reference achievement.
It is the teaching form, not full polyhedral outer approximation.
Default SLSQP ftol=1e-10, maxiter=120; sweep=21; seed=63.
Bounds and explicit constraints handled by SLSQP. Only scalar subproblems use SciPy.
Local solves are not a global optimality certificate. Inspect Benson reference improvement in src\algorithms\benson.py and identify the test_03_mechanism assertion before editing.

## 18 Explain A4 Weight Metric and predict one change
Weighted distance to fixed ideal. Weight Metric: distance from fixed ideal, weighted p=1,2,infinity.
Sweep weights for all three p values. p=infinity uses epigraph-free max.
Default SLSQP ftol=1e-10, maxiter=120; sweep=21; seed=63.
Bounds and explicit constraints handled by SLSQP. Only scalar subproblems use SciPy.
Local solves are not a global optimality certificate. Inspect Weight Metric in src\algorithms\weight_metric.py and identify the test_04_mechanism assertion before editing.

## 19 Explain A5 Value Function and predict one change
Declared decision-maker utility. Value Function: declared quadratic utility to a preferred normalized
aspiration. P14 uses [1.8 kg,12 h]; P4 uses three investor risk/return targets.
Utility is a decision-maker input, not a claim of universal preference.
Default SLSQP ftol=1e-10, maxiter=120; sweep=21; seed=63.
Bounds and explicit constraints handled by SLSQP. Only scalar subproblems use SciPy.
Local solves are not a global optimality certificate. Inspect Value Function in src\algorithms\value_function.py and identify the test_05_mechanism assertion before editing.

## 20 Explain A6 Goal Programming and predict one change
Explicit positive/negative goal deviations. Goal Programming: goals in natural output, penalize negative deviations
only (both goals are lower bounds). Explicit dminus=max(target-achieved,0),
dplus=max(achieved-target,0); elimination of linear deviation variables is exact.
Default SLSQP ftol=1e-10, maxiter=120; sweep=21; seed=63.
Bounds and explicit constraints handled by SLSQP. Only scalar subproblems use SciPy.
Local solves are not a global optimality certificate. Inspect Goal Programming in src\algorithms\goal_programming.py and identify the test_06_mechanism assertion before editing.

## 21 Explain A7 Lexicographic and predict one change
Sequential strict priorities with tolerances. Lexicographic: sequential strict-priority scalar minimizations, preserving
prior best objective within tolerance=1e-7 in normalized units. Profit first
then units on P11; agricultural yield first on P7.
Default SLSQP ftol=1e-10, maxiter=120; sweep=21; seed=63.
Bounds and explicit constraints handled by SLSQP. Only scalar subproblems use SciPy.
Local solves are not a global optimality certificate. Inspect Lexicographic in src\algorithms\lexicographic.py and identify the test_07_mechanism assertion before editing.

## 22 Explain A8 TOPSIS and predict one change
Closeness to weighted ideal and anti-ideal. TOPSIS ranking, not an optimizer. Vector normalization, weights,
benefit/cost ideal, Euclidean ideal and anti-ideal distance. Default equal
weights if not supplied; P12 uses [.3,.3,.2,.2]. Zero columns protected. Inspect TOPSIS in src\algorithms\topsis.py and identify the test_08_mechanism assertion before editing.

## 23 Explain A9 VIKOR and predict one change
Compromise via group regret and worst regret. VIKOR compromise ranking with S=sum weighted regret, R=max regret,
Q=v*(S-Sbest)/(Sworst-Sbest)+(1-v)*(R-Rbest)/(Rworst-Rbest).
Default v=.5. Report acceptable advantage 1/(N-1) and stability; never
force a unique compromise when the conditions fail. Inspect VIKOR in src\algorithms\vikor.py and identify the test_09_mechanism assertion before editing.

## 24 Explain A10 VEGA and predict one change
Objective-partitioned selection. VEGA: partition selection by objective, pool subpopulations, crossover and mutation.
Tournament by one objective; no parent+child elitism.
Shared defaults: population=40, budget=10000, optimizer seed from project config.
Constraints: Deb feasibility comparison unless the stated method uses scalar penalty.
Lecture decks supplied on 12 October 2026; teaching variants documented in docs/lecture_alignment.md. Inspect VEGA in src\algorithms\vega.py and identify the test_10_mechanism assertion before editing.

## 25 Explain A11 MOGA and predict one change
Domination-count rank and fitness sharing. MOGA: domination count rank, rank fitness divided by niche count.
Sharing radius sigma=.3; small radius weakens sharing; no elitism.
Shared defaults: population=40, budget=10000, seed=63.
Constraints: Deb feasibility comparison unless the stated method uses scalar penalty.
Lecture decks supplied on 12 October 2026; teaching variants documented in docs/lecture_alignment.md. Inspect MOGA in src\algorithms\moga.py and identify the test_11_mechanism assertion before editing.

## 26 Explain A12 NSGA and predict one change
Front layers and within-front sharing. NSGA: nondominated layers, dummy fitness and within-front sharing.
Sharing radius sigma=.3; non-elitist generational replacement.
Shared defaults: population=40, budget=10000, seed=63.
Constraints: Deb feasibility comparison unless the stated method uses scalar penalty.
Lecture decks supplied on 12 October 2026; teaching variants documented in docs/lecture_alignment.md. Inspect NSGA in src\algorithms\nsga.py and identify the test_12_mechanism assertion before editing.

## 27 Explain A13 NPGA and predict one change
Direct contestant dominance then separate comparison-set quadratic niche tie. Niched Pareto Genetic Algorithm: direct binary tournament with comparison-set crowding.
Direct dominance decides; otherwise smaller comparison-set niche count wins.
Defaults: comparison_size=2, sigma=.3; objective distances normalized.
Shared defaults: population=40, budget=10000, seed=63.
Constraints: Deb feasibility comparison unless the stated method uses scalar penalty.
Lecture decks supplied on 12 October 2026; teaching variants documented in docs/lecture_alignment.md. Inspect NPGA in src\algorithms\npga.py and identify the test_13_mechanism assertion before editing.

## 28 Explain A14 NSGA-II and predict one change
Front rank, crowding, parent-child elitism. NSGA-II: fast front sorting, crowded binary tournament, SBX and mutation,
parent+offspring elitist survival. Permutations use OX and swap/inversion.
Shared defaults: population=40, budget=10000, seed=63.
Constraints: Deb feasibility comparison unless the stated method uses scalar penalty.
Lecture decks supplied on 12 October 2026; teaching variants documented in docs/lecture_alignment.md. Inspect NSGA-II in src\algorithms\nsga2.py and identify the test_14_mechanism assertion before editing.

## 29 Explain A15 NSGA-III and predict one change
Reference-point niching after front rank. NSGA-III: front ranking, simplex-lattice reference association and niche
occupancy survival. Normalize by observed ranges (simplification of intercepts).
Shared defaults: population=40, budget=10000, seed=63.
Constraints: Deb feasibility comparison unless the stated method uses scalar penalty.
Lecture decks supplied on 12 October 2026; teaching variants documented in docs/lecture_alignment.md. Inspect NSGA-III in src\algorithms\nsga3.py and identify the test_15_mechanism assertion before editing.

## 30 Explain A16 SPEA2 and predict one change
Strength, raw fitness and neighbour density. SPEA2: strength S, raw fitness R=sum strengths of dominators;
density 1/(sigma_k+2), fixed archive, lexicographic nearest-distance truncation.
Shared defaults: population=40, budget=10000, seed=63.
Constraints: Deb feasibility comparison unless the stated method uses scalar penalty.
Lecture decks supplied on 12 October 2026; teaching variants documented in docs/lecture_alignment.md. Inspect SPEA2 in src\algorithms\spea2.py and identify the test_16_mechanism assertion before editing.

## 31 Explain A17 PESA-II and predict one change
Archive region occupancy selection. PESA-II: archive adaptive grid regions; region tournament selects lower
occupancy region, then uniform individual. Default grid divisions=8.
Shared defaults: population=40, budget=10000, seed=63.
Constraints: Deb feasibility comparison unless the stated method uses scalar penalty.
Lecture decks supplied on 12 October 2026; teaching variants documented in docs/lecture_alignment.md. Inspect PESA-II in src\algorithms\pesa2.py and identify the test_17_mechanism assertion before editing.

## 32 Explain A18 MOEA/D and predict one change
Neighbouring Tchebycheff subproblems. MOEA/D: reference weights, neighbourhood mating, running ideal,
cooperative Tchebycheff replacement. Neighbourhood size=10.
Shared defaults: population=40, budget=10000, seed=63.
Constraints: Deb feasibility comparison unless the stated method uses scalar penalty.
Lecture decks supplied on 12 October 2026; teaching variants documented in docs/lecture_alignment.md. Inspect MOEA/D in src\algorithms\moead.py and identify the test_18_mechanism assertion before editing.

## 33 Explain A19 MOEA/D-DE and predict one change
DE variation inside MOEA/D. MOEA/D-DE: neighbourhood donor x_a+F*(x_b-x_c), binomial
crossover CR=.9 with forced coordinate, F=.5; cooperative scalar replacement.
Shared defaults: population=40, budget=10000, seed=63.
Constraints: Deb feasibility comparison unless the stated method uses scalar penalty.
Lecture decks supplied on 12 October 2026; teaching variants documented in docs/lecture_alignment.md. Inspect MOEA/D-DE in src\algorithms\moead_de.py and identify the test_19_mechanism assertion before editing.

## 34 Explain A20 MOEA/D-ACO and predict one change
Weight-specific ant pheromones and scalar replacement. MOEA/D-ACO for tours: each weight has edge pheromone, weighted
distance/time heuristic, neighbour Tchebycheff replacement and deposits.
Defaults alpha=1 beta=2 evaporation=.1. Requires P8.
Shared defaults: population=40, budget=10000, seed=63.
Constraints: Deb feasibility comparison unless the stated method uses scalar penalty.
Lecture decks supplied on 12 October 2026; teaching variants documented in docs/lecture_alignment.md. Inspect MOEA/D-ACO in src\algorithms\moead_aco.py and identify the test_20_mechanism assertion before editing.

## 35 Explain A21 Constrained NSGA-II and predict one change
NSGA-II with Deb feasibility. Constrained NSGA-II: feasible beats infeasible, lower violation wins
among infeasible, Pareto rank then crowding among feasible.
NSGA-II in this project also supports Deb rules; this module exposes the rule.
Shared defaults: population=40, budget=10000, seed=63.
Constraints: Deb feasibility comparison unless the stated method uses scalar penalty.
Lecture decks supplied on 12 October 2026; teaching variants documented in docs/lecture_alignment.md. Inspect Constrained NSGA-II in src\algorithms\constrained_nsga2.py and identify the test_21_mechanism assertion before editing.

## 36 Explain A22 MOPSO and predict one change
Particle velocity with personal and archive leaders. MOPSO: inertia velocity, personal best, crowding-selected archive
leader, occasional mutation. Personal best changes only when a trial dominates it.
Defaults inertia=.4, c1=c2=1.5.
Shared defaults: population=40, budget=10000, optimizer seed from project config.
Constraints: Deb feasibility comparison unless the stated method uses scalar penalty.
Lecture decks supplied on 12 October 2026; teaching variants documented in docs/lecture_alignment.md. Inspect MOPSO in src\algorithms\mopso.py and identify the test_22_mechanism assertion before editing.

## 37 Explain A23 MOGWO and predict one change
Three archive leaders and encircling. MOGWO: alpha, beta, delta archive leaders; decreasing encircling
coefficient a=2*(1-used/budget), average three proposed positions.
Binary masks use a sigmoid transfer, then at-least-one repair.
Shared defaults: population=40, budget=10000, seed=63.
Constraints: Deb feasibility comparison unless the stated method uses scalar penalty.
Lecture decks supplied on 12 October 2026; teaching variants documented in docs/lecture_alignment.md. Inspect MOGWO in src\algorithms\mogwo.py and identify the test_23_mechanism assertion before editing.

## 38 Explain A24 MOABC and predict one change
Employed moves, crowding-based onlookers and abandonment scouts. MOABC: employed and onlooker differential-coordinate proposals,
Deb dominance greedy replacement, abandoned-source scouts. Limit=20.
Shared defaults: population=40, budget=10000, seed=63.
Constraints: Deb feasibility comparison unless the stated method uses scalar penalty.
Lecture decks supplied on 12 October 2026; teaching variants documented in docs/lecture_alignment.md. Inspect MOABC in src\algorithms\moabc.py and identify the test_24_mechanism assertion before editing.

## 39 Explain A25 MOACO and predict one change
Two pheromone matrices and route construction. MOACO: two pheromone matrices, randomized tradeoff exponent,
probabilistic valid tour construction, evaporation and archive deposits.
Defaults alpha=1 beta=2 evaporation=.1. P8 only.
Shared defaults: population=40, budget=10000, seed=63.
Constraints: Deb feasibility comparison unless the stated method uses scalar penalty.
Lecture decks supplied on 12 October 2026; teaching variants documented in docs/lecture_alignment.md. Inspect MOACO in src\algorithms\moaco.py and identify the test_25_mechanism assertion before editing.

## 40 Explain A26 MOSA and predict one change
Incomparable neighbour acceptance and Boltzmann dominated moves. Multiobjective Simulated Annealing: population of chains, normalized
summed worsened-objective energy for dominated moves, Boltzmann acceptance and archive.
Temperature T0=.1, cooling=.97 per population sweep, move scale=.1.
Lecture Part 4 slide 41 acceptance; parallel chains are a declared extension.
Incomparable neighbours always accepted. Normalized T0=.1 is not raw-unit T0=100.
Shared defaults: population=40, budget=10000, seed=63.
Constraints: Deb feasibility comparison unless the stated method uses scalar penalty.
Lecture decks supplied on 12 October 2026; teaching variants documented in docs/lecture_alignment.md. Inspect MOSA in src\algorithms\mosa.py and identify the test_26_mechanism assertion before editing.

## 41 Explain A27 MODE and predict one change
DE dominance-only trial replacement. MODE: DE/rand/1 and forced binomial crossover; trial replaces target
only if it dominates under Deb rules. F=.5, CR=.9. Output archive retains tradeoffs.
Shared defaults: population=40, budget=10000, seed=63.
Constraints: Deb feasibility comparison unless the stated method uses scalar penalty.
Lecture decks supplied on 12 October 2026; teaching variants documented in docs/lecture_alignment.md. Inspect MODE in src\algorithms\mode.py and identify the test_27_mechanism assertion before editing.

## 42 Explain A28 MO-TLBO and predict one change
Crowding archive teacher, shrinking TF and nondominated learner moves. MO-TLBO: teacher phase x+r*(teacher-TF*mean); learner phase
towards better peer or away from worse peer. TF shrinks from 2 to 1.
Nondominated replacement, archive tracks nondominated proposals.
Shared defaults: population=40, budget=10000, seed=63.
Constraints: Deb feasibility comparison unless the stated method uses scalar penalty.
Lecture decks supplied on 12 October 2026; teaching variants documented in docs/lecture_alignment.md. Inspect MO-TLBO in src\algorithms\motlbo.py and identify the test_28_mechanism assertion before editing.

## 43 Explain A29 MOBA and predict one change
Frequency velocity, pulse and loudness. MOBA: frequency velocity toward archive leader, pulse-controlled local
random walk, loudness acceptance. fmin=0 fmax=2, loudness*=.95,
pulse=1*(1-exp(-.1*g)). Pareto archive stores all visited feasible points.
Shared defaults: population=40, budget=10000, seed=63.
Constraints: Deb feasibility comparison unless the stated method uses scalar penalty.
Lecture decks supplied on 12 October 2026; teaching variants documented in docs/lecture_alignment.md. Inspect MOBA in src\algorithms\moba.py and identify the test_29_mechanism assertion before editing.

## 44 Explain A30 MOMA and predict one change
NSGA-II plus sparse-child combined-score hill climbing. MOMA: NSGA-II global search and normalized combined-improvement hill-climb on a subset
of children. Local fraction=.25, mutation scale=.02. Local calls count in budget.
Shared defaults: population=40, budget=10000, seed=63.
Constraints: Deb feasibility comparison unless the stated method uses scalar penalty.
Lecture decks supplied on 12 October 2026; teaching variants documented in docs/lecture_alignment.md. Inspect MOMA in src\algorithms\moma.py and identify the test_30_mechanism assertion before editing.

## 45 Explain A31 RVEA and predict one change
Normalized reference vectors and lecture linear-progress APD. RVEA: reference-vector association and angle-penalized distance (APD),
penalty strength alpha=2. Range-adapt vectors every 10 generations.
One best member per vector, fill unoccupied slots by APD.
Shared defaults: population=40, budget=10000, seed=63.
Constraints: Deb feasibility comparison unless the stated method uses scalar penalty.
Lecture decks supplied on 12 October 2026; teaching variants documented in docs/lecture_alignment.md. Inspect RVEA in src\algorithms\rvea.py and identify the test_31_mechanism assertion before editing.

## 46 Explain A32 IBEA and predict one change
Outgoing additive-epsilon fitness and largest-fitness deletion. IBEA: additive epsilon indicator I(a,b)=max_j(a_j-b_j);
outgoing fitness -sum_j exp(-I(i,j)/kappa), largest removed, iterative worst removal with recalculation.
kappa=.05; normalized objective ranges; feasibility penalty before indicator.
Shared defaults: population=40, budget=10000, seed=63.
Constraints: Deb feasibility comparison unless the stated method uses scalar penalty.
Lecture decks supplied on 12 October 2026; teaching variants documented in docs/lecture_alignment.md. Inspect IBEA in src\algorithms\ibea.py and identify the test_32_mechanism assertion before editing.

## 47 Explain A33 SMS-EMOA and predict one change
Steady-state smallest HV deletion. SMS-EMOA: one offspring, nondominated sorting, delete least HV
contribution in worst front. Exact 2-D exclusive contributions.
Reference is component maximum + .1 in normalized coordinates.
Shared defaults: population=40, budget=10000, seed=63.
Constraints: Deb feasibility comparison unless the stated method uses scalar penalty.
Lecture decks supplied on 12 October 2026; teaching variants documented in docs/lecture_alignment.md. Inspect SMS-EMOA in src\algorithms\sms_emoa.py and identify the test_33_mechanism assertion before editing.

## 48 Explain A34 HypE and predict one change
Equal-share Monte Carlo HV fitness and repeated deletion. HypE: Monte Carlo hypervolume fitness with equal shared credits,
iterative contribution deletion. Samples=256 selection, final HV uses 8192.
Credits account for shared dominated samples; noisy selection is a limitation.
Shared defaults: population=40, budget=10000, seed=63.
Constraints: Deb feasibility comparison unless the stated method uses scalar penalty.
Lecture decks supplied on 12 October 2026; teaching variants documented in docs/lecture_alignment.md. Inspect HypE in src\algorithms\hype.py and identify the test_34_mechanism assertion before editing.

## 49 Explain A35 R-NSGA-II and predict one change
Reference preference and epsilon clearing. R-NSGA-II: nondominated fronts, normalized distance to aspiration,
epsilon clearing to spread preferred survivors. epsilon=.05; default balanced
normalized aspiration [.5,.5], P14 uses natural [1.8,-12]; callers may override.
Shared defaults: population=40, budget=10000, optimizer seed from project config.
Constraints: Deb feasibility comparison unless the stated method uses scalar penalty.
Lecture decks supplied on 12 October 2026; teaching variants documented in docs/lecture_alignment.md. Inspect R-NSGA-II in src\algorithms\r_nsga2.py and identify the test_35_mechanism assertion before editing.

## 50 Explain A36 MGDA and predict one change
Minimum-norm gradient combination. MGDA: minimum-norm convex combination of task gradients.
For two tasks solve lambda analytically; clamp to [0,1]. Learning rate=.05.
Toy losses have gradients 2*(x-a),2*(x-b). No convergence theorem assumed
for arbitrary nonconvex neural networks. Inspect MGDA in src\algorithms\mgda.py and identify the test_36_mechanism assertion before editing.

## 51 Explain A37 GradNorm and predict one change
Gradient-norm adaptive task weights. GradNorm: adaptive weights minimizing sum |G_i-target_i|.
G_i=w_i*||gradient_i||; target=mean(G)*relative_training_rate**alpha,
stop-gradient target, weights renormalized to sum(tasks). Alpha=1.5,
weight_lr=.01, model_lr=.05. Hand-derived weight gradient uses sign.
This supports toy objectives and the handwritten shared network. Inspect GradNorm in src\algorithms\gradnorm.py and identify the test_37_mechanism assertion before editing.