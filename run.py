"""Run a bounded batch, checkpointing completed seeds without mixing versions."""
import argparse
import hashlib
import json
from pathlib import Path
import platform
import subprocess
import sys
import time
import numpy as np
from binding import SEEDS, run_seed, verdicts

ROOT = Path(__file__).resolve().parent


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def atomic_json(path, value):
    temporary = path.with_suffix(path.suffix+'.tmp')
    temporary.write_text(json.dumps(value, indent=2, allow_nan=False)+'\n', encoding='utf-8')
    temporary.replace(path)


def run_experiment(out, seeds=SEEDS, steps=5000, lr=.01, max_new=None):
    seeds = tuple(seeds)
    if (not seeds or len(set(seeds)) != len(seeds)
            or any(not isinstance(s, int) or s < 0 for s in seeds)
            or not isinstance(steps, int) or steps <= 0
            or not np.isfinite(lr) or lr <= 0
            or (max_new is not None and (not isinstance(max_new, int) or max_new < 0))):
        raise ValueError('invalid seeds, steps, learning rate or max_new')
    out = Path(out)
    source = {name: digest(ROOT/name) for name in ('binding.py', 'run.py', 'PREREG.md')}
    config = {'seeds': list(seeds), 'steps': steps, 'lr': lr, 'source': source,
              'python': platform.python_version(), 'numpy': np.__version__}
    manifest_path = out/'manifest.json'
    if manifest_path.exists():
        try:
            manifest = json.loads(manifest_path.read_text(encoding='utf-8'))
        except (ValueError, OSError) as exc:
            raise ValueError('unreadable manifest; preserve it and use a new directory') from exc
        if manifest.get('config') != config:
            raise ValueError('manifest mismatch; use a new output directory')
    else:
        if out.exists() and any(out.iterdir()):
            raise ValueError('nonempty output without manifest; refusing to overwrite')
        out.mkdir(parents=True, exist_ok=True)
        git = subprocess.run(['git', 'rev-parse', 'HEAD'], cwd=ROOT,
                             capture_output=True, text=True, check=False)
        manifest = {'config': config, 'git_commit': git.stdout.strip() or 'unknown',
                    'registered': seeds == SEEDS and steps == 5000 and lr == .01}
        atomic_json(manifest_path, manifest)
    fingerprint = hashlib.sha256(json.dumps(config, sort_keys=True).encode()).hexdigest()
    records, new = [], 0
    for seed in seeds:
        record_path, weights_path = out/f'seed-{seed}.json', out/f'seed-{seed}.npz'
        if record_path.exists():
            try:
                record = json.loads(record_path.read_text(encoding='utf-8'))
                if (record['seed'] != seed or record['fingerprint'] != fingerprint
                        or record['weights_sha256'] != digest(weights_path)):
                    raise ValueError('identity or weights mismatch')
                for name in ('joint', 'fresh', 'direct', 'linear'):
                    for metric in ('train', 'test', 'full'):
                        value = record[name][metric]
                        if not isinstance(value, (float, int)) or not 0 <= value <= 1:
                            raise ValueError('invalid accuracy')
                with np.load(weights_path, allow_pickle=False) as archive:
                    if not archive.files or not all(np.isfinite(archive[k]).all()
                                                    for k in archive.files):
                        raise ValueError('invalid weights')
            except (ValueError, KeyError, OSError, TypeError) as exc:
                raise ValueError(f'corrupt checkpoint {record_path}; preserve and investigate') from exc
            print(f'seed {seed}: cached', flush=True)
        elif max_new is None or new < max_new:
            started = time.perf_counter()
            record, weights = run_seed(seed, steps, lr)
            record['elapsed_seconds'] = time.perf_counter()-started
            temporary = weights_path.with_suffix('.npz.tmp')
            with temporary.open('wb') as handle:
                np.savez_compressed(handle, **weights)
            temporary.replace(weights_path)
            record.update(fingerprint=fingerprint, weights_sha256=digest(weights_path))
            atomic_json(record_path, record)
            new += 1
            print(f"seed {seed}: joint={record['joint']['test']:.3f} "
                  f"fresh={record['fresh']['test']:.3f} "
                  f"direct={record['direct']['test']:.3f} "
                  f"({record['elapsed_seconds']:.2f}s)", flush=True)
        else:
            continue
        records.append(record)
        # Keep the summary useful even if the next seed is interrupted.
        summary = {'registered': manifest['registered'], 'gates': verdicts(records, len(seeds)),
                   'seeds': [{k: r[k] for k in ('seed', 'joint', 'fresh', 'direct', 'linear')}
                             for r in records]}
        atomic_json(out/'summary.json', summary)
    if not records:
        summary = {'registered': manifest['registered'], 'gates': verdicts([], len(seeds)),
                   'seeds': []}
        atomic_json(out/'summary.json', summary)
    return summary


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', type=Path, default=ROOT/'results'/'v0')
    parser.add_argument('--max-new', type=int, help='stop after this many new seeds; later rerun resumes')
    args = parser.parse_args()
    # G0 must pass before any registered training. Tests use fixtures, not v0 fits.
    test = subprocess.run([sys.executable, '-m', 'unittest', 'discover', '-s',
                           str(ROOT/'tests'), '-v'], cwd=ROOT, capture_output=True, text=True)
    if test.returncode:
        print(test.stdout+test.stderr, file=sys.stderr)
        raise SystemExit('G0 failed: no registered training was run')
    print('G0: instrument and checkpoint tests passed', flush=True)
    result = run_experiment(args.out, max_new=args.max_new)
    atomic_json(args.out/'preflight.json', {'G0': 'PASS', 'output': test.stdout+test.stderr,
                'tests_sha256': {p.name: digest(p) for p in sorted((ROOT/'tests').glob('test_*.py'))}})
    print(json.dumps(result['gates'], indent=2))


if __name__ == '__main__':
    main()
