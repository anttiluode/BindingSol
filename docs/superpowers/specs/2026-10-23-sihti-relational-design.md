# Sihti: an inspectable learning and completion system

Date: 2026-10-23. Status: design for Sol, not an implemented system or experimental result.

## Intent and decision

Build a small system in which experience changes explicit relationships, those relationships change subsequent inference, and the user can inspect and intervene on both. The first useful demonstration is a visual circuit board with missing pieces, conflicting expectations and changing regularities. The research question is whether learned structure earns its storage and computation cost in prediction and revision.

Antti requested the design; Sol will implement it. The defaults below are the designer's choices, not claims that Antti selected numerical settings. Keep this work in BindingSol under a new module and result namespace. Preserve the existing communication experiment and all its failed gates. Do not modify Claude's repositories or publish supplied conversation transcripts.

### Approaches considered

1. Extend binary product branches directly. Cheapest connection to BindingClaude, but parity-specific features and zero-valued unknowns make a visual generalization easy to overstate.
2. **Chosen: a small categorical factor graph, with learned tables and exact conditional checks.** More explicit parameters, but handles actual piece types, ambiguity and conditional probabilities without inventing a new learning law. A binary product branch is a special case.
3. Immediately train a large image encoder and evolving latent graph. Greater possible reach, but mixes sensory learning, structure discovery and inference failures. Defer until the small system passes its tests.

This is a combination of known methods. Neither a novelty claim nor superiority to neural networks follows from the design. Differentiable optimization still learns the factor values; bounded search chooses where factors exist. This is deliberately a combination of the two strategies discussed in the conversation.

## What the evidence currently supports

- BindingSol v0, commit `6377f534934ba805a969a8955c4585680bf37dce`: 2/5 perfect communication runs, reliability gates failed; ordinary direct MLP mean 90% versus joint 85%.
- BindingClaude's Part 3 ledger read on October 23 reports 99.10% chain completion and selective context knockouts. It also reports only 1/10 revision recoveries, lookup catching up, and favourable sequential update order. These are reported results, not independently rerun here. Source blob: `38753bd0dc60bf01a60f3ff3763586d9ae1717e3`.
- SighImageSuper already supplied recurrent EQ filtering, input reinjection and optional normalization. The new part proposed here is learned relational constraints and accountable structural change.

Consequently, do not rerun a parity chain and call that the new milestone. Test revision and a visible assembly task. A fixed pairwise model may win this task; that is a legitimate outcome.

### New neighbouring instrument: SihtiGraphModel

During this design, Antti reported running SihtiGraphModel v1. Code inspected at commit `3596ac362aeb8e7bf62bfe90199f1911495c453a`: it fits a sparse Walsh surrogate to a frozen CNN's class margin over 64 switches of one fixed image. This supplies an interaction-discovery instrument, not this design's learned joint compatibility model or settling engine. Do not replace the running experiment or change its locked protocol.

In particular, a classifier-response coefficient theta_S is not automatically a coefficient of log p(scene). Reusing those numbers as completion couplings would change the meaning of the objective. Maximizing the surrogate selects a subset of already supplied image residues that raises a classifier margin; it does not invent unseen content. If the distillation succeeds, use its scopes as candidate proposals in a separately registered transfer test, then learn and validate completion factors from actual complete-scene observations. Count teacher queries and compare with random/local proposals. This integration is deferred; no image-specific coefficients are silently imported into version 1.

## Boundaries and budget

- Python 3.10+, NumPy, standard-library HTTP server and ordinary browser JavaScript. No GPU, paid API, model download or additional runtime dependency for the first version.
- Nine categorical board variables, eight states each; one observed binary context variable. At most three board tiles hidden per query: at most 512 candidate completions.
- Factor scopes have two or three variables. At most 24 active relational factors; unaries do not count toward that cap. One unique factor per sorted scope.
- No automatic chunks, latent symbol invention, unrestricted graph growth or natural-photo claims in version 1.
- Unit fixtures first; one development seed, then three registered seeds: 1201, 1213, 1231. Do not replace unlucky seeds.
- Maximum 30 minutes CPU wall time per registered seed, including learner search and baseline fits. Save resumable stage checkpoints. Timeout means INCOMPLETE, not a negative accuracy result. Stop after one registered batch.
- Before that batch, Sol must commit `relational/PROTOCOL.md`, the complete configuration, generator/split hashes, baseline budgets and gate definitions. This design is not a preregistration of code that does not yet exist.

