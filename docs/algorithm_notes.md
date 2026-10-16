# Task B algorithm comparison

Measured outcomes and theory-based mechanism arguments are distinguished. Values use the common normalized metric scales. Each method has two concrete observed strengths and two concrete observed limitations where the stored data permits them; causal attribution remains explicitly bounded.

## 1 Weighted Sum

Linear scalar solve and a sweep

Advantages (mechanism-based): Simple scalar objective;Direct preference weights;Reusable constrained scalar solver;Independent solves can be distributed

Disadvantages (mechanism-based): Unsupported nonconvex points are unreachable;Scaling changes weight meaning;Uniform weights give nonuniform spacing;Local scalar solves lack global guarantees

Evidence-linked strengths: Weighted Sum recorded HV 1.0258 ± 0 on P1, IGD 0.020135 ± 0 (Figure A01). In the comparable P3 study with the same 10,000-evaluation cap, Weighted Sum recorded HV 0.21 ± 0; the nearest peer by mean HV was Benson reference improvement at 0.21 ± 9.8457e-12, with runtime 0.4763 ± 0.072962 s versus 1.1766 ± 0 s for Weighted Sum. A separate P3 record gives HV 0.21 ± 0 after 847 ± 0 evaluations in 1.1766 ± 0 s, so the evidence is not limited to one problem.

Evidence-linked limitations: The nonzero P1 IGD of 0.020135 ± 0 measures remaining sampled-front error. Thus the run does not support exact convergence or global optimality. Across 10 P3 trials, HV SD was 1.4261e-11 and runtime SD was 0.44449 s, which quantifies seed sensitivity at this budget.

Evidence boundary: The measurements provide context for the claimed benefit "Simple scalar objective" and the risk "Unsupported nonconvex points are unreachable". They do not isolate either mechanism; controlled ablation would be required for causal attribution.

Suitable: Convex smooth two-objective design with interpretable weights; avoid: Dented fronts and an unknown preference distribution

## 2 Epsilon-Constraint

One objective minimized and others bounded

Advantages (mechanism-based): Can represent unsupported efficient points;Epsilon has physical interpretation;Scalar constraints remain explicit;Primary objective stays recognizable

Disadvantages (mechanism-based): Infeasible epsilon values waste solves;Sweeps can duplicate points;Constraint solver quality matters;Many objectives require multidimensional epsilon grids

Evidence-linked strengths: Epsilon-Constraint recorded HV 1.0865 ± 0 on P2, IGD 0.037129 ± 0 (Figure A02). In the comparable P3 study with the same 10,000-evaluation cap, Epsilon-Constraint recorded HV 0.52055 ± 0; the nearest peer by mean HV was Weight Metric at 0.52152 ± 0.0035033, with runtime 2.5137 ± 0.17386 s versus 0.59307 ± 0 s for Epsilon-Constraint. A separate P3 record gives HV 0.52055 ± 0 after 3488 ± 0 evaluations in 0.59307 ± 0 s, so the evidence is not limited to one problem.

Evidence-linked limitations: The nonzero P2 IGD of 0.037129 ± 0 measures remaining sampled-front error. Thus the run does not support exact convergence or global optimality. Across 10 P3 trials, HV SD was 0.0014644 and runtime SD was 0.033987 s, which quantifies seed sensitivity at this budget.

Evidence boundary: The measurements provide context for the claimed benefit "Can represent unsupported efficient points" and the risk "Infeasible epsilon values waste solves". They do not isolate either mechanism; controlled ablation would be required for causal attribution.

Suitable: Nonconvex constrained design with hard limits; avoid: High-dimensional objective grids

## 3 Benson reference improvement

Weighted improvement below a reference

Advantages (mechanism-based): Reference conveys aspiration;Nonnegative improvement is interpretable;Explicit upper objective bounds;Scalar subproblems are easy to inspect

Disadvantages (mechanism-based): This is the lecture achievement form, not outer approximation;Unrestricted reference sweeps inherit weighted-sum barrier;Reference coordinates require scaling;Weights still encode preferences

Evidence-linked strengths: Benson reference improvement recorded HV 1.0258 ± 0 on P1, IGD 0.020135 ± 0 (Figure A03). In the comparable P3 study with the same 10,000-evaluation cap, Benson reference improvement recorded HV 0.21 ± 9.8457e-12; the nearest peer by mean HV was Weighted Sum at 0.21 ± 1.4261e-11, with runtime 0.40343 ± 0.44449 s versus 0.4763 ± 0.072962 s for Benson reference improvement. A separate P7 record gives HV 0.45626 ± 0 after 3947 ± 0 evaluations in 0.91874 ± 0 s, so the evidence is not limited to one problem.

Evidence-linked limitations: The nonzero P1 IGD of 0.020135 ± 0 measures remaining sampled-front error. Thus the run does not support exact convergence or global optimality. Across 10 P3 trials, HV SD was 9.8457e-12 and runtime SD was 0.072962 s, which quantifies seed sensitivity at this budget.

Evidence boundary: The measurements provide context for the claimed benefit "Reference conveys aspiration" and the risk "This is the lecture achievement form, not outer approximation". They do not isolate either mechanism; controlled ablation would be required for causal attribution.

Suitable: Teaching reference improvement on P1/P7; avoid: Claiming a general Benson convergence theorem

## 4 Weight Metric

Weighted distance to fixed ideal

Advantages (mechanism-based): Infinity norm can reach unsupported tradeoffs;Different p values express balance;Ideal point makes distances interpretable;Scalar solver is reusable

Disadvantages (mechanism-based): Ideal estimation affects solution;Max norm is nonsmooth;p and weights require preferences;Finite weight sweep misses narrow regions

Evidence-linked strengths: Weight Metric recorded HV 1.0347 ± 0 on P1, IGD 0.012339 ± 0 (Figure A04). In the comparable P3 study with the same 10,000-evaluation cap, Weight Metric recorded HV 0.52368 ± 0; the nearest peer by mean HV was MOGA at 0.52378 ± 0.0010854, with runtime 3.7374 ± 0.4774 s versus 2.6382 ± 0 s for Weight Metric. A separate P3 record gives HV 0.52368 ± 0 after 9021 ± 0 evaluations in 2.6382 ± 0 s, so the evidence is not limited to one problem.

Evidence-linked limitations: The nonzero P1 IGD of 0.012339 ± 0 measures remaining sampled-front error. Thus the run does not support exact convergence or global optimality. Across 10 P3 trials, HV SD was 0.0035033 and runtime SD was 0.17386 s, which quantifies seed sensitivity at this budget.

Evidence boundary: The measurements provide context for the claimed benefit "Infinity norm can reach unsupported tradeoffs" and the risk "Ideal estimation affects solution". They do not isolate either mechanism; controlled ablation would be required for causal attribution.

Suitable: Compromise solutions on nonconvex fronts; avoid: Unreliable ideal estimates or many weights

## 5 Value Function

Declared decision-maker utility

Advantages (mechanism-based): Directly encodes a preferred outcome;Can express nonlinear preferences;Few scalar solves are economical;Natural targets communicate decisions

Disadvantages (mechanism-based): Utility must be elicited;Squared target utility need not be monotone;One preferred design is not a full front;Misspecified preferences bias results

Evidence-linked strengths: Value Function recorded HV 0.32905 ± 0 on P14, IGD 0.35302 ± 0 (Figure A05). The run used 45 ± 0 evaluations and took 0.022336 ± 0 s; no same-problem comparison row is used to manufacture a benchmark claim. A separate P4 record gives HV 0.66617 ± 0 after 156 ± 0 evaluations in 0.062954 ± 0 s, so the evidence is not limited to one problem.

