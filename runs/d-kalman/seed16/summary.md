# Search seed 16

task: regime collision3  alphabet: 20 ops, with Recip  readout: fixed o = S q  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 909251  time: 1445s  pop: 500  tournament: 10

commit: e979a8e  task seed: 1  train episodes: 144  persistent registers: 3 matrix, 0 vector, start identity  batch: 128

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* decayed linear attention: 3188 candidates
* unclassified: 8436 candidates
* linear attention: 11380 candidates
* delta rule: 11764 candidates
* linear, not error-correcting: 12788 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.362): 11380 candidates
- delta rule (beta=1) (acc 0.578): 11764 candidates
- delta rule (beta=0.5) (acc 0.617): 20084 candidates
- gated delta (alpha=0.9) (acc 0.519): 11764 candidates

## Best rule

```
S' = ((((v - S·k) + P2·(v - S·k)))⊗((σ(0)·norm((k - ((S·k ⊙ S·S·k) + (v ⊙ S·S·k)))) - ((S·k ⊙ S·S·k) + (v ⊙ S·S·k)))) - (0 - S))
P1' = (0 - S)
P2' = -0.134·S

Effective program (18 instructions):
  M1 = MatSub(M3, M0)
  V4 = MatVec(M0, V0)
  V5 = MatVec(M0, V4)
  s0 = Sigmoid(s0)
  V2 = VecSub(V1, V4)
  V1 = Hadamard(V1, V5)
  V5 = Hadamard(V4, V5)
  V5 = VecAdd(V5, V1)
  V1 = MatVec(M2, V2)
  V3 = VecSub(V0, V5)
  V0 = Normalize(V3)
  V0 = VecScale(s0, V0)
  s1 = -0.1337
  V4 = VecAdd(V2, V1)
  V2 = VecSub(V0, V5)
  M2 = MatScale(s1, M0)
  M0 = Outer(V4, V2)
  M0 = MatSub(M0, M1)

structure: unclassified  [a=1.000 b=0.516 c=-0.498 g=-0.013, erase c/a=0.498, R²=0.9410, 1408 steps]

train acc 0.635 ±0.014
test regime collision3: acc 0.636  margin 0.047  ±0.006
test d16 T12 ow0.3: acc 0.911  margin 0.253  ±0.004
test d16 T12 ow0.0: acc 0.908  margin 0.240  ±0.004
test d16 T12 ow0.6: acc 0.924  margin 0.251  ±0.005
test d32 T24 ow0.3: acc 0.979  margin 0.344  ±0.002
test d8 T6 ow0.3: acc 0.759  margin 0.093  ±0.009
test d16 T64 K8 ow0.3: acc 0.822  margin 0.146  ±0.008
test d16 T128 K8 ow0.3: acc 0.793  margin 0.134  ±0.013
```