## State and mathematical contract

Let z_i be a tile identity, c the observed context, y the observed raster, and M its observation mask. Missingness is a separate Boolean mask: it is never tile 0, an absent port, or a negative feature. Context is an observed input; do not infer or silently invent it in v1.

Each factor b stores a scope S_b, a small learned table T_b(z_Sb), a stable ID and an evidence ledger. Let a_i be learned unary preferences and u_i(a; y,M) a fixed sensory score for assigning tile a at location i. The episode score and energy are:

    S(z; y,M,c) = sum_i [u_i(z_i; y,M) + a_i(z_i)] + sum_b T_b(z_Sb)
    E(z; y,M,c) = -S(z; y,M,c)

Factors containing c have an axis of size two, not eight. Observed tiles and context are clamped. For hidden indices U and observations O:

    p(z_U | z_O,y,M,c) = exp(S(z)) / sum_{w_U} exp(S(w_U,z_O))

Use log-sum-exp for normalization. This is the model's conditional probability, not a guarantee of real-world calibration. It is a conditional energy model when the sensory scores depend on y and M, not an assertion that the raw pixels follow a learned generative density.

To keep factor order interpretable, constrain every relational table to zero mean along every individual axis (uniform ANOVA contrast gauge). Unaries sum to zero. Project gradients/parameters into those subspaces during fitting. Report both free contrast parameters (product of domain-size-minus-one) and actual serialized table bytes. This removes lower-order components from a purported three-site factor; it does not make a factor a semantic explanation by itself.

### Fast clock: inference with fixed memory

Freeze sensory scores, parameters and graph for the entire query. Initialize hidden tiles from unary maxima. A coordinate update tries all eight values of one hidden tile and accepts a strict score increase greater than 1e-12. Preserve the current value on a tie. Stop on a sweep with no change or after 32 sweeps, retaining an explicit limit flag.

This guarantees nonincreasing energy for accepted moves and termination on the finite state space if allowed to finish. It does not guarantee the global minimum. Record the actual coordinate order. Always report row-major, reverse and seeded random-order diagnostics; never describe one favourable sweep as evidence of a long thinking process.

Separately enumerate all at most 512 completions to obtain exact MAP states, marginals and entropy. This is a **model inference audit**, not a teacher supplied to the learner. The demo shows the recurrent state and the exact model check separately. Never quietly replace a failed recurrent result with exact MAP and call the recurrence successful. If top states tie, retain the alternatives. Show a single confident tile only when its model marginal is at least 0.90; otherwise display alternatives. Evaluate both forced predictions and abstention/coverage.

### Medium clock: learn from subsequently observed evidence

Training receives complete scenes; the system creates masked prediction exercises. That is self-supervised prediction from observed data, with designer-supplied tile vocabulary and positions. Do not train from the system's own guesses as though they were observations.

Fit shared factor tables and unaries by regularized categorical pseudolikelihood:

    L = mean_(scene,i in hidden mask) [-log p(z_i | z_-i, u(scene,mask),c)]
        + (1e-3 / 2) * sum_of_squared_parameters

The single-site distribution is a softmax over the unary plus all incident factor entries. Other site values in this training conditional are their observed complete-scene values, including sites that would be hidden at inference. This is the standard conditional fitting objective, **not** multi-hidden conditional likelihood and not a simulated negative phase. At evaluation, hidden truth is inaccessible and all hidden sites are inferred jointly or iteratively.

Use float64 projected Adam, learning rate 0.01, batches of 64, at most 200 updates for an ordinary fit and 50 for a candidate factor. Defaults may be adjusted once on the development split before the protocol is locked. Include finite-difference checks of the projected objective. Record convergence curves; an exhausted step cap does not prove a local minimum.

Ordinary fitting happens after every 128-scene fitting-buffer update, whether or not a structural edit is proposed or accepted. This applies during both initial learning and revision. Adaptation must never depend on passing a growth/deletion gate. The confirmatory comparison uses frozen snapshots after that ordinary fit.

### Slow clock: proposed connections must earn retention

