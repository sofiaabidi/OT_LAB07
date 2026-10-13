import unittest
import numpy as np

from src.experiments.traces import build


class HandTraces(unittest.TestCase):
    def test_r_nsga2_two_iterations(self):
        rows=build()['r_nsga2']; self.assertEqual(len(rows),2)
        for row in rows:
            self.assertEqual(row['population_size'],4)
            self.assertEqual(len(row['parents_x']),4)
            self.assertEqual(len(row['offspring_x']),4)
            z=np.asarray(row['normalized_F']); ref=np.asarray(row['normalized_reference'])
            np.testing.assert_allclose(np.linalg.norm(z-ref,axis=1),row['distance_to_reference'])
            chosen=row['selected_indices']; self.assertEqual(len(chosen),4)
            self.assertEqual(len(set(chosen)),4)
        np.testing.assert_allclose(rows[0]['selected_x'],[5.5,4.5,3.5,6.5])
        np.testing.assert_allclose(rows[1]['selected_x'],[5.25,4.5,6.,4.75])

    def test_vega_two_iterations(self):
        rows=build()['vega']; self.assertEqual(len(rows),2)
        np.testing.assert_allclose(rows[0]['mating_pool'],[40,30,40,30])
        np.testing.assert_allclose(rows[1]['mating_pool'],[40,40,40,40])
        for row in rows:
            self.assertEqual(row['population_size'],4)
            x=np.asarray(row['population'])
            np.testing.assert_allclose(row['f1_min'],1000/x)
            np.testing.assert_allclose(row['f2_max'],x*x/100)

    def test_mopso_two_iterations(self):
        rows=build()['mopso']; self.assertEqual(len(rows),2)
        self.assertTrue(all(r['population_size']==4 for r in rows))
        np.testing.assert_allclose(rows[0]['new_velocity'],[7.5,3.75,-7.5,-5.25])
        np.testing.assert_allclose(rows[0]['new_x'],[12.5,13.75,7.5,6.75])
        np.testing.assert_allclose(rows[1]['new_velocity'],[1.5,.75,-1.5,-1.05])
        np.testing.assert_allclose(rows[1]['new_x'],[14,14.5,6,5.7])
        self.assertEqual([r['archive_size_after'] for r in rows],[8,12])
        self.assertTrue(all(len(r['new_x']) == 4 for r in rows))


if __name__=='__main__': unittest.main()
