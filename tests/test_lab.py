import unittest
import numpy as np
from src import moo_utils as u
from src.problems import get_problem, SUPPLIERS, DIST, TIME, nearest_neighbour
from src.algorithms import load
from src.algorithms.common import crossover,mutate
from src.project_config import (
    DEFAULT_OPTIMIZER_SEED, OPTIMIZER_SEEDS, ROLL_SUFFIX, STUDENT,
    TASK_C_ALGORITHM_NUMBERS, task_c_algorithm_numbers,
)

class ProjectConfiguration(unittest.TestCase):
    def test_student_roll_and_task_c_formula(self):
        self.assertEqual(STUDENT.registration, '241071072')
        self.assertEqual(ROLL_SUFFIX, 72)
        self.assertEqual(task_c_algorithm_numbers(72), (35, 10, 22))
        self.assertEqual(TASK_C_ALGORITHM_NUMBERS, (35, 10, 22))
        self.assertEqual(task_c_algorithm_numbers(0), (37, 12, 24))

    def test_optimizer_seed_namespace(self):
        self.assertEqual(DEFAULT_OPTIMIZER_SEED, 720)
        self.assertEqual(OPTIMIZER_SEEDS, tuple(range(720, 730)))
        self.assertTrue(set(OPTIMIZER_SEEDS).isdisjoint(range(630, 640)))

    def test_missing_metric_series_is_explicit(self):
        from src.experiments.build_deliverables import metric_series
        rows=[{'IGD_mean':None,'IGD_std':None} for _ in range(3)]
        self.assertIsNone(metric_series(rows,'IGD'))
        means,stds=metric_series([{'HV_mean':1.,'HV_std':.1}],'HV')
        self.assertEqual(means,[1.]); self.assertEqual(stds,[.1])

class Utilities(unittest.TestCase):
    def test_dominance(self):
        self.assertTrue(u.dominates([1,2],[2,3])); self.assertFalse(u.dominates([1,3],[2,2]))
        self.assertFalse(u.dominates([1,2],[1,2]))
    def test_deb_table(self):
        f=np.array([[10,10],[1,1],[2,2],[3,3]]); c=np.array([0,.2,.1,0])
        self.assertTrue(u.dominates(f[0],f[1],c[0],c[1]))
        self.assertTrue(u.dominates(f[2],f[1],c[2],c[1]))
        self.assertTrue(u.dominates(f[3],f[0],c[3],c[0]))
        self.assertEqual([list(a) for a in u.non_dominated_sort(f,c)],[[3],[0],[2],[1]])
    def test_car_substitute(self):
        # Cost and fuel consumption: a labelled substitute, not missing lecture data.
        f=np.array([[10,8],[12,6],[14,9],[11,7]])
        self.assertEqual(set(u.nondominated(f)),{0,1,3})
    def test_crowding(self):
        d=u.crowding_distance(np.array([[0,2],[1,1],[2,0]])); self.assertTrue(np.isinf(d[0]) and np.isinf(d[2])); self.assertEqual(d[1],2)
    def test_metrics(self):
        f=np.array([[1,3],[2,2],[3,1]])
        self.assertEqual(u.hypervolume(f,[4,4]),6)
        self.assertEqual(u.igd(f,f),0); self.assertEqual(u.spacing(f),0)
        np.testing.assert_allclose(u.normalize([[2,3]],[0,1],[4,5]),[[.5,.5]])
        self.assertAlmostEqual(u.hypervolume(np.array([[.5,.5,.5]]),[1,1,1],samples=100000),.125,delta=.005)
    def test_archive(self):
        x=np.arange(4)[:,None]; f=np.array([[0,1],[1,0],[2,2],[0,1.]])
        a,b,c=u.archive(x,f,np.zeros(4)); self.assertEqual(len(b),2)

