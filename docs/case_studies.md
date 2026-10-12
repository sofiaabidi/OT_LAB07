# Task E six selection cases

## P1
Suitable: Weighted Sum,Weight Metric. Poor: VEGA. Convex one-variable problem; scalarization offers interpretable weights and metric methods expose compromise geometry.

Evidence: A1 M=2 base: HV=1.0258 +/- 0, IGD=0.020135 +/- 0; A4 M=2 base: HV=1.0347 +/- 0, IGD=0.012339 +/- 0

Recommendations combine measured finite-budget outcomes with encoding, constraints and preference reasoning; no universal winner is claimed.

## P3
Suitable: SMS-EMOA,MO-TLBO. Poor: Weighted Sum. Nonconvex front; hypervolume survival and teacher-learner moves both cover interior tradeoffs in the recorded experiments, while linear scalarization cannot support them.

Evidence: A28 M=2 D: HV=0.53182 +/- 6.3878e-05, IGD=0.0095565 +/- 0.00010113; A33 M=2 D: HV=0.53187 +/- 7.9941e-05, IGD=0.0096626 +/- 0.00018987; A28 M=2 base: HV=0.53182 +/- 6.3878e-05, IGD=0.0095565 +/- 0.00010113; A33 M=2 base: HV=0.53187 +/- 7.9941e-05, IGD=0.0096626 +/- 0.00018987

Recommendations combine measured finite-budget outcomes with encoding, constraints and preference reasoning; no universal winner is claimed.

## P5
Suitable: Constrained NSGA-II,SPEA2. Poor: VEGA. Nonlinear feasibility makes Deb rules useful; archive strength and density support constrained tradeoffs.

Evidence: A16 M=2 D: HV=1.1818 +/- 4.5953e-05, IGD=0.014428 +/- 0.0020419; A21 M=2 D: HV=1.1818 +/- 7.2189e-05, IGD=0.014663 +/- 0.002837; A16 M=2 base: HV=1.1818 +/- 4.5953e-05, IGD=0.014428 +/- 0.0020419; A21 M=2 base: HV=1.1818 +/- 7.2189e-05, IGD=0.014663 +/- 0.002837

Recommendations combine measured finite-budget outcomes with encoding, constraints and preference reasoning; no universal winner is claimed.

## P8
Suitable: NSGA-II,MOEA/D-ACO. Poor: MGDA. Permutation-safe NSGA-II and ant decomposition have the leading recorded HV means and retain valid tours; gradient descent is undefined for city orders.

Evidence: A14 M=2 D: HV=0.92385 +/- 0.00020309, IGD=N/A +/- N/A; A20 M=2 D: HV=0.92372 +/- 0.00050562, IGD=N/A +/- N/A; A20 M=2 base: HV=0.92372 +/- 0.00050562, IGD=N/A +/- N/A

Recommendations combine measured finite-budget outcomes with encoding, constraints and preference reasoning; no universal winner is claimed.

## P10
Suitable: RVEA,MOEA/D. Poor: VEGA. Five objectives weaken dominance; RVEA APD and MOEA/D scalar subproblems retain directional pressure and have the strongest recorded HV means at this budget.

Evidence: A18 M=5 D: HV=0.99988 +/- 0.033592, IGD=0.32929 +/- 0.024052; A31 M=5 D: HV=1.0076 +/- 0.020813, IGD=0.30822 +/- 0.011729; A18 M=5 base: HV=0.99988 +/- 0.033592, IGD=0.32929 +/- 0.024052; A31 M=3 base: HV=0.64011 +/- 0.0086752, IGD=0.10871 +/- 0.0050531; A31 M=5 base: HV=1.0076 +/- 0.020813, IGD=0.30822 +/- 0.011729

Recommendations combine measured finite-budget outcomes with encoding, constraints and preference reasoning; no universal winner is claimed.

## P14
Suitable: R-NSGA-II,Value Function. Poor: VEGA. Known manager aspiration makes a preferred region useful; utility or reference clearing expresses it directly.

Evidence: A5 M=2 base: HV=0.32905 +/- 0, IGD=0.35302 +/- 0; A35 M=2 base: HV=0.85628 +/- 0.00064468, IGD=0.0094464 +/- 0.00049587

Recommendations combine measured finite-budget outcomes with encoding, constraints and preference reasoning; no universal winner is claimed.