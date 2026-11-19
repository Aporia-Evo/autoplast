# Search seed 16

task: regime collision3  alphabet: 20 ops, with Recip  readout: fixed o = S q  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 968482  time: 2944s  pop: 500  tournament: 10

commit: 50c2d10  task seed: 1  train episodes: 144  persistent registers: 3 matrix, 0 vector, start identity  batch: 128

search: regularized evolution  tune-consts: 0  select: share (radius 0.05)

validation level (val > 0.651, T128 K8 val >= 0.838, train - val <= 0.03; checked every 50000 candidates): not reached

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* decayed linear attention: 3188 candidates
* linear attention: 5364 candidates
* unclassified: 50164 candidates
* delta rule: 149876 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.362): 5364 candidates
- delta rule (beta=1) (acc 0.578): 60916 candidates
- delta rule (beta=0.5) (acc 0.617): 149876 candidates
- gated delta (alpha=0.9) (acc 0.519): 51316 candidates

## Best rule

```
S' = ((P2 + ((v + (v - P1·k)))⊗(k)) + (σ((<(k ⊙ (v - P1·k)), (v - P1·k)> + 0))·(P2 + ((v + (v - P1·k)))⊗(k)) + (P2 + ((v + (v - P1·k)))⊗(k))))
P1' = σ((<(k ⊙ (v - P1·k)), (v - P1·k)> + 0))·(P2 + ((v + (v - P1·k)))⊗(k))
P2' = (P2 + ((v + (v - P1·k)))⊗(k))

Effective program (12 instructions):
  V3 = MatVec(M1, V0)
  V3 = VecSub(V1, V3)
  V2 = VecAdd(V1, V3)
  M1 = Outer(V2, V0)
  V2 = Hadamard(V0, V3)
  s1 = Dot(V2, V3)
  M2 = MatAdd(M2, M1)
  s1 = SAdd(s1, s2)
  s1 = Sigmoid(s1)
  M1 = MatScale(s1, M2)
  M0 = MatAdd(M1, M2)
  M0 = MatAdd(M2, M0)

structure: unclassified  [a=1.000 b=5.006 c=-0.502 g=-0.005, erase c/a=0.503, R²=0.9003, 1408 steps]

train acc 0.621 ±0.014
test regime collision3: acc 0.636  margin 0.043  ±0.006
test d16 T12 ow0.3: acc 0.916  margin 0.245  ±0.004
test d16 T12 ow0.0: acc 0.890  margin 0.223  ±0.004
test d16 T12 ow0.6: acc 0.934  margin 0.253  ±0.005
test d32 T24 ow0.3: acc 0.982  margin 0.337  ±0.002
test d8 T6 ow0.3: acc 0.774  margin 0.100  ±0.009
test d16 T64 K8 ow0.3: acc 0.838  margin 0.159  ±0.008
test d16 T128 K8 ow0.3: acc 0.819  margin 0.151  ±0.012
```
