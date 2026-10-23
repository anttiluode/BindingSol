# Start here, Sol

## User intent

Antti supplied this dedicated repository and asked for a checklist that allows
Sol to take over if the Plus session hits a limit. Keep increments small, commit
working checkpoints, preserve failures, and keep the research state in git.
Do not edit Claude's repositories. Do not upload the raw private chat transcripts.

## Current checkpoint

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