Evidence-linked limitations: The nonzero P14 IGD of 0.35302 ± 0 measures remaining sampled-front error. Thus the run does not support exact convergence or global optimality. The P14 output retained 1 ± 0 point(s). That finite resolution limits what the plot can demonstrate; front size or zero Spacing alone is not evidence of complete coverage.

Evidence boundary: The measurements provide context for the claimed benefit "Directly encodes a preferred outcome" and the risk "Utility must be elicited". They do not isolate either mechanism; controlled ablation would be required for causal attribution.

Suitable: Laptop or portfolio profile decisions; avoid: Exploration without known preferences

## 6 Goal Programming

Explicit positive/negative goal deviations

Advantages (mechanism-based): Shows unavoidable shortfall;Can normalize incompatible units;Soft goals remain interpretable;Constraint and aspiration roles are separate

Disadvantages (mechanism-based): Goal weights control tradeoffs;Infeasible goals cannot be guaranteed;Units can overwhelm deviations;Satisfied goals may leave efficiency ties

Evidence-linked strengths: Goal Programming recorded HV 1.21 ± 0 on P11, IGD 9.6355e-11 ± 0 (Figure A06). The run used 1219 ± 0 evaluations and took 0.52765 ± 0 s; no same-problem comparison row is used to manufacture a benchmark claim. A separate P7 record gives HV 0.34071 ± 0 after 304 ± 0 evaluations in 0.17763 ± 0 s, so the evidence is not limited to one problem.

Evidence-linked limitations: The nonzero P11 IGD of 9.6355e-11 ± 0 measures remaining sampled-front error. Thus the run does not support exact convergence or global optimality. The P11 output retained 1 ± 0 point(s). That finite resolution limits what the plot can demonstrate; front size or zero Spacing alone is not evidence of complete coverage.

Evidence boundary: The measurements provide context for the claimed benefit "Shows unavoidable shortfall" and the risk "Goal weights control tradeoffs". They do not isolate either mechanism; controlled ablation would be required for causal attribution.

Suitable: Production targets with soft priorities; avoid: Searching an entire front without goals

## 7 Lexicographic

Sequential strict priorities with tolerances

Advantages (mechanism-based): Priority order is transparent;Breaks first-objective ties;Uses scalar solvers;Preserves prior objective values to declared tolerance

Disadvantages (mechanism-based): Lower objectives may have little freedom;Tolerance changes strictness;Priority mistakes are expensive;Sequential solves add cost

Evidence-linked strengths: Lexicographic recorded HV 1.21 ± 0 on P11, IGD 1.6309e-11 ± 0 (Figure A07). The run used 219 ± 0 evaluations and took 0.08428 ± 0 s; no same-problem comparison row is used to manufacture a benchmark claim. A separate P7 record gives HV 0.11 ± 0 after 47 ± 0 evaluations in 0.023686 ± 0 s, so the evidence is not limited to one problem.

Evidence-linked limitations: The nonzero P11 IGD of 1.6309e-11 ± 0 measures remaining sampled-front error. Thus the run does not support exact convergence or global optimality. The P11 output retained 1 ± 0 point(s). That finite resolution limits what the plot can demonstrate; front size or zero Spacing alone is not evidence of complete coverage.

Evidence boundary: The measurements provide context for the claimed benefit "Priority order is transparent" and the risk "Lower objectives may have little freedom". They do not isolate either mechanism; controlled ablation would be required for causal attribution.

Suitable: Profit first and units second; avoid: Balanced objectives with no hierarchy

## 8 TOPSIS

Closeness to weighted ideal and anti-ideal

Advantages (mechanism-based): Fast finite-table ranking;Uses all criteria;Distances are explainable;Works with benefit and cost columns

Disadvantages (mechanism-based): Does not generate new designs;Vector normalization affects rank;Compensation can hide a bad criterion;Alternatives can change the ideal

Evidence-linked strengths: On the supplied alternatives, TOPSIS produced explicit top-three orders for 4 recorded preference settings; for example P12 gave [3, 1, 5]. The P12 and P4 tables therefore support its practical ability to turn stated weights into an auditable shortlist. These are ranking outcomes, not search quality.

Evidence-linked limitations: The same records contain only existing alternatives and no generated decision vector, directly confirming that TOPSIS is not an optimizer. Its orders also depend on weights; the recorded weight-shift rows quantify local sensitivity but do not establish global stability.

Evidence boundary: The ranking evidence supports auditable preference application, while the mechanism-based benefit "Fast finite-table ranking" and risk "Does not generate new designs" remain analytical claims rather than optimizer evidence.

Suitable: Supplier or existing-front ranking; avoid: Optimization without an alternatives table

## 9 VIKOR

Compromise via group regret and worst regret

Advantages (mechanism-based): Worst criterion enters R;v exposes group versus individual tradeoff;Compromise conditions avoid forced winners;Finite rankings are inexpensive

Disadvantages (mechanism-based): Requires preference weights;v can change rank;Range normalization changes regrets;Does not generate designs

Evidence-linked strengths: On the supplied alternatives, VIKOR produced explicit top-three orders for 8 recorded preference settings; for example P12 gave [1, 2, 5]. The P12 and P4 tables therefore support its practical ability to turn stated weights into an auditable shortlist. These are ranking outcomes, not search quality.

Evidence-linked limitations: The same records contain only existing alternatives and no generated decision vector, directly confirming that VIKOR is not an optimizer. Its orders also depend on weights and v; the recorded weight-shift rows quantify local sensitivity but do not establish global stability.

Evidence boundary: The ranking evidence supports auditable preference application, while the mechanism-based benefit "Worst criterion enters R" and risk "Requires preference weights" remain analytical claims rather than optimizer evidence.

Suitable: Supplier compromise with severe weak criteria; avoid: A Pareto front generator

## 10 VEGA

Objective-partitioned selection

Advantages (mechanism-based): Very simple selection;No preference weights needed;Handles several objective contests;Cheap scalar tournaments

Disadvantages (mechanism-based): Extremes can dominate mating pool;No parent elitism;Middle tradeoffs may disappear;Objective partition sizes affect pressure

Evidence-linked strengths: VEGA recorded HV 1.1109 ± 0.00092541 on P2, IGD 0.014362 ± 0.0015584 (Figure A10). In the comparable P3 study with the same 10,000-evaluation cap, VEGA recorded HV 0.17298 ± 0.045825; the nearest peer by mean HV was IBEA at 0.19276 ± 0.017015, with runtime 11.413 ± 0.95043 s versus 3.0626 ± 0.22029 s for VEGA. A separate P3 record gives HV 0.17298 ± 0.045825 after 10000 ± 0 evaluations in 3.0626 ± 0.22029 s, so the evidence is not limited to one problem.

Evidence-linked limitations: The nonzero P2 IGD of 0.014362 ± 0.0015584 measures remaining sampled-front error. Thus the run does not support exact convergence or global optimality. Across 10 P2 trials, HV SD was 0.00092541 and runtime SD was 0.27359 s, which quantifies seed sensitivity at this budget.

Evidence boundary: The measurements provide context for the claimed benefit "Very simple selection" and the risk "Extremes can dominate mating pool". They do not isolate either mechanism; controlled ablation would be required for causal attribution.

