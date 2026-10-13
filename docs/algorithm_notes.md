# Task B algorithm comparison

Measured output quality and theoretical mechanisms are distinguished. Values refer to normalized metrics with fixed scales. Each method has two explicit measured-use links and two measured cautions; these observations do not turn untested mechanism claims into causal conclusions.

## 1 Weighted Sum

Linear scalar solve and a sweep

Advantages (reasoned): Simple scalar objective;Direct preference weights;Reusable constrained scalar solver;Independent solves can be distributed

Disadvantages (reasoned): Unsupported nonconvex points are unreachable;Scaling changes weight meaning;Uniform weights give nonuniform spacing;Local scalar solves lack global guarantees

Measured run: Task A P1: HV 1.0258 +/- 0; IGD 0.020135 +/- 0; Spacing 1.5349e-08 +/- 0; front size 21 +/- 0; runtime 1.1064 +/- 0 s.

Measured links to use: 1) HV=1.0258 +/- 0 records achieved normalized dominated volume; 2) IGD=0.020135 +/- 0 measures distance to the sampled exact front.

Measured cautions: 1) The recorded front has 21 +/- 0 points and cannot certify complete coverage; 2) runtime=1.1064 +/- 0 s at 168 +/- 0 evaluations quantifies finite-budget cost, not asymptotic efficiency.

Evidence boundary: Measured links support achieved quality, coverage limits and cost observations. Mechanism-specific causal claims require additional targeted ablations; these are labelled reasoned.

Suitable: Convex smooth two-objective design with interpretable weights; avoid: Dented fronts and an unknown preference distribution

## 2 Epsilon-Constraint

One objective minimized and others bounded

Advantages (reasoned): Can represent unsupported efficient points;Epsilon has physical interpretation;Scalar constraints remain explicit;Primary objective stays recognizable

Disadvantages (reasoned): Infeasible epsilon values waste solves;Sweeps can duplicate points;Constraint solver quality matters;Many objectives require multidimensional epsilon grids

Measured run: Task A P2: HV 1.0865 +/- 0; IGD 0.037129 +/- 0; Spacing 0.14183 +/- 0; front size 21 +/- 0; runtime 0.23309 +/- 0 s.

Measured links to use: 1) HV=1.0865 +/- 0 records achieved normalized dominated volume; 2) IGD=0.037129 +/- 0 measures distance to the sampled exact front.

Measured cautions: 1) The recorded front has 21 +/- 0 points and cannot certify complete coverage; 2) runtime=0.23309 +/- 0 s at 870 +/- 0 evaluations quantifies finite-budget cost, not asymptotic efficiency.

Evidence boundary: Measured links support achieved quality, coverage limits and cost observations. Mechanism-specific causal claims require additional targeted ablations; these are labelled reasoned.

Suitable: Nonconvex constrained design with hard limits; avoid: High-dimensional objective grids

## 3 Benson reference improvement

Weighted improvement below a reference

Advantages (reasoned): Reference conveys aspiration;Nonnegative improvement is interpretable;Explicit upper objective bounds;Scalar subproblems are easy to inspect

Disadvantages (reasoned): This is the lecture achievement form, not outer approximation;Unrestricted reference sweeps inherit weighted-sum barrier;Reference coordinates require scaling;Weights still encode preferences

Measured run: Task A P1: HV 1.0258 +/- 0; IGD 0.020135 +/- 0; Spacing 2.7354e-08 +/- 0; front size 21 +/- 0; runtime 0.17368 +/- 0 s.

Measured links to use: 1) HV=1.0258 +/- 0 records achieved normalized dominated volume; 2) IGD=0.020135 +/- 0 measures distance to the sampled exact front.

Measured cautions: 1) The recorded front has 21 +/- 0 points and cannot certify complete coverage; 2) runtime=0.17368 +/- 0 s at 714 +/- 0 evaluations quantifies finite-budget cost, not asymptotic efficiency.

Evidence boundary: Measured links support achieved quality, coverage limits and cost observations. Mechanism-specific causal claims require additional targeted ablations; these are labelled reasoned.

Suitable: Teaching reference improvement on P1/P7; avoid: Claiming a general Benson convergence theorem

## 4 Weight Metric

Weighted distance to fixed ideal

Advantages (reasoned): Infinity norm can reach unsupported tradeoffs;Different p values express balance;Ideal point makes distances interpretable;Scalar solver is reusable

Disadvantages (reasoned): Ideal estimation affects solution;Max norm is nonsmooth;p and weights require preferences;Finite weight sweep misses narrow regions

Measured run: Task A P1: HV 1.0347 +/- 0; IGD 0.012339 +/- 0; Spacing 0.023805 +/- 0; front size 63 +/- 0; runtime 0.64793 +/- 0 s.

Measured links to use: 1) HV=1.0347 +/- 0 records achieved normalized dominated volume; 2) IGD=0.012339 +/- 0 measures distance to the sampled exact front.

Measured cautions: 1) The recorded front has 63 +/- 0 points and cannot certify complete coverage; 2) runtime=0.64793 +/- 0 s at 1857 +/- 0 evaluations quantifies finite-budget cost, not asymptotic efficiency.

Evidence boundary: Measured links support achieved quality, coverage limits and cost observations. Mechanism-specific causal claims require additional targeted ablations; these are labelled reasoned.

Suitable: Compromise solutions on nonconvex fronts; avoid: Unreliable ideal estimates or many weights

## 5 Value Function

Declared decision-maker utility

Advantages (reasoned): Directly encodes a preferred outcome;Can express nonlinear preferences;Few scalar solves are economical;Natural targets communicate decisions

Disadvantages (reasoned): Utility must be elicited;Squared target utility need not be monotone;One preferred design is not a full front;Misspecified preferences bias results

Measured run: Task A P14: HV 0.32905 +/- 0; IGD 0.35302 +/- 0; Spacing 0 +/- 0; front size 1 +/- 0; runtime 0.022336 +/- 0 s.

Measured links to use: 1) HV=0.32905 +/- 0 records achieved normalized dominated volume; 2) IGD=0.35302 +/- 0 measures distance to the sampled exact front.

