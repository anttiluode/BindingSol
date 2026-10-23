# Binding v0 design

Intent: turn the supplied sender/receiver proposal into one small measurable
experiment and keep it resumable for Sol. PREREG.md is the scientific authority.

Approaches considered by the implementer: a pretrained-language-model study
would reconnect directly to Välikäsi but requires downloads/GPU and has more
confounds; a rendered-image study adds perceptual learning before the channel is
tested; a finite symbolic baseline isolates channel learning cheaply. Use the
third for this checkpoint, as the small first experiment proposed in the supplied
discussion. These are implementation choices, not additional user promises.

Python 3.10+, NumPy, unittest. `binding.py` owns data, networks, optimization,
metrics and gates. `run.py` owns manifests, atomic result/checkpoint persistence,
resumption and CLI. Tests independently check split balance, known answers,
gradients and interrupted/changed-run handling. README/CHECKLIST/HANDOFF expose
state without needing the chat. RESULTS records all outcomes.

No downloads, GPU, paid calls, UI, natural photographs or J-lens work in v0.
Five fixed seeds, no tuning after inspection. Compute budget is bounded by
5000 steps for each of four fits per seed. Preserve weights and predictions.

Success means a runnable, audited experiment with honest verdicts, including a
negative one. A demo or positive scientific finding is not required for delivery.
