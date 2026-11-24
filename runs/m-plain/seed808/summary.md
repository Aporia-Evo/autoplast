# Search seed 808

task: regime collision3  alphabet: 20 ops, with Recip  readout: fixed o = S q  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 899550  time: 1713s  pop: 500  tournament: 10

commit: dce11aa  task seed: 808  train episodes: 144  persistent registers: 3 matrix, 0 vector, start identity  batch: 128

search: regularized evolution  tune-consts: 0  select: fitness  residual-insert: off

validation level (val > 0.651, T128 K8 val >= 0.838, train - val <= 0.03; checked every 50000 candidates): not reached

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* unclassified: 3060 candidates
* decayed linear attention: 4596 candidates
* linear attention: 24436 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.368): 24436 candidates
- delta rule (beta=1) (acc 0.610): 134516 candidates
- delta rule (beta=0.5) (acc 0.637): 258164 candidates
- gated delta (alpha=0.9) (acc 0.527): 133748 candidates

## Best rule

```
S' = ((P2 + S) + (((tanh((v - norm(S·k))) + (((v - norm(S·k)) + v) + ((v - norm(S·k)) + v))) + σ(<(|((v - norm(S·k)) + v)| + |((v - norm(S·k)) + v)|)·k, k>)·((v - norm(S·k)) + v)))⊗((|((v - norm(S·k)) + v)| + |((v - norm(S·k)) + v)|)·k))
P1' = (((σ(<(|((v - norm(S·k)) + v)| + |((v - norm(S·k)) + v)|)·k, k>)·((v - norm(S·k)) + v) ⊙ (|((v - norm(S·k)) + v)| + |((v - norm(S·k)) + v)|)·k) + ((tanh((v - norm(S·k))) + (((v - norm(S·k)) + v) + ((v - norm(S·k)) + v))) + σ(<(|((v - norm(S·k)) + v)| + |((v - norm(S·k)) + v)|)·k, k>)·((v - norm(S·k)) + v))))⊗(k)
P2' = ((tanh((v - norm(S·k))))⊗((|((v - norm(S·k)) + v)| + |((v - norm(S·k)) + v)|)·k) + P1)

Effective program (22 instructions):
  M2 = MatAdd(M2, M0)
  V4 = MatVec(M0, V0)
  V2 = Normalize(V4)
  V4 = VecSub(V1, V2)
  V2 = VecAdd(V4, V1)
  s0 = Norm(V2)
  V5 = Tanh(V4)
  s3 = SAdd(s0, s0)
  V4 = VecScale(s3, V0)
  s0 = Dot(V4, V0)
  s0 = Sigmoid(s0)
  V1 = VecAdd(V2, V2)
  V1 = VecAdd(V5, V1)
  V2 = VecScale(s0, V2)
  V1 = VecAdd(V1, V2)
  M0 = Outer(V1, V4)
  M0 = MatAdd(M2, M0)
  M2 = Outer(V5, V4)
  V5 = Hadamard(V2, V4)
  M2 = MatAdd(M2, M1)
  V2 = VecAdd(V5, V1)
  M1 = Outer(V2, V0)

structure: unclassified  [a=1.018 b=30.912 c=-0.405 g=-0.288, erase c/a=0.398, R²=0.9134, 1408 steps]

train acc 0.666 ±0.014
test regime collision3: acc 0.637  margin 0.026  ±0.006
test d16 T12 ow0.3: acc 0.868  margin 0.227  ±0.005
test d16 T12 ow0.0: acc 0.795  margin 0.174  ±0.005
test d16 T12 ow0.6: acc 0.897  margin 0.229  ±0.006
test d32 T24 ow0.3: acc 0.936  margin 0.322  ±0.004
test d8 T6 ow0.3: acc 0.739  margin 0.078  ±0.009
test d16 T64 K8 ow0.3: acc 0.827  margin 0.146  ±0.008
test d16 T128 K8 ow0.3: acc 0.814  margin 0.138  ±0.012
```