Start with unary terms only. Run at most 24 structural decisions per training phase. At each decision propose up to eight scopes not previously proposed in that phase: six spatially local connected pairs/triples (context may join a local scope), two unrestricted pairs/triples. When a pool is exhausted, fill from the other; if both are exhausted, stop new-scope proposals only. Continue the scheduled data blocks, ordinary parameter updates and deletion assessments. Rejected/deleted scopes become eligible again in the next phase; already active scopes never duplicate. Random proposals and graph-based extensions may share the pool, but their exact allocation is fixed before testing. Do not supply the true adjacency or generator compatibility tables as learned factors.

Use three disjoint roles: fitting, candidate screening, then fresh confirmation. Fit candidates on the fitting buffer with existing factors frozen, rank on the screening block, and bring only the best candidate to confirmation. Never choose a different candidate after seeing confirmation. Keep screening and confirmation boards permanently outside the fitting buffer; fitting data comes only from the designated fitting split. No confirmation board can confirm a later decision again.

On confirmation, define d_e = old minus candidate mean single-site NLL for scene e. Keep the candidate only if:

    mean(d_e) > 2 * SE_over_scenes(d_e) + 1e-5 * added_free_parameters

This is a conservative engineering selection rule in nats per predicted tile, not an MDL theorem or a universal significance guarantee under repeated adaptive testing. Fresh final evaluation remains essential. Keep all rejected proposals and their compute costs in the ledger.

At capacity, assess deletion only. Below capacity, screen additions and leave-one-factor-out deletions together in both initial learning and revision; rank by mean screening NLL improvement minus signed complexity change. Confirm at most one selected edit on fresh observations. Accept deletion when:

    mean(d_e) + 1e-5 * removed_free_parameters > 2 * SE_over_scenes(d_e)

This allows a modest accuracy cost for a measured simplicity benefit. Log that trade explicitly. Refit surviving parameters on fitting data after an accepted edit. Permanently retain a tombstone and the old checkpoint so the decision is reversible and inspectable. A factor's losing an internal vote is never a deletion criterion.

## The sensory/EQ connection

Render each board as a 48x48 grayscale image, nine 16x16 tiles. The eight tiles are the even-degree port patterns: empty, horizontal, vertical, four elbows, and a four-way crossing. Ports are north/east/south/west; glyph strokes connect active ports to tile centre. Sol chooses exact stroke width and antialiasing once and hashes the templates. The first task uses whole-tile masks and known tile positions. No claim of learned segmentation follows.

The frontend receives only masked pixels and M. Initialize v_0 with observed pixels and zeros elsewhere, then run 32 steps:

    v_(t+1) = M*y + (1-M)*F_EQ(v_t)

Use a symmetric Gaussian Fourier low-pass with spatial sigma 1 pixel and periodic boundary convention. This is a specified masked EQ baseline derived from the lineage, **not an assertion that it exactly reproduces the original SighImageSuper recurrence**. Save v at every step.

For a hidden tile, compare its v_32 patch with each rendered tile template. Use u_i(a) = -0.25 * MSE(patch,template_a)/(2*0.25^2). Observed exact tiles are clamped. Freeze u before relational settling. A separate no-EQ arm sets all hidden sensory scores to zero. This deliberately avoids an unproved convergence claim for alternating two changing operators.

Evaluate the four combinations: EQ alone, learned factors without EQ, factors plus EQ, and factors plus EQ with one sweep only. Include a learned-unary-only control. If the no-EQ graph wins, keep that result and stop claiming EQ helps. Retaining an ancestor is not a success criterion.

## A finite visual world with an exact reference

The 3x3 board has 12 internal edges and 12 external boundary half-edges. Each is a binary port occupancy. At every tile, incident occupancy has even parity, giving exactly the eight tile identities above. Adjacent tiles share an edge. Enumerate the nullspace over GF(2) of the 9x24 incidence matrix to produce the complete finite catalogue (expected dimension 15, 32,768 boards; verify rank rather than assume it).

These construction constraints belong only to the generator and reference evaluator. The learner sees tile identities and renders, not nullspace coordinates or validity tests. The task is contour/circuit assembly; its local vocabulary is supplied. Although the generator uses parity to enumerate valid ports, the benchmark target is eight-way visual completion, and ordinary pairwise tile compatibility may solve it. Do not market it as escaping all parity structure or requiring high-order factors.

