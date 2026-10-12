# Task B complete algorithm comparison

Measured output quality and theoretical mechanisms are distinguished. Values refer to normalized metrics with fixed scales. Additional causal ablations are needed before attributing every advantage/disadvantage to one mechanism.

## 1 Weighted Sum

Linear scalar solve and a sweep

Advantages (reasoned): Simple scalar objective;Direct preference weights;Reusable constrained scalar solver;Independent solves can be distributed

Disadvantages (reasoned): Unsupported nonconvex points are unreachable;Scaling changes weight meaning;Uniform weights give nonuniform spacing;Local scalar solves lack global guarantees

Measured: Task A P1: HV 1.0258 +/- 0; IGD 0.020135 +/- 0; Spacing 9.6958e-09 +/- 0; front size 21 +/- 0; runtime 0.30034 +/- 0 s.

Measured limits: Finite recorded front size=21; this is no certificate of complete coverage. Residual sampled-front IGD=0.020135; positive residual measures finite-budget approximation error.

Suitable: Convex smooth two-objective design with interpretable weights; avoid: Dented fronts and an unknown preference distribution

## 2 Epsilon-Constraint

One objective minimized and others bounded

Advantages (reasoned): Can represent unsupported efficient points;Epsilon has physical interpretation;Scalar constraints remain explicit;Primary objective stays recognizable

Disadvantages (reasoned): Infeasible epsilon values waste solves;Sweeps can duplicate points;Constraint solver quality matters;Many objectives require multidimensional epsilon grids

Measured: Task A P2: HV 1.0865 +/- 0; IGD 0.037129 +/- 0; Spacing 0.14183 +/- 0; front size 21 +/- 0; runtime 0.036385 +/- 0 s.

Measured limits: Finite recorded front size=21; this is no certificate of complete coverage. Residual sampled-front IGD=0.037129; positive residual measures finite-budget approximation error.

Suitable: Nonconvex constrained design with hard limits; avoid: High-dimensional objective grids

## 3 Benson reference improvement

Weighted improvement below a reference

Advantages (reasoned): Reference conveys aspiration;Nonnegative improvement is interpretable;Explicit upper objective bounds;Scalar subproblems are easy to inspect

Disadvantages (reasoned): This is the lecture achievement form, not outer approximation;Unrestricted reference sweeps inherit weighted-sum barrier;Reference coordinates require scaling;Weights still encode preferences

Measured: Task A P1: HV 1.0258 +/- 0; IGD 0.020135 +/- 0; Spacing 2.7258e-08 +/- 0; front size 21 +/- 0; runtime 0.049804 +/- 0 s.

Measured limits: Finite recorded front size=21; this is no certificate of complete coverage. Residual sampled-front IGD=0.020135; positive residual measures finite-budget approximation error.

Suitable: Teaching reference improvement on P1/P7; avoid: Claiming a general Benson convergence theorem

## 4 Weight Metric

Weighted distance to fixed ideal

Advantages (reasoned): Infinity norm can reach unsupported tradeoffs;Different p values express balance;Ideal point makes distances interpretable;Scalar solver is reusable

Disadvantages (reasoned): Ideal estimation affects solution;Max norm is nonsmooth;p and weights require preferences;Finite weight sweep misses narrow regions

Measured: Task A P1: HV 1.0347 +/- 0; IGD 0.012339 +/- 0; Spacing 0.023806 +/- 0; front size 63 +/- 0; runtime 0.18194 +/- 0 s.

Measured limits: Finite recorded front size=63; this is no certificate of complete coverage. Residual sampled-front IGD=0.012339; positive residual measures finite-budget approximation error.

Suitable: Compromise solutions on nonconvex fronts; avoid: Unreliable ideal estimates or many weights

## 5 Value Function

Declared decision-maker utility

Advantages (reasoned): Directly encodes a preferred outcome;Can express nonlinear preferences;Few scalar solves are economical;Natural targets communicate decisions

Disadvantages (reasoned): Utility must be elicited;Squared target utility need not be monotone;One preferred design is not a full front;Misspecified preferences bias results

Measured: Task A P14: HV 0.32905 +/- 0; IGD 0.35302 +/- 0; Spacing 0 +/- 0; front size 1 +/- 0; runtime 0.0050517 +/- 0 s.

