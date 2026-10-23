# BindingSol

**Can a learned relationship become a message another reader can use?**

Small, CPU-only experiments connecting the October 23 discussion of Välikäsi,
three-piece binding and usable information. Start with [CHECKLIST.md](CHECKLIST.md)
and [HANDOFF.md](HANDOFF.md). They are the durable working memory for Sol or any
successor; the chat is not required.

**Status:** v0 is complete; reliability gates failed (2/5 perfect runs).
Read [RESULTS.md](RESULTS.md) for all seeds and controls. Ten tests pass; [independent review](REVIEW.md) verified the saved results.

**New design, not implemented:** [Inspectable Sihti learning and completion](docs/superpowers/specs/2026-10-23-sihti-relational-design.md), with a [Sol build checklist](docs/superpowers/plans/2026-10-23-sihti-relational.md).
The [SihtiGraphModel v1 review](docs/sihtigraphmodel-v1-review.md) explains how the
separate running image-distillation experiment fits this proposal. Its real CIFAR
results have not been inspected here.

## First experiment

Two worlds have opposite rules. A sender sees three signs from one world. A
receiver sees two signs from a different example and must fill in the third.
The sender can transmit **one binary symbol**. Neither learner gets a hand-written
parity feature or the world label. They learn from completion errors.

This is a deliberately tiny emergent-communication baseline, not a new image
model, a J-lens implementation, or evidence about consciousness. Training uses
ordinary backpropagation and a shared task loss. [PREREG.md](PREREG.md) fixes the
experiment before the first run; failures stay recorded.

## Run (Python 3.10+)

```bash
python -m pip install -r requirements.txt
python -m unittest discover -s tests -v
python run.py --out results/local-v0
```

Windows: replace `python` with `python3.13` if that is your installed command.
No GPU, API key, model download or paid inference is needed. The runner resumes
completed seeds and refuses to mix changed code/configuration with existing runs.
Use `results/local-v0` for your own run; `results/v0` contains the frozen recorded batch.

## Reading order

1. [CHECKLIST.md](CHECKLIST.md): completed work and the next unchecked gate.
2. [HANDOFF.md](HANDOFF.md): exact resume command, decisions and stopping point.
3. [PREREG.md](PREREG.md): locked methods and decision rules.
4. `results/v0/summary.json`: measured results once run.
5. [Design](docs/superpowers/specs/2026-10-23-binding-v0-design.md) and
   [implementation plan](docs/superpowers/plans/2026-10-23-binding-v0.md).

## Context and limits

- [Välikäsi](https://github.com/anttiluode/Valikasi): distinguish causal influence,
  conditional/oracle recoverability, generalizable decoding and actual behaviour.
- [ClaudeRepo1](https://github.com/anttiluode/ClaudeRepo1): synthetic relational
  completion motivated the two-rule task.
- [ModelImage](https://github.com/anttiluode/ModelImage) and
  [SihtiImageModel5](https://github.com/anttiluode/SihtiImageModel5): motivation for
  eventual sensory transfer and trusted memory, not functionality implemented here.

These links are provenance from the supplied discussion, not a new audit of those
repositories. A linear probe may decode parity if an upstream nonlinear model has
already represented it. Distinct deterministic notes alone do not demonstrate a
shared code, a generalizing reader, or a mechanism for subliminal learning.
