import itertools
import unittest
import numpy as np

try:
    import binding as b
except ImportError:
    b = None


class InstrumentTests(unittest.TestCase):
    def setUp(self):
        self.assertIsNotNone(b, 'binding instrument is not implemented')

    def test_split_and_receiver_balance(self):
        d = b.dataset()
        self.assertEqual(len(d['y']), 32)
        self.assertEqual(int(d['train'].sum()), 24)
        self.assertEqual(len(set(map(tuple, np.c_[d['s'], d['q']]))), 32)
        for mask in (d['train'], ~d['train']):
            for query in itertools.product((-1, 1), repeat=2):
                selected = mask & (d['q'] == query).all(axis=1)
                self.assertGreater(int(selected.sum()), 0)
                self.assertEqual(float(d['y'][selected].mean()), 0.5)
        self.assertEqual(set(map(tuple, d['s'][d['train']])),
                         set(map(tuple, d['s'][~d['train']])))

    def test_worlds_have_identical_one_and_two_piece_marginals(self):
        d = b.dataset()
        for size in (1, 2):
            for cols in itertools.combinations(range(3), size):
                distributions = []
                for w in (-1, 1):
                    rows = d['s'][d['w'] == w][:, cols]
                    distributions.append(sorted(map(tuple, rows)))
                self.assertEqual(*distributions)

    def test_oracle_and_causal_interventions(self):
        d = b.dataset()
        sender = lambda s: 10 * np.prod(s, axis=1)
        receiver = lambda x: 10 * np.prod(x, axis=1)
        metrics, cases = b.evaluate(sender, receiver, d)
        for key in ('train', 'test', 'full', 'rule_alignment'):
            self.assertEqual(metrics[key], 1.0)
        for key in ('erased', 'random'):
            self.assertEqual(metrics[key], 0.5)
        for key in ('opposite_world', 'flipped'):
            self.assertEqual(metrics[key], 0.0)
        self.assertEqual(len(cases), 32)
        # Hand-derived: s=(-1,+1,+1) gives w=-1; q=(-1,+1) gives y=+1.
        found = [r for r in cases if r['source'] == [-1, 1, 1]
                 and r['query'] == [-1, 1]]
        self.assertEqual(found[0]['target'], 1)
        self.assertTrue(all(r['message'] in (-1, 1) for r in cases))

    def test_joint_gradient_is_exact_discrete_expectation(self):
        rng = np.random.default_rng(7)
        sender, receiver = b.MLP(3, 3, rng), b.MLP(3, 3, rng)
        d = b.dataset()
        s, q, y = (d[k][d['train']] for k in ('s', 'q', 'y'))
        loss, gs, gr = b.joint_loss_grad(sender, receiver, s, q, y)
        self.assertTrue(np.isfinite(loss))
        for model, grads in ((sender, gs), (receiver, gr)):
            for name, param in model.params.items():
                for index in np.ndindex(param.shape):
                    old = param[index]
                    param[index] = old + 1e-5
                    plus = b.joint_loss_grad(sender, receiver, s, q, y)[0]
                    param[index] = old - 1e-5
                    minus = b.joint_loss_grad(sender, receiver, s, q, y)[0]
                    param[index] = old
                    self.assertAlmostEqual(grads[name][index],
                                           (plus-minus)/2e-5, places=7)

    def test_supervised_gradient_and_parameter_budget(self):
        rng = np.random.default_rng(9)
        net = b.MLP(5, 23, rng)
        self.assertEqual(sum(p.size for p in net.params.values()), 162)
        small = b.MLP(3, 16, rng)
        self.assertEqual(sum(p.size for p in small.params.values()), 81)
        x = rng.normal(size=(6, 5))
        y = np.array([0, 1, 1, 0, 1, 0])
        for width in (0, 3):
            model = b.MLP(5, width, rng)
            loss, grads = b.supervised_loss_grad(model, x, y)
            for name, param in model.params.items():
                for index in np.ndindex(param.shape):
                    old = param[index]
                    param[index] = old + 1e-5
                    plus = b.supervised_loss_grad(model, x, y)[0]
                    param[index] = old - 1e-5
                    minus = b.supervised_loss_grad(model, x, y)[0]
                    param[index] = old
                    self.assertAlmostEqual(grads[name][index],
                                           (plus-minus)/2e-5, places=7)

    def test_incomplete_gates_never_pass(self):
        self.assertEqual(b.verdicts([], expected=5)['status'], 'INCOMPLETE')


if __name__ == '__main__':
    unittest.main()
