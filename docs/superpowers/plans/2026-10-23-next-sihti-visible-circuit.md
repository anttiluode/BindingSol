# Implementation plan — Next Sihti visible circuit (deferred)

**Design:** [visible-circuit specification](../specs/2026-10-23-next-sihti-visible-circuit.md)  
**Status:** ready for scientific review; *not yet an approved/registered run*. No code or experiment was executed by this handoff. Stop before implementation until Sol completes BindingSol's first unchecked v1 sender/channel diagnostic **or** explicitly creates a separately versioned, non-interfering next-Sihti workspace.

## Definition of done for the handoff (not the science)

A reader can identify: what already exists, which parts are missing, exactly what first version should contain, leakage/ambiguity/revision hazards, required ordinary controls, affordable reproduction, and what would count as failure. This plan is preserved without modifying v0 or rewriting BindingClaude results.

## Implementation order for a subsequent session

**0. Preregistration checkpoint — no experimental runs yet.**
- Read BindingSol \`AGENTS.md\`, \`CHECKLIST.md\`, \`HANDOFF.md\`, \`RESULTS.md\` and the new spec; identify whether continuing Sol's v1 diagnosis or starting a separate visual project.
- Write a new locked \`PREREG_VISUAL_V1.md\` in that *future* project/branch: generator, independent seeds, split, full acceptance thresholds, maximum run cost, main hypothesis, secondary outcomes, and stopping rule.
- Freeze all masks, order variants, candidate budgets and controls before held-out measurements. Save a git hash identifying the exact preregistration. **Do not run v0 with changed settings or overwrite its results.**

**1. Generator and leakage tests.**
- Implement a deterministic small grid of colored/monochrome patches with independently sampled \`a,b,c∈{−1,+1}\`, hidden \`m=c*a*b\`, independent distractors and limited translations.
- Provide \`render(scene)\`, \`read_visible(image, mask)\`, \`ground_truth(scene)\` as strictly separated functions. Return \`None\`/unknown for masked tiles. Replacing any ground-truth hidden pixel must leave inference features unchanged.
- Enumerate the discrete worlds to verify exact balancing and lack of all lower-order shortcuts for the intended task. Split by independent random scene identity and translations; never upload the identical full scene for train and held-out with only new masks.

**2. Fixed sensory operator.**
- Port/retain a tiny reproducible EQ with original-image reinjection (SighImageSuper semantics), not an invented proxy. Be precise about the frequency binning and possible normalization.
- Mask original evidence *before* reinjection; do not allow filtering to read the evaluation-only missing region.
- Build non-EQ local interpolation and static-patch baselines first. Record visible/evaluation images separately.

**3. Branch discovery (one learning clock).**
- Start with no edges. Random and local candidate proposals receive the same bounded budget. Branch orders 2–4; record \`indices, J, age, evidence, validated_gain, proposal_source\`.
- Use observed complete training episodes for evidence. Compare learned \`J\` using a conditional objective (small-world exact partition function) with a moment-heuristic alternative.
- Keep only if pre-registered training/validation predictive improvement minus complexity cost is positive. Validation for branch selection is **not** the final held-out test. Log rejected edges, not just successes.
- Serialize graph and generator seeds; reload must reproduce graph and predictions byte-for-byte (within declared numeric tolerance).

**4. Settling and uncertainty (one thinking clock).**
- Freeze graph for each inference. Clamp visible signs. Unknown starts at 0, ties retain previous state.
- Implement asynchronous forward/reverse/permuted order; separately implement truly simultaneous \`one_shot\`, and a maximum-sweep/oscillation cutoff.
- Exhaustively enumerate possible hidden signs when hidden count ≤8 to compute exact model-conditional marginal probabilities, alternate modes and abstentions. Never present single-mode convergence as calibrated confidence.
- Per-sweep trace: changes, energy for complete assignments, contributions per active edge, unresolved count, elapsed operations. Unit tests for coordinate energy decrease on complete binary states and for ambiguous/disconnected graph.

**5. Explanatory interventions.**
- Replay the *same* observation with an edge disabled or randomized. Report the delta in marginal probability, predicted symbols and log loss.
- Negative control: removing irrelevant same-size branch should affect fewer examples than removing a true predictive branch. Preserve contradiction cases with more than one local minimum.
- Do not call a receipt a causal discovery of a black-box teacher's internals.

**6. Revision / forgetting (separate experience clock).**
- After the frozen evaluation, flip \`m\` to \`-a*b\` only in context +. Keep separate held-out post-flip and unchanged-context test sets.
- Out-of-loop new complete episodes provide contradiction evidence; branch reopening/pruning uses context-stratified validation rather than attractor agreement. Compare frozen graph, simple weight revision, prune/regrow, and conventional full retraining.
- Score recovery delay in samples, preserved context -, memory size, compute, false deletions and any temporarily unresolved state. BindingClaude's 1/10 recovery is prior motivation, not a visual-world result.

**7. One visible circuit page.**
- Canvas A: training image and genuine covered inference input, with missing truth revealed in a visibly separate pane only for scoring.
- Canvas B: dynamic factor/hyperedge graph, hover/select edge shows contribution, \`J\`, support, age, selection evidence, knockout button and per-example replay.
- Canvas C: settling sweep strip and exact alternatives/confidence. Canvas D: seed-by-seed controls, failed gates, replayable growth and revision timeline.
- No animation whose links are invented purely for aesthetics; state shown must derive from the actual model objects.

**8. Audit, bounded experiment and record.**
- Run unit tests before models; provide small smoke mode separate from frozen benchmark. Freeze and commit the preregistration and code **before** testing fresh seeds.
- Run the registered seeds once. Report all seed results, pass/fail per preregistered criterion, confusion/ambiguity counts, code+config hash, reproducibility command, ordinary baselines, branch counts and runtime.
- If the effect disappears against a matching lookup, plain EQ, pairwise model, or different update order, report that as a limit or failure; do not silently adjust thresholds.
- Commit a concise ledger, raw JSON, and handoff instructions. Add to Genealogy *only after* the measured result exists.

## Suggested future files (do not create them in BindingSol v0 by accident)

\`\`\`text
PREREG_VISUAL_V1.md
visual_world.py          # independent generator / held-out evaluation labels
visual_reader.py         # fixed, disclosed motif or band reader
eq_loop.py               # faithful masked EQ control
branches.py              # candidate growth, weights, selection, revision
settle.py                # masked recurrence + exact small-world posterior
baseline.py              # interpolation, pairwise, lookup, MLP, fixed EQ
experiment.py            # seed/metric/JSON runner
tests/test_leakage.py
tests/test_inference.py
tests/test_revision.py
web/index.html           # renderer of actual traces, not mock statistics
results/visual-v1/       # created only after registered run
\`\`\`

## Stop conditions and primary hazards

1. **Before image work:** BindingSol's existing first-unchecked scientific checkpoint cannot be reclassified as done by this design.
2. **Before a positive claim:** numerical success must exceed justified controls and be independently reproducible; score accuracy, conditional log loss, uncertainty, revision and resource cost separately.
3. **If target leaks:** invalidate the run, repair the instrument with a recorded preregistration addendum and restart new held-out seeds.
4. **If conflict or multi-missing state never resolves:** show unknowns and multiple hypotheses; do not force a confident ±1.
5. **If revision fails:** preserve seed-by-seed failure and protected-context accuracy. No retrospectively enlarged forgetting window or secretly reset network.

## Handoff summary for Sol

The old EQ is an **existing fast sensory recurrence**; the novel-to-this-project experiment is *learning explicit, inspectable connections and letting them affect recurrent completion*. The first mathematical target is a finite conditional visual completion world, with a tiny exact posterior to catch false confidence. The engineering priorities are **revision, uncertainty and causal deletion**, not ever-larger hypergraphs or image generators.

This plan is a useful checkpoint independent of model credits. It deliberately does **not** pretend Astra's inaccessible uncommitted edit or any unrun implementation has been recovered.