Split by full canonical board identity using SHA-256 of the nine tile IDs, first four digest bytes interpreted as an unsigned big-endian integer modulo 10: residues 0-5 fitting, 6 screening, 7 confirmation, 8 development, 9 final evaluation. A single board and all its masked/rendered versions belong to one split. No whole-board duplicates cross splits. Replay may repeat fitting boards; disclose it. Before any model fits, deterministically shuffle the confirmation boards within each centre-tile category and distribute round-robin into four disjoint pools: initial/c0, initial/c1, revision/c0, revision/c1. Verify each contains at least 768 boards; insufficient capacity is a preflight failure requiring a protocol addendum before learning, not recycling of confirmation data.

For context c=0, sample uniformly within the relevant split. For c=1, use weights proportional to exp(eta*g(z)), where g is +1 for a horizontal centre tile, -1 for a vertical centre tile, and 0 otherwise. History A uses eta=+2, history B eta=-2. Contexts are equally frequent. Revision changes only the c=1 preference; c=0 remains uniform. These are changes in experience, not a world label handed to the learner: c denotes an observed stable context, while eta is never an input.

Training starts with 2,048 fitting scenes; each structural decision uses 64 fresh screening scenes and 64 fresh confirmation scenes (32 in each context), one preselected mask of size 1, 2 or 3 per scene. Sample screening with replacement if needed. Sample confirmation without replacement from its preassigned phase/context pool, proportional to the context's weights on the remaining boards. This is an explicitly finite-urn selection audit, not IID evidence from the fixed final distribution; record remaining counts and treat 2*SE as a heuristic, not a confidence guarantee. Initial learning cannot consume revision's confirmation pool. Keep a 2,048-scene fitting buffer. Use 24 decisions for initial learning and 24 for revision, refilling fitting data in 128-scene blocks. Revision starts from the learned checkpoint; fitting buffer gradually replaces old experiences, while half its slots remain allocated to each context. No preferential storage of test cases.

Draw 1,024 final evaluation scenes per history, balanced across contexts and mask sizes as closely as integer counts allow, with case identities pinned before fitting. Sample within the reserved final split with replacement if required; report unique counts. An exact generator-conditional reference sums the known sampling weights over final-split boards consistent with visible tiles. It supplies ambiguity and achievable performance measures to the evaluator only. Never substitute the sampled hidden answer for evidence that an intrinsically ambiguous completion is uniquely correct.

## What must be measured

All numbers below are proposed engineering gates to freeze in the protocol; none is a result.

| Gate | Required evidence |
|---|---|
| G0 integrity | Hidden pixel/label mutation cannot affect learner inputs; split disjointness; exact conditional normalization; coordinate energy check; deterministic resume. Any failure invalidates learning claims. |
| G1 useful learned relations | Exact graph conditional NLL per hidden tile is at least 5% below learned-unary-only NLL in each of three seeds; report EQ-only too. Otherwise stop expansion. |
| G2 useful recurrent inference | In every seed, recurrent score is within 1e-8 of exact maximum on at least 95% of final cases for each of row-major, reverse and random update order. Failures remain visible; exact inference may still be a useful separate system. |
| G3 faithful interventions | Every displayed contribution reproduces its local score difference to 1e-9; every claimed branch effect is rerun without that branch from the same initialization/order. No effect is a valid displayed outcome. Report effects for all factors on the first 128 fixed final cases. |
| G4 revision with retention | On c=1 final cases, recover at least 80% of the NLL gap between frozen history-A model and a fresh history-B fit, within the fixed revision budget. On c=0, NLL rises by no more than 0.02 nats per hidden tile. Require all three seeds. If the fresh model offers no positive gap, mark recovery NOT IDENTIFIABLE. |
| G5 competitive value | Report performance, storage and total compute against all controls below. A useful-architecture claim requires matching the strongest ordinary control within 0.02 nats/tile, or a documented performance/cost tradeoff; a win over EQ alone is insufficient. |

Use joint conditional NLL divided by the number of hidden tiles as the primary completion metric. Also report tile accuracy, exact-board accuracy, Brier score, confidence coverage, error among confident answers, time/updates to settle, coordinate-order sensitivity and per-context revision curves. Keep initial and post-revision final sets sealed until the complete scheduled learning run finishes; use development cases for progress displays. Report each seed, not just a pooled number. Bootstrap uncertainty over complete boards if used, not over pixels or repeated masks; three seeds do not establish broad reliability.