class Problems(unittest.TestCase):
    def test_sanity_checks(self):
        checks={'P1':([5],[4,4]),'P2':([2],[50,4]),'P3':([.5]+[0]*9,[.5,.75]),
        'P4':([0,0,1,0],[.09,-.15]),'P5':([.01,.05],[3.925,.016]),
        'P6':([0,0],[0,50]),'P7':([10,80],[-8,-96]),'P11':([300,200],[-2400,-500]),
        'P13':([0,5],[13,73]),'P14':([13,40],[1.53,-8/.89])}
        for key,(x,expected) in checks.items():
            with self.subTest(key=key):
                f,c=get_problem(key).evaluate(np.array(x)[None]); np.testing.assert_allclose(f[0],expected); self.assertLessEqual(c[0],1e-10)
        p=get_problem('P6'); f,cv=p.evaluate(np.array([[0,0],[1,1],[0,3],[.2,3]]))
        np.testing.assert_allclose(f,[[0,50],[8,32],[36,29],[36.16,27.04]])
        np.testing.assert_allclose(cv,[0,0,.36,.2816])
        self.assertEqual([list(z) for z in u.non_dominated_sort(f,cv)],[[0,1],[3],[2]])
    def test_dtlz_sphere(self):
        for m in [3,5]:
            p=get_problem('P10',m); x=p.sample(np.random.default_rng(2),12); x[:,m-1:]=.5
            f,c=p.evaluate(x); np.testing.assert_allclose((f*f).sum(1),1)
    def test_p8(self):
        self.assertTrue(np.allclose(DIST,DIST.T)); self.assertTrue(np.allclose(TIME,TIME.T))
        p=get_problem('P8'); tour=nearest_neighbour(DIST); f,c=p.evaluate(tour[None]); self.assertEqual(c[0],0)
        for seed in range(20):
            r=np.random.default_rng(seed); child=crossover(p,tour,r.permutation(15),r); child=mutate(p,child,r)
            np.testing.assert_array_equal(np.sort(child),np.arange(15))
    def test_p9_loader_classifier(self):
        from src.problems import cancer_data,knn_error
        ds,folds=cancer_data(); self.assertEqual(ds.data.shape,(569,30)); error=knn_error((True,)*30)
        self.assertLess(error,.1); self.assertEqual(sum(len(z[2]) for z in folds),569)
    def test_p12(self):
        f,c=get_problem('P12').evaluate(np.arange(5)[:,None]); np.testing.assert_equal(f[:,0],SUPPLIERS[:,0])

class Mechanisms(unittest.TestCase):
    pass

def mechanism(number):
    def test(self):
        a=load(number); f=np.array([[0.,1.],[.5,.5],[1.,0.],[1.,1.]])
        c=np.zeros(4)
        if number==1: self.assertEqual(a.scalar([2,4],[.25,.75]),3.5); self.assertEqual(a.analytic_p1(.25),6.)
        elif number==2: self.assertEqual(a.scalar([2,4]),2)
        elif number==3: self.assertEqual(a.improvement(np.array([.2,.3]),[.5,.5],np.array([1.,1.])),.75)
        elif number==4: self.assertEqual(a.metric(np.array([2,4]),[.5,.5],np.inf),2)
        elif number==5: self.assertEqual(a.utility(np.array([1,2]),np.array([1,2])),0)
        elif number==6:
            minus,plus=a.deviations(np.array([2400,500]),np.array([2400,600])); np.testing.assert_equal(minus,[0,100]); np.testing.assert_equal(plus,[0,0])
        elif number==7: self.assertGreater(a.preserve(1,1),0); self.assertLess(a.preserve(1.01,1),0)
        elif number==8:
            r=a.run([[1,1],[2,2]]); self.assertEqual(r['order'][0],0); self.assertAlmostEqual(r['score'][0],1)
        elif number==9:
            r=a.run([[1,1],[2,2]]); self.assertEqual(r['order'][0],0); self.assertTrue(r['advantage'] and r['stability'])
        elif number==10:
            s=a.initialize(get_problem('P3'),100,1,population=4); ids=a.select(s); self.assertEqual(len(ids),4)
        elif number in [11,12]:
            fit=a.fitness(f,c); self.assertLess(fit[3],fit[0])
        elif number==13:
            self.assertEqual(a.pareto_tournament(f,c,0,3,[1]),0)
        elif number in [14,21]:
            from src.algorithms.common import environmental
            self.assertNotIn(3,environmental(f,c,3))
            if number==21: self.assertTrue(a.deb_compare([10,10],[1,1],0,.1))
        elif number==15:
            groups,d=a.associate(np.array([[1,0],[0,1]]),np.eye(2)); np.testing.assert_equal(groups,[0,1])
        elif number==16:
            fit=a.fitness(f,c); self.assertGreater(fit[3],fit[0]); self.assertNotIn(3,a.select(f,c,3))
        elif number==17:
            group,counts=a.regions(np.array([[0,0],[0,0],[1,1]])); self.assertEqual(counts.max(),2)
        elif number in [18,19,20]:
            self.assertAlmostEqual(a.tchebycheff(np.array([2,4]),[.5,.5],[0,0]),2)
            if number==20:
                tour=a.construct(np.random.default_rng(1),np.ones((15,15)),1/np.maximum(DIST,1e-9)); self.assertEqual(len(set(tour)),15)
        elif number==22: np.testing.assert_allclose(a.velocity(np.zeros(2),np.zeros(2),np.ones(2),np.ones(2),np.ones(2),np.ones(2)),[3,3])
        elif number==23: np.testing.assert_allclose(a.encircle(np.zeros(2),np.ones((3,2)),np.zeros((3,2)),np.ones((3,2))),[1,1])
        elif number==24:
            s=a.initialize(get_problem('P5'),100,1,population=4); y=a.neighbour(s,0); self.assertTrue(np.all(y>=s.p.lower) and np.all(y<=s.p.upper))
        elif number==25:
            tau=np.ones((15,15)); a.deposit(tau,np.arange(15),1); self.assertEqual(tau[0,1],2); self.assertEqual(tau[1,0],2)
        elif number==26:
            self.assertAlmostEqual(a.acceptance(np.array([0,0]),np.array([1,1]),1,[.5,.5]),np.exp(-2))
            self.assertEqual(a.acceptance(np.array([1,1]),np.array([0,0]),1,[.5,.5]),1)
        elif number==27: np.testing.assert_allclose(a.donor(np.array([1,1]),np.array([3,3]),np.array([1,1])),[2,2])
        elif number==28: np.testing.assert_allclose(a.teacher_move(np.array([1,1]),np.array([3,3]),np.array([1,1]),.5,2),[1.5,1.5])
        elif number==29:
            aa,pp=a.schedules(0); self.assertEqual(pp,0); self.assertLess(a.schedules(20)[0],aa); self.assertGreater(a.schedules(20)[1],pp)
        elif number==30:
            s=a.initialize(get_problem('P8'),100,1,population=4); a.iterate(s); self.assertGreater(s.used,8)
        elif number==31:
            g,v=a.apd(np.array([[1,0],[0,1],[1,1]]),np.eye(2),.5); self.assertGreater(v[2],v[0])
        elif number==32: self.assertLess(a.indicator(f)[0,3],0.01); self.assertNotIn(3,a.select(f,c,3))
        elif number==33:
            z=np.array([[1,3],[2,2],[3,1.]])
            cont=a.contributions(z,[4,4]); np.testing.assert_allclose(cont,[1,1,1])
        elif number==34:
            cont=a.contributions(np.array([[.5,.5,.5]]),[1,1,1],np.random.default_rng(1),100000)
            self.assertAlmostEqual(cont[0],.125,delta=.005)
        elif number==35:
            ids=a.preference_select(f,c,2,get_problem('P3')); self.assertIn(1,ids); self.assertNotIn(3,ids)
        elif number==36: np.testing.assert_allclose(a.weights([[1,0],[-1,0]]),[.5,.5])
        elif number==37:
            w=a.update_weights(np.ones(2),np.ones(2),np.ones(2),np.array([[10.,0],[1.,0]]))
            self.assertLess(w[0],w[1]); self.assertAlmostEqual(w.sum(),2)
    return test
