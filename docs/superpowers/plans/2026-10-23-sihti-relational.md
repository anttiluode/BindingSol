# Sihti Relational Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking. Antti assigned implementation to Sol; this document does not launch implementation.

**Goal:** Build an inspectable learner that completes small visual assemblies and revises learned relationships from new observations.

**Architecture:** A categorical factor graph separates fixed-parameter inference from parameter fitting and evidence-based structural edits. An EQ frontend supplies fixed sensory scores; exact small conditional enumeration audits recurrent results. All interventions and edits produce replayable records.

**Tech Stack:** Python 3.10+, NumPy, standard-library local HTTP server, browser JavaScript.

**Spec:** ../specs/2026-10-23-sihti-relational-design.md

## Global Constraints

- Work only in BindingSol; preserve `binding.py`, `run.py`, `PREREG.md` and `results/v0`.
- Use new `relational/`, `tests/test_relational_*.py`, `web/relational/` and `results/relational-v1/` namespaces.
- Nine eight-state tiles, one observed two-state context, at most three hidden tiles, at most 24 relational factors of order two or three.
- No GPU, external model, paid API or new runtime dependency.
- Implement the design's masks, projection, update tolerance, fitting budgets, splits, seeds and stopping rules exactly; register any development changes before final evaluation.
- Never change SihtiGraphModel's ongoing run, its protocol or its repository. It is a separate distillation instrument.

## Review Focus

- A hidden target must not leak through rendered patches, cached arrays or JSON sent before reveal: Tasks 1 and 5.
- Equal-scoring completions must remain ambiguous and cannot cause oscillatory tie changes: Task 2.
- Mixed domain sizes (context two, tiles eight) and factor axis order must stay consistent: Task 2.
- Rejected proposals, interrupted decisions and deleted factors must preserve evidence and deterministic resume: Task 3.
- Finite confirmation exhaustion, a zero revision gap, missing baselines and timeouts must not become false PASS verdicts: Task 4.

## Task 1: Finite world and sensory boundary

**Files:** create `relational/__init__.py`, `relational/types.py`, `relational/world.py`, `relational/sensory.py`, `tests/test_relational_world.py`.

**Interfaces:** `Scene(board_id: str, tiles: ndarray[9], context: int)`; `Query(observed: ndarray[9], mask: ndarray[9,bool], context: int, pixels: ndarray[48,48], pixel_mask: ndarray[48,48,bool])`, where `mask=True` means observed and missing tile storage is -1. `make_catalogue() -> list[Scene]` enumerates boards independent of context; assign context when sampling. `make_query(scene, hidden_indices) -> Query` removes truth. `sensory_scores(query) -> ndarray[9,8]` knows no hidden targets. Reference answers remain in a separate evaluator object.

- [ ] Write tests for rank 9 and 32,768 unique even-degree boards, template mapping, shared ports, exact board split disjointness and deterministic SHA-based split assignment.
- [ ] Add a hidden-target mutation test: identical observed tiles and masked pixels must produce identical Query contents and sensory scores regardless of hidden truth.
- [ ] Run `python -m unittest discover -s tests -p 'test_relational_world.py' -v`; confirm the tests fail before implementation.
- [ ] Implement the finite catalogue and EQ frontend from the spec. Choose/hash template rendering details; no learner access to generator constraints.
- [ ] Rerun the same tests; commit the passing instrument and its choices.

## Task 2: Coherent model, fitting objective and inference audit

**Files:** create `relational/model.py`, `relational/inference.py`, `relational/fit.py`, `tests/test_relational_model.py`.

**Interfaces:** `Factor(id: str, scope: tuple[int,...], table: ndarray)`; context index is 9. `Model(unaries: ndarray[9,8], factors: list[Factor])`; `score(model, assignments, sensory) -> ndarray`; `infer_exact(model, query, sensory) -> ExactResult`; `settle(model, query, sensory, order, max_sweeps=32) -> SettleResult`; `fit(model, fitting_scenes, config, rng) -> FitResult`. ExactResult includes assignments, normalized probabilities, marginals and all MAP ties. SettleResult includes initial/final state, move trace, energies and stop reason. Define these result dataclasses in `types.py` before consumers use them.