Suitable: Teaching objective competition; avoid: Reliable uniform front preservation

## 11 MOGA

Domination-count rank and fitness sharing

Advantages (mechanism-based): No scalar utility required;Sharing promotes sparse niches;Dominance counts are easy to inspect;Can search unsupported regions

Disadvantages (mechanism-based): No elitism;Sharing radius sensitive;All nondominated members tie in rank;Pairwise density costs quadratically

Evidence-linked strengths: MOGA recorded HV 0.52378 ± 0.0010854 on P3, IGD 0.012703 ± 0.00047311 (Figure A11). In the comparable P3 study with the same 10,000-evaluation cap, MOGA recorded HV 0.52378 ± 0.0010854; the nearest peer by mean HV was NSGA at 0.52521 ± 0.001173, with runtime 3.5297 ± 0.27057 s versus 3.7674 ± 0.43826 s for MOGA. A separate P5 record gives HV 1.1817 ± 0.0001344 after 10000 ± 0 evaluations in 3.5464 ± 0.31467 s, so the evidence is not limited to one problem.

Evidence-linked limitations: The nonzero P3 IGD of 0.012703 ± 0.00047311 measures remaining sampled-front error. Thus the run does not support exact convergence or global optimality. Across 10 P3 trials, HV SD was 0.0010854 and runtime SD was 0.43826 s, which quantifies seed sensitivity at this budget.

Evidence boundary: The measurements provide context for the claimed benefit "No scalar utility required" and the risk "No elitism". They do not isolate either mechanism; controlled ablation would be required for causal attribution.

Suitable: Small bi-objective populations; avoid: Many objectives with sparse dominance

## 12 NSGA

Front layers and within-front sharing

Advantages (mechanism-based): Explicit Pareto hierarchy;Sharing is local to fronts;No objective weights required;Variation supports arbitrary encodings

Disadvantages (mechanism-based): No elitism;Quadratic sorting and sharing;Dummy fitness spacing is arbitrary;Niche radius must be tuned

Evidence-linked strengths: NSGA recorded HV 1.1818 ± 6.7066e-05 on P5, IGD 0.013578 ± 0.0014855 (Figure A12). In the comparable P5 study with the same 10,000-evaluation cap, NSGA recorded HV 1.1818 ± 6.7066e-05; the nearest peer by mean HV was SPEA2 at 1.1818 ± 0.00012094, with runtime 8.2078 ± 0.36449 s versus 3.6444 ± 0.27288 s for NSGA. A separate P7 record gives HV 0.68866 ± 0.0014876 after 10000 ± 0 evaluations in 3.8733 ± 0.31273 s, so the evidence is not limited to one problem.

Evidence-linked limitations: The nonzero P5 IGD of 0.013578 ± 0.0014855 measures remaining sampled-front error. Thus the run does not support exact convergence or global optimality. Across 10 P5 trials, HV SD was 6.7066e-05 and runtime SD was 0.27288 s, which quantifies seed sensitivity at this budget.

Evidence boundary: The measurements provide context for the claimed benefit "Explicit Pareto hierarchy" and the risk "No elitism". They do not isolate either mechanism; controlled ablation would be required for causal attribution.

Suitable: Teaching early Pareto GAs; avoid: Large fast convergence requirements

## 13 NPGA

Direct contestant dominance then separate comparison-set quadratic niche tie

Advantages (mechanism-based): No fixed utility weights;Niche tie-break preserves sparse points;Comparison sample controls work;Can visit nonconvex tradeoffs

Disadvantages (mechanism-based): Nonelitist generations lose parents;Small comparison set gives noisy niche counts;Sigma changes density pressure;Lecture tournament differs from original publication

Evidence-linked strengths: NPGA recorded HV 0.45723 ± 0.07144 on P3, IGD 0.052909 ± 0.063934 (Figure A13). In the comparable P3 study with the same 10,000-evaluation cap, NPGA recorded HV 0.45723 ± 0.07144; the nearest peer by mean HV was MOPSO at 0.41909 ± 0.03166, with runtime 1.8638 ± 0.12697 s versus 6.4637 ± 0.38143 s for NPGA. A separate P5 record gives HV 1.1811 ± 0.00080777 after 10000 ± 0 evaluations in 6.7801 ± 0.44357 s, so the evidence is not limited to one problem.

Evidence-linked limitations: The nonzero P3 IGD of 0.052909 ± 0.063934 measures remaining sampled-front error. Thus the run does not support exact convergence or global optimality. Across 10 P3 trials, HV SD was 0.07144 and runtime SD was 0.38143 s, which quantifies seed sensitivity at this budget.

Evidence boundary: The measurements provide context for the claimed benefit "No fixed utility weights" and the risk "Nonelitist generations lose parents". They do not isolate either mechanism; controlled ablation would be required for causal attribution.

Suitable: Bi-objective diversity experiments; avoid: Many-objective fronts where most tournaments tie

## 14 NSGA-II

Front rank, crowding, parent-child elitism

Advantages (mechanism-based): Elitist survivor retention;Boundary points receive protection;No sharing radius;Permutation and real variation share selection

Disadvantages (mechanism-based): Crowding weakens as objectives grow;Quadratic pairwise sorting;Finite population truncates front;Crowding is not an explicit convergence measure

Evidence-linked strengths: NSGA-II recorded HV 0.52858 ± 0.0010011 on P3, IGD 0.012078 ± 0.0012439 (Figure A14). In the comparable P3 study with the same 10,000-evaluation cap, NSGA-II recorded HV 0.52858 ± 0.0010011; the nearest peer by mean HV was Constrained NSGA-II at 0.52858 ± 0.0010011, with runtime 3.3525 ± 0.089792 s versus 3.5278 ± 0.33619 s for NSGA-II. A separate P5 record gives HV 1.1818 ± 3.9631e-05 after 10000 ± 0 evaluations in 3.5675 ± 0.28869 s, so the evidence is not limited to one problem.

Evidence-linked limitations: The nonzero P3 IGD of 0.012078 ± 0.0012439 measures remaining sampled-front error. Thus the run does not support exact convergence or global optimality. Across 10 P3 trials, HV SD was 0.0010011 and runtime SD was 0.33619 s, which quantifies seed sensitivity at this budget.

Evidence boundary: The measurements provide context for the claimed benefit "Elitist survivor retention" and the risk "Crowding weakens as objectives grow". They do not isolate either mechanism; controlled ablation would be required for causal attribution.

Suitable: General constrained two-objective search; avoid: Very many objectives with weak dominance

## 15 NSGA-III

Reference-point niching after front rank

Advantages (mechanism-based): Reference niches control coverage;Supports many objectives;Occupancy encourages unused directions;Does not use a sharing radius

Disadvantages (mechanism-based): Range normalization simplifies original intercepts;Reference count grows combinatorially;Poor reference geometry biases coverage;Dominance layers still require quadratic work

Evidence-linked strengths: NSGA-III recorded HV 0.66113 ± 0.0058963 on P10, IGD 0.10798 ± 0.0058195 (Figure A15). In the comparable P10 study with the same 10,000-evaluation cap, NSGA-III recorded HV 0.98827 ± 0.018811; the nearest peer by mean HV was MOEA/D at 0.99538 ± 0.038577, with runtime 19.644 ± 0.8166 s versus 5.2657 ± 0.30871 s for NSGA-III. A separate P10 record gives HV 0.98827 ± 0.018811 after 10000 ± 0 evaluations in 5.2657 ± 0.30871 s, so the evidence is not limited to one problem.

