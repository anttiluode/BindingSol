# Next Sihti — a visible learning-and-settling circuit

**Status: architecture specification / handoff, NOT an implemented result or a new preregistered experiment.**  
2026-10-23. Prepared to finish Astra's interrupted design thread. For future work **after** BindingSol's v0 failure diagnosis; this does **not** authorize skipping the first unchecked item in [CHECKLIST.md](../../../CHECKLIST.md). No existing v0 files, claims, or gates are changed.

## One-sentence experiment

Can connections discovered from *complete visual examples* improve **masked visual completion** over the original fixed SighImageSuper-style filtering loop, while exposing when the answer is uncertain, which connections caused it, and which connections must be revised after the world changes?

The first implementation is a **finite small visual-symbol experiment**, not general photography or a black-box-to-hypergraph translator.

## What exists versus what is proposed

- **SighImageSuper:** a controllable radial Fourier EQ and a *recursive* state update \`x_next = alpha * x_original + (1-alpha) * EQ(x)\`, plus optional renormalization. The original-image term is reinjection, *not* a learned relational constraint. A fixed EQ preserves some image phase information; phase scrambling alone does not prove all linear filters lose spatial relations. [Source](https://github.com/anttiluode/SighImageSuper/blob/main/sigh_image_live_loop.py).
- **BindingClaude Part 3:** unsupervised sample-based branch consolidation + frozen higher-order couplings + masked asynchronous settling on **toy bits**. Its reported results include a chain completion win and a **failed 9/10 revision**; the fixed update ordering gives favourable one-sweep propagation. [Preregistration](https://github.com/anttiluode/BindingClaude/blob/main/PREREG.md) · [ledger](https://github.com/anttiluode/BindingClaude/blob/main/results/PART3_LEDGER.md).
- **BindingSol v0:** a distinct one-bit sender/receiver experiment. **G0 passes; G1/G2/G3 fail** (2/5 qualifying seeds; mean held-out 85% vs 90% for the direct MLP). Its next valid step remains a *versioned v1 sender diagnostic*, not natural-image claims. [Results](../../../RESULTS.md).
- **Proposed here:** put a modest fixed visual reader in front of a learnable, inspectable constraint graph; keep EQ filtering as a separately controllable sensory arm; learn edges only from training observations; compare completions with exact held-out truth. Do not assert this combination already exists.

## Architecture: three clocks, two separate state spaces

**Visual input** \`o\`: tiny binary/RGB motif patches arranged on a grid. A deterministic, disclosed patch reader gives typed symbol responses \`z_i\` (with location and uncertainty). This first version does **not** learn its vocabulary from raw pixels. The nodes are known *measurements*; no edges or logical rules are supplied.

**Fast EQ:** the original recursion is preserved as a baseline/sensory stream:

\`\`\`text
q[t+1] = alpha * q_original + (1-alpha) * EQ(q[t])
optional original-style display normalization is kept out of the inference path
\`\`\`

It is a linear Fourier EQ plus optional external normalization, **not automatically equivalent** to the graph energy. Input reinjection must use only *unmasked observed* pixels at inference; the covered ground-truth patch is never reintroduced by a shortcut.

**Fast binding inference:** variables \`s_i\` are signs \`-1/+1\`; \`0\` marks *unresolved*, not a valid negative sign. A learned branch \`b=(indices, J, age, support, validation_score, provenance)\` contributes

\`\`\`text
E(s | H,J) = - sum_b J_b * product_{i in b} s_i
field_j   =   sum_{b contains j} J_b * product_{i in b, i != j} s_i
\`\`\`

Clamped observations never update. Hidden sites start at 0. One at a time, update a hidden site to the sign of its nonzero field; keep its current value on exact tie. Freeze \`H,J\` during a settling episode. For complete ±1 assignments, asynchronous sign coordinate updates are non-increasing in this multilinear energy; that does **not** prove correct completion, order independence, or uniqueness. The transient unresolved-zero state is handled explicitly and is not itself a probabilistic latent state.

**Uncertainty:** on this deliberately tiny world, enumerate *all* binary assignments to the hidden sites (bounded at 2^8) and normalize \`exp(-beta * E)\` for **exact model-conditional marginals**. Report marginal probability, second-best completion and abstain when ambiguous. The recurrent attractor is a separate **MAP heuristic**, not the uncertainty oracle. Record contradictions and multiple equally good minima.

**Medium coupling clock:** candidate moments \`mean(product_i s_i)\` are useful evidence but are **not generally the same as log-linear parameters** after several branches coexist. Fit candidate \`J\` using a small disclosed conditional objective (exact finite enumeration is practical here) or clearly label moment-estimate weights as heuristic. Compare with a no-relationship and fixed-structure model. Reserve untouched test scenes for evaluation.

**Slow structural clock:** propose bounded local tuples from co-active nearby visual responses; no edges are supplied by the world generator. For each candidate, score the improvement in **future/validation conditional predictive log loss** against the current graph, minus storage/compute/description penalty. Record accepted and rejected candidates. Allow prunes/reopens only from **later outside-the-settling observed episodes** with context-stratified support. Never delete a rare-but-true branch just because the current attractor disagrees with it. A new test set, untouched by keep/prune decisions, measures genuine adaptation.

The three clocks must be independently switchable. Before an update to the medium/slow clock, the current fast settling must reach a stopping condition.

## Minimal visual world: complete scenes and covered pieces

Canvas: small 2D field containing a movable 3-part motif (two independent binary appearance bits \`a,b\`, and a third bit \`m\`) plus unrelated distractors. A visible context marker \`c∈{-1,+1}\` chooses one of two equally frequent worlds:

\`\`\`text
m = c * a * b
\`\`\`

Train on complete scenes, random shifts and independent clutter. At inference hide the entire third motif patch, not merely its label; show the image, mask, completion and branch explanation. The patch reader maps specified tiny motifs to signed variables and location tags; it must **never output the hidden label when covered**. Exact symmetry makes individual and pairwise observations of \`a,b,c\` insufficient to determine \`m\` without combining all three.

Second controlled world: the BindingClaude chain \`h1=a*b; h2=h1*c; h3=h2*d\` rendered into tiles. Vary forward, reverse, random and synchronous update orders. One-shot starts every unknown at zero and performs a **simultaneous** sweep, not a favourable sequential sweep. Preserve unresolved outcomes.

This is intentionally a toy that isolates **learned connections**, not a claim that the app discovered eyes, objects, or perceptual invariance. Avoid labelling known synthetic roles "emergent semantics."

## Visible circuit board — required behavior

Single browser page (dependency-light; calculations can be in a local Python service or ported to JavaScript **without changing numerical semantics**):

1. **Teach complete scenes:** show raw scene, fixed extracted nodes, *candidate* edges (faint), accepted edges (solid), per-edge tuple \`(node IDs, order, weight, evidence, age, held-out gain)\`. Display which edges were **not** selected. Animate new branch formation only when an actual evidence threshold is crossed.
2. **Cover a piece:** display the original input only on a clearly separate **evaluation** panel. The model view has an opaque mask. Show each settling sweep, node value/unknown, per-edge local-field contribution, current energy, confidence and alternative completions.
3. **Intervene:** clicking an edge disables it for a new replay; provide remove-all-high-order, shuffle-edge, and pairwise-only controls. A "receipt" lists paths of evidence and counterfactual changes, never claims a single branch alone caused the answer without a knockout test.
4. **Change context / change rule:** introduce new *complete* episodes in context + with \`m=-a*b\` while preserving context -. Show held-out scores for old and new contexts separately and each proposed forget/regrow action. Make failed revisions and damaged untouched memories visible.
5. **Compare arms:** identical scene seeds, training examples and test masks for fixed EQ, plain nearest-neighbour/pixel fill, pairwise-only binder, grown high-order binder, frozen random hyperedges, supervised lookup over visible sign patterns and a modest direct MLP. Disclose differences in supervision and compute.

**Panels:** original vs masked vs current reconstructed view; live graph; active-branch ledger; confidence/alternative hypotheses; timeline of growth/turnover/forgotten edges; exact evaluation metrics. No decorative growing neurons detached from actual computations.

## Failure and safety modes built in from day one

- Unknown \`0\` is never confused with negative \`-1\`. When two or more inputs of a multiplicative branch are unknown, it may not activate; leave sites unresolved and/or enumerate alternatives rather than hallucinate a resolution.
- Multiple compatible completions: output alternatives and calibrated uncertainty, not a false single answer.
- Conflicting constraints: inspect energy minima, mark non-convergence or hysteresis; never equate *stable* with *correct*.
- Clamping and masked reinjection: no original hidden pixels or truth-dependent gates in any inference arm.
- Structural evidence: no repeated tuning to the final held-out set; reserve a separate stream for keep/prune and final evaluation.
- Order sensitivity: run the same examples with reverse/random updates and report convergence rate and final accuracy independently.
- Revision: compare plasticity with rebuilding from scratch at the same sample/storage/compute budgets.
- Explainability: a rendered positive-edge trace is descriptive; causal explanations require interventions plus comparison to counterfactual predictions.
- Cost: cap candidate edges, nodes, hidden enumeration and UI work so a CPU laptop can reproduce all initial tests.

## Suggested proposed gates (NOT preregistered until separately frozen)

| ID | required observation | falsifying control / treatment |
|---|---|---|
| V0 | zero inference-time leakage, equal world/class frequencies, accurate mask/read, deterministic seed replay | hide target before *every* read, shuffled labels, assert target substitution invariance |
| V1 | discovered edges materially improve held-out hidden-patch accuracy **and** negative log loss over plain EQ and pairwise controls | same examples/masks, matched storage, at least 10 fresh seeds; if lookup matches, say so |
| V2 | confidence separates solvable from ambiguous cases and alternative assignments account for ties | synthetic ambiguous cases with exact enumerated posterior, abstention and calibration scores |
| V3 | branch knockout changes the intended prediction more than unrelated-context predictions | cut matching edge vs size-matched random edge, measure damage in both contexts |
| V4 | new contradictory experience causes obsolete branch revision *without* erasing untouched context | evaluate held-out post-flip + and unchanged -; compare frozen, retrained and replacement controls |
| V5 | results do not depend on one favourable processing order | reverse/random/synchronous test; preserve oscillations and unresolved zeros |

**Do not write PASS/FAIL or lock numerical acceptance thresholds before implementation and a separate preregistration commit.** No gate outcome is being claimed in this design. If fixed EQ / a lookup matches performance at lower cost, this architecture does not earn a superiority claim.

## Explicitly deferred, not part of first build

- **Black-box to readable graph compilation:** teacher-network input/output or activation distillation is an attractive *separate* experiment. A surrogate graph matching outputs is **behavioral fidelity**, not proof its edges correspond to the neural network's actual internal causal mechanism. Requires a separate teacher, distribution shifts, and teacher interventions.
- **Replacing transformer layers**, general real photographs, learned patch dictionaries, continual deployment, automatically learned hierarchy, and neuroscience interpretations.
- Using this visual task to bypass BindingSol's existing **first unchecked v1 sender-diagnostic**. Finish that checkpoint first or run the visual study as a separately versioned project with its own protocol.

## What would count as a win

On fresh visual scenes, the system discovers auditable relationships it wasn't handed; its masked predictions improve on fair fixed-operator/pairwise controls; uncertainty survives ambiguity; branch interventions selectively alter predictions; and its learning machinery can adapt to changed relationships without trashing other memories. **Any one failure is still an informative receipt.**

This is a *specific engineering hypothesis*, not a priority claim that no previous adaptive hypergraph/graphical-model system ever did something similar.
