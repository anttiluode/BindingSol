# SihtiGraphModel v1: code review while the first real run is pending

2026-10-23. Read-only inspection of `anttiluode/SihtiGraphModel` at commit `3596ac362aeb8e7bf62bfe90199f1911495c453a`. No changes to that repository or the user's running experiment. No CIFAR result was available to this reviewer.

## What it computes

For one fully supplied image I, `sieve.py` constructs 64 additive spatial/octave pieces. A mask chooses which already known pieces to include. The renderer clips RGB values, the frozen CNN evaluates the altered image, and the oracle returns bird logit minus the largest competing logit. `walsh.py` estimates a sparse expansion in products of +/-1 input switches. This is an image-specific behavioral surrogate; it is not CNN weight extraction, scene-density learning, missing-pixel generation or recurrent purification.

The hybrid is real: gradient optimization learns the teacher; query-based search seeks an explicit representation of its response. Whether that representation is compact and useful is precisely what the run tests.

## Positive checks

- Training and checkpoint selection use a fixed 45k/5k split; no test data fit the teacher. The image-selection condition (first correctly classified bird) is disclosed.
- The additive sieve telescopes; switches have named band/patch coordinates. Mean replacement is handled as an additive baseline contrast, with all-on reconstruction preserved.
- The KM pair estimator has the correct shared-suffix/prefix-parity structure for bucket mass. Candidate caps and finite sampling prevent a completeness guarantee.
- Candidate discovery, coefficient refitting and final evaluation use separate draws. Competitor coefficients use the same refit observations; the larger discovery cost is disclosed.
- R2 uses actual held-out variance; sign agreement and class balance are reported separately. Zero/mean replacements and retention shifts get separate results.
- No obvious blocker found in the default execution path by inspection. This is not a complete security or performance audit.

## Findings affecting interpretation

1. **Interactions belong to the entire query function.** RGB clipping and the maximum competing-class operation can introduce joint effects, in addition to CNN nonlinearities. A high-order branch does not isolate a high-order internal CNN circuit. Subsequent controls could use raw class logits, a fixed competitor and a linear teacher through the same renderer, under a new protocol.
2. **The coefficient signs are contrasts, not literal excitatory wires.** A product is positive with an even number of disabled switches too; it does not mean all named pieces are present. The report's influence map sums absolute incident coefficients. It is a participation map, not a signed causal attribution or probability.
3. **Local pairwise baseline is restricted.** It examines 64 singletons plus 144 spatial/adjacent-band pairs, retaining 50. A win over it need not beat unrestricted pairwise structure. Before calling long-range branches necessary, compare all 2,016 pairs and proper validation-selected refits in a follow-up; do not change the running gate.
4. **A negative result has several meanings.** Sparse-search miss, too many weak interactions, distribution shift or an almost always negative masked teacher can each cause failure. Uniform-mask sparsity does not guarantee accuracy at retention .75/.9. The capped estimator cannot certify a dense spectrum from absence of recovered terms.
5. **The stored image pieces contain the original detail.** Switching a piece back on retrieves supplied pixels; this cannot establish that the graph can infer pixels it has never received. Shared image coefficients and a separate learned scene-compatibility objective would be needed for the proposed completion architecture.
6. **Accounting is distillation-specific.** A full 64-depth search uses 141,312 forward examples including calibration/screening, then 8,192 refit and 6,144 evaluation examples: 155,648 per replacement before factorial probes. Two replacements total 311,296 plus probes. CNN training, validation and original-image selection are additional work outside the per-oracle counter. These are examples, not GPU batch calls.
7. **Receipts can be strengthened later.** Checkpoint metadata and invocation flags are saved, but the receipt does not pin a checkpoint file hash, full environment or source revision. The original image and sample perturbations are also absent from the HTML; it shows band/patch maps and tables. Preserve the checkpoint and current revision with the first result. Reusing an existing checkpoint can silently carry a different training history from current command-line epoch settings.

## Local verification performed

- `python -m unittest discover -s tests -v`: three NumPy tests passed; two PyTorch-dependent tests skipped because this environment has no PyTorch. Do not describe this as five executed passes.
- `python run.py --mode smoke`: the three correct synthetic branches were recovered, fresh-mask R2 = 0.999707815907868. Sieve check skipped for the same dependency reason.
- A separate 64-switch synthetic diagnostic with the locked search defaults and known terms `{0}`, `{1,4}`, `{2,7,60}` recovered all three; fresh-mask R2 = 0.9994650967012494, 141,312 queries, 64 depths, no capped levels. This verifies one sparse known-function case, not CIFAR fidelity or universal search reliability.

## Read the user's result in this order

1. Per replacement: reconstruction, original correctness, teacher variance and positive fraction (G0).
2. Uniform-mask graph R2 and its difference from all 64 singleton terms (G1).
3. Local-pair/random controls, retained orders, search cap events and coefficient stability limits.
4. Retention .75 gate and .9 report; clipping and zero/mean dependence.
5. Factorial mixed differences, if an eligible higher-order branch exists.

Leave the current run untouched. Pass means a compact local surrogate under specified interventions. It does not by itself establish a new general image model, a hidden neural circuit, or an adaptive completion engine.

See the accompanying relational design for the proposed separate learning/settling system. Distilled scopes could later guide proposals, but classifier coefficients must not be treated as log-probability couplings without a new learning objective and test.
