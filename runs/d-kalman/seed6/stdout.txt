# Search seed 6

task: regime collision3  alphabet: 20 ops, with Recip  readout: fixed o = S q  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 700999  time: 5356s  pop: 500  tournament: 10

commit: e979a8e  task seed: 1  train episodes: 144  persistent registers: 3 matrix, 0 vector, start identity  batch: 128

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* decayed linear attention: 628 candidates
* unclassified: 10996 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.362): 11636 candidates
- delta rule (beta=1) (acc 0.578): 164980 candidates
- delta rule (beta=0.5) (acc 0.617): 194676 candidates
- gated delta (alpha=0.9) (acc 0.519): 162932 candidates

## Best rule

```
S' = ((P2 - P1) + σ(0)·(v)⊗(k))
P1' = ((P2 - P1))(((((((v)⊗(k))(P1))((v)⊗(k)) + (v)⊗(k)))ᵀ)(σ(0)·(v)⊗(k)))
P2' = 0.993·((P2 - P1) + σ(0)·(v)⊗(k))

Effective program (13 instructions):
  M2 = MatSub(M2, M1)
  M0 = Outer(V1, V0)
  M3 = MatMul(M0, M1)
  M1 = MatMul(M3, M0)
  s2 = Sigmoid(s3)
  M3 = MatAdd(M1, M0)
  M1 = Transpose(M3)
  M0 = MatScale(s2, M0)
  M1 = MatMul(M1, M0)
  M0 = MatAdd(M2, M0)
  M1 = MatMul(M2, M1)
  s2 = 0.9925
  M2 = MatScale(s2, M0)

structure: unclassified  [a=0.925 b=0.501 c=-0.027 g=-0.002, erase c/a=0.029, R²=0.8389, 1408 steps]

train acc 0.622 ±0.014
test regime collision3: acc 0.629  margin 0.035  ±0.006
test d16 T12 ow0.3: acc 0.907  margin 0.242  ±0.004
test d16 T12 ow0.0: acc 0.895  margin 0.226  ±0.004
test d16 T12 ow0.6: acc 0.886  margin 0.226  ±0.006
test d32 T24 ow0.3: acc 0.976  margin 0.335  ±0.002
test d8 T6 ow0.3: acc 0.745  margin 0.090  ±0.009
test d16 T64 K8 ow0.3: acc 0.793  margin 0.139  ±0.009
test d16 T128 K8 ow0.3: acc 0.787  margin 0.131  ±0.013
```
