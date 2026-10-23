# v0 verification record — 2026-10-23

One fresh-context read-only reviewer checked the implementation against PREREG.md,
the design/plan, tests and saved results. It did not train or modify anything.

Verdict: acceptable for this registered checkpoint; no Critical, Important or
Minor findings requiring changes. Ten tests passed. The reviewer independently
reloaded all five NPZ files and reproduced every metric and saved case prediction;
source hashes, weight hashes and fingerprints matched.

Checked: hard discrete receiver inputs; exact expected-loss gradients; disjoint
24/8 combinations; disclosed symbol/rule limitations; 162-parameter comparison;
supervised fresh receiver; manifest validation; atomic per-seed write order;
correct FAIL verdicts for G1/G2/G3.

Scope decisions retained by the implementer:
- Matching parameters and training steps does not mean matching compute. Claim
  only the recorded budget, not equal FLOPs or speed superiority.
- Broader transfer, novelty and neuroscience are not evaluated; no such result
  is claimed. These require different experiments.
- Adversarial tampering, concurrent writers and power-loss durability were not
  audited. This is a trusted local single-process experiment runner. Run one writer
  per output directory. Atomic replacement protects ordinary interruption, not a
  claimed transactional or adversarial storage guarantee.

The implementation deliberately keeps v0 fixed after results. Any model or
protocol change belongs in a new registered version and new output directory.