Evidence-linked limitations: The nonzero P10 IGD of 0.10798 ± 0.0058195 measures remaining sampled-front error. Thus the run does not support exact convergence or global optimality. Across 10 P10 trials, HV SD was 0.0058963 and runtime SD was 0.45929 s, which quantifies seed sensitivity at this budget.

Evidence boundary: The measurements provide context for the claimed benefit "Reference niches control coverage" and the risk "Range normalization simplifies original intercepts". They do not isolate either mechanism; controlled ablation would be required for causal attribution.

Suitable: DTLZ2 with three or five objectives; avoid: Irregular fronts without adapted references

## 16 SPEA2

Strength, raw fitness and neighbour density

Advantages (mechanism-based): Strength combines domination information;Density distinguishes ties;Fixed archive bounds memory;Lexicographic truncation considers nearest distances

Disadvantages (mechanism-based): Quadratic distance storage;Repeated truncation adds cost;k-neighbour density depends on scale;Archive size limits attainable resolution

Evidence-linked strengths: SPEA2 recorded HV 0.93318 ± 0.0017067 on P4, and Spacing 0.014089 ± 0.0016077 where exact-front IGD is unavailable (Figure A16). In the comparable P5 study with the same 10,000-evaluation cap, SPEA2 recorded HV 1.1818 ± 0.00012094; the nearest peer by mean HV was NSGA at 1.1818 ± 6.7066e-05, with runtime 3.6169 ± 0.17249 s versus 8.2376 ± 0.35817 s for SPEA2. A separate P5 record gives HV 1.1818 ± 0.00012094 after 10000 ± 0 evaluations in 8.2376 ± 0.35817 s, so the evidence is not limited to one problem.

Evidence-linked limitations: No exact front is available for P4, so the run cannot experimentally establish convergence; HV 0.93318 ± 0.0017067 and Spacing 0.014089 ± 0.0016077 cover different questions. Across 10 P4 trials, HV SD was 0.0017067 and runtime SD was 0.087996 s, which quantifies seed sensitivity at this budget.

Evidence boundary: The measurements provide context for the claimed benefit "Strength combines domination information" and the risk "Quadratic distance storage". They do not isolate either mechanism; controlled ablation would be required for causal attribution.

Suitable: Small smooth front archives; avoid: Large populations with tight memory

## 17 PESA-II

Archive region occupancy selection

Advantages (mechanism-based): Region selection directly rewards sparsity;Archive keeps observed tradeoffs;Grid counts are interpretable;Less dependence on precise distances

Disadvantages (mechanism-based): Grid divisions sensitive;High-dimensional grids become sparse;Archive can shrink to few members;Grid boundaries change selection abruptly

Evidence-linked strengths: PESA-II recorded HV 0.511 ± 0.0071042 on P3, IGD 0.021934 ± 0.0033027 (Figure A17). In the comparable P3 study with the same 10,000-evaluation cap, PESA-II recorded HV 0.511 ± 0.0071042; the nearest peer by mean HV was MOABC at 0.50853 ± 0.0089927, with runtime 9.6225 ± 0.75254 s versus 5.2361 ± 0.23935 s for PESA-II. A separate P5 record gives HV 1.1811 ± 0.0005926 after 10000 ± 0 evaluations in 6.3281 ± 0.45901 s, so the evidence is not limited to one problem.

Evidence-linked limitations: The nonzero P3 IGD of 0.021934 ± 0.0033027 measures remaining sampled-front error. Thus the run does not support exact convergence or global optimality. Across 10 P3 trials, HV SD was 0.0071042 and runtime SD was 0.23935 s, which quantifies seed sensitivity at this budget.

Evidence boundary: The measurements provide context for the claimed benefit "Region selection directly rewards sparsity" and the risk "Grid divisions sensitive". They do not isolate either mechanism; controlled ablation would be required for causal attribution.

Suitable: Bi-objective region coverage; avoid: Many objectives with almost unique cells

## 18 MOEA/D

Neighbouring Tchebycheff subproblems

Advantages (mechanism-based): Cooperation shares good designs;Scalar subproblems retain pressure with many objectives;Neighbourhood limits update work;Weights provide coverage plan

Disadvantages (mechanism-based): Reference geometry biases front;Neighbourhood size affects spread;Shared donors can homogenize subproblems;Ideal updates alter scalar values

Evidence-linked strengths: MOEA/D recorded HV 0.99538 ± 0.038577 on P10, IGD 0.32121 ± 0.020673 (Figure A18). In the comparable P10 study with the same 10,000-evaluation cap, MOEA/D recorded HV 0.99538 ± 0.038577; the nearest peer by mean HV was NSGA-III at 0.98827 ± 0.018811, with runtime 5.3109 ± 0.27819 s versus 19.578 ± 0.88406 s for MOEA/D. A separate P3 record gives HV 0.53179 ± 8.6192e-05 after 10000 ± 0 evaluations in 14.443 ± 0.70036 s, so the evidence is not limited to one problem.

Evidence-linked limitations: The nonzero P10 IGD of 0.32121 ± 0.020673 measures remaining sampled-front error. Thus the run does not support exact convergence or global optimality. Across 10 P10 trials, HV SD was 0.038577 and runtime SD was 0.88406 s, which quantifies seed sensitivity at this budget.

Evidence boundary: The measurements provide context for the claimed benefit "Cooperation shares good designs" and the risk "Reference geometry biases front". They do not isolate either mechanism; controlled ablation would be required for causal attribution.

Suitable: Smooth continuous many-objective design; avoid: Disconnected fronts badly matched by weights

## 19 MOEA/D-DE

DE variation inside MOEA/D

Advantages (mechanism-based): DE exploits vector differences;Neighbour cooperation;Tchebycheff reaches nonconvex fronts;Forced crossover guarantees a changed coordinate

Disadvantages (mechanism-based): F and CR need tuning;DE requires enough distinct neighbours;Boundary clipping distorts donors;Weight coverage may be uneven

Evidence-linked strengths: MOEA/D-DE recorded HV 0.21242 ± 0.27423 on P3, IGD 1.0419 ± 0.9331 (Figure A19). In the comparable P3 study with the same 10,000-evaluation cap, MOEA/D-DE recorded HV 0.21242 ± 0.27423; the nearest peer by mean HV was Weighted Sum at 0.21 ± 1.4261e-11, with runtime 0.40343 ± 0.44449 s versus 11.795 ± 2.1489 s for MOEA/D-DE. A separate P5 record gives HV 1.1819 ± 3.2311e-05 after 10000 ± 0 evaluations in 12.836 ± 0.55488 s, so the evidence is not limited to one problem.

Evidence-linked limitations: The nonzero P3 IGD of 1.0419 ± 0.9331 measures remaining sampled-front error. Thus the run does not support exact convergence or global optimality. Across 10 P3 trials, HV SD was 0.27423 and runtime SD was 2.1489 s, which quantifies seed sensitivity at this budget.

Evidence boundary: The measurements provide context for the claimed benefit "DE exploits vector differences" and the risk "F and CR need tuning". They do not isolate either mechanism; controlled ablation would be required for causal attribution.

Suitable: Continuous real-coded nonconvex design; avoid: Permutation encodings without a new donor operator

## 20 MOEA/D-ACO

Weight-specific ant pheromones and scalar replacement

Advantages (mechanism-based): Valid tours by construction;Heuristic directs ant choices;Separate subproblems retain tradeoffs;Pheromone records good edges