Measured limits: Finite recorded front size=1; this is no certificate of complete coverage. Residual sampled-front IGD=0.35302; positive residual measures finite-budget approximation error.

Suitable: Laptop or portfolio profile decisions; avoid: Exploration without known preferences

## 6 Goal Programming

Explicit positive/negative goal deviations

Advantages (reasoned): Shows unavoidable shortfall;Can normalize incompatible units;Soft goals remain interpretable;Constraint and aspiration roles are separate

Disadvantages (reasoned): Goal weights control tradeoffs;Infeasible goals cannot be guaranteed;Units can overwhelm deviations;Satisfied goals may leave efficiency ties

Measured: Task A P11: HV 1.21 +/- 0; IGD 4.8252e-11 +/- 0; Spacing 0 +/- 0; front size 1 +/- 0; runtime 0.025949 +/- 0 s.

Measured limits: Finite recorded front size=1; this is no certificate of complete coverage. Residual sampled-front IGD=4.8252e-11; positive residual measures finite-budget approximation error.

Suitable: Production targets with soft priorities; avoid: Searching an entire front without goals

## 7 Lexicographic

Sequential strict priorities with tolerances

Advantages (reasoned): Priority order is transparent;Breaks first-objective ties;Uses scalar solvers;Preserves prior objective values to declared tolerance

Disadvantages (reasoned): Lower objectives may have little freedom;Tolerance changes strictness;Priority mistakes are expensive;Sequential solves add cost

Measured: Task A P11: HV 1.21 +/- 0; IGD 6.457e-08 +/- 0; Spacing 0 +/- 0; front size 1 +/- 0; runtime 0.029337 +/- 0 s.

Measured limits: Finite recorded front size=1; this is no certificate of complete coverage. Residual sampled-front IGD=6.457e-08; positive residual measures finite-budget approximation error.

Suitable: Profit first and units second; avoid: Balanced objectives with no hierarchy

## 8 TOPSIS

Closeness to weighted ideal and anti-ideal

Advantages (reasoned): Fast finite-table ranking;Uses all criteria;Distances are explainable;Works with benefit and cost columns

Disadvantages (reasoned): Does not generate new designs;Vector normalization affects rank;Compensation can hide a bad criterion;Alternatives can change the ideal

Measured: P12 w=[0.3, 0.3, 0.2, 0.2] v=0.5: top 3 [3, 1, 5]; P12 w=[0.4, 0.2, 0.2, 0.2] v=0.5: top 3 [1, 2, 3]; P4 NSGA-II front w=[0.5, 0.5] v=0.5: top 3 [2, 14, 27]; P4 NSGA-II front w=[0.6, 0.4] v=0.5: top 3 [27, 7, 15]

Measured limits: Five existing suppliers are ranked; no new design is generated. Preference changes are measured in rankings.csv; ranking quality does not imply a global optimum.

Suitable: Supplier or existing-front ranking; avoid: Optimization without an alternatives table

## 9 VIKOR

Compromise via group regret and worst regret

Advantages (reasoned): Worst criterion enters R;v exposes group versus individual tradeoff;Compromise conditions avoid forced winners;Finite rankings are inexpensive

Disadvantages (reasoned): Requires preference weights;v can change rank;Range normalization changes regrets;Does not generate designs

Measured: P12 w=[0.3, 0.3, 0.2, 0.2] v=0.25: top 3 [1, 2, 5]; P12 w=[0.4, 0.2, 0.2, 0.2] v=0.25: top 3 [2, 1, 4]; P12 w=[0.3, 0.3, 0.2, 0.2] v=0.5: top 3 [1, 2, 5]; P12 w=[0.4, 0.2, 0.2, 0.2] v=0.5: top 3 [2, 1, 3]; P12 w=[0.3, 0.3, 0.2, 0.2] v=0.75: top 3 [1, 3, 2]; P12 w=[0.4, 0.2, 0.2, 0.2] v=0.75: top 3 [1, 2, 3]; P4 NSGA-II front w=[0.5, 0.5] v=0.5: top 3 [27, 14, 2]; P4 NSGA-II front w=[0.6, 0.4] v=0.5: top 3 [7, 15, 20]

