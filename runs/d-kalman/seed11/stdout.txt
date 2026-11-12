# Search seed 11

task: regime collision3  alphabet: 20 ops, with Recip  readout: fixed o = S q  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 672143  time: 1288s  pop: 500  tournament: 10

commit: e979a8e  task seed: 1  train episodes: 144  persistent registers: 3 matrix, 0 vector, start identity  batch: 128

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* decayed linear attention: 4724 candidates
* unclassified: 10356 candidates
* linear attention: 13428 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.362): 13428 candidates
- delta rule (beta=1) (acc 0.578): not reached
- delta rule (beta=0.5) (acc 0.617): not reached
- gated delta (alpha=0.9) (acc 0.519): 158580 candidates

## Best rule

```
S' = (<tanh(k), tanh(k)>·S - (v)⊗(tanh(norm(tanh((P1·(k + k) - tanh(k)))))))
P1' = 0·P1
P2' = (v)⊗(tanh(norm(tanh((P1·(k + k) - tanh(k))))))

Effective program (12 instructions):
  V4 = Tanh(V0)
  V2 = VecAdd(V0, V0)
  V5 = MatVec(M1, V2)
  V5 = VecSub(V5, V4)
  V3 = Tanh(V5)
  V0 = Normalize(V3)
  V2 = Tanh(V0)
  M2 = Outer(V1, V2)
  s3 = Dot(V4, V4)
  M1 = MatScale(s0, M1)
  M0 = MatScale(s3, M0)
  M0 = MatSub(M0, M2)

structure: unclassified  [a=0.894 b=0.884 c=0.001 g=0.022, erase c/a=-0.001, R²=0.8593, 1408 steps]

train acc 0.518 ±0.014
test regime collision3: acc 0.515  margin -0.049  ±0.006
test d16 T12 ow0.3: acc 0.754  margin 0.110  ±0.006
test d16 T12 ow0.0: acc 0.735  margin 0.068  ±0.006
test d16 T12 ow0.6: acc 0.705  margin 0.092  ±0.009
test d32 T24 ow0.3: acc 0.847  margin 0.206  ±0.005
test d8 T6 ow0.3: acc 0.607  margin -0.054  ±0.010
test d16 T64 K8 ow0.3: acc 0.565  margin -0.010  ±0.011
test d16 T128 K8 ow0.3: acc 0.558  margin -0.026  ±0.016
```