Disadvantages (mechanism-based): Pheromone arrays cost N*cities^2;Deposits can lock routes;Alpha beta evaporation matter;Continuous encodings unsupported

Evidence-linked strengths: MOEA/D-ACO recorded HV 0.92348 ± 0.00073621 on P8, and Spacing 0.0036041 ± 0.0011622 where exact-front IGD is unavailable (Figure A20). In the comparable P8 study with the same 10,000-evaluation cap, MOEA/D-ACO recorded HV 0.92348 ± 0.00073621; the nearest peer by mean HV was MOMA at 0.92348 ± 0.0011631, with runtime 7.6185 ± 0.51051 s versus 26.418 ± 0.90564 s for MOEA/D-ACO. A separate P8 record gives HV 0.92348 ± 0.00073621 after 10000 ± 0 evaluations in 26.149 ± 0.97718 s, so the evidence is not limited to one problem.

Evidence-linked limitations: No exact front is available for P8, so the run cannot experimentally establish convergence; HV 0.92348 ± 0.00073621 and Spacing 0.0036041 ± 0.0011622 cover different questions. Across 10 P8 trials, HV SD was 0.00073621 and runtime SD was 0.90564 s, which quantifies seed sensitivity at this budget.

Evidence boundary: The measurements provide context for the claimed benefit "Valid tours by construction" and the risk "Pheromone arrays cost N*cities^2". They do not isolate either mechanism; controlled ablation would be required for causal attribution.

Suitable: Bi-objective routing; avoid: Smooth gradient problems

## 21 Constrained NSGA-II

NSGA-II with Deb feasibility

Advantages (mechanism-based): Feasible beats infeasible without objective penalty;Lower violation guides infeasible search;Pareto ranking within feasible;Crowding retains feasible diversity

Disadvantages (mechanism-based): Violation normalization affects infeasible order;Feasibility boundary can trap search;Quadratic ranking;Finite crowding resolution

Evidence-linked strengths: Constrained NSGA-II recorded HV 1.1818 ± 3.9631e-05 on P5, IGD 0.014057 ± 0.0012871 (Figure A21). In the comparable P5 study with the same 10,000-evaluation cap, Constrained NSGA-II recorded HV 1.1818 ± 3.9631e-05; the nearest peer by mean HV was NSGA-II at 1.1818 ± 3.9631e-05, with runtime 3.5601 ± 0.2764 s versus 3.3173 ± 0.34218 s for Constrained NSGA-II. A separate P6 record gives HV 1.0111 ± 0.0011787 after 10000 ± 0 evaluations in 3.3899 ± 0.30771 s, so the evidence is not limited to one problem.

Evidence-linked limitations: The nonzero P5 IGD of 0.014057 ± 0.0012871 measures remaining sampled-front error. Thus the run does not support exact convergence or global optimality. Across 10 P5 trials, HV SD was 3.9631e-05 and runtime SD was 0.34218 s, which quantifies seed sensitivity at this budget.

Evidence boundary: The measurements provide context for the claimed benefit "Feasible beats infeasible without objective penalty" and the risk "Violation normalization affects infeasible order". They do not isolate either mechanism; controlled ablation would be required for causal attribution.

Suitable: Constrained beam or Binh-Korn; avoid: Problems needing stochastic feasibility guarantees

## 22 MOPSO

Particle velocity with personal and archive leaders

Advantages (mechanism-based): Memory of personal successes;Few basic coefficients;Archive leader spreads movement;No crossover operator needed

Disadvantages (mechanism-based): Velocities can collapse;Boundary clipping affects dynamics;Leader policy controls diversity;Coefficients require tuning

Evidence-linked strengths: MOPSO recorded HV 0.92587 ± 0.0045498 on P4, and Spacing 0.013429 ± 0.0037554 where exact-front IGD is unavailable (Figure A22). In the comparable P5 study with the same 10,000-evaluation cap, MOPSO recorded HV 1.1816 ± 0.00064467; the nearest peer by mean HV was Weight Metric at 1.1817 ± 1.5148e-06, with runtime 3.4155 ± 0.29556 s versus 2.0314 ± 0.3814 s for MOPSO. A separate P5 record gives HV 1.1816 ± 0.00064467 after 10000 ± 0 evaluations in 2.0314 ± 0.3814 s, so the evidence is not limited to one problem.

Evidence-linked limitations: No exact front is available for P4, so the run cannot experimentally establish convergence; HV 0.92587 ± 0.0045498 and Spacing 0.013429 ± 0.0037554 cover different questions. Across 10 P4 trials, HV SD was 0.0045498 and runtime SD was 0.2485 s, which quantifies seed sensitivity at this budget.

Evidence boundary: The measurements provide context for the claimed benefit "Memory of personal successes" and the risk "Velocities can collapse". They do not isolate either mechanism; controlled ablation would be required for causal attribution.

Suitable: Continuous portfolio and beam designs; avoid: Permutation tours without discrete velocity

## 23 MOGWO

Three archive leaders and encircling

Advantages (mechanism-based): Multiple leaders guide movement;Coefficient shrinks automatically;Archive covers tradeoffs;Binary transfer enables masks

Disadvantages (mechanism-based): Averaging leaders may erase diversity;No strict improvement guarantee;Transfer sigmoid biases masks;Binary objective evaluation is costly

Evidence-linked strengths: MOGWO recorded HV 1.1817 ± 0.00011936 on P5, IGD 0.013415 ± 0.0012894 (Figure A23). In the comparable P5 study with the same 10,000-evaluation cap, MOGWO recorded HV 1.1817 ± 0.00011936; the nearest peer by mean HV was Weight Metric at 1.1817 ± 1.5148e-06, with runtime 3.4155 ± 0.29556 s versus 4.1017 ± 0.37263 s for MOGWO. A separate P9 record gives HV 0.78176 ± 0.042714 after 200 ± 0 evaluations in 30.445 ± 2.0142 s, so the evidence is not limited to one problem.

Evidence-linked limitations: The nonzero P5 IGD of 0.013415 ± 0.0012894 measures remaining sampled-front error. Thus the run does not support exact convergence or global optimality. Across 10 P5 trials, HV SD was 0.00011936 and runtime SD was 0.37263 s, which quantifies seed sensitivity at this budget.

Evidence boundary: The measurements provide context for the claimed benefit "Multiple leaders guide movement" and the risk "Averaging leaders may erase diversity". They do not isolate either mechanism; controlled ablation would be required for causal attribution.

Suitable: Continuous design or exploratory feature masks; avoid: Required stable high-accuracy feature conclusions on tiny budgets

## 24 MOABC

Employed moves, crowding-based onlookers and abandonment scouts

Advantages (mechanism-based): Scouts restart abandoned sources;Onlooker pressure favours sparse regions;Coordinate moves are inspectable;No gradients needed

Disadvantages (mechanism-based): Dominance-only greed can reject useful tradeoffs;Limit needs tuning;Three phases complicate budget accounting;One-coordinate changes may be slow

Evidence-linked strengths: MOABC recorded HV 0.50853 ± 0.0089927 on P3, IGD 0.022472 ± 0.0044901 (Figure A24). In the comparable P3 study with the same 10,000-evaluation cap, MOABC recorded HV 0.50853 ± 0.0089927; the nearest peer by mean HV was PESA-II at 0.511 ± 0.0071042, with runtime 5.2138 ± 0.18371 s versus 9.7198 ± 0.72292 s for MOABC. A separate P6 record gives HV 1.0157 ± 0.00027371 after 10000 ± 0 evaluations in 13.04 ± 1.2447 s, so the evidence is not limited to one problem.

