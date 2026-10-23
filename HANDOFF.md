# Start here, Sol

## User intent

Antti supplied this dedicated repository and asked for a checklist that allows
Sol to take over if the Plus session hits a limit. Keep increments small, commit
working checkpoints, preserve failures, and keep the research state in git.
Do not edit Claude's repositories. Do not upload the raw private chat transcripts.

## Current checkpoint

Protocol and implementation plan written. No training has run yet. Next: push
this checkpoint, implement tests and the tiny NumPy baseline, run exactly the
registered five seeds, update this file and CHECKLIST.md, push the results.

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

## Resume commands once code exists

```bash
git pull --ff-only
python -m pip install -r requirements.txt
python -m unittest discover -s tests -v
python run.py --out results/v0
```

Read PREREG.md before touching a model. If results/v0 already has all five seeds,
do not retrain; read summary.json and RESULTS.md. If a change alters the protocol
or experiment code, leave v0 intact and start a versioned directory/protocol.

## Source context

The user supplied an October 23 synthesis and an older Claude/Välikäsi transcript.
The synthesis proposes this sender/receiver experiment. The transcript motivates
separating influence, oracle recoverability and usable information. Its stronger
claims about XOR, linear probes and subliminal-learning mechanisms are not treated
as established. No new external-paper result is being claimed here.
