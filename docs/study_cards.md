# Task C: roll 63 study cards

## 26. MOSA - Multiobjective Simulated Annealing

Historical context: Paolo Serafini's 1994 chapter, "Simulated annealing for multi objective optimization problems", in Multiple Criteria Decision Making: Expand and Enrich the Domains of Thinking and Application, Springer, pp. 283-292, is an early multiobjective SA treatment. The author's older web listing says 1993; his current CV says 1994. We report 1994 as the publication year and record this discrepancy. MOSA is a family rather than one universally fixed algorithm; this implementation does not claim to reproduce all of Serafini's acceptance rules.

Core idea (five lines): keep four or more local-search chains; propose a nearby design; accept improving or incomparable neighbours; occasionally accept dominated moves with probability exp(-delta/T); cool T and record a Pareto archive.

Flow: initialize chains -> mutate -> evaluate -> Deb feasibility check -> energy/temperature acceptance -> update chain -> record nondominated proposals -> cool -> budget reached?

1. Sample population uniformly in bounds. Repair encodings and initialize recording archive.
2. Propose one mutation per chain. Real coordinate mutation: x'=clip(x+0.1*(upper-lower)*z), z normal(0,1); permutations use swap or inversion.
3. Normalize z_j=(f_j-ideal_j)/(nadir_j-ideal_j). Use the lecture sum of positive objective differences for dominated moves.
4. If proposal dominates chain under Deb's rules, accept. Feasible-to-infeasible moves are rejected. If the current solution does not dominate the feasible proposal, accept unconditionally. Otherwise delta=sum(max(z'-z,0)), p=exp(-delta/T). Between infeasible proposals use violation increase.
5. Accept if uniform u<p; record every proposal in a passive archive; cool T=T0*cooling^generation.
6. Terminate at 10000 counted candidate evaluations. Archive capped at population size by crowding.

Parameters: T0=.1; too small freezes uphill escape, too large yields random wandering. Cooling=.97; too low cools before exploration, too high prolongs random acceptance. Move scale=.1; small misses distant basins, large repeatedly hits bounds. Population=40; small limits output coverage, large uses budget on fewer sweeps. Archive cap=population; low cap loses diversity, large increases O(A^2*M) bookkeeping. Violation penalty=10 only between infeasible candidates; stronger promotes feasibility but can erase objective influence.

Convergence: cooling helps exploitation but finite-budget runs do not inherit a global SA theorem. Diversity: unconditional tradeoff moves and archive crowding, without a guaranteed uniform front. Constraints: feasibility first, then violation. Nonconvex/disconnected fronts: local moves can traverse them at sufficient temperature but may miss separated basins. Many objectives: scalar energies remain usable, yet domination becomes sparse and bounded archives lose coverage.

Cost: proposal O(d), evaluation problem dependent, chain update O(M); archive maintenance O(M*A^2) per recorded population in a straightforward implementation. This implementation records each population batch for MOSA; peak memory O(A*d+A*M+M*A^2).

Hand traces: exact Part 4 chip example x=10->13->15, F=(20,10)->(17,11.5)->(15,12.5), T=100->90->81; both moves incomparable and accepted. Additional population-four P1 fixture starts [3,4,6,7], T0=.1. Proposals [3.5,4.5,6.5,7.5] have summed positive normalized differences [.015625,.078125,.203125,.28125]; only the fourth is dominated, probability exp(-2.8125). Fixed uniforms [.1,.2,.9,.1] yield [3.5,4.5,6.5,7]. Next proposals [4,5,7,6.5] are all incomparable and accepted. Full objective tables, acceptance and mutation draws are stored in hand_traces.json and tested.

Sensitivity: cooling=.90,.97,.995, 10 seeds each on P3, fixed 10000 cap. These correspond to fast, moderate and slow cooling. Interpretation is generated from measured summary rows, not assumed.

## 1. Weighted Sum

Historical context: weighted sums predate modern named multiobjective optimizers, so a unique inventor/year is not asserted. Lotfi A. Zadeh's 1963 "Optimality and non-scalar-valued performance criteria", IEEE Transactions on Automatic Control 8(1), 59-60, DOI 10.1109/TAC.1963.1105511, is a foundational efficiency reference, not a claim that he invented the weighted-sum method.

Core idea: choose nonnegative weights; normalize objectives; minimize one linear combination; repeat for a sequence of weights; keep feasible nondominated solutions.

Flow: fixed scales -> simplex weight -> scalar solve -> save feasible endpoint -> next weight -> Pareto filter.

1. Declare common objective ideal/nadir constants.
2. Choose w_j>=0 with sum(w)=1. Default two-objective weights t,1-t for t in linspace(0,1,21).
3. Solve min s(x)=sum_j w_j*z_j(x), subject to the original bounds and constraints using SLSQP.
4. Record solver termination, actual objective/constraint objective calls and decision.
5. Pareto-filter successful feasible sweep candidates. Natural termination means fewer than 10000 actual calls; no unused calls are relabelled.

Parameters: weight t controls orientation; near 0 favours objective 2 and near 1 objective 1. Number of settings=21; fewer than 10 violates Task D; very many spends effort on duplicate supported solutions. Ideal/nadir scales control weight meaning; poor scales overwhelm small objectives. SLSQP tolerance=1e-10: loose leaves error, extremely tight increases work; max iterations=120: low truncates solves, high increases cost. Starting point depends on seed; a local optimizer may miss a global scalar minimum. Zero weights can produce only weak efficiency.

