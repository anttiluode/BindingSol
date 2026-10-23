# BindingSol v0 — locked before training, 2026-10-23

## Question and scope

Can two ordinary small neural networks learn a binary communication protocol
that transfers a three-piece rule to held-out source/query combinations? Can a
fresh receiver learn to read the frozen sender? All claims concern this finite,
constructed task. A positive result is an engineering baseline, not novelty.

## Data and split

Signs are -1 or +1. Enumerate all 32 tuples `(w,a,b,u,v)` exactly once.
The sender sees `s=(a,b,c)` where `c=w*a*b`; the receiver sees `q=(u,v)` and
predicts `y=w*u*v`. World `w` and `y` never enter the sender input; `w`, `s`,
episode index and random seed never enter the receiver input.

Hold out the eight tuples with `(u,v)=(a,a*b)`. Train on the other 24.
Both worlds and every individual sender triple and query pair are in training;
only their combinations are held out. This is compositional transfer within one
fixed symbol system, NOT a new rule, alphabet, spatial layout or natural image.
The split is fixed and disclosed; there is no validation-based tuning.

Receiver-only inputs have exactly balanced labels within each query in both
splits. The full world distributions agree on all one- and two-piece marginals.
An analytic oracle computes `w=a*b*c`; it is a sanity control only.

## Models and training

- Sender: tanh MLP 3 -> 16 -> 1, sigmoid probability of message +1.
- Receiver: tanh MLP 3 -> 16 -> 1, input `(message,u,v)`, output logit for y=+1.
- Joint objective: exact expectation of binary cross-entropy over messages -1,+1.
  This is differentiable without a straight-through estimator. The receiver only
  sees the discrete symbol, never the sender's real-valued probability.
- Evaluation: deterministic message from probability >=0.5; output sign from
  logit >=0. Labels are supplied to the loss, not to input features.
- Adam, learning rate 0.01, beta1 0.9, beta2 0.999, epsilon 1e-8; 5,000 full-batch
  steps, float64. No early stopping, model selection or seed retries.
- Seeds: 41, 97, 127, 203, 509. Independent initialized models for each seed.
- Fresh receiver: freeze sender, initialize receiver with seed+10000, train on
  the same 24 task examples and hard messages for 5,000 steps. No world label or
  codebook is supplied. This is supervised adaptation, NOT zero-shot agreement.
- Direct baseline: tanh MLP 5 -> 23 -> 1 on `(a,b,c,u,v)`, exactly 162 parameters,
  matching the 81+81 sender/receiver parameters; same steps, seed+20000.
- Linear baseline: affine logit on the same five raw inputs, same steps,
  seed+30000. No product features are supplied to any learned model.

## Readouts and interventions

Report training, held-out and full 32-case accuracy per seed; never report only
successful seeds. Save case-level predictions and sender probabilities.
Report best binary relabeling accuracy of the message against world (diagnostic
only, not a decoder provided to the model).

For both jointly trained and fresh receivers, evaluate on the held-out cases:
1. Normal hard message.
2. Message erased (0).
3. Independent fair random message, evaluated exactly over both signs.
4. Message from the opposite-world sender triple with the same `(a,b)`.
5. Sign-flipped message.

The erase and random controls should each be exactly 0.5 by label balance.
Swapping the world should reverse a successfully read rule.

## Gates (all fixed before results)

- G0 instrument: 32 unique cases, 24/8 disjoint split, balanced receiver-only
  labels, oracle 1.0, pair marginals equal across worlds, gradient checks pass.
  Failure voids learning gates until fixed with an explicit addendum.
- G1 usable channel: at least 4/5 seeds have held-out AND full accuracy >=0.95.
- G2 causal use: at least 4/5 seeds have normal held-out accuracy >=0.95,
  erase/random accuracy exactly 0.5 (numerical tolerance 1e-12), and opposite-world
  and sign-flipped accuracy <=0.10.
- G3 new reader: same >=0.95 held-out AND full criterion for fresh receivers in
  at least 4/5 seeds. Report their interventions too.
- G4 ordinary comparison: report direct and linear baselines at equal training
  budget, with no required advantage and no novelty claim even if v0 wins.

All five seeds must finish for a gate verdict. Partial runs say INCOMPLETE. Stop
after this batch, successful or failed. Do not tune on its held-out examples.
Any new architecture/split/hyperparameters require a v1 protocol and new runs.

## Budget and reproducibility

NumPy only; no API calls or GPU. Save one atomic result and weights file per seed;
interrupted seeds restart (at most one seed of work), finished seeds are reused.
Manifest pins source/protocol hash, configuration, Python/NumPy and git revision.
Changed source/configuration must use a new output directory. Tests use numerical
fixtures, never train a learner or inspect registered learning outcomes.

## Deferred questions

Zero-shot cross-play between independent pairs; mapping/permutation shifts;
multiple relations and longer messages; sensory learning from pixels; an actual
J-lens analysis; recipient trust and timescales. None is established by v0.