for number in range(1,38): setattr(Mechanisms,'test_%02d_mechanism'%number,mechanism(number))

class Reproducibility(unittest.TestCase):
    def test_stochastic_modules(self):
        for number in range(10,36):
            with self.subTest(algorithm=number):
                p=get_problem('P8') if number in [20,25] else get_problem('P3')
                a=load(number); r=a.run(p,budget=64,seed=5,population=8); t=a.run(p,budget=64,seed=5,population=8)
                np.testing.assert_allclose(r['f'],t['f']); self.assertEqual(r['evaluations'],64)
                if len(r['x']): self.assertTrue(np.all(r['x']>=p.lower) and np.all(r['x']<=p.upper))

if __name__=='__main__': unittest.main()

class NetworkGradient(unittest.TestCase):
    def test_finite_difference(self):
        from src.problems.network import initialize,data,forward_backward
        p=initialize(1); batch=data(2); f,g,shared=forward_backward(p,batch)
        for task in range(2):
            for param,index in [(0,(1,2)),(2,(3,)),(4,(3,)),(1,(2,))]:
                old=p[param][index]; h=1e-6
                p[param][index]=old+h; fp=forward_backward(p,batch)[0][task]
                p[param][index]=old-h; fm=forward_backward(p,batch)[0][task]; p[param][index]=old
                self.assertAlmostEqual(g[task][param][index],(fp-fm)/(2*h),places=5)


class ActualCallAccounting(unittest.TestCase):
    def test_scalar_and_gradient_call_counts(self):
        for a in [1,2,3,4,5,6,7,36,37]:
            with self.subTest(algorithm=a):
                p=get_problem('P11' if a in [6,7] else 'P14' if a==5 else 'P13' if a>=36 else 'P1')
                original=p.evaluate; counter=[0]
                def counted(x):
                    counter[0]+=len(np.atleast_2d(x)); return original(x)
                p.evaluate=counted
                result=load(a).run(p,budget=1000,seed=DEFAULT_OPTIMIZER_SEED)
                self.assertEqual(counter[0],result['evaluations'])
                self.assertLessEqual(counter[0],1000)
