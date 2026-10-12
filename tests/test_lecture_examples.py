"""Exact supplied lecture data; numerical rounding is explicit."""
import unittest
import numpy as np
from src.moo_utils import dominates,nondominated,non_dominated_sort
from src.algorithms import npga,mosa,benson

class Lectures(unittest.TestCase):
    def test_car_front_part1_slide8(self):
        f=np.array([[5,-15],[8,-22],[6,-18],[10,-25],[7,-12],[9,-20.]])
        self.assertEqual(set(nondominated(f)),{0,1,2,3})
        self.assertTrue(dominates(f[0],f[4])); self.assertTrue(dominates(f[1],f[5]))
    def test_deb_part1_slide22(self):
        f=np.array([[3,6],[4,5],[1,2],[.5,1]]); cv=np.array([0,0,2,5])
        self.assertEqual([list(x) for x in non_dominated_sort(f,cv)],[[0,1],[2],[3]])
    def test_npga_lecture_two_rounds(self):
        # Telecom: cost min, reliability max. Preserve specified fixed scales.
        f=np.array([[10,-.8],[15,-.9],[12,-.85],[18,-.95]])
        nc=npga.comparison_niches(f,0,1,[2,3],.5,np.array([10,-1.]),np.array([20,-.8]))
        np.testing.assert_allclose(nc,[.59,.78],atol=1e-12)
        self.assertEqual(npga.pareto_tournament(f,np.zeros(4),0,1,[2,3],.5,np.array([10,-1.]),np.array([20,-.8])),0)
        nc=npga.comparison_niches(f,2,3,[0,1],.5,np.array([10,-1.]),np.array([20,-.8]))
        np.testing.assert_allclose(nc,[.98,.39],atol=1e-12)
        self.assertEqual(npga.pareto_tournament(f,np.zeros(4),2,3,[0,1],.5,np.array([10,-1.]),np.array([20,-.8])),3)
        # Slides round sh=.389, NC=.778/.979; exact specified formulas give
        # .390, .780/.980. Decisions agree; we retain exact arithmetic.
    def test_mosa_lecture_two_iterations(self):
        x=10.; archive=[]; T=100.
        for proposal in [13.,15.]:
            old=np.array([30-x,5+.5*x]); new=np.array([30-proposal,5+.5*proposal])
            self.assertEqual(mosa.acceptance(old,new,T),1.)
            archive.append(new); x=proposal; T*=.9
        np.testing.assert_allclose(archive,[[17,11.5],[15,12.5]]); self.assertAlmostEqual(T,81.)
        self.assertAlmostEqual(mosa.acceptance(np.array([20,10]),np.array([23,12]),100),np.exp(-.05))
    def test_benson_lecture_signs(self):
        # Hospital natural reference (100 min cost,50 max patients).
        reference=np.array([100,-50]); f=np.array([90,-60]); achievements=reference-f
        np.testing.assert_equal(achievements,[10,10]); self.assertEqual(benson.improvement(f,[.5,.5],reference),10)
