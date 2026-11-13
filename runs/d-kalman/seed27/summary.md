# Search seed 27

task: regime collision3  alphabet: 20 ops, with Recip  readout: fixed o = S q  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 1045608  time: 3270s  pop: 500  tournament: 10

commit: e979a8e  task seed: 1  train episodes: 144  persistent registers: 3 matrix, 0 vector, start identity  batch: 128

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* decayed linear attention: 1396 candidates
* unclassified: 12404 candidates
* linear attention: 14068 candidates
* gated delta rule: 74740 candidates
* delta rule: 75380 candidates
* delta + Kronecker mix: 78068 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.362): 14068 candidates
- delta rule (beta=1) (acc 0.578): 75380 candidates
- delta rule (beta=0.5) (acc 0.617): 75892 candidates
- gated delta (alpha=0.9) (acc 0.519): 74740 candidates

## Best rule

```
S' = (σ(<tanh((P1 - (S + P2))·tanh(tanh(k))), norm((tanh((P1 - (S + P2))·tanh(tanh(k))) + tanh(tanh(v))))>·<tanh((P1 - (S + P2))·tanh(tanh(k))), norm((tanh((P1 - (S + P2))·tanh(tanh(k))) + tanh(tanh(v))))>)·((tanh((P1 - (S + P2))·tanh(tanh(k))) + tanh(tanh(v))))⊗(norm(tanh(tanh(tanh(k))))) - (P1 - (S + P2)))
P1' = (… - …)
P2' = (tanh(tanh(v)))⊗(norm(tanh(tanh(tanh(k)))))

Effective program (24 instructions):
  M0 = MatAdd(M0, M2)
  M1 = MatSub(M1, M0)
  V5 = Tanh(V0)
  V4 = Tanh(V5)
  V2 = MatVec(M1, V4)
  V3 = Tanh(V2)
  V2 = Tanh(V1)
  V5 = Tanh(V4)
  V0 = Normalize(V5)
  V1 = Tanh(V2)
  V5 = VecAdd(V3, V1)
  V2 = Normalize(V5)
  M0 = Outer(V5, V0)
  s1 = Dot(V3, V2)
  s3 = SMul(s1, s1)
  s3 = Sigmoid(s3)
  M3 = MatScale(s3, M0)
  M2 = Outer(V1, V0)
  M0 = MatSub(M3, M1)
  M3 = MatScale(s1, M3)
  M3 = MatSub(M3, M2)
  M1 = MatScale(s3, M3)
  M1 = MatScale(s3, M1)
  M1 = MatSub(M3, M1)

structure: unclassified  [a=1.048 b=0.720 c=-0.680 g=-0.016, erase c/a=0.649, R²=0.6308, 1408 steps]

train acc 0.681 ±0.013
test regime collision3: acc 0.687  margin 0.072  ±0.006
test d16 T12 ow0.3: acc 0.940  margin 0.250  ±0.004
test d16 T12 ow0.0: acc 0.943  margin 0.240  ±0.003
test d16 T12 ow0.6: acc 0.939  margin 0.233  ±0.005
test d32 T24 ow0.3: acc 0.991  margin 0.361  ±0.001
test d8 T6 ow0.3: acc 0.668  margin 0.058  ±0.010
test d16 T64 K8 ow0.3: acc 0.816  margin 0.132  ±0.009
test d16 T128 K8 ow0.3: acc 0.808  margin 0.124  ±0.012
```