Measured cautions: 1) The recorded front has 1 +/- 0 points and cannot certify complete coverage; 2) runtime=0.022336 +/- 0 s at 45 +/- 0 evaluations quantifies finite-budget cost, not asymptotic efficiency.

Evidence boundary: Measured links support achieved quality, coverage limits and cost observations. Mechanism-specific causal claims require additional targeted ablations; these are labelled reasoned.

Suitable: Laptop or portfolio profile decisions; avoid: Exploration without known preferences

## 6 Goal Programming

Explicit positive/negative goal deviations

Advantages (reasoned): Shows unavoidable shortfall;Can normalize incompatible units;Soft goals remain interpretable;Constraint and aspiration roles are separate

Disadvantages (reasoned): Goal weights control tradeoffs;Infeasible goals cannot be guaranteed;Units can overwhelm deviations;Satisfied goals may leave efficiency ties

Measured run: Task A P11: HV 1.21 +/- 0; IGD 9.6355e-11 +/- 0; Spacing 0 +/- 0; front size 1 +/- 0; runtime 0.52765 +/- 0 s.

Measured links to use: 1) HV=1.21 +/- 0 records achieved normalized dominated volume; 2) IGD=9.6355e-11 +/- 0 measures distance to the sampled exact front.

Measured cautions: 1) The recorded front has 1 +/- 0 points and cannot certify complete coverage; 2) runtime=0.52765 +/- 0 s at 1219 +/- 0 evaluations quantifies finite-budget cost, not asymptotic efficiency.

Evidence boundary: Measured links support achieved quality, coverage limits and cost observations. Mechanism-specific causal claims require additional targeted ablations; these are labelled reasoned.

Suitable: Production targets with soft priorities; avoid: Searching an entire front without goals

## 7 Lexicographic

Sequential strict priorities with tolerances

Advantages (reasoned): Priority order is transparent;Breaks first-objective ties;Uses scalar solvers;Preserves prior objective values to declared tolerance

Disadvantages (reasoned): Lower objectives may have little freedom;Tolerance changes strictness;Priority mistakes are expensive;Sequential solves add cost

Measured run: Task A P11: HV 1.21 +/- 0; IGD 1.6309e-11 +/- 0; Spacing 0 +/- 0; front size 1 +/- 0; runtime 0.08428 +/- 0 s.

Measured links to use: 1) HV=1.21 +/- 0 records achieved normalized dominated volume; 2) IGD=1.6309e-11 +/- 0 measures distance to the sampled exact front.

Measured cautions: 1) The recorded front has 1 +/- 0 points and cannot certify complete coverage; 2) runtime=0.08428 +/- 0 s at 219 +/- 0 evaluations quantifies finite-budget cost, not asymptotic efficiency.

Evidence boundary: Measured links support achieved quality, coverage limits and cost observations. Mechanism-specific causal claims require additional targeted ablations; these are labelled reasoned.

Suitable: Profit first and units second; avoid: Balanced objectives with no hierarchy

## 8 TOPSIS

Closeness to weighted ideal and anti-ideal

Advantages (reasoned): Fast finite-table ranking;Uses all criteria;Distances are explainable;Works with benefit and cost columns

Disadvantages (reasoned): Does not generate new designs;Vector normalization affects rank;Compensation can hide a bad criterion;Alternatives can change the ideal

Measured run: P12 w=[0.3, 0.3, 0.2, 0.2] v=0.5: top 3 [3, 1, 5]; P12 w=[0.4, 0.2, 0.2, 0.2] v=0.5: top 3 [1, 2, 3]; P4 NSGA-II front w=[0.5, 0.5] v=0.5: top 3 [18, 22, 2]; P4 NSGA-II front w=[0.6, 0.4] v=0.5: top 3 [32, 8, 3]

Measured links to use: 1) Two weight settings produce traceable ranked orders; 2) both P12 and a generated P4 front are evaluated.

Measured cautions: 1) Only existing alternatives are ranked; 2) preference sensitivity does not demonstrate search or global optimality.

Evidence boundary: Measured links support achieved quality, coverage limits and cost observations. Mechanism-specific causal claims require additional targeted ablations; these are labelled reasoned.

Suitable: Supplier or existing-front ranking; avoid: Optimization without an alternatives table

## 9 VIKOR

Compromise via group regret and worst regret

Advantages (reasoned): Worst criterion enters R;v exposes group versus individual tradeoff;Compromise conditions avoid forced winners;Finite rankings are inexpensive

Disadvantages (reasoned): Requires preference weights;v can change rank;Range normalization changes regrets;Does not generate designs

Measured run: P12 w=[0.3, 0.3, 0.2, 0.2] v=0.25: top 3 [1, 2, 5]; P12 w=[0.4, 0.2, 0.2, 0.2] v=0.25: top 3 [2, 1, 4]; P12 w=[0.3, 0.3, 0.2, 0.2] v=0.5: top 3 [1, 2, 5]; P12 w=[0.4, 0.2, 0.2, 0.2] v=0.5: top 3 [2, 1, 3]; P12 w=[0.3, 0.3, 0.2, 0.2] v=0.75: top 3 [1, 3, 2]; P12 w=[0.4, 0.2, 0.2, 0.2] v=0.75: top 3 [1, 2, 3]; P4 NSGA-II front w=[0.5, 0.5] v=0.5: top 3 [2, 38, 35]; P4 NSGA-II front w=[0.6, 0.4] v=0.5: top 3 [8, 32, 3]

Measured links to use: 1) Two weight settings produce traceable ranked orders; 2) both P12 and a generated P4 front are evaluated.

Measured cautions: 1) Only existing alternatives are ranked; 2) preference sensitivity does not demonstrate search or global optimality.

Evidence boundary: Measured links support achieved quality, coverage limits and cost observations. Mechanism-specific causal claims require additional targeted ablations; these are labelled reasoned.

Suitable: Supplier compromise with severe weak criteria; avoid: A Pareto front generator

## 10 VEGA

Objective-partitioned selection

Advantages (reasoned): Very simple selection;No preference weights needed;Handles several objective contests;Cheap scalar tournaments

Disadvantages (reasoned): Extremes can dominate mating pool;No parent elitism;Middle tradeoffs may disappear;Objective partition sizes affect pressure

