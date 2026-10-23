# Living checklist

Update this file and HANDOFF.md in every meaningful checkpoint commit.
`[x]` means verified work, not an intention. Never erase a failed gate.

## Checkpoint 0 — scope and continuity
- [x] Read both supplied discussions; inspect BindingSol (initially LICENSE only).
- [x] Work only in BindingSol; preserve predecessor repositories.
- [x] Record finite-task scope, ordinary controls and claim limits.
- [x] Write fixed v0 protocol before training.
- [x] Push the protocol checkpoint before running any learner (`f18a0c4`).

## Checkpoint 1 — implementation
- [x] Implement exhaustive generator and leakage/balance checks.
- [x] Verify exact discrete-channel gradients with finite differences.
- [x] Implement joint learning, frozen-sender fresh reader and matched baseline.
- [x] Implement interventions, atomic per-seed saves and manifest-checked resume.
- [x] Run the complete test suite.

## Checkpoint 2 — one registered CPU batch
- [x] Run seeds 41, 97, 127, 203, 509 without retuning.
- [x] Preserve each seed's weights, predictions and metrics.
- [x] Record all G0–G4 verdicts, including negative results.
- [x] Verify resume and review implementation/claims (REVIEW.md).
- [x] Push code, results, updated checklist and handoff (this checkpoint).

G0 PASS; G1/G2/G3 FAIL (2/5; required 4/5); G4 reported.
See RESULTS.md. Stop after this batch; do not retune v0.

## Later checkpoints — not authorized evidence claims
- [ ] Preregister the next test based on v0's actual failure or success.
- [ ] Test new symbol/layout contexts and zero-shot cross-play.
- [ ] Only then consider rendered pieces, images or a language-model/J-lens reader.