Guarantee: positive weights and an exact global solve imply Pareto efficiency: any dominator would reduce the weighted scalar, a contradiction. The converse holds only for supported efficient points. On P3, z2=1-z1^2; for fixed w the scalar is concave in z1 and attains its minimum at 0 or 1, so interior dented points cannot be selected by any positive weight. Finite local solves need independent convergence checks.

Diversity: controlled by sweep, not automatic. Equal weights are not equal arc lengths. Constraints: inherited from scalar solver. Many objectives: number of simplex settings grows rapidly and preferences become difficult. Discrete variants need enumeration or a discrete scalar solver; SLSQP is used only for real-valued problems here.

Cost: K scalar solves; O(K*S*C_eval) objective work, where S is calls per solve, plus O(K^2*M) Pareto filtering. Solver complexity is problem dependent, not universally O(n^3).

Hand trace P1 (raw scale is equal in both objectives): derivative 2*w*(x-3)+2*(1-w)*(x-7)=0 -> x=7-4*w. w=.25 gives x=6, F=(9,1), scalar=3. w=.75 gives x=4, F=(1,9), scalar=3. Second derivative=2>0, bounds satisfied. Both normalized scalars are 3/16.

Sensitivity: 11,21,41 settings, ten seeds on P3. Sampling density cannot overcome unsupported-front geometry; actual call counts change and this is not a strict equal-consumed-budget comparison.

## 13. NPGA - Niched Pareto Genetic Algorithm

Jeffrey Horn, N. Nafpliotis and David E. Goldberg (1994), "A niched Pareto genetic algorithm for multiobjective optimization", Proceedings of the First IEEE Conference on Evolutionary Computation, pp. 82-87, DOI 10.1109/ICEC.1994.350037. An author-uploaded copy verifies the metadata. The method addresses maintaining a diverse tradeoff population without choosing one scalar utility. Earlier technical reports may precede the conference paper; 1994 is the cited publication.

Core idea: draw two contestants; compare them directly by dominance; otherwise measure each niche count against a separate comparison set and choose the less crowded contestant; vary winners to produce a new non-elitist generation.

Flow: population -> contestants and comparison set -> direct dominance -> comparison-set niche tie-break -> mating -> SBX/mutation -> replace population -> record output archive.

1. Initialize real vectors uniformly or valid discrete encodings.
2. Normalize the current generation by observed ranges for niche distances; this differs from fixed quality-metric scales.
3. Sample distinct contestants a,b and comparison set C of size min(2,N-2), excluding contestants. Compare a and b directly under Deb rules; this is the supplied lecture teaching variant.
4. If one contestant dominates the other, return that contestant. Otherwise use niche_i=sum_(j in C) max(0,1-(distance(i,j)/sigma)^2), sigma=.3. The comparison set excludes contestants; ties select the first within numerical tolerance 1e-12.
5. Pool tournament winners; SBX eta=15 and mutation probability 1/d create children. Permutations, when applicable, use OX plus swap/inversion.
6. Replace the generation without elitism. A passive logging archive does not participate in selection. Stop at 10000 actual candidate evaluations.

Parameters: sigma=.3; too small loses sharing except duplicates, too large averages global density and weakens local niche resolution. Comparison size=2; small gives noisy niche estimates, large costs more and approaches full-population density. Population=40; small misses niches, large reduces generations per fixed budget. Crossover eta=15; small jumps widely, large stays close to parents. Mutation scale=.1 and probability=1/d; too low stalls exploration, too high disrupts useful coordinates. Direct contestant dominance and separate comparison-set sharing follow Non-Elitist slide 27. The original publication uses a different tournament convention; the course variant is explicit.

Convergence: selection favours directly dominating contestants but provides no elitist guarantee. Diversity: sharing explicitly rewards sparse regions. Constraints: Deb-aware comparisons. Nonconvex fronts: no linear scalarization barrier. Many objectives: most contestants become incomparable and niche decisions dominate; distances also become less discriminative.

Cost: the running selector computes normalization and comparison distances per tournament, costing O(N*(N*M+|C|*M)); a cached alternative could reduce repeated normalization, crossover/mutation O(N*d), plus evaluations and output archive costs. Peak comparison-set memory O(|C|*M), plus population O(N*d+N*M) and passive archive pairwise bookkeeping. The standalone tournament helper recomputes sharing for transparent trace verification; the running selector uses the lecture comparison-set helper.

Hand traces: exact four-topology lecture table A=(10,.80),B=(15,.90),C=(12,.85),D=(18,.95). Fixed scales are (cost-10)/10 and (reliability-.8)/.2. For A vs B with C,D: distances .320156,1.096586,.390512,.390512; quadratic shares .59,0,.39,.39 give NC(A)=.59,NC(B)=.78; A wins. C vs D with A,B gives NC(C)=.98,NC(D)=.39; D wins. The displayed lecture values .778/.979 are approximate; exact arithmetic preserves both decisions. Additional full population-four generations on P1 enumerate every distance, sharing term, pair-specific comparison set, winner, fixed SBX beta=1 and Gaussian mutation draw in hand_traces.json. The second generation recomputes dominance before using density.

Sensitivity: sigma=.1,.3,.6, ten seeds on P3. The three values test local, moderate and broad sharing. Compare HV, IGD and Spacing along with final population diversity; a zero Spacing singleton is not good coverage.