Measured run: Task A P2: HV 1.1109 +/- 0.00092541; IGD 0.014362 +/- 0.0015584; Spacing 0.017002 +/- 0.0027901; front size 40 +/- 0; runtime 3.0395 +/- 0.27359 s.

Measured links to use: 1) HV=1.1109 +/- 0.00092541 records achieved normalized dominated volume; 2) IGD=0.014362 +/- 0.0015584 measures distance to the sampled exact front.

Measured cautions: 1) The recorded front has 40 +/- 0 points and cannot certify complete coverage; 2) runtime=3.0395 +/- 0.27359 s at 10000 +/- 0 evaluations quantifies finite-budget cost, not asymptotic efficiency.

Evidence boundary: Measured links support achieved quality, coverage limits and cost observations. Mechanism-specific causal claims require additional targeted ablations; these are labelled reasoned.

Suitable: Teaching objective competition; avoid: Reliable uniform front preservation

## 11 MOGA

Domination-count rank and fitness sharing

Advantages (reasoned): No scalar utility required;Sharing promotes sparse niches;Dominance counts are easy to inspect;Can search unsupported regions

Disadvantages (reasoned): No elitism;Sharing radius sensitive;All nondominated members tie in rank;Pairwise density costs quadratically

Measured run: Task A P3: HV 0.52378 +/- 0.0010854; IGD 0.012703 +/- 0.00047311; Spacing 0.012773 +/- 0.002314; front size 40 +/- 0; runtime 3.7674 +/- 0.43826 s.

Measured links to use: 1) HV=0.52378 +/- 0.0010854 records achieved normalized dominated volume; 2) IGD=0.012703 +/- 0.00047311 measures distance to the sampled exact front.

Measured cautions: 1) The recorded front has 40 +/- 0 points and cannot certify complete coverage; 2) runtime=3.7674 +/- 0.43826 s at 10000 +/- 0 evaluations quantifies finite-budget cost, not asymptotic efficiency.

Evidence boundary: Measured links support achieved quality, coverage limits and cost observations. Mechanism-specific causal claims require additional targeted ablations; these are labelled reasoned.

Suitable: Small bi-objective populations; avoid: Many objectives with sparse dominance

## 12 NSGA

Front layers and within-front sharing

Advantages (reasoned): Explicit Pareto hierarchy;Sharing is local to fronts;No objective weights required;Variation supports arbitrary encodings

Disadvantages (reasoned): No elitism;Quadratic sorting and sharing;Dummy fitness spacing is arbitrary;Niche radius must be tuned

Measured run: Task A P5: HV 1.1818 +/- 6.7066e-05; IGD 0.013578 +/- 0.0014855; Spacing 0.019587 +/- 0.0029038; front size 40 +/- 0; runtime 3.6444 +/- 0.27288 s.

Measured links to use: 1) HV=1.1818 +/- 6.7066e-05 records achieved normalized dominated volume; 2) IGD=0.013578 +/- 0.0014855 measures distance to the sampled exact front.

Measured cautions: 1) The recorded front has 40 +/- 0 points and cannot certify complete coverage; 2) runtime=3.6444 +/- 0.27288 s at 10000 +/- 0 evaluations quantifies finite-budget cost, not asymptotic efficiency.

Evidence boundary: Measured links support achieved quality, coverage limits and cost observations. Mechanism-specific causal claims require additional targeted ablations; these are labelled reasoned.

Suitable: Teaching early Pareto GAs; avoid: Large fast convergence requirements

## 13 NPGA

Direct contestant dominance then separate comparison-set quadratic niche tie

Advantages (reasoned): No fixed utility weights;Niche tie-break preserves sparse points;Comparison sample controls work;Can visit nonconvex tradeoffs

Disadvantages (reasoned): Nonelitist generations lose parents;Small comparison set gives noisy niche counts;Sigma changes density pressure;Lecture tournament differs from original publication

Measured run: Task A P3: HV 0.45723 +/- 0.07144; IGD 0.052909 +/- 0.063934; Spacing 0.032899 +/- 0.019469; front size 36.9 +/- 4.1218; runtime 6.4637 +/- 0.38143 s.

Measured links to use: 1) HV=0.45723 +/- 0.07144 records achieved normalized dominated volume; 2) IGD=0.052909 +/- 0.063934 measures distance to the sampled exact front.

Measured cautions: 1) The recorded front has 36.9 +/- 4.1218 points and cannot certify complete coverage; 2) runtime=6.4637 +/- 0.38143 s at 10000 +/- 0 evaluations quantifies finite-budget cost, not asymptotic efficiency.

Evidence boundary: Measured links support achieved quality, coverage limits and cost observations. Mechanism-specific causal claims require additional targeted ablations; these are labelled reasoned.

Suitable: Bi-objective diversity experiments; avoid: Many-objective fronts where most tournaments tie

## 14 NSGA-II

Front rank, crowding, parent-child elitism

Advantages (reasoned): Elitist survivor retention;Boundary points receive protection;No sharing radius;Permutation and real variation share selection

Disadvantages (reasoned): Crowding weakens as objectives grow;Quadratic pairwise sorting;Finite population truncates front;Crowding is not an explicit convergence measure

Measured run: Task A P3: HV 0.52858 +/- 0.0010011; IGD 0.012078 +/- 0.0012439; Spacing 0.017655 +/- 0.0017465; front size 40 +/- 0; runtime 3.5278 +/- 0.33619 s.

Measured links to use: 1) HV=0.52858 +/- 0.0010011 records achieved normalized dominated volume; 2) IGD=0.012078 +/- 0.0012439 measures distance to the sampled exact front.

Measured cautions: 1) The recorded front has 40 +/- 0 points and cannot certify complete coverage; 2) runtime=3.5278 +/- 0.33619 s at 10000 +/- 0 evaluations quantifies finite-budget cost, not asymptotic efficiency.

Evidence boundary: Measured links support achieved quality, coverage limits and cost observations. Mechanism-specific causal claims require additional targeted ablations; these are labelled reasoned.

Suitable: General constrained two-objective search; avoid: Very many objectives with weak dominance

## 15 NSGA-III

Reference-point niching after front rank

