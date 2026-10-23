# v0 results — 2026-10-23

**The registered reliability gates failed.** Two of five seeds learned a perfect
usable binary rule code; three reached 75% on both training and held-out cases.
No tuning or retries were performed. This is a working finite-task demonstration
in some runs, not a reliable learning method or a novelty result.

Protocol: [`f18a0c4`](https://github.com/anttiluode/BindingSol/commit/f18a0c49a4dc458650a3a03e4610350b3c54f04e).
Code before training: [`3f440dc`](https://github.com/anttiluode/BindingSol/commit/3f440dcae6d027bd7c182450ea3661ec57fb91cb).
Raw evidence: [summary](results/v0/summary.json), [manifest](results/v0/manifest.json),
[instrument preflight](results/v0/preflight.json), and per-seed JSON/NPZ in that directory.

## Complete registered batch

Accuracies below are percentages. Train/test/full means 24/8/32 cases respectively.

| Seed | Joint train/test/full | Fresh reader train/test/full | Direct MLP train/test/full | Linear test |
|---|---|---|---|---|
| 41 | 100 / 100 / 100 | 100 / 100 / 100 | 100 / 100 / 100 | 50 |
| 97 | 75 / 75 / 75 | 75 / 75 / 75 | 100 / 100 / 100 | 50 |
| 127 | 75 / 75 / 75 | 75 / 75 / 75 | 100 / 75 / 93.75 | 50 |
| 203 | 100 / 100 / 100 | 100 / 100 / 100 | 100 / 75 / 93.75 | 50 |
| 509 | 75 / 75 / 75 | 75 / 75 / 75 | 100 / 100 / 100 | 50 |

Mean held-out accuracy: joint 85%, fresh reader 85%, direct MLP 90%, linear 50%.
The two communication networks together and the direct MLP each have 162
parameters. These five seeds are descriptive, not evidence of statistical
superiority. Every model sees the same training cases and fixed step budget.

| Gate | Verdict | Evidence |
|---|---|---|
| G0 instrument | PASS | Split/marginals/oracle, finite-difference gradients, checkpoint tests |
| G1 usable channel | FAIL | 2/5 successful seeds; required 4/5 |
| G2 causal use | FAIL | 2/5 meet all intervention criteria; required 4/5 |
| G3 new receiver | FAIL | 2/5 successful seeds; required 4/5 |
| G4 ordinary comparison | REPORTED | Direct MLP succeeds completely in 3/5 seeds |

## What the message does

| Seeds | Normal | Erased | Fair random | Opposite-world message | Sign flipped |
|---|---|---|---|---|---|
| 41, 203 | 100% | 50% | 50% | 0% | 0% |
| 97, 127, 509 | 75% | 50% | 50% | 25% | 25% |

These are held-out scores. The fresh receivers have identical intervention
scores. They were initialized separately and trained with frozen-sender messages
and task labels. This shows supervised readability in this task, not zero-shot
agreement or decoder-free interpretation.

In the perfect runs the binary message equals the world rule, up to the arbitrary
naming of its signs. No product feature or world label was provided to the sender.
Its input was the complete three-sign example; the shared completion loss was
the teacher. The receiving model never received the sender probability.

## Post-hoc failure inspection (not another registered gate)

After aligning the arbitrary message signs to the worlds, the misencoded source
triples are:

| Seed | Misencoded triples out of the eight possible |
|---|---|
| 41 | None |
| 97 | (-1,+1,+1), (+1,-1,-1) |
| 127 | (-1,+1,+1), (+1,-1,-1) |
| 203 | None |
| 509 | (+1,+1,-1), (-1,-1,+1) |

The failures already appear on training examples. Therefore this batch does not
isolate a held-out generalization failure: incomplete sender-rule learning is a
concrete failure location. A fresh receiver does not repair it here. This does
not prove optimization is the sole cause; a v1 diagnostic should separate sender
learning from channel/receiver learning with suitable controls.

## Reproducibility and handoff

Five seeds took about 8.17 seconds of training total in this environment (not a
promise about other hardware). Saved weights were independently reloaded and
reproduced every recorded model metric. A second invocation reused all five
cached seeds without training. The complete test suite passed before training.

To reproduce on another machine, keep the recorded results intact and use:

```bash
python -m pip install -r requirements.txt
python -m unittest discover -s tests -v
python run.py --out results/local-v0
```

The manifest deliberately rejects a changed Python/NumPy version or changed
experiment code in an existing directory. Use a new output directory for such a
run. Interrupted seeds restart; finished seeds are reused. The registered source
revision is linked above and pinned in the manifest.

**Stop point:** v0 is closed. Next is a written v1 diagnostic protocol, before any
new fits. Suggested question: why do some senders encode two of eight triples
incorrectly, and can a fixed-budget learning change improve reliability across
fresh seeds? Preserve this failed v0. Images and J-lens remain deferred.
