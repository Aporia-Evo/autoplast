# Search seed 21

task: regime collision3  alphabet: 20 ops, with Recip  readout: fixed o = S q  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 940418  time: 2832s  pop: 500  tournament: 10

commit: 50c2d10  task seed: 1  train episodes: 144  persistent registers: 3 matrix, 0 vector, start identity  batch: 128

search: regularized evolution  tune-consts: 0  select: share (radius 0.05)

validation level (val > 0.651, T128 K8 val >= 0.838, train - val <= 0.03; checked every 50000 candidates): not reached

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* decayed linear attention: 756 candidates
* unclassified: 3188 candidates
* linear attention: 4852 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.362): 4852 candidates
- delta rule (beta=1) (acc 0.578): 351988 candidates
- delta rule (beta=0.5) (acc 0.617): 351988 candidates
- gated delta (alpha=0.9) (acc 0.519): 75764 candidates

## Best rule

```
S' = ((-0.916·((P1 + (v)⊗(k)) - P2)·k)⊗(norm(tanh(k))) - -0.916·((P1 + (v)⊗(k)) - P2))
P1' = σ(0)·σ(0)·(-0.916·((P1 + (v)⊗(k)) - P2)·k)⊗(norm(tanh(k)))
P2' = -0.916·((P1 + (v)⊗(k)) - P2)

Effective program (13 instructions):
  V4 = Tanh(V0)
  M0 = Outer(V1, V0)
  V4 = Normalize(V4)
  M3 = MatAdd(M1, M0)
  s0 = -0.9164
  M3 = MatSub(M3, M2)
  M2 = MatScale(s0, M3)
  s1 = Sigmoid(s2)
  s2 = SMul(s1, s1)
  V1 = MatVec(M2, V0)
  M0 = Outer(V1, V4)
  M1 = MatScale(s2, M0)
  M0 = MatSub(M0, M2)

structure: unclassified  [a=0.909 b=0.001 c=-0.908 g=0.000, erase c/a=0.999, R²=0.2900, 1408 steps]

train acc 0.643 ±0.014
test regime collision3: acc 0.649  margin 0.048  ±0.006
test d16 T12 ow0.3: acc 0.858  margin 0.217  ±0.005
test d16 T12 ow0.0: acc 0.814  margin 0.189  ±0.005
test d16 T12 ow0.6: acc 0.891  margin 0.220  ±0.006
test d32 T24 ow0.3: acc 0.792  margin 0.218  ±0.006
test d8 T6 ow0.3: acc 0.783  margin 0.111  ±0.009
test d16 T64 K8 ow0.3: acc 0.739  margin 0.104  ±0.010
test d16 T128 K8 ow0.3: acc 0.732  margin 0.094  ±0.014
```