Advantages (reasoned): Reference niches control coverage;Supports many objectives;Occupancy encourages unused directions;Does not use a sharing radius

Disadvantages (reasoned): Range normalization simplifies original intercepts;Reference count grows combinatorially;Poor reference geometry biases coverage;Dominance layers still require quadratic work

Measured run: Task A P10: HV 0.66113 +/- 0.0058963; IGD 0.10798 +/- 0.0058195; Spacing 0.099172 +/- 0.010105; front size 40 +/- 0; runtime 5.1274 +/- 0.45929 s.

Measured links to use: 1) HV=0.66113 +/- 0.0058963 records achieved normalized dominated volume; 2) IGD=0.10798 +/- 0.0058195 measures distance to the sampled exact front.

Measured cautions: 1) The recorded front has 40 +/- 0 points and cannot certify complete coverage; 2) runtime=5.1274 +/- 0.45929 s at 10000 +/- 0 evaluations quantifies finite-budget cost, not asymptotic efficiency.

Evidence boundary: Measured links support achieved quality, coverage limits and cost observations. Mechanism-specific causal claims require additional targeted ablations; these are labelled reasoned.

Suitable: DTLZ2 with three or five objectives; avoid: Irregular fronts without adapted references

## 16 SPEA2

Strength, raw fitness and neighbour density

Advantages (reasoned): Strength combines domination information;Density distinguishes ties;Fixed archive bounds memory;Lexicographic truncation considers nearest distances

Disadvantages (reasoned): Quadratic distance storage;Repeated truncation adds cost;k-neighbour density depends on scale;Archive size limits attainable resolution

Measured run: Task A P4: HV 0.93318 +/- 0.0017067; IGD N/A +/- N/A; Spacing 0.014089 +/- 0.0016077; front size 40 +/- 0; runtime 6.1215 +/- 0.087996 s.

Measured links to use: 1) HV=0.93318 +/- 0.0017067 records achieved normalized dominated volume; 2) Spacing=0.014089 +/- 0.0016077 measures within-front regularity because exact-front IGD is unavailable.

Measured cautions: 1) The recorded front has 40 +/- 0 points and cannot certify complete coverage; 2) runtime=6.1215 +/- 0.087996 s at 10000 +/- 0 evaluations quantifies finite-budget cost, not asymptotic efficiency.

Evidence boundary: Measured links support achieved quality, coverage limits and cost observations. Mechanism-specific causal claims require additional targeted ablations; these are labelled reasoned.

Suitable: Small smooth front archives; avoid: Large populations with tight memory

## 17 PESA-II

Archive region occupancy selection

Advantages (reasoned): Region selection directly rewards sparsity;Archive keeps observed tradeoffs;Grid counts are interpretable;Less dependence on precise distances

Disadvantages (reasoned): Grid divisions sensitive;High-dimensional grids become sparse;Archive can shrink to few members;Grid boundaries change selection abruptly

Measured run: Task A P3: HV 0.511 +/- 0.0071042; IGD 0.021934 +/- 0.0033027; Spacing 0.023398 +/- 0.0078827; front size 40 +/- 0; runtime 5.2361 +/- 0.23935 s.

Measured links to use: 1) HV=0.511 +/- 0.0071042 records achieved normalized dominated volume; 2) IGD=0.021934 +/- 0.0033027 measures distance to the sampled exact front.

Measured cautions: 1) The recorded front has 40 +/- 0 points and cannot certify complete coverage; 2) runtime=5.2361 +/- 0.23935 s at 10000 +/- 0 evaluations quantifies finite-budget cost, not asymptotic efficiency.

Evidence boundary: Measured links support achieved quality, coverage limits and cost observations. Mechanism-specific causal claims require additional targeted ablations; these are labelled reasoned.

Suitable: Bi-objective region coverage; avoid: Many objectives with almost unique cells

## 18 MOEA/D

Neighbouring Tchebycheff subproblems

Advantages (reasoned): Cooperation shares good designs;Scalar subproblems retain pressure with many objectives;Neighbourhood limits update work;Weights provide coverage plan

Disadvantages (reasoned): Reference geometry biases front;Neighbourhood size affects spread;Shared donors can homogenize subproblems;Ideal updates alter scalar values

Measured run: Task A P10: HV 0.99538 +/- 0.038577; IGD 0.32121 +/- 0.020673; Spacing 0.26134 +/- 0.029898; front size 40 +/- 0; runtime 19.578 +/- 0.88406 s.

Measured links to use: 1) HV=0.99538 +/- 0.038577 records achieved normalized dominated volume; 2) IGD=0.32121 +/- 0.020673 measures distance to the sampled exact front.

Measured cautions: 1) The recorded front has 40 +/- 0 points and cannot certify complete coverage; 2) runtime=19.578 +/- 0.88406 s at 10000 +/- 0 evaluations quantifies finite-budget cost, not asymptotic efficiency.

Evidence boundary: Measured links support achieved quality, coverage limits and cost observations. Mechanism-specific causal claims require additional targeted ablations; these are labelled reasoned.

Suitable: Smooth continuous many-objective design; avoid: Disconnected fronts badly matched by weights

## 19 MOEA/D-DE

DE variation inside MOEA/D

Advantages (reasoned): DE exploits vector differences;Neighbour cooperation;Tchebycheff reaches nonconvex fronts;Forced crossover guarantees a changed coordinate

Disadvantages (reasoned): F and CR need tuning;DE requires enough distinct neighbours;Boundary clipping distorts donors;Weight coverage may be uneven

Measured run: Task A P3: HV 0.21242 +/- 0.27423; IGD 1.0419 +/- 0.9331; Spacing 0.0010261 +/- 0.0015032; front size 16.6 +/- 20.14; runtime 11.795 +/- 2.1489 s.

Measured links to use: 1) HV=0.21242 +/- 0.27423 records achieved normalized dominated volume; 2) IGD=1.0419 +/- 0.9331 measures distance to the sampled exact front.

Measured cautions: 1) The recorded front has 16.6 +/- 20.14 points and cannot certify complete coverage; 2) runtime=11.795 +/- 2.1489 s at 10000 +/- 0 evaluations quantifies finite-budget cost, not asymptotic efficiency.

