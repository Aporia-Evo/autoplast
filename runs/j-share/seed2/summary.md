# Search seed 2

task: regime collision3  alphabet: 20 ops, with Recip  readout: fixed o = S q  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 971921  time: 2790s  pop: 500  tournament: 10

commit: 50c2d10  task seed: 1  train episodes: 144  persistent registers: 3 matrix, 0 vector, start identity  batch: 128

search: regularized evolution  tune-consts: 0  select: share (radius 0.05)

validation level (val > 0.651, T128 K8 val >= 0.838, train - val <= 0.03; checked every 50000 candidates): 800116 candidates

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* unclassified: 1268 candidates
* decayed linear attention: 2164 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.362): 7412 candidates
- delta rule (beta=1) (acc 0.578): 78580 candidates
- delta rule (beta=0.5) (acc 0.617): 79604 candidates
- gated delta (alpha=0.9) (acc 0.519): 24180 candidates

## Best rule

```
S' = (P1 + (P2 + ((v - σ(σ(0))·P2·k))⊗(norm(k))))
P1' = (σ(0) + 0)·(((P2 + ((v - σ(σ(0))·P2·k))⊗(norm(k))))(P1) + σ(σ(0))·P2)
P2' = (P2 + ((v - σ(σ(0))·P2·k))⊗(norm(k)))

Effective program (14 instructions):
  V5 = MatVec(M2, V0)
  s3 = Sigmoid(s1)
  s2 = SAdd(s3, s1)
  s1 = Sigmoid(s3)
  V2 = VecScale(s1, V5)
  V1 = VecSub(V1, V2)
  V0 = Normalize(V0)
  M0 = Outer(V1, V0)
  M3 = MatScale(s1, M2)
  M2 = MatAdd(M2, M0)
  M0 = MatAdd(M1, M2)
  M1 = MatMul(M2, M1)
  M3 = MatAdd(M1, M3)
  M1 = MatScale(s2, M3)

structure: unclassified  [a=0.995 b=1.002 c=-0.388 g=0.004, erase c/a=0.390, R²=0.3658, 1408 steps]

train acc 0.651 ±0.014
test regime collision3: acc 0.663  margin 0.056  ±0.006
test d16 T12 ow0.3: acc 0.903  margin 0.223  ±0.004
test d16 T12 ow0.0: acc 0.879  margin 0.202  ±0.004
test d16 T12 ow0.6: acc 0.878  margin 0.201  ±0.006
test d32 T24 ow0.3: acc 0.976  margin 0.326  ±0.002
test d8 T6 ow0.3: acc 0.677  margin 0.057  ±0.010
test d16 T64 K8 ow0.3: acc 0.833  margin 0.157  ±0.008
test d16 T128 K8 ow0.3: acc 0.816  margin 0.155  ±0.012
```
