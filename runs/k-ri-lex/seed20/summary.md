# Search seed 20

task: regime collision3  alphabet: 20 ops, with Recip  readout: fixed o = S q  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 993458  time: 2545s  pop: 500  tournament: 10

commit: 6c2f60a  task seed: 1  train episodes: 144  persistent registers: 3 matrix, 0 vector, start identity  batch: 128

search: regularized evolution  tune-consts: 0  select: lexicase  residual-insert: on

residual insert: 357359 attempts, 207696 blocks inserted, 225898 times dead instructions removed first

validation level (val > 0.651, T128 K8 val >= 0.838, train - val <= 0.03; checked every 50000 candidates): not reached

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* unclassified: 1012 candidates
* decayed linear attention: 9716 candidates
* gated delta rule: 18036 candidates
* delta rule: 22132 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.362): 4980 candidates
- delta rule (beta=1) (acc 0.578): 21236 candidates
- delta rule (beta=0.5) (acc 0.617): 22644 candidates
- gated delta (alpha=0.9) (acc 0.519): 19444 candidates

## Best rule

```
S' = (((v + -0.443·S·k))⊗(k) + (S + 0.085·((-0.443·(P2)ᵀ + P1) + (P2 + 0.063·-0.443·(P2)ᵀ))))
P1' = ((v + -0.443·S·k))⊗(k)
P2' = (((-0.443·(P2)ᵀ + P1) + (-0.443·(P2)ᵀ + P1)) + -0.033·((-0.443·(P2)ᵀ + P1) + (S + 0.085·((-0.443·(P2)ᵀ + P1) + (P2 + 0.063·-0.443·(P2)ᵀ)))))

Effective program (21 instructions):
  V2 = MatVec(M0, V0)
  s2 = -0.4428
  V2 = VecScale(s2, V2)
  M3 = Transpose(M2)
  M3 = MatScale(s2, M3)
  M1 = MatAdd(M3, M1)
  s3 = 0.0631
  M3 = MatScale(s3, M3)
  M2 = MatAdd(M2, M3)
  M3 = MatAdd(M1, M2)
  M2 = MatAdd(M1, M1)
  V1 = VecAdd(V1, V2)
  s1 = 0.0847
  M3 = MatScale(s1, M3)
  M3 = MatAdd(M0, M3)
  M0 = MatAdd(M1, M3)
  s3 = -0.0334
  M0 = MatScale(s3, M0)
  M2 = MatAdd(M2, M0)
  M1 = Outer(V1, V0)
  M0 = MatAdd(M1, M3)

structure: unclassified  [a=1.025 b=1.000 c=-0.431 g=-0.001, erase c/a=0.420, R²=0.9205, 1408 steps]

train acc 0.686 ±0.013
test regime collision3: acc 0.674  margin 0.066  ±0.006
test d16 T12 ow0.3: acc 0.943  margin 0.257  ±0.003
test d16 T12 ow0.0: acc 0.935  margin 0.248  ±0.003
test d16 T12 ow0.6: acc 0.929  margin 0.226  ±0.005
test d32 T24 ow0.3: acc 0.977  margin 0.347  ±0.002
test d8 T6 ow0.3: acc 0.783  margin 0.107  ±0.009
test d16 T64 K8 ow0.3: acc 0.833  margin 0.147  ±0.008
test d16 T128 K8 ow0.3: acc 0.817  margin 0.139  ±0.012
```
