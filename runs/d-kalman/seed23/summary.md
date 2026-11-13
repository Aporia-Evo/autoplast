# Search seed 23

task: regime collision3  alphabet: 20 ops, with Recip  readout: fixed o = S q  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 479361  time: 883s  pop: 500  tournament: 10

commit: e979a8e  task seed: 1  train episodes: 144  persistent registers: 3 matrix, 0 vector, start identity  batch: 128

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* decayed linear attention: 1396 candidates
* unclassified: 6132 candidates
* linear attention: 7924 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.362): 7924 candidates
- delta rule (beta=1) (acc 0.578): not reached
- delta rule (beta=0.5) (acc 0.617): not reached
- gated delta (alpha=0.9) (acc 0.519): not reached

## Best rule

```
S' = ((v)⊗(tanh(tanh(k))) - (0.563·(S + S) - (S + S)))
P1' = (S + S)
P2' = 0.563·(S + S)

Effective program (8 instructions):
  V3 = Tanh(V0)
  M1 = MatAdd(M0, M0)
  V2 = Tanh(V3)
  s3 = 0.5629
  M2 = MatScale(s3, M1)
  M0 = Outer(V1, V2)
  M3 = MatSub(M2, M1)
  M0 = MatSub(M0, M3)

structure: decayed linear attention  [a=0.874 b=0.901 c=-0.000 g=0.002, erase c/a=0.000, R²=0.9955, 1408 steps]

train acc 0.509 ±0.014
test regime collision3: acc 0.516  margin -0.043  ±0.006
test d16 T12 ow0.3: acc 0.734  margin 0.126  ±0.007
test d16 T12 ow0.0: acc 0.712  margin 0.108  ±0.006
test d16 T12 ow0.6: acc 0.728  margin 0.112  ±0.008
test d32 T24 ow0.3: acc 0.629  margin 0.092  ±0.007
test d8 T6 ow0.3: acc 0.641  margin 0.033  ±0.010
test d16 T64 K8 ow0.3: acc 0.583  margin -0.010  ±0.011
test d16 T128 K8 ow0.3: acc 0.550  margin -0.030  ±0.016
```