Measured limits: Five existing suppliers are ranked; no new design is generated. Preference changes are measured in rankings.csv; ranking quality does not imply a global optimum.

Suitable: Supplier compromise with severe weak criteria; avoid: A Pareto front generator

## 10 VEGA

Objective-partitioned selection

Advantages (reasoned): Very simple selection;No preference weights needed;Handles several objective contests;Cheap scalar tournaments

Disadvantages (reasoned): Extremes can dominate mating pool;No parent elitism;Middle tradeoffs may disappear;Objective partition sizes affect pressure

Measured: Task A P2: HV 1.1097 +/- 0.0017957; IGD 0.015417 +/- 0.0022031; Spacing 0.01628 +/- 0.0012429; front size 40 +/- 0; runtime 0.41085 +/- 0.02133 s.

Measured limits: Finite recorded front size=40; this is no certificate of complete coverage. Residual sampled-front IGD=0.015417; positive residual measures finite-budget approximation error.

Suitable: Teaching objective competition; avoid: Reliable uniform front preservation

## 11 MOGA

Domination-count rank and fitness sharing

Advantages (reasoned): No scalar utility required;Sharing promotes sparse niches;Dominance counts are easy to inspect;Can search unsupported regions

Disadvantages (reasoned): No elitism;Sharing radius sensitive;All nondominated members tie in rank;Pairwise density costs quadratically

Measured: Task A P3: HV 0.52443 +/- 0.00078858; IGD 0.012438 +/- 0.00050827; Spacing 0.013095 +/- 0.001648; front size 40 +/- 0; runtime 0.38295 +/- 0.010848 s.

Measured limits: Finite recorded front size=40; this is no certificate of complete coverage. Residual sampled-front IGD=0.012438; positive residual measures finite-budget approximation error.

Suitable: Small bi-objective populations; avoid: Many objectives with sparse dominance

## 12 NSGA

Front layers and within-front sharing

Advantages (reasoned): Explicit Pareto hierarchy;Sharing is local to fronts;No objective weights required;Variation supports arbitrary encodings

Disadvantages (reasoned): No elitism;Quadratic sorting and sharing;Dummy fitness spacing is arbitrary;Niche radius must be tuned

Measured: Task A P5: HV 1.1818 +/- 7.7235e-05; IGD 0.014333 +/- 0.00117; Spacing 0.0191 +/- 0.0013825; front size 40 +/- 0; runtime 0.428 +/- 0.011804 s.

Measured limits: Finite recorded front size=40; this is no certificate of complete coverage. Residual sampled-front IGD=0.014333; positive residual measures finite-budget approximation error.

Suitable: Teaching early Pareto GAs; avoid: Large fast convergence requirements

## 13 NPGA

Direct contestant dominance then separate comparison-set quadratic niche tie

Advantages (reasoned): No fixed utility weights;Niche tie-break preserves sparse points;Comparison sample controls work;Can visit nonconvex tradeoffs

Disadvantages (reasoned): Nonelitist generations lose parents;Small comparison set gives noisy niche counts;Sigma changes density pressure;Lecture tournament differs from original publication

Measured: Task A P3: HV 0.47123 +/- 0.04723; IGD 0.040099 +/- 0.034626; Spacing 0.022057 +/- 0.0056312; front size 38.3 +/- 3.335; runtime 0.73103 +/- 0.020128 s.

Measured limits: Finite recorded front size=38.3; this is no certificate of complete coverage. Residual sampled-front IGD=0.040099; positive residual measures finite-budget approximation error.

Suitable: Bi-objective diversity experiments; avoid: Many-objective fronts where most tournaments tie

## 14 NSGA-II

Front rank, crowding, parent-child elitism

Advantages (reasoned): Elitist survivor retention;Boundary points receive protection;No sharing radius;Permutation and real variation share selection

Disadvantages (reasoned): Crowding weakens as objectives grow;Quadratic pairwise sorting;Finite population truncates front;Crowding is not an explicit convergence measure

Measured: Task A P3: HV 0.52839 +/- 0.0006346; IGD 0.01223 +/- 0.00062729; Spacing 0.018498 +/- 0.0029193; front size 40 +/- 0; runtime 0.50741 +/- 0.0096394 s.

