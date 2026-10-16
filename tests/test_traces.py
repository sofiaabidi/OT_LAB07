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
            np.testing.assert_allclose(row['reference_natural'],[4,4])
            np.testing.assert_allclose(row['normalization_ideal'],[0,0])
            np.testing.assert_allclose(row['normalization_nadir'],[16,16])
            np.testing.assert_allclose(ref,[.25,.25])
            np.testing.assert_allclose(np.linalg.norm(z-ref,axis=1),row['distance_to_reference'])
            chosen=row['selected_indices']; self.assertEqual(len(chosen),4)
            self.assertEqual(len(set(chosen)),4)
            self.assertEqual(row['fronts'],[list(range(8))])
            self.assertTrue(all(d['decision'] in {'accept','defer','backfill'}
                                for d in row['clearing_decisions']))
        np.testing.assert_allclose(rows[0]['selected_x'],[5.5,4.5,3.5,6.5])
        np.testing.assert_allclose(rows[1]['parents_x'],rows[0]['selected_x'])
        np.testing.assert_allclose(rows[1]['selected_x'],[5.25,4.5,6.5,3.5])

    def test_vega_two_iterations(self):
        rows=build()['vega']; self.assertEqual(len(rows),2)
        np.testing.assert_allclose(rows[0]['mating_pool'],[3,7,4,6])
        np.testing.assert_allclose(rows[1]['mating_pool'],rows[0]['next_population'])
        self.assertEqual([row['winner_indices'] for row in rows],
                         [[0,3,1,2],[0,1,2,3]])
        for row in rows:
            self.assertEqual(row['population_size'],4)
            self.assertEqual(len(row['winner_indices']),4)
            beta=(2*row['sbx_u'])**(1/16)
            self.assertAlmostEqual(beta,row['sbx_beta'])
            expected=[]
            for left,right in row['parent_pairs']:
                expected.extend([.5*((1+beta)*left+(1-beta)*right),
                                 .5*((1-beta)*left+(1+beta)*right)])
            np.testing.assert_allclose(row['offspring'],expected)
            np.testing.assert_allclose(row['next_population'],row['offspring'])
            population=np.asarray(row['population'])
            expected_f=np.c_[(population-3)**2,(population-7)**2]
            np.testing.assert_allclose(row['F'],expected_f)
            offspring=np.asarray(row['offspring'])
            np.testing.assert_allclose(row['offspring_F'],
                                       np.c_[(offspring-3)**2,(offspring-7)**2])

    def test_mopso_two_iterations(self):
        rows=build()['mopso']; self.assertEqual(len(rows),2)
        self.assertTrue(all(r['population_size']==4 for r in rows))
        np.testing.assert_allclose(rows[0]['new_velocity'],[7.5,3.75,-7.5,-5.25])
        np.testing.assert_allclose(rows[0]['new_x'],[12.5,13.75,7.5,6.75])
        np.testing.assert_allclose(rows[1]['new_velocity'],[1.5,.75,-1.5,-1.05])
        np.testing.assert_allclose(rows[1]['new_x'],[14,14.5,6,5.7])
        self.assertEqual([r['archive_size_after'] for r in rows],[8,12])
        self.assertTrue(all(len(r['new_x']) == 4 for r in rows))
        for row in rows:
            self.assertEqual(row['problem_definition'],
                             'independent scalar toy; not assignment P2')
            self.assertTrue(np.all(np.asarray(row['old_x']) >= 1))
            self.assertTrue(np.all(np.asarray(row['old_x']) <= 20))
            self.assertTrue(np.all(np.asarray(row['new_x']) >= 1))
            self.assertTrue(np.all(np.asarray(row['new_x']) <= 20))
            self.assertTrue(np.all(np.abs(row['new_velocity']) <= 10))
            self.assertTrue(all(leader in row['archive_before']
                                for leader in row['leader']))
            np.testing.assert_allclose(np.asarray(row['inertia_term'])+
                                       np.asarray(row['cognitive_term'])+
                                       np.asarray(row['social_term']),row['new_velocity'])
            np.testing.assert_allclose(np.asarray(row['old_x'])+
                                       np.asarray(row['new_velocity']),row['new_x'])
            self.assertEqual(row['pbest_decisions'],['retain: incomparable']*4)
            old=np.asarray(row['old_x']); new=np.asarray(row['new_x'])
            np.testing.assert_allclose(row['old_F'],np.c_[100/old,old**2])
            np.testing.assert_allclose(row['F'],np.c_[100/new,new**2])
            np.testing.assert_allclose(row['archive_after'],
                                       row['archive_before']+row['new_x'])
            archive=np.asarray(row['archive_after'])
            archive_f=np.c_[100/archive,archive**2]
            for i in range(len(archive)):
                for j in range(len(archive)):
                    if i!=j:
                        self.assertFalse(np.all(archive_f[i]<=archive_f[j]) and
                                         np.any(archive_f[i]<archive_f[j]))


if __name__=='__main__': unittest.main()
