# Search seed 2

task: regime collision3  alphabet: 20 ops, with Recip  readout: fixed o = S q  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 956204  time: 2783s  pop: 500  tournament: 10

commit: 6c2f60a  task seed: 1  train episodes: 144  persistent registers: 3 matrix, 0 vector, start identity  batch: 128

search: regularized evolution  tune-consts: 0  select: lexicase  residual-insert: on

residual insert: 357156 attempts, 262109 blocks inserted, 279807 times dead instructions removed first

validation level (val > 0.651, T128 K8 val >= 0.838, train - val <= 0.03; checked every 50000 candidates): 50036 candidates

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* unclassified: 3060 candidates
* decayed linear attention: 7284 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.362): 6516 candidates
- delta rule (beta=1) (acc 0.578): 28148 candidates
- delta rule (beta=0.5) (acc 0.617): 29172 candidates
- gated delta (alpha=0.9) (acc 0.519): 16372 candidates

## Best rule

```
S' = (((P1 - P2) + (0.385·S - ((v + (-0.736·(P1 - P2)·k + tanh(v))))⊗((0.011·v - k)))) + (0.385·S - ((v + (-0.736·(P1 - P2)·k + tanh(v))))⊗((0.011·v - k))))
P1' = (P1 - P2)
P2' = ((v + (-0.736·(P1 - P2)·k + tanh(v))))⊗((0.011·v - k))

Effective program (16 instructions):
  M1 = MatSub(M1, M2)
  V5 = MatVec(M1, V0)
  s3 = -0.7355
  s2 = 0.0112
  V2 = VecScale(s2, V1)
  V2 = VecSub(V2, V0)
  V5 = VecScale(s3, V5)
  V0 = Tanh(V1)
  V5 = VecAdd(V5, V0)
  V4 = VecAdd(V1, V5)
  s2 = 0.3849
  M3 = MatScale(s2, M0)
  M2 = Outer(V4, V2)
  M3 = MatSub(M3, M2)
  M0 = MatAdd(M1, M3)
  M0 = MatAdd(M0, M3)

structure: unclassified  [a=1.032 b=3.899 c=-0.393 g=0.001, erase c/a=0.380, R²=0.9202, 1408 steps]

train acc 0.676 ±0.013
test regime collision3: acc 0.668  margin 0.076  ±0.006
test d16 T12 ow0.3: acc 0.948  margin 0.280  ±0.003
test d16 T12 ow0.0: acc 0.935  margin 0.258  ±0.003
test d16 T12 ow0.6: acc 0.924  margin 0.258  ±0.005
test d32 T24 ow0.3: acc 0.979  margin 0.369  ±0.002
test d8 T6 ow0.3: acc 0.823  margin 0.130  ±0.008
test d16 T64 K8 ow0.3: acc 0.825  margin 0.161  ±0.008
test d16 T128 K8 ow0.3: acc 0.812  margin 0.155  ±0.012
```