Measured limits: Finite recorded front size=40; this is no certificate of complete coverage. Residual sampled-front IGD=0.01223; positive residual measures finite-budget approximation error.

Suitable: General constrained two-objective search; avoid: Very many objectives with weak dominance

## 15 NSGA-III

Reference-point niching after front rank

Advantages (reasoned): Reference niches control coverage;Supports many objectives;Occupancy encourages unused directions;Does not use a sharing radius

Disadvantages (reasoned): Range normalization simplifies original intercepts;Reference count grows combinatorially;Poor reference geometry biases coverage;Dominance layers still require quadratic work

Measured: Task A P10: HV 0.65785 +/- 0.012066; IGD 0.10953 +/- 0.0058358; Spacing 0.10223 +/- 0.011323; front size 40 +/- 0; runtime 0.72152 +/- 0.013569 s.

Measured limits: Finite recorded front size=40; this is no certificate of complete coverage. Residual sampled-front IGD=0.10953; positive residual measures finite-budget approximation error.

Suitable: DTLZ2 with three or five objectives; avoid: Irregular fronts without adapted references

## 16 SPEA2

Strength, raw fitness and neighbour density

Advantages (reasoned): Strength combines domination information;Density distinguishes ties;Fixed archive bounds memory;Lexicographic truncation considers nearest distances

Disadvantages (reasoned): Quadratic distance storage;Repeated truncation adds cost;k-neighbour density depends on scale;Archive size limits attainable resolution

Measured: Task A P4: HV 0.93383 +/- 0.0015081; IGD N/A +/- N/A; Spacing 0.014057 +/- 0.0033503; front size 40 +/- 0; runtime 1.3313 +/- 0.019422 s.

Measured limits: Finite recorded front size=40; this is no certificate of complete coverage. Exact-front IGD is unavailable for this problem, so convergence is not certified.

Suitable: Small smooth front archives; avoid: Large populations with tight memory

## 17 PESA-II

Archive region occupancy selection

Advantages (reasoned): Region selection directly rewards sparsity;Archive keeps observed tradeoffs;Grid counts are interpretable;Less dependence on precise distances

Disadvantages (reasoned): Grid divisions sensitive;High-dimensional grids become sparse;Archive can shrink to few members;Grid boundaries change selection abruptly

Measured: Task A P3: HV 0.51 +/- 0.010935; IGD 0.025403 +/- 0.0080166; Spacing 0.025956 +/- 0.003239; front size 40 +/- 0; runtime 0.72595 +/- 0.019302 s.

Measured limits: Finite recorded front size=40; this is no certificate of complete coverage. Residual sampled-front IGD=0.025403; positive residual measures finite-budget approximation error.

Suitable: Bi-objective region coverage; avoid: Many objectives with almost unique cells

## 18 MOEA/D

Neighbouring Tchebycheff subproblems

Advantages (reasoned): Cooperation shares good designs;Scalar subproblems retain pressure with many objectives;Neighbourhood limits update work;Weights provide coverage plan

Disadvantages (reasoned): Reference geometry biases front;Neighbourhood size affects spread;Shared donors can homogenize subproblems;Ideal updates alter scalar values

Measured: Task A P10: HV 0.99988 +/- 0.033592; IGD 0.32929 +/- 0.024052; Spacing 0.27088 +/- 0.033604; front size 40 +/- 0; runtime 3.2985 +/- 0.094054 s.

Measured limits: Finite recorded front size=40; this is no certificate of complete coverage. Residual sampled-front IGD=0.32929; positive residual measures finite-budget approximation error.

Suitable: Smooth continuous many-objective design; avoid: Disconnected fronts badly matched by weights

## 19 MOEA/D-DE

DE variation inside MOEA/D

Advantages (reasoned): DE exploits vector differences;Neighbour cooperation;Tchebycheff reaches nonconvex fronts;Forced crossover guarantees a changed coordinate

Disadvantages (reasoned): F and CR need tuning;DE requires enough distinct neighbours;Boundary clipping distorts donors;Weight coverage may be uneven

Measured: Task A P3: HV 0.082464 +/- 0.18269; IGD 1.2572 +/- 0.8031; Spacing 0.00071465 +/- 0.0016128; front size 8.8 +/- 16.444; runtime 1.6722 +/- 0.29288 s.