Evidence boundary: Measured links support achieved quality, coverage limits and cost observations. Mechanism-specific causal claims require additional targeted ablations; these are labelled reasoned.

Suitable: Continuous real-coded nonconvex design; avoid: Permutation encodings without a new donor operator

## 20 MOEA/D-ACO

Weight-specific ant pheromones and scalar replacement

Advantages (reasoned): Valid tours by construction;Heuristic directs ant choices;Separate subproblems retain tradeoffs;Pheromone records good edges

Disadvantages (reasoned): Pheromone arrays cost N*cities^2;Deposits can lock routes;Alpha beta evaporation matter;Continuous encodings unsupported

Measured run: Task A P8: HV 0.92348 +/- 0.00073621; IGD N/A +/- N/A; Spacing 0.0036041 +/- 0.0011622; front size 4.6 +/- 0.96609; runtime 26.418 +/- 0.90564 s.

Measured links to use: 1) HV=0.92348 +/- 0.00073621 records achieved normalized dominated volume; 2) Spacing=0.0036041 +/- 0.0011622 measures within-front regularity because exact-front IGD is unavailable.

Measured cautions: 1) The recorded front has 4.6 +/- 0.96609 points and cannot certify complete coverage; 2) runtime=26.418 +/- 0.90564 s at 10000 +/- 0 evaluations quantifies finite-budget cost, not asymptotic efficiency.

Evidence boundary: Measured links support achieved quality, coverage limits and cost observations. Mechanism-specific causal claims require additional targeted ablations; these are labelled reasoned.

Suitable: Bi-objective routing; avoid: Smooth gradient problems

## 21 Constrained NSGA-II

NSGA-II with Deb feasibility

Advantages (reasoned): Feasible beats infeasible without objective penalty;Lower violation guides infeasible search;Pareto ranking within feasible;Crowding retains feasible diversity

Disadvantages (reasoned): Violation normalization affects infeasible order;Feasibility boundary can trap search;Quadratic ranking;Finite crowding resolution

Measured run: Task A P5: HV 1.1818 +/- 3.9631e-05; IGD 0.014057 +/- 0.0012871; Spacing 0.020672 +/- 0.0032737; front size 40 +/- 0; runtime 3.3173 +/- 0.34218 s.

Measured links to use: 1) HV=1.1818 +/- 3.9631e-05 records achieved normalized dominated volume; 2) IGD=0.014057 +/- 0.0012871 measures distance to the sampled exact front.

Measured cautions: 1) The recorded front has 40 +/- 0 points and cannot certify complete coverage; 2) runtime=3.3173 +/- 0.34218 s at 10000 +/- 0 evaluations quantifies finite-budget cost, not asymptotic efficiency.

Evidence boundary: Measured links support achieved quality, coverage limits and cost observations. Mechanism-specific causal claims require additional targeted ablations; these are labelled reasoned.

Suitable: Constrained beam or Binh-Korn; avoid: Problems needing stochastic feasibility guarantees

## 22 MOPSO

Particle velocity with personal and archive leaders

Advantages (reasoned): Memory of personal successes;Few basic coefficients;Archive leader spreads movement;No crossover operator needed

Disadvantages (reasoned): Velocities can collapse;Boundary clipping affects dynamics;Leader policy controls diversity;Coefficients require tuning

Measured run: Task A P4: HV 0.92587 +/- 0.0045498; IGD N/A +/- N/A; Spacing 0.013429 +/- 0.0037554; front size 40 +/- 0; runtime 2.1787 +/- 0.2485 s.

Measured links to use: 1) HV=0.92587 +/- 0.0045498 records achieved normalized dominated volume; 2) Spacing=0.013429 +/- 0.0037554 measures within-front regularity because exact-front IGD is unavailable.

Measured cautions: 1) The recorded front has 40 +/- 0 points and cannot certify complete coverage; 2) runtime=2.1787 +/- 0.2485 s at 10000 +/- 0 evaluations quantifies finite-budget cost, not asymptotic efficiency.

Evidence boundary: Measured links support achieved quality, coverage limits and cost observations. Mechanism-specific causal claims require additional targeted ablations; these are labelled reasoned.

Suitable: Continuous portfolio and beam designs; avoid: Permutation tours without discrete velocity

## 23 MOGWO

Three archive leaders and encircling

Advantages (reasoned): Multiple leaders guide movement;Coefficient shrinks automatically;Archive covers tradeoffs;Binary transfer enables masks

Disadvantages (reasoned): Averaging leaders may erase diversity;No strict improvement guarantee;Transfer sigmoid biases masks;Binary objective evaluation is costly

Measured run: Task A P5: HV 1.1817 +/- 0.00011936; IGD 0.013415 +/- 0.0012894; Spacing 0.020775 +/- 0.0019689; front size 40 +/- 0; runtime 4.1017 +/- 0.37263 s.

Measured links to use: 1) HV=1.1817 +/- 0.00011936 records achieved normalized dominated volume; 2) IGD=0.013415 +/- 0.0012894 measures distance to the sampled exact front.

Measured cautions: 1) The recorded front has 40 +/- 0 points and cannot certify complete coverage; 2) runtime=4.1017 +/- 0.37263 s at 10000 +/- 0 evaluations quantifies finite-budget cost, not asymptotic efficiency.

Evidence boundary: Measured links support achieved quality, coverage limits and cost observations. Mechanism-specific causal claims require additional targeted ablations; these are labelled reasoned.

Suitable: Continuous design or exploratory feature masks; avoid: Required stable high-accuracy feature conclusions on tiny budgets

## 24 MOABC

Employed moves, crowding-based onlookers and abandonment scouts

Advantages (reasoned): Scouts restart abandoned sources;Onlooker pressure favours sparse regions;Coordinate moves are inspectable;No gradients needed

Disadvantages (reasoned): Dominance-only greed can reject useful tradeoffs;Limit needs tuning;Three phases complicate budget accounting;One-coordinate changes may be slow

Measured run: Task A P3: HV 0.50853 +/- 0.0089927; IGD 0.022472 +/- 0.0044901; Spacing 0.023861 +/- 0.0049917; front size 37.2 +/- 4.0497; runtime 9.7198 +/- 0.72292 s.