Evidence-linked limitations: The nonzero P3 IGD of 0.022472 ± 0.0044901 measures remaining sampled-front error. Thus the run does not support exact convergence or global optimality. Across 10 P3 trials, HV SD was 0.0089927 and runtime SD was 0.72292 s, which quantifies seed sensitivity at this budget.

Evidence boundary: The measurements provide context for the claimed benefit "Scouts restart abandoned sources" and the risk "Dominance-only greed can reject useful tradeoffs". They do not isolate either mechanism; controlled ablation would be required for causal attribution.

Suitable: Small continuous design with restarts; avoid: Strongly coupled high-dimensional variables

## 25 MOACO

Two pheromone matrices and route construction

Advantages (mechanism-based): Produces valid permutations;Two objectives retain separate memories;Heuristic reduces random route work;Archive deposits reward tradeoffs

Disadvantages (mechanism-based): Strong evaporation forgets edges;Weak evaporation stagnates;Traffic/distance scales matter;No exact TSP optimality guarantee

Evidence-linked strengths: MOACO recorded HV 0.92394 ± 0 on P8, and Spacing 0.0031115 ± 0.00082031 where exact-front IGD is unavailable (Figure A25). In the comparable P8 study with the same 10,000-evaluation cap, MOACO recorded HV 0.92394 ± 0; the nearest peer by mean HV was NSGA-II at 0.92354 ± 0.0011666, with runtime 5.8743 ± 0.25408 s versus 18.135 ± 2.1703 s for MOACO. A separate P8 record gives HV 0.92394 ± 0 after 10000 ± 0 evaluations in 17.956 ± 1.854 s, so the evidence is not limited to one problem.

Evidence-linked limitations: No exact front is available for P8, so the run cannot experimentally establish convergence; HV 0.92394 ± 0 and Spacing 0.0031115 ± 0.00082031 cover different questions. The P8 output retained 5.2 ± 0.42164 point(s). That finite resolution limits what the plot can demonstrate; front size or zero Spacing alone is not evidence of complete coverage.

Evidence boundary: The measurements provide context for the claimed benefit "Produces valid permutations" and the risk "Strong evaporation forgets edges". They do not isolate either mechanism; controlled ablation would be required for causal attribution.

Suitable: Distance-time routing; avoid: Continuous portfolio allocation

## 26 MOSA

Incomparable neighbour acceptance and Boltzmann dominated moves

Advantages (mechanism-based): May accept uphill escape moves;Works without derivatives;Mutation adapts to encoding;Archive records tradeoffs from many chains

Disadvantages (mechanism-based): Cooling schedule sensitive;Local moves can miss distant regions;Incomparable moves remain random at low temperature;Finite cooling gives no global guarantee

Evidence-linked strengths: MOSA recorded HV 0.51354 ± 0.0060662 on P3, IGD 0.020405 ± 0.0038149 (Figure A26). In the comparable P3 study with the same 10,000-evaluation cap, MOSA recorded HV 0.51354 ± 0.0060662; the nearest peer by mean HV was PESA-II at 0.511 ± 0.0071042, with runtime 5.2138 ± 0.18371 s versus 1.4704 ± 0.13765 s for MOSA. A separate P5 record gives HV 1.1814 ± 0.00036639 after 10000 ± 0 evaluations in 1.5232 ± 0.11932 s, so the evidence is not limited to one problem.

Evidence-linked limitations: The nonzero P3 IGD of 0.020405 ± 0.0038149 measures remaining sampled-front error. Thus the run does not support exact convergence or global optimality. Across 10 P3 trials, HV SD was 0.0060662 and runtime SD was 0.13765 s, which quantifies seed sensitivity at this budget.

Evidence boundary: The measurements provide context for the claimed benefit "May accept uphill escape moves" and the risk "Cooling schedule sensitive". They do not isolate either mechanism; controlled ablation would be required for causal attribution.

Suitable: Budgeted local exploration on nonconvex fronts; avoid: Uniform global coverage with insufficient chains

## 27 MODE

DE dominance-only trial replacement

Advantages (mechanism-based): Simple vector donor;No utility weights;CR forces one donor coordinate;Dominating trials preserve target improvement

Disadvantages (mechanism-based): Incomparable trials do not replace targets;F CR sensitivity;Coordinate clipping can stagnate;Only real encoding is implemented

Evidence-linked strengths: MODE recorded HV 0.11 ± 3.0227e-10 on P3, IGD 0.6098 ± 1.1468e-10 (Figure A27). In the comparable P3 study with the same 10,000-evaluation cap, MODE recorded HV 0.11 ± 3.0227e-10; the nearest peer by mean HV was VEGA at 0.17298 ± 0.045825, with runtime 3.0357 ± 0.21072 s versus 1.7695 ± 0.068943 s for MODE. A separate P5 record gives HV 1.1807 ± 0.0020828 after 10000 ± 0 evaluations in 2.1901 ± 0.27727 s, so the evidence is not limited to one problem.

Evidence-linked limitations: The nonzero P3 IGD of 0.6098 ± 1.1468e-10 measures remaining sampled-front error. Thus the run does not support exact convergence or global optimality. Across 10 P3 trials, HV SD was 3.0227e-10 and runtime SD was 0.068943 s, which quantifies seed sensitivity at this budget.

Evidence boundary: The measurements provide context for the claimed benefit "Simple vector donor" and the risk "Incomparable trials do not replace targets". They do not isolate either mechanism; controlled ablation would be required for causal attribution.

Suitable: Continuous design with comparable improvements; avoid: Many objectives with almost no domination

## 28 MO-TLBO

Crowding archive teacher, shrinking TF and nondominated learner moves

Advantages (mechanism-based): No crossover design needed;Teacher encourages exploitation;Learners use peer information;Shrinking TF changes search scale

Disadvantages (mechanism-based): Teacher choice depends on archive;Incomparable moves can wander;Population means blur disconnected regions;TF schedule differs from conventional TLBO

Evidence-linked strengths: MO-TLBO recorded HV 0.53179 ± 7.0884e-05 on P3, IGD 0.0095087 ± 9.0745e-05 (Figure A28). In the comparable P3 study with the same 10,000-evaluation cap, MO-TLBO recorded HV 0.53179 ± 7.0884e-05; the nearest peer by mean HV was MOEA/D at 0.53179 ± 8.6192e-05, with runtime 14.525 ± 0.79452 s versus 11.386 ± 1.2374 s for MO-TLBO. A separate P5 record gives HV 1.1819 ± 1.6587e-05 after 10000 ± 0 evaluations in 11.361 ± 1.0124 s, so the evidence is not limited to one problem.

Evidence-linked limitations: The nonzero P3 IGD of 0.0095087 ± 9.0745e-05 measures remaining sampled-front error. Thus the run does not support exact convergence or global optimality. Across 10 P3 trials, HV SD was 7.0884e-05 and runtime SD was 1.2374 s, which quantifies seed sensitivity at this budget.

Evidence boundary: The measurements provide context for the claimed benefit "No crossover design needed" and the risk "Teacher choice depends on archive". They do not isolate either mechanism; controlled ablation would be required for causal attribution.

Suitable: Small continuous educational examples; avoid: Highly multimodal separated feasible regions

## 29 MOBA

Frequency velocity, pulse and loudness