Measured limits: Finite recorded front size=8.8; this is no certificate of complete coverage. Residual sampled-front IGD=1.2572; positive residual measures finite-budget approximation error.

Suitable: Continuous real-coded nonconvex design; avoid: Permutation encodings without a new donor operator

## 20 MOEA/D-ACO

Weight-specific ant pheromones and scalar replacement

Advantages (reasoned): Valid tours by construction;Heuristic directs ant choices;Separate subproblems retain tradeoffs;Pheromone records good edges

Disadvantages (reasoned): Pheromone arrays cost N*cities^2;Deposits can lock routes;Alpha beta evaporation matter;Continuous encodings unsupported

Measured: Task A P8: HV 0.92372 +/- 0.00050562; IGD N/A +/- N/A; Spacing 0.0038903 +/- 0.0017628; front size 5 +/- 0.8165; runtime 4.1297 +/- 0.026407 s.

Measured limits: Finite recorded front size=5; this is no certificate of complete coverage. Exact-front IGD is unavailable for this problem, so convergence is not certified.

Suitable: Bi-objective routing; avoid: Smooth gradient problems

## 21 Constrained NSGA-II

NSGA-II with Deb feasibility

Advantages (reasoned): Feasible beats infeasible without objective penalty;Lower violation guides infeasible search;Pareto ranking within feasible;Crowding retains feasible diversity

Disadvantages (reasoned): Violation normalization affects infeasible order;Feasibility boundary can trap search;Quadratic ranking;Finite crowding resolution

Measured: Task A P5: HV 1.1818 +/- 7.2189e-05; IGD 0.014663 +/- 0.002837; Spacing 0.019743 +/- 0.0023194; front size 40 +/- 0; runtime 0.56378 +/- 0.0070457 s.

Measured limits: Finite recorded front size=40; this is no certificate of complete coverage. Residual sampled-front IGD=0.014663; positive residual measures finite-budget approximation error.

Suitable: Constrained beam or Binh-Korn; avoid: Problems needing stochastic feasibility guarantees

## 22 MOPSO

Particle velocity with personal and archive leaders

Advantages (reasoned): Memory of personal successes;Few basic coefficients;Archive leader spreads movement;No crossover operator needed

Disadvantages (reasoned): Velocities can collapse;Boundary clipping affects dynamics;Leader policy controls diversity;Coefficients require tuning

Measured: Task A P4: HV 0.93253 +/- 0.0010078; IGD N/A +/- N/A; Spacing 0.013262 +/- 0.0021254; front size 40 +/- 0; runtime 0.34884 +/- 0.014273 s.

Measured limits: Finite recorded front size=40; this is no certificate of complete coverage. Exact-front IGD is unavailable for this problem, so convergence is not certified.

Suitable: Continuous portfolio and beam designs; avoid: Permutation tours without discrete velocity

## 23 MOGWO

Three archive leaders and encircling

Advantages (reasoned): Multiple leaders guide movement;Coefficient shrinks automatically;Archive covers tradeoffs;Binary transfer enables masks

Disadvantages (reasoned): Averaging leaders may erase diversity;No strict improvement guarantee;Transfer sigmoid biases masks;Binary objective evaluation is costly

Measured: Task A P5: HV 1.1817 +/- 0.00012554; IGD 0.013138 +/- 0.00062362; Spacing 0.019854 +/- 0.001345; front size 40 +/- 0; runtime 0.5998 +/- 0.042198 s.

Measured limits: Finite recorded front size=40; this is no certificate of complete coverage. Residual sampled-front IGD=0.013138; positive residual measures finite-budget approximation error.

Suitable: Continuous design or exploratory feature masks; avoid: Required stable high-accuracy feature conclusions on tiny budgets

## 24 MOABC

Employed moves, crowding-based onlookers and abandonment scouts

Advantages (reasoned): Scouts restart abandoned sources;Onlooker pressure favours sparse regions;Coordinate moves are inspectable;No gradients needed

Disadvantages (reasoned): Dominance-only greed can reject useful tradeoffs;Limit needs tuning;Three phases complicate budget accounting;One-coordinate changes may be slow

