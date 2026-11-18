# Search seed 5

task: regime collision3  alphabet: 20 ops, with Recip  readout: fixed o = S q  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 771730  time: 2845s  pop: 500  tournament: 10

commit: 50c2d10  task seed: 1  train episodes: 144  persistent registers: 3 matrix, 0 vector, start identity  batch: 128

search: regularized evolution  tune-consts: 0  select: lexicase

validation level (val > 0.651, T128 K8 val >= 0.838, train - val <= 0.03; checked every 50000 candidates): 700020 candidates

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* unclassified: 1524 candidates
* linear, not error-correcting: 2804 candidates
* decayed linear attention: 3060 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.362): 8052 candidates
- delta rule (beta=1) (acc 0.578): 12020 candidates
- delta rule (beta=0.5) (acc 0.617): 13812 candidates
- gated delta (alpha=0.9) (acc 0.519): 10868 candidates

## Best rule

```
S' = (((P1 - ((P1·tanh(tanh(k)) + v))⊗(|tanh(tanh(k))|·tanh(tanh(tanh(k))))))(P2) - (P1 - ((P1·tanh(tanh(k)) + v))⊗(|tanh(tanh(k))|·tanh(tanh(tanh(k))))))
P1' = (P1 - ((P1·tanh(tanh(k)) + v))⊗(|tanh(tanh(k))|·tanh(tanh(tanh(k)))))
P2' = 1.896·σ(0)·σ(0)·S

Effective program (16 instructions):
  s3 = Sigmoid(s2)
  M3 = MatScale(s3, M0)
  V3 = Tanh(V0)
  s1 = 1.8956
  V5 = Tanh(V3)
  V4 = MatVec(M1, V5)
  V1 = VecAdd(V4, V1)
  V4 = Tanh(V5)
  s2 = Norm(V5)
  V0 = VecScale(s2, V4)
  M0 = Outer(V1, V0)
  M1 = MatSub(M1, M0)
  M2 = MatMul(M1, M2)
  M0 = MatSub(M2, M1)
  s3 = SMul(s1, s3)
  M2 = MatScale(s3, M3)

structure: unclassified  [a=1.013 b=0.866 c=-0.497 g=0.009, erase c/a=0.491, R²=0.5228, 1408 steps]

train acc 0.671 ±0.013
test regime collision3: acc 0.672  margin 0.064  ±0.006
test d16 T12 ow0.3: acc 0.898  margin 0.229  ±0.005
test d16 T12 ow0.0: acc 0.861  margin 0.191  ±0.004
test d16 T12 ow0.6: acc 0.898  margin 0.221  ±0.006
test d32 T24 ow0.3: acc 0.981  margin 0.335  ±0.002
test d8 T6 ow0.3: acc 0.621  margin 0.032  ±0.010
test d16 T64 K8 ow0.3: acc 0.820  margin 0.150  ±0.008
test d16 T128 K8 ow0.3: acc 0.813  margin 0.141  ±0.012
```