Measured links to use: 1) HV=0.50853 +/- 0.0089927 records achieved normalized dominated volume; 2) IGD=0.022472 +/- 0.0044901 measures distance to the sampled exact front.

Measured cautions: 1) The recorded front has 37.2 +/- 4.0497 points and cannot certify complete coverage; 2) runtime=9.7198 +/- 0.72292 s at 10000 +/- 0 evaluations quantifies finite-budget cost, not asymptotic efficiency.

Evidence boundary: Measured links support achieved quality, coverage limits and cost observations. Mechanism-specific causal claims require additional targeted ablations; these are labelled reasoned.

Suitable: Small continuous design with restarts; avoid: Strongly coupled high-dimensional variables

## 25 MOACO

Two pheromone matrices and route construction

Advantages (reasoned): Produces valid permutations;Two objectives retain separate memories;Heuristic reduces random route work;Archive deposits reward tradeoffs

Disadvantages (reasoned): Strong evaporation forgets edges;Weak evaporation stagnates;Traffic/distance scales matter;No exact TSP optimality guarantee

Measured run: Task A P8: HV 0.92394 +/- 0; IGD N/A +/- N/A; Spacing 0.0031115 +/- 0.00082031; front size 5.2 +/- 0.42164; runtime 18.135 +/- 2.1703 s.

Measured links to use: 1) HV=0.92394 +/- 0 records achieved normalized dominated volume; 2) Spacing=0.0031115 +/- 0.00082031 measures within-front regularity because exact-front IGD is unavailable.

Measured cautions: 1) The recorded front has 5.2 +/- 0.42164 points and cannot certify complete coverage; 2) runtime=18.135 +/- 2.1703 s at 10000 +/- 0 evaluations quantifies finite-budget cost, not asymptotic efficiency.

Evidence boundary: Measured links support achieved quality, coverage limits and cost observations. Mechanism-specific causal claims require additional targeted ablations; these are labelled reasoned.

Suitable: Distance-time routing; avoid: Continuous portfolio allocation

## 26 MOSA

Incomparable neighbour acceptance and Boltzmann dominated moves

Advantages (reasoned): May accept uphill escape moves;Works without derivatives;Mutation adapts to encoding;Archive records tradeoffs from many chains

Disadvantages (reasoned): Cooling schedule sensitive;Local moves can miss distant regions;Incomparable moves remain random at low temperature;Finite cooling gives no global guarantee

Measured run: Task A P3: HV 0.51354 +/- 0.0060662; IGD 0.020405 +/- 0.0038149; Spacing 0.033881 +/- 0.01308; front size 35 +/- 4.5704; runtime 1.4704 +/- 0.13765 s.

Measured links to use: 1) HV=0.51354 +/- 0.0060662 records achieved normalized dominated volume; 2) IGD=0.020405 +/- 0.0038149 measures distance to the sampled exact front.

Measured cautions: 1) The recorded front has 35 +/- 4.5704 points and cannot certify complete coverage; 2) runtime=1.4704 +/- 0.13765 s at 10000 +/- 0 evaluations quantifies finite-budget cost, not asymptotic efficiency.

Evidence boundary: Measured links support achieved quality, coverage limits and cost observations. Mechanism-specific causal claims require additional targeted ablations; these are labelled reasoned.

Suitable: Budgeted local exploration on nonconvex fronts; avoid: Uniform global coverage with insufficient chains

## 27 MODE

DE dominance-only trial replacement

Advantages (reasoned): Simple vector donor;No utility weights;CR forces one donor coordinate;Dominating trials preserve target improvement

Disadvantages (reasoned): Incomparable trials do not replace targets;F CR sensitivity;Coordinate clipping can stagnate;Only real encoding is implemented

Measured run: Task A P3: HV 0.11 +/- 3.0227e-10; IGD 0.6098 +/- 1.1468e-10; Spacing 0 +/- 0; front size 1 +/- 0; runtime 1.7695 +/- 0.068943 s.

Measured links to use: 1) HV=0.11 +/- 3.0227e-10 records achieved normalized dominated volume; 2) IGD=0.6098 +/- 1.1468e-10 measures distance to the sampled exact front.

Measured cautions: 1) The recorded front has 1 +/- 0 points and cannot certify complete coverage; 2) runtime=1.7695 +/- 0.068943 s at 10000 +/- 0 evaluations quantifies finite-budget cost, not asymptotic efficiency.

Evidence boundary: Measured links support achieved quality, coverage limits and cost observations. Mechanism-specific causal claims require additional targeted ablations; these are labelled reasoned.

Suitable: Continuous design with comparable improvements; avoid: Many objectives with almost no domination

## 28 MO-TLBO

Crowding archive teacher, shrinking TF and nondominated learner moves

Advantages (reasoned): No crossover design needed;Teacher encourages exploitation;Learners use peer information;Shrinking TF changes search scale

Disadvantages (reasoned): Teacher choice depends on archive;Incomparable moves can wander;Population means blur disconnected regions;TF schedule differs from conventional TLBO

Measured run: Task A P3: HV 0.53179 +/- 7.0884e-05; IGD 0.0095087 +/- 9.0745e-05; Spacing 0.0036712 +/- 0.0012871; front size 40 +/- 0; runtime 11.386 +/- 1.2374 s.

Measured links to use: 1) HV=0.53179 +/- 7.0884e-05 records achieved normalized dominated volume; 2) IGD=0.0095087 +/- 9.0745e-05 measures distance to the sampled exact front.

Measured cautions: 1) The recorded front has 40 +/- 0 points and cannot certify complete coverage; 2) runtime=11.386 +/- 1.2374 s at 10000 +/- 0 evaluations quantifies finite-budget cost, not asymptotic efficiency.

Evidence boundary: Measured links support achieved quality, coverage limits and cost observations. Mechanism-specific causal claims require additional targeted ablations; these are labelled reasoned.

Suitable: Small continuous educational examples; avoid: Highly multimodal separated feasible regions

## 29 MOBA

Frequency velocity, pulse and loudness

Advantages (reasoned): Few interpretable schedules;Local walks exploit leaders;Frequency creates long moves;Archive records candidate tradeoffs

