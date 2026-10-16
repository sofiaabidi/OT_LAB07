# Task E six selection cases

## P1
Suitable: Weighted Sum,Weight Metric. Poor: VEGA. Convex one-variable problem; scalarization offers interpretable weights and metric methods expose compromise geometry.

Evidence: A1 M=2 base: HV=1.0258 ± 0, IGD=0.020135 ± 0; A4 M=2 base: HV=1.0347 ± 0, IGD=0.012339 ± 0

Recommendations combine measured finite-budget outcomes with encoding, constraints and preference reasoning; no universal winner is claimed.

## P3
Suitable: SMS-EMOA,MO-TLBO. Poor: Weighted Sum. Nonconvex front; hypervolume survival and teacher-learner moves both cover interior tradeoffs in the recorded experiments, while linear scalarization cannot support them.

Evidence: A28 M=2 D: HV=0.53179 ± 7.0884e-05, IGD=0.0095087 ± 9.0745e-05; A33 M=2 D: HV=0.53181 ± 0.00010904, IGD=0.0095649 ± 0.00012778; A28 M=2 base: HV=0.53179 ± 7.0884e-05, IGD=0.0095087 ± 9.0745e-05; A33 M=2 base: HV=0.53181 ± 0.00010904, IGD=0.0095649 ± 0.00012778

Recommendations combine measured finite-budget outcomes with encoding, constraints and preference reasoning; no universal winner is claimed.

## P5
Suitable: Constrained NSGA-II,SPEA2. Poor: VEGA. Nonlinear feasibility makes Deb rules useful; archive strength and density support constrained tradeoffs.

Evidence: A16 M=2 D: HV=1.1818 ± 0.00012094, IGD=0.016079 ± 0.0026026; A21 M=2 D: HV=1.1818 ± 3.9631e-05, IGD=0.014057 ± 0.0012871; A16 M=2 base: HV=1.1818 ± 0.00012094, IGD=0.016079 ± 0.0026026; A21 M=2 base: HV=1.1818 ± 3.9631e-05, IGD=0.014057 ± 0.0012871

Recommendations combine measured finite-budget outcomes with encoding, constraints and preference reasoning; no universal winner is claimed.

## P8
Suitable: NSGA-II,MOEA/D-ACO. Poor: MGDA. Permutation-safe NSGA-II and ant decomposition have the leading recorded HV means and retain valid tours; gradient descent is undefined for city orders.

Evidence: A14 M=2 D: HV=0.92354 ± 0.0011666, IGD=N/A; A20 M=2 D: HV=0.92348 ± 0.00073621, IGD=N/A; A20 M=2 base: HV=0.92348 ± 0.00073621, IGD=N/A

Recommendations combine measured finite-budget outcomes with encoding, constraints and preference reasoning; no universal winner is claimed.

## P10
Suitable: RVEA,MOEA/D. Poor: VEGA. Five objectives weaken dominance; RVEA APD and MOEA/D scalar subproblems retain directional pressure and have the strongest recorded HV means at this budget.

Evidence: A18 M=5 D: HV=0.99538 ± 0.038577, IGD=0.32121 ± 0.020673; A31 M=5 D: HV=1.0121 ± 0.030242, IGD=0.31113 ± 0.0085541; A18 M=5 base: HV=0.99538 ± 0.038577, IGD=0.32121 ± 0.020673; A31 M=3 base: HV=0.64035 ± 0.011426, IGD=0.10879 ± 0.0032335; A31 M=5 base: HV=1.0121 ± 0.030242, IGD=0.31113 ± 0.0085541

Recommendations combine measured finite-budget outcomes with encoding, constraints and preference reasoning; no universal winner is claimed.

## P14
Suitable: R-NSGA-II,Value Function. Poor: VEGA. Known manager aspiration makes a preferred region useful; utility or reference clearing expresses it directly.

Evidence: A5 M=2 base: HV=0.32905 ± 0, IGD=0.35302 ± 0; A35 M=2 base: HV=0.85563 ± 0.00087984, IGD=0.010043 ± 0.00082871

Recommendations combine measured finite-budget outcomes with encoding, constraints and preference reasoning; no universal winner is claimed.