# Start here, Sol

## User intent

Antti supplied this dedicated repository and asked for a checklist that allows
Sol to take over if the Plus session hits a limit. Keep increments small, commit
working checkpoints, preserve failures, and keep the research state in git.
Do not edit Claude's repositories. Do not upload the raw private chat transcripts.

## Current checkpoint

### New design request, October 23

Antti asked Astra to design an inspectable learning/purification system for Sol
to build, then asked for analysis while SihtiGraphModel's real run was active.
These are separate from the completed communication v0 below.

- Design: `docs/superpowers/specs/2026-10-23-sihti-relational-design.md`.
- Task checklist: `docs/superpowers/plans/2026-10-23-sihti-relational.md`.
- Current instrument review: `docs/sihtigraphmodel-v1-review.md`.

The design is proposed and unimplemented. A builder review identified four
issues; the design now specifies unconditional weight updates, a joint neural
baseline, separated finite confirmation pools and continued learning after
proposal exhaustion. No new learning result is claimed. The next design-track
action is Task 1 in the plan; read the spec first. Do not launch another CIFAR
run or edit the existing SihtiGraphModel experiment. Its classifier-response
coefficients are not automatically scene-completion couplings.

A separate binary-motif proposal appeared during this review on
`design/next-sihti-visible-circuit-20261023` (head `25e7f39`). It is preserved;
this checkpoint neither merges nor edits that branch. The categorical design
here is a more explicit alternative, not a second build request. Sol should
reconcile the two before implementation and build only one agreed scope.

Read-only verification for SihtiGraphModel: three NumPy tests passed; two torch
tests skipped here; synthetic smoke R2 0.9997078; separate 64-switch sparse fixture
R2 0.9994651. Real CIFAR receipt remains on Antti's machine and was not inspected.
The old v0 diagnostic below remains an unresolved separate track, not a gate that
silently cancels Antti's newer design request.

Exact next read command:

```bash
cat docs/superpowers/specs/2026-10-23-sihti-relational-design.md docs/superpowers/plans/2026-10-23-sihti-relational.md
```

v0 has completed its one registered batch. G0 PASS; G1/G2/G3 FAIL (2/5
seeds qualify, required 4/5). G4 comparison recorded. Joint and fresh-reader mean
held-out accuracy 85%, direct MLP 90%, linear 50%. Full table: RESULTS.md.

Ten tests passed. Reloading saved NPZ weights reproduced all model metrics.
Resume reused all five seeds without retraining. Independent review found no issues requiring changes (REVIEW.md). All code,
results and handoff documents are included in this result checkpoint on main.

**First unchecked scientific step:** write a v1 diagnostic protocol, not another
v0 tuning run. Inspect the two misencoded source triples in each failed seed
(RESULTS.md) and separate sender-learning failure from receiver/channel failure.
Choose fresh seeds and a controlled intervention before running anything. Do not
jump to images or a J-lens yet. v0 proves feasibility in 2/5 runs, not reliability.

Git HTTPS pushes lack credentials here; authenticated GitHub connector tree/commit/
ref operations work. Use a compare-and-swap expected head, never force overwrite.

## Decisions made by this implementer

- Use an exact finite parity task before pixels or pretrained LMs: cheap and
  auditable. This cannot establish natural-image transfer.
- One binary message, optimized via its exact expected task loss. Shared training
  is a teacher; we are not claiming unsupervised discovery or biological learning.
- The new receiver gets supervised examples with a frozen sender; it does not
  share a decoder by magic. Zero-shot cross-play remains a separate experiment.
- New combinations are held out, not new symbols/rules. Enumerate all 32 cases
  to expose shortcuts; show training and full-domain accuracy alongside held-out.
- Native implementation in this isolated fresh clone on work/binding-v0.
  No large installs, expensive model runs, or repeated tuning batches.
- Durable CHECKLIST/HANDOFF take precedence over ephemeral workflow scratch.

## Verify and reproduce

```bash
git pull --ff-only
python -m pip install -r requirements.txt
python -m unittest discover -s tests -v
python run.py --out results/local-v0
```

Read PREREG.md before touching a model. The committed results/v0 already has all five seeds; read summary.json and
RESULTS.md first. The command above creates/resumes a separate local reproduction. If a change alters the protocol
or experiment code, leave v0 intact and start a versioned directory/protocol.

## Source context

The user supplied an October 23 synthesis and an older Claude/Välikäsi transcript.
The synthesis proposes this sender/receiver experiment. The transcript motivates
separating influence, oracle recoverability and usable information. Its stronger
claims about XOR, linear probes and subliminal-learning mechanisms are not treated
as established. No new external-paper result is being claimed here.
