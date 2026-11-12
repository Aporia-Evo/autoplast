# Search seed 10

task: regime collision3  alphabet: 20 ops, with Recip  readout: fixed o = S q  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 818272  time: 6422s  pop: 500  tournament: 10

commit: e979a8e  task seed: 1  train episodes: 144  persistent registers: 3 matrix, 0 vector, start identity  batch: 128

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* decayed linear attention: 2036 candidates
* unclassified: 3572 candidates
* linear attention: 6772 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.362): 6772 candidates
- delta rule (beta=1) (acc 0.578): 41332 candidates
- delta rule (beta=0.5) (acc 0.617): 42740 candidates
- gated delta (alpha=0.9) (acc 0.519): 24436 candidates

## Best rule

```
S' = ((…)((0.430·((P2 - (v)⊗(k)) - (P1)((P2 - (v)⊗(k)))) + ((P2 - (v)⊗(k)) - (P1)((P2 - (v)⊗(k)))))) - ((P2 - (v)⊗(k)) - (P1)((P2 - (v)⊗(k)))))
P1' = ((0.430·((P2 - (v)⊗(k)) - (P1)((P2 - (v)⊗(k)))) - ((P2 - (v)⊗(k)) - (P1)((P2 - (v)⊗(k))))))((0.469·(0.430·((P2 - (v)⊗(k)) - (P1)((P2 - (v)⊗(k)))) - ((P2 - (v)⊗(k)) - (P1)((P2 - (v)⊗(k))))))ᵀ)
P2' = ((P2 - (v)⊗(k)) - (P1)((P2 - (v)⊗(k))))

Effective program (15 instructions):
  M0 = Outer(V1, V0)
  s1 = 0.4689
  M2 = MatSub(M2, M0)
  M3 = MatMul(M1, M2)
  M2 = MatSub(M2, M3)
  s0 = 0.4297
  M0 = MatScale(s0, M2)
  M3 = MatSub(M0, M2)
  M1 = MatScale(s1, M3)
  M1 = Transpose(M1)
  M1 = MatMul(M3, M1)
  M3 = MatAdd(M0, M2)
  M0 = MatAdd(M1, M1)
  M0 = MatMul(M0, M3)
  M0 = MatSub(M0, M2)

structure: unclassified  [a=0.983 b=0.325 c=-0.511 g=-1.060, erase c/a=0.520, R²=0.6174, 1408 steps]

train acc 0.644 ±0.014
test regime collision3: acc 0.644  margin 0.041  ±0.006
test d16 T12 ow0.3: acc 0.862  margin 0.206  ±0.005
test d16 T12 ow0.0: acc 0.840  margin 0.173  ±0.005
test d16 T12 ow0.6: acc 0.839  margin 0.183  ±0.007
test d32 T24 ow0.3: acc 0.928  margin 0.298  ±0.004
test d8 T6 ow0.3: acc 0.690  margin 0.023  ±0.010
test d16 T64 K8 ow0.3: acc 0.731  margin 0.104  ±0.010
test d16 T128 K8 ow0.3: acc 0.726  margin 0.088  ±0.014
```
