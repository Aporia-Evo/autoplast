# Search seed 7

task: regime collision3  alphabet: 20 ops, with Recip  readout: fixed o = S q  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 768408  time: 1558s  pop: 500  tournament: 10

commit: e979a8e  task seed: 1  train episodes: 144  persistent registers: 3 matrix, 0 vector, start identity  batch: 128

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* unclassified: 756 candidates
* decayed linear attention: 1012 candidates
* linear attention: 18036 candidates
* delta rule: 66292 candidates
* gated delta rule: 66804 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.362): 18036 candidates
- delta rule (beta=1) (acc 0.578): 67060 candidates
- delta rule (beta=0.5) (acc 0.617): 67572 candidates
- gated delta (alpha=0.9) (acc 0.519): 65268 candidates

## Best rule

```
S' = (-0.052·1/(-0.052)·(P2 + S) + (((((v + v) + (v + v)) + ((v + v) + (v + v))) - 0.810·(P2 + S)·norm(k)))⊗(norm(k)))
P1' = (((((v + v) + (v + v)) + ((v + v) + (v + v))) - 0.810·(P2 + S)·norm(k)))⊗(norm(k))
P2' = 0.810·(P2 + ((((v + v) + (v + v)) + ((v + v) + (v + v))))⊗(norm(k)))

Effective program (18 instructions):
  V5 = Normalize(V0)
  s1 = -0.0522
  s2 = Recip(s1)
  s0 = SMul(s1, s2)
  M0 = MatAdd(M2, M0)
  V0 = VecAdd(V1, V1)
  s3 = 0.8098
  M1 = MatScale(s3, M0)
  V4 = VecAdd(V0, V0)
  V0 = VecAdd(V4, V4)
  V3 = MatVec(M1, V5)
  M3 = Outer(V0, V5)
  V1 = VecSub(V0, V3)
  M1 = Outer(V1, V5)
  M0 = MatScale(s0, M0)
  M3 = MatAdd(M2, M3)
  M2 = MatScale(s3, M3)
  M0 = MatAdd(M0, M1)

structure: unclassified  [a=1.071 b=8.007 c=-0.858 g=-0.000, erase c/a=0.801, R²=0.8733, 1408 steps]

train acc 0.726 ±0.013
test regime collision3: acc 0.713  margin 0.109  ±0.006
test d16 T12 ow0.3: acc 0.955  margin 0.285  ±0.003
test d16 T12 ow0.0: acc 0.954  margin 0.276  ±0.003
test d16 T12 ow0.6: acc 0.937  margin 0.255  ±0.005
test d32 T24 ow0.3: acc 0.986  margin 0.372  ±0.002
test d8 T6 ow0.3: acc 0.849  margin 0.143  ±0.007
test d16 T64 K8 ow0.3: acc 0.849  margin 0.167  ±0.008
test d16 T128 K8 ow0.3: acc 0.851  margin 0.168  ±0.011
```