- [ ] Write numerical fixtures verifying normalized conditional probabilities, all eight candidates per tile, clamped observations, two-state context axes, score-delta decomposition and gauge projection.
- [ ] Add a strict-improvement/tie fixture and a deliberately trapped local optimum: exact inference must expose the gap instead of silently correcting the recurrent output.
- [ ] Add finite-difference tests of pseudolikelihood projected gradients and a no-hidden/no-factor boundary case.
- [ ] Run `python -m unittest discover -s tests -p 'test_relational_model.py' -v`; confirm failure, implement the specified algorithms, rerun and commit once passing.

## Task 3: Bounded growth and revision

**Files:** create `relational/structure.py`, `relational/checkpoint.py`, `tests/test_relational_structure.py`.

**Interfaces:** `propose_scopes(model, config, rng) -> list[tuple[int,...]]`; `structural_decision(model, fitting, screening, confirmation, config, rng) -> DecisionResult`; `save_checkpoint(path, state)` / `load_checkpoint(path, expected_manifest) -> state`. DecisionResult contains selected edit, acceptance inequality inputs, data IDs and complete rejected-candidate records. Saved state includes model, replay, RNG, used-confirmation IDs, decision index and tombstones.

- [ ] Write fixtures where a candidate helps only screening and is rejected on confirmation; an unhelpful costly factor is deleted; a rare useful factor survives contrary internal votes.
- [ ] Test fresh-confirmation enforcement, caps, exhausted candidate pools, exhausted confirmation data and hash-mismatched resume rejection. Kill/resume a deterministic tiny decision sequence and compare to uninterrupted output.
- [ ] Run `python -m unittest discover -s tests -p 'test_relational_structure.py' -v`; confirm failure.
- [ ] Implement candidate fitting, selection, one fresh confirmation, reversible edits and between-episode updates exactly as specified. Freeze all model state during inference.
- [ ] Rerun tests and commit. Do not use registered final cases to inspect growth.

## Task 4: Locked comparison and revision runner

**Files:** create `relational/baselines.py`, `relational/evaluate.py`, `relational/run.py`, `relational/PROTOCOL.md`, `tests/test_relational_evaluate.py`.

**Interfaces:** `evaluate(model, cases, config) -> dict`; `run_seed(seed, config, out) -> dict`. CLI: `python -m relational.run --mode preflight|registered --out PATH`. Preflight uses development data only. Registered mode refuses uncommitted/unhashed protocol/configuration or a mismatched resume directory.

- [ ] Write fixtures for joint-NLL-per-hidden-tile, accuracy, abstention, all G0-G5 verdict branches, finite budgets, zero/negative fresh-fit revision gap and incomplete baseline handling.
- [ ] Implement specified controls and identical data exposure. Select MLP architecture and stopping on development data; pin them, the exact mask schedule, proposal allocation and cost records in the protocol.
- [ ] Run tests and development preflight only. Commit protocol, generated split hashes and cost estimates before opening final results.
- [ ] Run the one registered three-seed batch, including all schedules and controls. Save checkpoints before final evaluation and all per-case outputs afterwards. Do not retune failed gates.
- [ ] Commit a ledger with every seed, gate, limitation and exact resume command. No image-AI or efficiency claim without the relevant comparison.

## Task 5: Inspector powered by measured traces

**Files:** create `relational/server.py`, `web/relational/index.html`, `web/relational/app.js`, `tests/test_relational_server.py`.

**Interfaces:** bind to localhost; GET `/api/state` returns a selected saved model/query and permitted trace; POST `/api/infer` takes query ID, model ID, coordinate order and disabled factor IDs; POST `/api/reveal` reveals the selected observation. Responses never include hidden labels before reveal. The browser does not implement another numerical inference algorithm.

- [ ] Test payload boundaries and that factor toggles alter only episode overlays; restoration reproduces the original inference exactly.
- [ ] Implement the four views from the spec: board/EQ, recurrent versus exact results, factor inspector, same-query intervention comparison. Demo activity must come from logged numeric updates.
- [ ] Run `python -m unittest discover -s tests -v`. Open the local page and verify unknowns, alternatives, disable/restore, A/B history comparison, displayed delta sums and a failed/ambiguous case.
- [ ] Commit the inspector and update README/CHECKLIST/HANDOFF with measured status and next unchecked item. Preserve all design limits in the visible page.

## First handoff action

Sol should read the spec and current repository state, reconcile the separate binary-motif proposal on `design/next-sihti-visible-circuit-20261023`, then implement Task 1 of the chosen scope in an isolated branch. Do not build both proposals or start a second CIFAR run. SihtiGraphModel's running receipt will inform a later scope-proposal transfer experiment, not this version's inference coefficients.