Measured: Task A P3: HV 0.50954 +/- 0.01272; IGD 0.022583 +/- 0.0070538; Spacing 0.026638 +/- 0.006989; front size 36.6 +/- 3.3731; runtime 0.92756 +/- 0.026621 s.

Measured limits: Finite recorded front size=36.6; this is no certificate of complete coverage. Residual sampled-front IGD=0.022583; positive residual measures finite-budget approximation error.

Suitable: Small continuous design with restarts; avoid: Strongly coupled high-dimensional variables

## 25 MOACO

Two pheromone matrices and route construction

Advantages (reasoned): Produces valid permutations;Two objectives retain separate memories;Heuristic reduces random route work;Archive deposits reward tradeoffs

Disadvantages (reasoned): Strong evaporation forgets edges;Weak evaporation stagnates;Traffic/distance scales matter;No exact TSP optimality guarantee

Measured: Task A P8: HV 0.92341 +/- 0.0012174; IGD N/A +/- N/A; Spacing 0.0027239 +/- 0.0011462; front size 4.6 +/- 1.1738; runtime 2.0433 +/- 0.022421 s.

Measured limits: Finite recorded front size=4.6; this is no certificate of complete coverage. Exact-front IGD is unavailable for this problem, so convergence is not certified.

Suitable: Distance-time routing; avoid: Continuous portfolio allocation

## 26 MOSA

Incomparable neighbour acceptance and Boltzmann dominated moves

Advantages (reasoned): May accept uphill escape moves;Works without derivatives;Mutation adapts to encoding;Archive records tradeoffs from many chains

Disadvantages (reasoned): Cooling schedule sensitive;Local moves can miss distant regions;Incomparable moves remain random at low temperature;Finite cooling gives no global guarantee

Measured: Task A P3: HV 0.5048 +/- 0.011421; IGD 0.023434 +/- 0.0065873; Spacing 0.040497 +/- 0.013832; front size 35.1 +/- 4.4335; runtime 0.1936 +/- 0.010629 s.

Measured limits: Finite recorded front size=35.1; this is no certificate of complete coverage. Residual sampled-front IGD=0.023434; positive residual measures finite-budget approximation error.

Suitable: Budgeted local exploration on nonconvex fronts; avoid: Uniform global coverage with insufficient chains

## 27 MODE

DE dominance-only trial replacement

Advantages (reasoned): Simple vector donor;No utility weights;CR forces one donor coordinate;Dominating trials preserve target improvement

Disadvantages (reasoned): Incomparable trials do not replace targets;F CR sensitivity;Coordinate clipping can stagnate;Only real encoding is implemented

Measured: Task A P3: HV 0.11 +/- 3.731e-11; IGD 0.6098 +/- 1.4155e-11; Spacing 0 +/- 0; front size 1 +/- 0; runtime 0.21803 +/- 0.0066205 s.

Measured limits: Finite recorded front size=1; this is no certificate of complete coverage. Residual sampled-front IGD=0.6098; positive residual measures finite-budget approximation error.

Suitable: Continuous design with comparable improvements; avoid: Many objectives with almost no domination

## 28 MO-TLBO

Crowding archive teacher, shrinking TF and nondominated learner moves

Advantages (reasoned): No crossover design needed;Teacher encourages exploitation;Learners use peer information;Shrinking TF changes search scale

Disadvantages (reasoned): Teacher choice depends on archive;Incomparable moves can wander;Population means blur disconnected regions;TF schedule differs from conventional TLBO

Measured: Task A P3: HV 0.53182 +/- 6.3878e-05; IGD 0.0095565 +/- 0.00010113; Spacing 0.0033392 +/- 0.0011262; front size 40 +/- 0; runtime 1.3873 +/- 0.0082006 s.

Measured limits: Finite recorded front size=40; this is no certificate of complete coverage. Residual sampled-front IGD=0.0095565; positive residual measures finite-budget approximation error.

Suitable: Small continuous educational examples; avoid: Highly multimodal separated feasible regions

## 29 MOBA

Frequency velocity, pulse and loudness

Advantages (reasoned): Few interpretable schedules;Local walks exploit leaders;Frequency creates long moves;Archive records candidate tradeoffs