Controls get identical complete training observations and masked queries: unary-only, the EQ frontend, nearest-neighbour lookup, fixed local pairwise factors, a fixed random graph matched to learned factor storage, and a small masked categorical MLP. Include fixed-structure weight adaptation, growth without deletion, and frozen memory in revision. Candidate search, replay memory, confirmation data and exact inference all count in the graph's costs. Neural parameter count and optimizer steps alone are not compute matching; record wall time and learning curves. Sol must pin MLP architecture, validation-only stopping and separate train budgets before final evaluation. If an adequate MLP cannot finish inside budget, report the comparison incomplete.

The neural control must represent a joint distribution: use shared masked MLP conditionals in a fixed row-major autoregressive factorization over hidden tiles, with preceding hidden truth supplied only for training likelihood or scoring a specified candidate, never as test evidence. Enumerate the same <=512 assignments to obtain its joint distribution and marginals. Lookup uses the 32 nearest fitting scenes by visible-tile Hamming distance within the observed context; estimate a joint histogram of their hidden tuples, with a total symmetric Dirichlet pseudocount of 1 across all 8^|U| completions. Resolve neighbour ties by stored training order; disclose buffer and example-storage cost. Both joint NLL and marginal metrics are reported for every model. Independent tile heads alone are not an adequate joint control.

Do not force deletion when weight revision suffices. Do not claim structure growth helped if a fixed graph performs equally. Do not claim the EQ helped if its removal improves predictions. An ordinary model winning is useful closure.

## Visible interface and explanation contract

One local page, backed by Python endpoints, with four views:

1. The observed board, unknown tiles shown as unknown, and the EQ reconstruction.
2. The recurrent proposal beside exact model alternatives and confidence. A timeline steps actual logged updates; no decorative activation animations.
3. The learned graph. Select a factor to see its scope, table, age, current activity, training evidence, confirmation gain, parameter/byte cost and prior revisions. Render a factor as a small junction connecting its variables.
4. An intervention panel: disable/restore a factor, replay the identical query, compare before/after probabilities and affected tiles. Load history A/B checkpoints for the same masked input. A 'reveal evidence' action displays newly observed truth and only then permits learning.

For a tile changing from a to a', show each incident factor's actual delta T_b(a')-T_b(a), along with sensory and unary deltas. These sum to the local score change. Label them 'local contributions'. Label knockout effects separately: they require rerunning inference and may involve redundant paths. A high contribution is not automatically the cause of the final answer. Learned compatibility tables are inspectable, but semantic names such as 'cable continuity' remain human annotations unless separately tested.

Use an episode-scoped intervention overlay; do not delete trained memory when the user merely toggles a branch for inspection. Show whether a state came from observation, inference or user intervention. No hidden truth in browser response payloads before reveal. Backend retains the reference answers separately.

## Beyond version 1

Only after G0-G4: register a larger held-out assembly task, then a small real-image patch task. Keep the same factor interface while replacing supplied tile recognition with learned local features; account for encoder cost and compare with ordinary models using the same features. Exact enumeration will stop scaling: evaluate approximate inference against exact small subproblems before extending masks. Introduce latent chunks only with a separate criterion for predictive benefit, cost and causal use. No claim that history-dependent computation is unique to this architecture; recurrent and adaptive networks already do it.

## References and provenance

- [SighImageSuper recurrence](https://github.com/anttiluode/SighImageSuper/blob/main/sigh_image_live_loop.py): ancestor, not a claimed identical energy model.
- [BindingClaude Part 3 ledger](https://github.com/anttiluode/BindingClaude/blob/main/results/PART3_LEDGER.md): frozen inference success and revision limitation.
- [Della Pietra, Della Pietra & Lafferty, Inducing Features of Random Fields](https://arxiv.org/abs/cmp-lg/9506014): prior art for growing interaction features.
- [Besag, Statistical Analysis of Non-lattice Data (1975)](https://www2.stat.duke.edu/~sschmid/Courses/Stat376/Papers/GibbsFieldEst/BesagPseudoLik1975.pdf): pseudolikelihood prior art.
- [Krotov & Hopfield (2016)](https://papers.neurips.cc/paper_files/paper/2016/hash/eaae339c4d89fc102edd9dbdb6a28915-Abstract.html): higher-order associative-memory context, not proof of this system's performance.
