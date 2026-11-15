# Search seed 9

task: regime collision3  alphabet: 20 ops, with Recip  readout: fixed o = S q  add-node mutation: on  candidates: 1500164  real evaluations (after cache): 1126434  time: 2473s  pop: 500  tournament: 10

commit: ad31161  task seed: 1  train episodes: 144  persistent registers: 3 matrix, 0 vector, start identity  batch: 128

search: regularized evolution  tune-consts: 8  select: fitness

validation level (val > 0.651, T128 K8 val >= 0.838, train - val <= 0.03; checked every 50000 candidates): 1000172 candidates

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* unclassified: 3708 candidates
* decayed linear attention: 19956 candidates
* linear attention: 21468 candidates
* delta rule: 347412 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.362): 21468 candidates
- delta rule (beta=1) (acc 0.578): 347804 candidates
- delta rule (beta=0.5) (acc 0.617): 354220 candidates
- gated delta (alpha=0.9) (acc 0.519): 344988 candidates

## Best rule

```
S' = (σ(σ(0)·σ(0)·σ(σ(0)·σ(0)))·((v)⊗(((k + k) + (k + k))) + σ(σ(0)·σ(0))·σ(0)·P1) - ((σ(σ(0)·σ(0))·σ(0)·P1 - (P1 + S)) + (3.382·(P1 + S)·k)⊗(σ(0)·σ(0)·k)))
P1' = (σ(0)·P1 + ((v)⊗(((k + k) + (k + k))) + σ(σ(0)·σ(0))·σ(0)·P1))
P2' = ((σ(σ(0)·σ(0))·σ(0)·P1 - (P1 + S)) + (3.382·(P1 + S)·k)⊗(σ(0)·σ(0)·k))

Effective program (22 instructions):
  s2 = 3.3819
  M2 = MatAdd(M1, M0)
  s1 = Sigmoid(s0)
  s3 = SMul(s1, s1)
  V4 = VecScale(s3, V0)
  V5 = VecAdd(V0, V0)
  V3 = VecAdd(V5, V5)
  M0 = Outer(V1, V3)
  M3 = MatScale(s1, M1)
  V0 = MatVec(M2, V0)
  s0 = Sigmoid(s3)
  M1 = MatScale(s0, M3)
  M2 = MatSub(M1, M2)
  M0 = MatAdd(M0, M1)
  M1 = MatAdd(M3, M0)
  V3 = VecScale(s2, V0)
  s2 = SMul(s3, s0)
  s1 = Sigmoid(s2)
  M3 = Outer(V3, V4)
  M2 = MatAdd(M2, M3)
  M3 = MatScale(s1, M0)
  M0 = MatSub(M3, M2)

structure: unclassified  [a=1.067 b=2.141 c=-0.909 g=-0.000, erase c/a=0.852, R²=0.8169, 1408 steps]

train acc 0.729 ±0.013
test regime collision3: acc 0.713  margin 0.108  ±0.006
test d16 T12 ow0.3: acc 0.950  margin 0.279  ±0.003
test d16 T12 ow0.0: acc 0.944  margin 0.267  ±0.003
test d16 T12 ow0.6: acc 0.929  margin 0.252  ±0.005
test d32 T24 ow0.3: acc 0.980  margin 0.369  ±0.002
test d8 T6 ow0.3: acc 0.839  margin 0.138  ±0.008
test d16 T64 K8 ow0.3: acc 0.832  margin 0.169  ±0.008
test d16 T128 K8 ow0.3: acc 0.845  margin 0.172  ±0.011
```
