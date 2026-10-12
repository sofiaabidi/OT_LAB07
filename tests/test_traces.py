import unittest
import numpy as np
from src.experiments.traces import build
from src.algorithms.npga import pareto_tournament
from src.problems import get_problem

class HandTraces(unittest.TestCase):
    def test_weighted_sum(self):
        t=build()['weighted_sum']; self.assertEqual([v['x'] for v in t],[6,4])
        np.testing.assert_equal([v['objectives'] for v in t],[[9,1],[1,9]])
        np.testing.assert_equal([v['raw_scalar'] for v in t],[3,3])
    def test_mosa_two_generations(self):
        t=build()['mosa']; np.testing.assert_allclose(t[0]['worsened_sum'],[.015625,.078125,.203125,.28125])
        np.testing.assert_equal(t[0]['accepted'],[True,True,True,False])
        np.testing.assert_allclose(t[0]['next_x'],[3.5,4.5,6.5,7])
        np.testing.assert_allclose(t[1]['T'],.097)
        np.testing.assert_equal(t[1]['accepted'],[True,True,True,True])
        np.testing.assert_allclose(t[1]['next_x'],[4,5,7,6.5])
    def test_npga_two_generations(self):
        t=build()['npga']; self.assertEqual(len(t),2)
        # Independent loop sharing check, then winner decisions from counts.
        for row in t:
            z=np.array(row['normalized_F']); nc=[]
            for a in z: nc.append(sum(max(0,1-sum((a-b)**2)/(.8**2)) for b in z))
            np.testing.assert_allclose(nc,row['niche_counts'])
            expected=[]
            f=np.array(row['F'])
            for (a,b),C in zip(row['pairs'],row['comparison_sets']):
                if np.all(f[a]<=f[b]) and np.any(f[a]<f[b]): expected.append(a)
                elif np.all(f[b]<=f[a]) and np.any(f[b]<f[a]): expected.append(b)
                else:
                    na=sum(max(0,1-sum((z[a]-z[j])**2)/.8**2) for j in C)
                    nb=sum(max(0,1-sum((z[b]-z[j])**2)/.8**2) for j in C)
                    expected.append(a if na<=nb+1e-12 else b)
            self.assertEqual(expected,row['winners'])
            child=np.array(row['population'])[expected]+np.array(row['increments'])
            np.testing.assert_allclose(child,row['offspring'])