Disadvantages (reasoned): Loudness decay suppresses replacement;Velocity can explode then clip;Pulse schedule sensitive;Archive quality may exceed final-chain quality

Measured run: Task A P3: HV 0.39676 +/- 0.14429; IGD 0.12888 +/- 0.16313; Spacing 0.04146 +/- 0.050385; front size 36.3 +/- 6.3605; runtime 4.6044 +/- 0.22895 s.

Measured links to use: 1) HV=0.39676 +/- 0.14429 records achieved normalized dominated volume; 2) IGD=0.12888 +/- 0.16313 measures distance to the sampled exact front.

Measured cautions: 1) The recorded front has 36.3 +/- 6.3605 points and cannot certify complete coverage; 2) runtime=4.6044 +/- 0.22895 s at 10000 +/- 0 evaluations quantifies finite-budget cost, not asymptotic efficiency.

Evidence boundary: Measured links support achieved quality, coverage limits and cost observations. Mechanism-specific causal claims require additional targeted ablations; these are labelled reasoned.

Suitable: Continuous local refinement; avoid: Robust full-front exploration without schedule tuning

## 30 MOMA

NSGA-II plus sparse-child combined-score hill climbing

Advantages (reasoned): Local moves refine global children;Elitist survival;Works with binary/tour mutation;Local cost explicitly counted

Disadvantages (reasoned): Local calls reduce global generations;Combined-score preference changes tradeoffs;Mutation neighbourhood determines refinement;Feature CV makes local search costly

Measured run: Task A P5: HV 1.1818 +/- 5.8274e-05; IGD 0.01291 +/- 0.0015554; Spacing 0.018358 +/- 0.0017049; front size 40 +/- 0; runtime 6.3309 +/- 0.65198 s.

Measured links to use: 1) HV=1.1818 +/- 5.8274e-05 records achieved normalized dominated volume; 2) IGD=0.01291 +/- 0.0015554 measures distance to the sampled exact front.

Measured cautions: 1) The recorded front has 40 +/- 0 points and cannot certify complete coverage; 2) runtime=6.3309 +/- 0.65198 s at 10000 +/- 0 evaluations quantifies finite-budget cost, not asymptotic efficiency.

Evidence boundary: Measured links support achieved quality, coverage limits and cost observations. Mechanism-specific causal claims require additional targeted ablations; these are labelled reasoned.

Suitable: Beam refinement or routing; avoid: Expensive objectives with no local structure

## 31 RVEA

Normalized reference vectors and lecture linear-progress APD

Advantages (reasoned): Angular niches aid many objectives;APD shifts toward convergence;Vector adaptation tracks scales;Sparse niches can retain representatives

Disadvantages (reasoned): Penalty strength and adaptation period matter;Observed ranges can be unstable;Empty niches require fill policy;Reference alignment can bias coverage

Measured run: Task A P10: HV 0.64035 +/- 0.011426; IGD 0.10879 +/- 0.0032335; Spacing 0.10064 +/- 0.01106; front size 40 +/- 0; runtime 5.6417 +/- 0.57606 s.

Measured links to use: 1) HV=0.64035 +/- 0.011426 records achieved normalized dominated volume; 2) IGD=0.10879 +/- 0.0032335 measures distance to the sampled exact front.

Measured cautions: 1) The recorded front has 40 +/- 0 points and cannot certify complete coverage; 2) runtime=5.6417 +/- 0.57606 s at 10000 +/- 0 evaluations quantifies finite-budget cost, not asymptotic efficiency.

Evidence boundary: Measured links support achieved quality, coverage limits and cost observations. Mechanism-specific causal claims require additional targeted ablations; these are labelled reasoned.

Suitable: Five-objective DTLZ2; avoid: Strongly irregular disconnected fronts

## 32 IBEA

Outgoing additive-epsilon fitness and largest-fitness deletion

Advantages (reasoned): No separate sharing operator;Indicator gives selection pressure;Works on nonconvex fronts;Kappa controls discrimination

Disadvantages (reasoned): Exponentials can saturate;Kappa changes selection;Recalculated deletion is costly;Fitness depends strongly on scales

Measured run: Task A P14: HV 0.81944 +/- 0.012245; IGD 0.026183 +/- 0.0076532; Spacing 0.027632 +/- 0.0073516; front size 40 +/- 0; runtime 11.829 +/- 0.66806 s.

Measured links to use: 1) HV=0.81944 +/- 0.012245 records achieved normalized dominated volume; 2) IGD=0.026183 +/- 0.0076532 measures distance to the sampled exact front.

Measured cautions: 1) The recorded front has 40 +/- 0 points and cannot certify complete coverage; 2) runtime=11.829 +/- 0.66806 s at 10000 +/- 0 evaluations quantifies finite-budget cost, not asymptotic efficiency.

Evidence boundary: Measured links support achieved quality, coverage limits and cost observations. Mechanism-specific causal claims require additional targeted ablations; these are labelled reasoned.

Suitable: Small bi-objective indicator experiments; avoid: Large populations with limited CPU

## 33 SMS-EMOA

Steady-state smallest HV deletion

Advantages (reasoned): Direct quality indicator survival;One-offspring updates are simple;Exact two-objective contribution;Protects coverage within the chosen reference

Disadvantages (reasoned): HV reference controls preferences;One-at-a-time sorting costs many calls;Implemented only for two objectives;HV can prioritize extremes unevenly

Measured run: Task A P14: HV 0.85873 +/- 1.9917e-05; IGD 0.0075773 +/- 1.8795e-05; Spacing 0.0026642 +/- 0.00083706; front size 40 +/- 0; runtime 30.594 +/- 1.6848 s.

Measured links to use: 1) HV=0.85873 +/- 1.9917e-05 records achieved normalized dominated volume; 2) IGD=0.0075773 +/- 1.8795e-05 measures distance to the sampled exact front.

Measured cautions: 1) The recorded front has 40 +/- 0 points and cannot certify complete coverage; 2) runtime=30.594 +/- 1.6848 s at 10000 +/- 0 evaluations quantifies finite-budget cost, not asymptotic efficiency.

