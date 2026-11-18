# Search seed 11

task: regime collision3  alphabet: 20 ops, with Recip  readout: fixed o = S q  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 643819  time: 2366s  pop: 500  tournament: 10

commit: 50c2d10  task seed: 1  train episodes: 144  persistent registers: 3 matrix, 0 vector, start identity  batch: 128

search: regularized evolution  tune-consts: 0  select: lexicase

validation level (val > 0.651, T128 K8 val >= 0.838, train - val <= 0.03; checked every 50000 candidates): not reached

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* unclassified: 1396 candidates
* decayed linear attention: 2676 candidates
* linear attention: 9076 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.362): 9076 candidates
- delta rule (beta=1) (acc 0.578): 412276 candidates
- delta rule (beta=0.5) (acc 0.617): 413300 candidates
- gated delta (alpha=0.9) (acc 0.519): 392948 candidates

## Best rule

```
S' = (((v)⊗(k) + S) + ((v)⊗(k) - (|P2·k|·((P2·k)⊗(|P2·k|·v) - (v)⊗(k)))((v)⊗(k))))
P1' = (|P2·k|·((P2·k)⊗(|P2·k|·v) - (v)⊗(k)))((v)⊗(k))
P2' = 0.454·(((v)⊗(k) + S) + ((v)⊗(k) - (|P2·k|·((P2·k)⊗(|P2·k|·v) - (v)⊗(k)))((v)⊗(k))))

Effective program (13 instructions):
  V5 = MatVec(M2, V0)
  s1 = Norm(V5)
  V4 = VecScale(s1, V1)
  M1 = Outer(V5, V4)
  M2 = Outer(V1, V0)
  M1 = MatSub(M1, M2)
  s0 = 0.4541
  M1 = MatScale(s1, M1)
  M1 = MatMul(M1, M2)
  M3 = MatSub(M2, M1)
  M2 = MatAdd(M2, M0)
  M0 = MatAdd(M2, M3)
  M2 = MatScale(s0, M0)

structure: unclassified  [a=1.000 b=1.983 c=-0.513 g=0.002, erase c/a=0.513, R²=0.9582, 1408 steps]

train acc 0.636 ±0.014
test regime collision3: acc 0.642  margin 0.045  ±0.006
test d16 T12 ow0.3: acc 0.932  margin 0.243  ±0.004
test d16 T12 ow0.0: acc 0.922  margin 0.221  ±0.003
test d16 T12 ow0.6: acc 0.938  margin 0.248  ±0.005
test d32 T24 ow0.3: acc 0.989  margin 0.330  ±0.002
test d8 T6 ow0.3: acc 0.768  margin 0.096  ±0.009
test d16 T64 K8 ow0.3: acc 0.809  margin 0.158  ±0.009
test d16 T128 K8 ow0.3: acc 0.806  margin 0.154  ±0.012
```