Advantages (mechanism-based): Few interpretable schedules;Local walks exploit leaders;Frequency creates long moves;Archive records candidate tradeoffs

Disadvantages (mechanism-based): Loudness decay suppresses replacement;Velocity can explode then clip;Pulse schedule sensitive;Archive quality may exceed final-chain quality

Evidence-linked strengths: MOBA recorded HV 0.39676 ± 0.14429 on P3, IGD 0.12888 ± 0.16313 (Figure A29). In the comparable P3 study with the same 10,000-evaluation cap, MOBA recorded HV 0.39676 ± 0.14429; the nearest peer by mean HV was MOPSO at 0.41909 ± 0.03166, with runtime 1.8638 ± 0.12697 s versus 4.6044 ± 0.22895 s for MOBA. A separate P4 record gives HV 0.93318 ± 0.0012862 after 10000 ± 0 evaluations in 4.7957 ± 0.37886 s, so the evidence is not limited to one problem.

Evidence-linked limitations: The nonzero P3 IGD of 0.12888 ± 0.16313 measures remaining sampled-front error. Thus the run does not support exact convergence or global optimality. Across 10 P3 trials, HV SD was 0.14429 and runtime SD was 0.22895 s, which quantifies seed sensitivity at this budget.

Evidence boundary: The measurements provide context for the claimed benefit "Few interpretable schedules" and the risk "Loudness decay suppresses replacement". They do not isolate either mechanism; controlled ablation would be required for causal attribution.

Suitable: Continuous local refinement; avoid: Robust full-front exploration without schedule tuning

## 30 MOMA

NSGA-II plus sparse-child combined-score hill climbing

Advantages (mechanism-based): Local moves refine global children;Elitist survival;Works with binary/tour mutation;Local cost explicitly counted

Disadvantages (mechanism-based): Local calls reduce global generations;Combined-score preference changes tradeoffs;Mutation neighbourhood determines refinement;Feature CV makes local search costly

Evidence-linked strengths: MOMA recorded HV 1.1818 ± 5.8274e-05 on P5, IGD 0.01291 ± 0.0015554 (Figure A30). In the comparable P5 study with the same 10,000-evaluation cap, MOMA recorded HV 1.1818 ± 5.8274e-05; the nearest peer by mean HV was MOBA at 1.1818 ± 3.4425e-05, with runtime 4.2628 ± 0.30584 s versus 6.3309 ± 0.65198 s for MOMA. A separate P9 record gives HV 0.87363 ± 0.032115 after 200 ± 0 evaluations in 39.459 ± 6.7459 s, so the evidence is not limited to one problem.

Evidence-linked limitations: The nonzero P5 IGD of 0.01291 ± 0.0015554 measures remaining sampled-front error. Thus the run does not support exact convergence or global optimality. Across 10 P5 trials, HV SD was 5.8274e-05 and runtime SD was 0.65198 s, which quantifies seed sensitivity at this budget.

Evidence boundary: The measurements provide context for the claimed benefit "Local moves refine global children" and the risk "Local calls reduce global generations". They do not isolate either mechanism; controlled ablation would be required for causal attribution.

Suitable: Beam refinement or routing; avoid: Expensive objectives with no local structure

## 31 RVEA

Normalized reference vectors and lecture linear-progress APD

Advantages (mechanism-based): Angular niches aid many objectives;APD shifts toward convergence;Vector adaptation tracks scales;Sparse niches can retain representatives

Disadvantages (mechanism-based): Penalty strength and adaptation period matter;Observed ranges can be unstable;Empty niches require fill policy;Reference alignment can bias coverage

Evidence-linked strengths: RVEA recorded HV 0.64035 ± 0.011426 on P10, IGD 0.10879 ± 0.0032335 (Figure A31). In the comparable P10 study with the same 10,000-evaluation cap, RVEA recorded HV 1.0121 ± 0.030242; the nearest peer by mean HV was MOEA/D at 0.99538 ± 0.038577, with runtime 19.644 ± 0.8166 s versus 4.9951 ± 0.52206 s for RVEA. A separate P10 record gives HV 1.0121 ± 0.030242 after 10000 ± 0 evaluations in 4.9951 ± 0.52206 s, so the evidence is not limited to one problem.

Evidence-linked limitations: The nonzero P10 IGD of 0.10879 ± 0.0032335 measures remaining sampled-front error. Thus the run does not support exact convergence or global optimality. Across 10 P10 trials, HV SD was 0.011426 and runtime SD was 0.57606 s, which quantifies seed sensitivity at this budget.

Evidence boundary: The measurements provide context for the claimed benefit "Angular niches aid many objectives" and the risk "Penalty strength and adaptation period matter". They do not isolate either mechanism; controlled ablation would be required for causal attribution.

Suitable: Five-objective DTLZ2; avoid: Strongly irregular disconnected fronts

## 32 IBEA

Outgoing additive-epsilon fitness and largest-fitness deletion

Advantages (mechanism-based): No separate sharing operator;Indicator gives selection pressure;Works on nonconvex fronts;Kappa controls discrimination

Disadvantages (mechanism-based): Exponentials can saturate;Kappa changes selection;Recalculated deletion is costly;Fitness depends strongly on scales

Evidence-linked strengths: IBEA recorded HV 0.81944 ± 0.012245 on P14, IGD 0.026183 ± 0.0076532 (Figure A32). In the comparable P3 study with the same 10,000-evaluation cap, IBEA recorded HV 0.19276 ± 0.017015; the nearest peer by mean HV was Benson reference improvement at 0.21 ± 9.8457e-12, with runtime 0.4763 ± 0.072962 s versus 11.449 ± 1.0226 s for IBEA. A separate P3 record gives HV 0.19276 ± 0.017015 after 10000 ± 0 evaluations in 11.449 ± 1.0226 s, so the evidence is not limited to one problem.

Evidence-linked limitations: The nonzero P14 IGD of 0.026183 ± 0.0076532 measures remaining sampled-front error. Thus the run does not support exact convergence or global optimality. Across 10 P14 trials, HV SD was 0.012245 and runtime SD was 0.66806 s, which quantifies seed sensitivity at this budget.

Evidence boundary: The measurements provide context for the claimed benefit "No separate sharing operator" and the risk "Exponentials can saturate". They do not isolate either mechanism; controlled ablation would be required for causal attribution.

Suitable: Small bi-objective indicator experiments; avoid: Large populations with limited CPU

## 33 SMS-EMOA

Steady-state smallest HV deletion

Advantages (mechanism-based): Direct quality indicator survival;One-offspring updates are simple;Exact two-objective contribution;Protects coverage within the chosen reference

Disadvantages (mechanism-based): HV reference controls preferences;One-at-a-time sorting costs many calls;Implemented only for two objectives;HV can prioritize extremes unevenly

Evidence-linked strengths: SMS-EMOA recorded HV 0.85873 ± 1.9917e-05 on P14, IGD 0.0075773 ± 1.8795e-05 (Figure A33). In the comparable P3 study with the same 10,000-evaluation cap, SMS-EMOA recorded HV 0.53181 ± 0.00010904; the nearest peer by mean HV was MOEA/D at 0.53179 ± 8.6192e-05, with runtime 14.525 ± 0.79452 s versus 31.093 ± 1.9721 s for SMS-EMOA. A separate P3 record gives HV 0.53181 ± 0.00010904 after 10000 ± 0 evaluations in 31.093 ± 1.9721 s, so the evidence is not limited to one problem.