Evidence boundary: Measured links support achieved quality, coverage limits and cost observations. Mechanism-specific causal claims require additional targeted ablations; these are labelled reasoned.

Suitable: Small bi-objective design; avoid: Many objectives without an HV approximation

## 34 HypE

Equal-share Monte Carlo HV fitness and repeated deletion

Advantages (reasoned): HV sharing supports many objectives;Shared samples account for overlapping domination;Re-estimation updates remaining credit;Final evaluation samples are identical across methods

Disadvantages (reasoned): Sampling noise changes survivors;Selection sample count is small;Repeated deletion costs CPU;HV still needs a reference box

Measured run: Task A P10: HV 0.6611 +/- 0.0082237; IGD 0.11712 +/- 0.0042523; Spacing 0.086127 +/- 0.011397; front size 40 +/- 0; runtime 20.197 +/- 0.60127 s.

Measured links to use: 1) HV=0.6611 +/- 0.0082237 records achieved normalized dominated volume; 2) IGD=0.11712 +/- 0.0042523 measures distance to the sampled exact front.

Measured cautions: 1) The recorded front has 40 +/- 0 points and cannot certify complete coverage; 2) runtime=20.197 +/- 0.60127 s at 10000 +/- 0 evaluations quantifies finite-budget cost, not asymptotic efficiency.

Evidence boundary: Measured links support achieved quality, coverage limits and cost observations. Mechanism-specific causal claims require additional targeted ablations; these are labelled reasoned.

Suitable: Many-objective indicator study; avoid: High-precision survival contribution estimates

## 35 R-NSGA-II

Reference preference and epsilon clearing

Advantages (reasoned): Focuses on desired region;Clearing promotes local diversity;Retains nondominated hierarchy;Preference is physically interpretable on P14

Disadvantages (reasoned): Wrong aspiration biases search;Epsilon controls local spacing;Full-front quality can drop;Default balanced aspiration is arbitrary

Measured run: Task A P14: HV 0.85563 +/- 0.00087984; IGD 0.010043 +/- 0.00082871; Spacing 0.013059 +/- 0.0019458; front size 40 +/- 0; runtime 4.1524 +/- 0.33328 s.

Measured links to use: 1) HV=0.85563 +/- 0.00087984 records achieved normalized dominated volume; 2) IGD=0.010043 +/- 0.00082871 measures distance to the sampled exact front.

Measured cautions: 1) The recorded front has 40 +/- 0 points and cannot certify complete coverage; 2) runtime=4.1524 +/- 0.33328 s at 10000 +/- 0 evaluations quantifies finite-budget cost, not asymptotic efficiency.

Evidence boundary: Measured links support achieved quality, coverage limits and cost observations. Mechanism-specific causal claims require additional targeted ablations; these are labelled reasoned.

Suitable: Decision-maker laptop region; avoid: Unknown or frequently changing preferences

## 36 MGDA

Minimum-norm gradient combination

Advantages (reasoned): Common descent when norm is nonzero;Analytical two-task weights;No objective-scale utility required;Can converge to Pareto stationarity

Disadvantages (reasoned): Requires gradients;Stationarity is not full-front coverage;May stop while each task has gradient;Nonconvex network optima are local

Measured run: Task A P13: HV 0.28389 +/- 0; IGD 0.62794 +/- 0; Spacing 0 +/- 0; front size 1 +/- 0; runtime 2.3516 +/- 0 s.

Measured links to use: 1) HV=0.28389 +/- 0 records achieved normalized dominated volume; 2) IGD=0.62794 +/- 0 measures distance to the sampled exact front.

Measured cautions: 1) The recorded front has 1 +/- 0 points and cannot certify complete coverage; 2) runtime=2.3516 +/- 0 s at 10000 +/- 0 evaluations quantifies finite-budget cost, not asymptotic efficiency.

Evidence boundary: Measured links support achieved quality, coverage limits and cost observations. Mechanism-specific causal claims require additional targeted ablations; these are labelled reasoned.

Suitable: Differentiable conflicting tasks; avoid: Discrete designs or a full Pareto-front sweep

## 37 GradNorm

Gradient-norm adaptive task weights

Advantages (reasoned): Balances task gradient magnitudes;Training rates influence targets;Hand-derived update is inspectable;Task-scale stress can be evaluated

Disadvantages (reasoned): Requires gradients and initial losses;Alpha weight_lr matter;Does not guarantee common descent;Toy final point is not an entire front

Measured run: Task A P13: HV 0.60519 +/- 0; IGD 0.43296 +/- 0; Spacing 0 +/- 0; front size 1 +/- 0; runtime 2.6674 +/- 0 s.

Measured links to use: 1) HV=0.60519 +/- 0 records achieved normalized dominated volume; 2) IGD=0.43296 +/- 0 measures distance to the sampled exact front.

Measured cautions: 1) The recorded front has 1 +/- 0 points and cannot certify complete coverage; 2) runtime=2.6674 +/- 0 s at 10000 +/- 0 evaluations quantifies finite-budget cost, not asymptotic efficiency.

Evidence boundary: Measured links support achieved quality, coverage limits and cost observations. Mechanism-specific causal claims require additional targeted ablations; these are labelled reasoned.

Suitable: Shared network with unequal loss gradients; avoid: A guaranteed Pareto descent method


## Family comparison
Classical methods convert preferences or bounds into scalar solves, making their numerical accuracy depend on the scalar solver. Early GAs use objective selection, rank or sharing without parent elitism; the passive archive records discoveries but does not prevent the breeding population from losing them. Elitist methods spend quadratic comparisons to retain high-ranked parents and use crowding, density or grids for diversity. Decomposition gives each direction its own scalar pressure, although a fixed lattice may not match disconnected fronts. Swarms and local heuristics rely on archive leaders and neighbourhood moves; their schedules can exploit quickly or stagnate. Indicators replace explicit density with epsilon or hypervolume fitness but require scales and, for HV, a reference box. Reference methods remain useful when dominance loses discrimination in five dimensions. Preferences intentionally trade full-front coverage for a useful region. Gradient methods optimize differentiable tasks toward stationarity and do not produce a full front from one start. Feasibility rules are applied before Pareto comparisons, and comparisons use common normalized metric scales.