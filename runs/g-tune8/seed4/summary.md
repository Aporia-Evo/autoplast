# Search seed 4

task: regime collision3  alphabet: 20 ops, with Recip  readout: fixed o = S q  add-node mutation: on  candidates: 1500220  real evaluations (after cache): 1094062  time: 2992s  pop: 500  tournament: 10

commit: ad31161  task seed: 1  train episodes: 144  persistent registers: 3 matrix, 0 vector, start identity  batch: 128

search: regularized evolution  tune-consts: 8  select: fitness

validation level (val > 0.651, T128 K8 val >= 0.838, train - val <= 0.03; checked every 50000 candidates): 1000100 candidates

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* unclassified: 3828 candidates
* decayed linear attention: 4468 candidates
* linear attention: 13596 candidates
* delta rule: 880668 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.362): 13596 candidates
- delta rule (beta=1) (acc 0.578): 881180 candidates
- delta rule (beta=0.5) (acc 0.617): 882756 candidates
- gated delta (alpha=0.9) (acc 0.519): 75932 candidates

## Best rule

```
S' = ((0 - P1) + ((S + (P1 - P2)) + ((v - (S + (P1 - P2))·k))⊗(1/(1.171)·k)))
P1' = (norm(((S + (P1 - P2)) + ((v - (S + (P1 - P2))·k))⊗(1/(1.171)·k))·1/(1.171)·k))⊗(1/(1.171)·k)
P2' = (((0 - P1) + (0 - P1)) - (1/(1.171) + 1/(1.171))·(norm(((S + (P1 - P2)) + ((v - (S + (P1 - P2))·k))⊗(1/(1.171)·k))·1/(1.171)·k))⊗(1/(1.171)·k))

Effective program (18 instructions):
  M2 = MatSub(M1, M2)
  M0 = MatAdd(M0, M2)
  s1 = 1.1705
  V2 = MatVec(M0, V0)
  s2 = Recip(s1)
  V0 = VecScale(s2, V0)
  V4 = VecSub(V1, V2)
  M2 = Outer(V4, V0)
  M0 = MatAdd(M0, M2)
  V5 = MatVec(M0, V0)
  M3 = MatSub(M3, M1)
  M0 = MatAdd(M3, M0)
  M3 = MatAdd(M3, M3)
  s1 = SAdd(s2, s2)
  V2 = Normalize(V5)
  M1 = Outer(V2, V0)
  M2 = MatScale(s1, M1)
  M2 = MatSub(M3, M2)

structure: unclassified  [a=1.037 b=0.852 c=-0.893 g=-0.002, erase c/a=0.862, R²=0.5473, 1408 steps]

train acc 0.691 ±0.013
test regime collision3: acc 0.697  margin 0.086  ±0.006
test d16 T12 ow0.3: acc 0.936  margin 0.255  ±0.004
test d16 T12 ow0.0: acc 0.940  margin 0.250  ±0.003
test d16 T12 ow0.6: acc 0.928  margin 0.233  ±0.005
test d32 T24 ow0.3: acc 0.981  margin 0.332  ±0.002
test d8 T6 ow0.3: acc 0.802  margin 0.119  ±0.008
test d16 T64 K8 ow0.3: acc 0.805  margin 0.121  ±0.009
test d16 T128 K8 ow0.3: acc 0.791  margin 0.119  ±0.013
```
