import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import numpy as np

try:
    import run as runner
except ImportError:
    runner = None


def fixture(seed, steps, lr):
    # Replace only the costly training boundary. The real persistence and gates run.
    m = dict(train=1., test=1., full=1., rule_alignment=1., erased=.5,
             random=.5, opposite_world=0., flipped=0.)
    return dict(seed=seed, joint=m, fresh=m, direct=m, linear=m,
                cases=[], fresh_cases=[]), {'fixture': np.array([seed], dtype=float)}


class ResumeTests(unittest.TestCase):
    def setUp(self):
        self.assertIsNotNone(runner, 'checkpoint runner is not implemented')
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.out = Path(self.temp.name)/'run'

    def test_partial_resume_and_configuration_guard(self):
        with patch.object(runner, 'run_seed', side_effect=fixture) as train:
            partial = runner.run_experiment(self.out, (11, 12), 2, .01, max_new=1)
            self.assertEqual(partial['gates']['status'], 'INCOMPLETE')
            self.assertEqual(train.call_count, 1)
            done = runner.run_experiment(self.out, (11, 12), 2, .01)
            self.assertEqual(len(done['seeds']), 2)
            self.assertEqual(train.call_count, 2)
            runner.run_experiment(self.out, (11, 12), 2, .01)
            self.assertEqual(train.call_count, 2)
            with self.assertRaisesRegex(ValueError, 'manifest'):
                runner.run_experiment(self.out, (11, 12), 3, .01)
        self.assertEqual(len(list(self.out.glob('seed-*.npz'))), 2)

    def test_corrupt_weights_and_result_are_rejected(self):
        with patch.object(runner, 'run_seed', side_effect=fixture):
            runner.run_experiment(self.out, (11,), 2, .01)
        (self.out/'seed-11.npz').write_bytes(b'broken')
        with self.assertRaisesRegex(ValueError, 'checkpoint'):
            runner.run_experiment(self.out, (11,), 2, .01)
        (self.out/'seed-11.json').write_text('{')
        with self.assertRaisesRegex(ValueError, 'checkpoint'):
            runner.run_experiment(self.out, (11,), 2, .01)

    def test_orphan_weights_are_recomputed_and_unknown_files_rejected(self):
        with patch.object(runner, 'run_seed', side_effect=fixture) as train:
            runner.run_experiment(self.out, (11,), 2, .01, max_new=0)
            (self.out/'seed-11.npz').write_bytes(b'interrupted')
            runner.run_experiment(self.out, (11,), 2, .01)
            self.assertEqual(train.call_count, 1)
        other = self.out.parent/'unmanaged'
        other.mkdir()
        (other/'precious.txt').write_text('keep')
        with self.assertRaisesRegex(ValueError, 'nonempty'):
            runner.run_experiment(other, (11,), 2, .01)

    def test_invalid_settings_do_not_write(self):
        for seeds, steps, lr in (((), 2, .01), ((1, 1), 2, .01),
                                 ((1,), 0, .01), ((1,), 2, float('nan'))):
            with self.assertRaises(ValueError):
                runner.run_experiment(self.out, seeds, steps, lr)
        self.assertFalse(self.out.exists())


if __name__ == '__main__':
    unittest.main()
