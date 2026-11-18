# Search seed 31

task: regime collision3  alphabet: 20 ops, with Recip  readout: fixed o = S q  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 818102  time: 2767s  pop: 500  tournament: 10

commit: 50c2d10  task seed: 1  train episodes: 144  persistent registers: 3 matrix, 0 vector, start identity  batch: 128

search: regularized evolution  tune-consts: 0  select: lexicase

validation level (val > 0.651, T128 K8 val >= 0.838, train - val <= 0.03; checked every 50000 candidates): 100084 candidates

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* unclassified: 1524 candidates
* decayed linear attention: 2036 candidates
* linear attention: 4596 candidates
* gated delta rule: 71924 candidates
* delta rule: 72948 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.362): 4596 candidates
- delta rule (beta=1) (acc 0.578): 72948 candidates
- delta rule (beta=0.5) (acc 0.617): 82804 candidates
- gated delta (alpha=0.9) (acc 0.519): 71924 candidates

## Best rule

```
S' = (((norm(v))⊗(tanh(tanh(k))) + ((0 + P1) - (P1·tanh(tanh(k)))⊗(tanh(tanh(k))))) + (((norm(v))⊗(tanh(tanh(k))) + ((0 + P1) - (P1·tanh(tanh(k)))⊗(tanh(tanh(k))))))(0.641·(P2 + (((0 + P1) - (P1·tanh(tanh(k)))⊗(tanh(tanh(k)))))(((0 + P1) - (P1·tanh(tanh(k)))⊗(tanh(tanh(k))))))))
P1' = ((norm(v))⊗(tanh(tanh(k))) + ((0 + P1) - (P1·tanh(tanh(k)))⊗(tanh(tanh(k)))))
P2' = 0.641·(P2 + (((0 + P1) - (P1·tanh(tanh(k)))⊗(tanh(tanh(k)))))(((0 + P1) - (P1·tanh(tanh(k)))⊗(tanh(tanh(k))))))

Effective program (15 instructions):
  V3 = Normalize(V1)
  V0 = Tanh(V0)
  V1 = Tanh(V0)
  M0 = MatAdd(M3, M1)
  V2 = MatVec(M1, V1)
  M1 = Outer(V3, V1)
  M3 = Outer(V2, V1)
  M3 = MatSub(M0, M3)
  M1 = MatAdd(M1, M3)
  s3 = 0.6413
  M3 = MatMul(M3, M3)
  M0 = MatAdd(M2, M3)
  M2 = MatScale(s3, M0)
  M0 = MatMul(M1, M2)
  M0 = MatAdd(M1, M0)

structure: unclassified  [a=1.010 b=1.167 c=-0.634 g=0.006, erase c/a=0.627, R²=0.4337, 1408 steps]

train acc 0.684 ±0.013
test regime collision3: acc 0.670  margin 0.070  ±0.006
test d16 T12 ow0.3: acc 0.906  margin 0.232  ±0.004
test d16 T12 ow0.0: acc 0.823  margin 0.166  ±0.005
test d16 T12 ow0.6: acc 0.927  margin 0.258  ±0.005
test d32 T24 ow0.3: acc 0.964  margin 0.297  ±0.003
test d8 T6 ow0.3: acc 0.756  margin 0.095  ±0.009
test d16 T64 K8 ow0.3: acc 0.772  margin 0.125  ±0.009
test d16 T128 K8 ow0.3: acc 0.792  margin 0.135  ±0.013
```