Disadvantages (reasoned): Loudness decay suppresses replacement;Velocity can explode then clip;Pulse schedule sensitive;Archive quality may exceed final-chain quality

Measured: Task A P3: HV 0.4002 +/- 0.11298; IGD 0.13896 +/- 0.12161; Spacing 0.043804 +/- 0.062473; front size 37.1 +/- 6.1545; runtime 0.48204 +/- 0.011403 s.

Measured limits: Finite recorded front size=37.1; this is no certificate of complete coverage. Residual sampled-front IGD=0.13896; positive residual measures finite-budget approximation error.

Suitable: Continuous local refinement; avoid: Robust full-front exploration without schedule tuning

## 30 MOMA

NSGA-II plus sparse-child combined-score hill climbing

Advantages (reasoned): Local moves refine global children;Elitist survival;Works with binary/tour mutation;Local cost explicitly counted

Disadvantages (reasoned): Local calls reduce global generations;Combined-score preference changes tradeoffs;Mutation neighbourhood determines refinement;Feature CV makes local search costly

Measured: Task A P5: HV 1.1818 +/- 4.2647e-05; IGD 0.013616 +/- 0.0021346; Spacing 0.019714 +/- 0.002315; front size 40 +/- 0; runtime 0.7399 +/- 0.014007 s.

Measured limits: Finite recorded front size=40; this is no certificate of complete coverage. Residual sampled-front IGD=0.013616; positive residual measures finite-budget approximation error.

Suitable: Beam refinement or routing; avoid: Expensive objectives with no local structure

## 31 RVEA

Normalized reference vectors and lecture linear-progress APD

Advantages (reasoned): Angular niches aid many objectives;APD shifts toward convergence;Vector adaptation tracks scales;Sparse niches can retain representatives

Disadvantages (reasoned): Penalty strength and adaptation period matter;Observed ranges can be unstable;Empty niches require fill policy;Reference alignment can bias coverage

Measured: Task A P10: HV 0.64011 +/- 0.0086752; IGD 0.10871 +/- 0.0050531; Spacing 0.10132 +/- 0.0076621; front size 40 +/- 0; runtime 0.54633 +/- 0.012232 s.

Measured limits: Finite recorded front size=40; this is no certificate of complete coverage. Residual sampled-front IGD=0.10871; positive residual measures finite-budget approximation error.

Suitable: Five-objective DTLZ2; avoid: Strongly irregular disconnected fronts

## 32 IBEA

Outgoing additive-epsilon fitness and largest-fitness deletion

Advantages (reasoned): No separate sharing operator;Indicator gives selection pressure;Works on nonconvex fronts;Kappa controls discrimination

Disadvantages (reasoned): Exponentials can saturate;Kappa changes selection;Recalculated deletion is costly;Fitness depends strongly on scales

Measured: Task A P14: HV 0.83052 +/- 0.010347; IGD 0.020185 +/- 0.0053152; Spacing 0.024488 +/- 0.0066145; front size 40 +/- 0; runtime 1.5016 +/- 0.032249 s.

Measured limits: Finite recorded front size=40; this is no certificate of complete coverage. Residual sampled-front IGD=0.020185; positive residual measures finite-budget approximation error.

Suitable: Small bi-objective indicator experiments; avoid: Large populations with limited CPU

## 33 SMS-EMOA

Steady-state smallest HV deletion

Advantages (reasoned): Direct quality indicator survival;One-offspring updates are simple;Exact two-objective contribution;Protects coverage within the chosen reference

Disadvantages (reasoned): HV reference controls preferences;One-at-a-time sorting costs many calls;Implemented only for two objectives;HV can prioritize extremes unevenly

Measured: Task A P14: HV 0.85874 +/- 1.9478e-05; IGD 0.0075754 +/- 1.6479e-05; Spacing 0.0024298 +/- 0.00081774; front size 40 +/- 0; runtime 5.5929 +/- 0.29487 s.

Measured limits: Finite recorded front size=40; this is no certificate of complete coverage. Residual sampled-front IGD=0.0075754; positive residual measures finite-budget approximation error.

Suitable: Small bi-objective design; avoid: Many objectives without an HV approximation

## 34 HypE

Equal-share Monte Carlo HV fitness and repeated deletion