Evidence-linked limitations: The nonzero P14 IGD of 0.0075773 ± 1.8795e-05 measures remaining sampled-front error. Thus the run does not support exact convergence or global optimality. Across 10 P14 trials, HV SD was 1.9917e-05 and runtime SD was 1.6848 s, which quantifies seed sensitivity at this budget.

Evidence boundary: The measurements provide context for the claimed benefit "Direct quality indicator survival" and the risk "HV reference controls preferences". They do not isolate either mechanism; controlled ablation would be required for causal attribution.

Suitable: Small bi-objective design; avoid: Many objectives without an HV approximation

## 34 HypE

Equal-share Monte Carlo HV fitness and repeated deletion

Advantages (mechanism-based): HV sharing supports many objectives;Shared samples account for overlapping domination;Re-estimation updates remaining credit;Final evaluation samples are identical across methods

Disadvantages (mechanism-based): Sampling noise changes survivors;Selection sample count is small;Repeated deletion costs CPU;HV still needs a reference box

Evidence-linked strengths: HypE recorded HV 0.6611 ± 0.0082237 on P10, IGD 0.11712 ± 0.0042523 (Figure A34). In the comparable P10 study with the same 10,000-evaluation cap, HypE recorded HV 0.80567 ± 0.14729; the nearest peer by mean HV was NSGA-III at 0.98827 ± 0.018811, with runtime 5.3109 ± 0.27819 s versus 23.724 ± 1.8975 s for HypE. A separate P10 record gives HV 0.80567 ± 0.14729 after 10000 ± 0 evaluations in 23.724 ± 1.8975 s, so the evidence is not limited to one problem.

Evidence-linked limitations: The nonzero P10 IGD of 0.11712 ± 0.0042523 measures remaining sampled-front error. Thus the run does not support exact convergence or global optimality. Across 10 P10 trials, HV SD was 0.0082237 and runtime SD was 0.60127 s, which quantifies seed sensitivity at this budget.

Evidence boundary: The measurements provide context for the claimed benefit "HV sharing supports many objectives" and the risk "Sampling noise changes survivors". They do not isolate either mechanism; controlled ablation would be required for causal attribution.

Suitable: Many-objective indicator study; avoid: High-precision survival contribution estimates

## 35 R-NSGA-II

Reference preference and epsilon clearing

Advantages (mechanism-based): Focuses on desired region;Clearing promotes local diversity;Retains nondominated hierarchy;Preference is physically interpretable on P14

Disadvantages (mechanism-based): Wrong aspiration biases search;Epsilon controls local spacing;Full-front quality can drop;Default balanced aspiration is arbitrary

Evidence-linked strengths: R-NSGA-II recorded HV 0.85563 ± 0.00087984 on P14, IGD 0.010043 ± 0.00082871 (Figure A35). In the comparable P5 study with the same 10,000-evaluation cap, R-NSGA-II recorded HV 1.1758 ± 0.014288; the nearest peer by mean HV was VEGA at 1.1805 ± 0.0012363, with runtime 3.3831 ± 0.12189 s versus 4.8108 ± 0.3217 s for R-NSGA-II. A separate P5 record gives HV 1.1758 ± 0.014288 after 10000 ± 0 evaluations in 4.8108 ± 0.3217 s, so the evidence is not limited to one problem.

Evidence-linked limitations: The nonzero P14 IGD of 0.010043 ± 0.00082871 measures remaining sampled-front error. Thus the run does not support exact convergence or global optimality. Across 10 P14 trials, HV SD was 0.00087984 and runtime SD was 0.33328 s, which quantifies seed sensitivity at this budget.

Evidence boundary: The measurements provide context for the claimed benefit "Focuses on desired region" and the risk "Wrong aspiration biases search". They do not isolate either mechanism; controlled ablation would be required for causal attribution.

Suitable: Decision-maker laptop region; avoid: Unknown or frequently changing preferences

## 36 MGDA

Minimum-norm gradient combination

Advantages (mechanism-based): Common descent when norm is nonzero;Analytical two-task weights;No objective-scale utility required;Can converge to Pareto stationarity

Disadvantages (mechanism-based): Requires gradients;Stationarity is not full-front coverage;May stop while each task has gradient;Nonconvex network optima are local

Evidence-linked strengths: MGDA recorded HV 0.28389 ± 0 on P13, IGD 0.62794 ± 0 (Figure A36). The run used 10000 ± 0 evaluations and took 2.3516 ± 0 s; no same-problem comparison row is used to manufacture a benchmark claim. The saved result supports finite-run quality and cost only, not an asymptotic efficiency claim.

Evidence-linked limitations: The nonzero P13 IGD of 0.62794 ± 0 measures remaining sampled-front error. Thus the run does not support exact convergence or global optimality. The P13 output retained 1 ± 0 point(s). That finite resolution limits what the plot can demonstrate; front size or zero Spacing alone is not evidence of complete coverage.

Evidence boundary: The measurements provide context for the claimed benefit "Common descent when norm is nonzero" and the risk "Requires gradients". They do not isolate either mechanism; controlled ablation would be required for causal attribution.

Suitable: Differentiable conflicting tasks; avoid: Discrete designs or a full Pareto-front sweep

## 37 GradNorm

Gradient-norm adaptive task weights

Advantages (mechanism-based): Balances task gradient magnitudes;Training rates influence targets;Hand-derived update is inspectable;Task-scale stress can be evaluated

Disadvantages (mechanism-based): Requires gradients and initial losses;Alpha weight_lr matter;Does not guarantee common descent;Toy final point is not an entire front

Evidence-linked strengths: GradNorm recorded HV 0.60519 ± 0 on P13, IGD 0.43296 ± 0 (Figure A37). The run used 10000 ± 0 evaluations and took 2.6674 ± 0 s; no same-problem comparison row is used to manufacture a benchmark claim. The saved result supports finite-run quality and cost only, not an asymptotic efficiency claim.

Evidence-linked limitations: The nonzero P13 IGD of 0.43296 ± 0 measures remaining sampled-front error. Thus the run does not support exact convergence or global optimality. The P13 output retained 1 ± 0 point(s). That finite resolution limits what the plot can demonstrate; front size or zero Spacing alone is not evidence of complete coverage.

Evidence boundary: The measurements provide context for the claimed benefit "Balances task gradient magnitudes" and the risk "Requires gradients and initial losses". They do not isolate either mechanism; controlled ablation would be required for causal attribution.

Suitable: Shared network with unequal loss gradients; avoid: A guaranteed Pareto descent method


## Family comparison
Classical methods convert preferences or bounds into scalar solves, making their numerical accuracy depend on the scalar solver. Early GAs use objective selection, rank or sharing without parent elitism; the passive archive records discoveries but does not prevent the breeding population from losing them. Elitist methods spend quadratic comparisons to retain high-ranked parents and use crowding, density or grids for diversity. Decomposition gives each direction its own scalar pressure, although a fixed lattice may not match disconnected fronts. Swarms and local heuristics rely on archive leaders and neighbourhood moves; their schedules can exploit quickly or stagnate. Indicators replace explicit density with epsilon or hypervolume fitness but require scales and, for HV, a reference box. Reference methods remain useful when dominance loses discrimination in five dimensions. Preferences intentionally trade full-front coverage for a useful region. Gradient methods optimize differentiable tasks toward stationarity and do not produce a full front from one start. Feasibility rules are applied before Pareto comparisons, and comparisons use common normalized metric scales.