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

## Code Walkthrough Preparation

### A10 VEGA
In src/algorithms/vega.py, change the population default from 40 to 20 while retaining the 10000-evaluation cap. Predict twice as many approximate generations but half as many simultaneous candidates. Objective-wise tournaments remain unchanged; coverage can become less stable even if later generations improve convergence. The existing N=20,40,80 sensitivity rows test this tradeoff.

### A22 MOPSO
In src/algorithms/mopso.py, change inertia from 0.4 to 0.8 in the velocity call. The retained w*v term doubles, so particles preserve momentum longer, explore farther and can overshoot leaders or hit clipping more often. Personal-best and archive dominance rules do not change. The stored w=0.2,0.4,0.8 P4 study provides the numerical comparison.

### A35 R-NSGA-II
In src/algorithms/r_nsga2.py, increase epsilon in preference selection from 0.05 to 0.10. Candidates must then be farther apart in normalized objective space to survive clearing; more near-reference points are deferred and distance-ordered backfill becomes more likely. Nondominated fronts and reference distances themselves do not change. The stored epsilon=0.02,0.05,0.10 P14 study tests the effect.