Advantages (reasoned): HV sharing supports many objectives;Shared samples account for overlapping domination;Re-estimation updates remaining credit;Final evaluation samples are identical across methods

Disadvantages (reasoned): Sampling noise changes survivors;Selection sample count is small;Repeated deletion costs CPU;HV still needs a reference box

Measured: Task A P10: HV 0.66139 +/- 0.023239; IGD 0.12184 +/- 0.012992; Spacing 0.096292 +/- 0.017092; front size 40 +/- 0; runtime 4.2892 +/- 0.046984 s.

Measured limits: Finite recorded front size=40; this is no certificate of complete coverage. Residual sampled-front IGD=0.12184; positive residual measures finite-budget approximation error.

Suitable: Many-objective indicator study; avoid: High-precision survival contribution estimates

## 35 R-NSGA-II

Reference preference and epsilon clearing

Advantages (reasoned): Focuses on desired region;Clearing promotes local diversity;Retains nondominated hierarchy;Preference is physically interpretable on P14

Disadvantages (reasoned): Wrong aspiration biases search;Epsilon controls local spacing;Full-front quality can drop;Default balanced aspiration is arbitrary

Measured: Task A P14: HV 0.85628 +/- 0.00064468; IGD 0.0094464 +/- 0.00049587; Spacing 0.012888 +/- 0.0018259; front size 40 +/- 0; runtime 0.817 +/- 0.017786 s.

Measured limits: Finite recorded front size=40; this is no certificate of complete coverage. Residual sampled-front IGD=0.0094464; positive residual measures finite-budget approximation error.

Suitable: Decision-maker laptop region; avoid: Unknown or frequently changing preferences

## 36 MGDA

Minimum-norm gradient combination

Advantages (reasoned): Common descent when norm is nonzero;Analytical two-task weights;No objective-scale utility required;Can converge to Pareto stationarity

Disadvantages (reasoned): Requires gradients;Stationarity is not full-front coverage;May stop while each task has gradient;Nonconvex network optima are local

Measured: Task A P13: HV 0.28389 +/- 0; IGD 0.62794 +/- 0; Spacing 0 +/- 0; front size 1 +/- 0; runtime 0.31087 +/- 0 s.

Measured limits: Finite recorded front size=1; this is no certificate of complete coverage. Residual sampled-front IGD=0.62794; positive residual measures finite-budget approximation error.

Suitable: Differentiable conflicting tasks; avoid: Discrete designs or a full Pareto-front sweep

## 37 GradNorm

Gradient-norm adaptive task weights

Advantages (reasoned): Balances task gradient magnitudes;Training rates influence targets;Hand-derived update is inspectable;Task-scale stress can be evaluated

Disadvantages (reasoned): Requires gradients and initial losses;Alpha weight_lr matter;Does not guarantee common descent;Toy final point is not an entire front

Measured: Task A P13: HV 0.60519 +/- 0; IGD 0.43296 +/- 0; Spacing 0 +/- 0; front size 1 +/- 0; runtime 0.40707 +/- 0 s.

Measured limits: Finite recorded front size=1; this is no certificate of complete coverage. Residual sampled-front IGD=0.43296; positive residual measures finite-budget approximation error.

Suitable: Shared network with unequal loss gradients; avoid: A guaranteed Pareto descent method


## Family comparison
Classical methods convert preferences or bounds into scalar solves, making their numerical accuracy depend on the scalar solver. Early GAs use objective selection, rank or sharing without parent elitism; the passive archive records discoveries but does not prevent the breeding population from losing them. Elitist methods spend quadratic comparisons to retain high-ranked parents and use crowding, density or grids for diversity. Decomposition gives each direction its own scalar pressure, although a fixed lattice may not match disconnected fronts. Swarms and local heuristics rely on archive leaders and neighbourhood moves; their schedules can exploit quickly or stagnate. Indicators replace explicit density with epsilon or hypervolume fitness but require scales and, for HV, a reference box. Reference methods remain useful when dominance loses discrimination in five dimensions. Preferences intentionally trade full-front coverage for a useful region. Gradient methods optimize differentiable tasks toward stationarity and do not produce a full front from one start. Feasibility rules are applied before Pareto comparisons, and comparisons use common normalized metric scales.