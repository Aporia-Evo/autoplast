# Search seed 4

task: regime collision3  alphabet: 20 ops, with Recip  readout: fixed o = S q  add-node mutation: on  candidates: 2100084  real evaluations (after cache): 1255460  time: 3008s  pop: 500  tournament: 10

commit: 6c2f60a  task seed: 1  train episodes: 144  persistent registers: 3 matrix, 0 vector, start identity  batch: 128

search: regularized evolution  tune-consts: 0  select: fitness  residual-insert: off

validation level (val > 0.651, T128 K8 val >= 0.838, train - val <= 0.03; checked every 50000 candidates): not reached

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* unclassified: 3828 candidates
* decayed linear attention: 4468 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.362): 10100 candidates
- delta rule (beta=1) (acc 0.578): 274676 candidates
- delta rule (beta=0.5) (acc 0.617): 275444 candidates
- gated delta (alpha=0.9) (acc 0.519): 273524 candidates

## Best rule

```
S' = (((((((P1 - S)·(0 - P1)·k ⊙ norm(tanh(tanh(v)))) + tanh(tanh(v))) + (0 - P1)·k))⊗(k) + (((((P1 - S)·(0 - P1)·k ⊙ norm(tanh(tanh(v)))) + tanh(tanh(v))) + (0 - P1)·k))⊗(k)) - (0 - S))
P1' = -0.230·((0 - S) - (((((P1 - S)·(0 - P1)·k ⊙ norm(tanh(tanh(v)))) + tanh(tanh(v))) + (0 - P1)·k))⊗(k))
P2' = (0 - S)

Effective program (17 instructions):
  M2 = MatSub(M3, M0)
  V2 = Tanh(V1)
  V4 = Tanh(V2)
  M3 = MatSub(M3, M1)
  V2 = Normalize(V4)
  V1 = MatVec(M3, V0)
  M0 = MatSub(M1, M0)
  V3 = MatVec(M0, V1)
  V2 = Hadamard(V3, V2)
  V5 = VecAdd(V2, V4)
  V1 = VecAdd(V5, V1)
  s3 = -0.2301
  M0 = Outer(V1, V0)
  M3 = MatAdd(M0, M0)
  M0 = MatSub(M2, M0)
  M1 = MatScale(s3, M0)
  M0 = MatSub(M3, M2)

structure: unclassified  [a=1.000 b=1.817 c=-0.429 g=0.000, erase c/a=0.429, R²=0.9359, 1408 steps]

train acc 0.628 ±0.014
test regime collision3: acc 0.632  margin 0.035  ±0.006
test d16 T12 ow0.3: acc 0.892  margin 0.231  ±0.005
test d16 T12 ow0.0: acc 0.877  margin 0.213  ±0.004
test d16 T12 ow0.6: acc 0.901  margin 0.219  ±0.006
test d32 T24 ow0.3: acc 0.978  margin 0.331  ±0.002
test d8 T6 ow0.3: acc 0.695  margin 0.056  ±0.010
test d16 T64 K8 ow0.3: acc 0.782  margin 0.119  ±0.009
test d16 T128 K8 ow0.3: acc 0.769  margin 0.113  ±0.013
```
