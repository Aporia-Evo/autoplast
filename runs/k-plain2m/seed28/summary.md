# Search seed 28

task: regime collision3  alphabet: 20 ops, with Recip  readout: fixed o = S q  add-node mutation: on  candidates: 2100084  real evaluations (after cache): 1325653  time: 2257s  pop: 500  tournament: 10

commit: 6c2f60a  task seed: 1  train episodes: 144  persistent registers: 3 matrix, 0 vector, start identity  batch: 128

search: regularized evolution  tune-consts: 0  select: fitness  residual-insert: off

validation level (val > 0.651, T128 K8 val >= 0.838, train - val <= 0.03; checked every 50000 candidates): not reached

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* unclassified: 884 candidates
* decayed linear attention: 1524 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.362): 18676 candidates
- delta rule (beta=1) (acc 0.578): 2086260 candidates
- delta rule (beta=0.5) (acc 0.617): 2086260 candidates
- gated delta (alpha=0.9) (acc 0.519): 626932 candidates

## Best rule

```
S' = ((((0.115·((v - -1.892·k) - (tanh((((P2 - P1))ᵀ·k + k)) + (((P2 - P1))ᵀ·k + k))) + (0.115·((v - -1.892·k) - (tanh((((P2 - P1))ᵀ·k + k)) + (((P2 - P1))ᵀ·k + k))) + (tanh((((P2 - P1))ᵀ·k + k)) + (((P2 - P1))ᵀ·k + k)))))⊗(0.115·((v - -1.892·k) - (tanh((((P2 - P1))ᵀ·k + k)) + (((P2 - P1))ᵀ·k + k)))))ᵀ + ((P2 - P1))ᵀ)
P1' = (0 - (P2 - P1))
P2' = ((0.115·((v - -1.892·k) - (tanh((((P2 - P1))ᵀ·k + k)) + (((P2 - P1))ᵀ·k + k))) + (0.115·((v - -1.892·k) - (tanh((((P2 - P1))ᵀ·k + k)) + (((P2 - P1))ᵀ·k + k))) + (tanh((((P2 - P1))ᵀ·k + k)) + (((P2 - P1))ᵀ·k + k)))))⊗(0.115·((v - -1.892·k) - (tanh((((P2 - P1))ᵀ·k + k)) + (((P2 - P1))ᵀ·k + k))))

Effective program (18 instructions):
  s0 = -1.8922
  M0 = MatSub(M2, M1)
  M1 = MatSub(M3, M0)
  M0 = Transpose(M0)
  V4 = VecScale(s0, V0)
  V1 = VecSub(V1, V4)
  V2 = MatVec(M0, V0)
  V2 = VecAdd(V2, V0)
  s1 = 0.1146
  V5 = Tanh(V2)
  V0 = VecAdd(V5, V2)
  V4 = VecSub(V1, V0)
  V5 = VecScale(s1, V4)
  V3 = VecAdd(V5, V0)
  V1 = VecAdd(V5, V3)
  M2 = Outer(V1, V5)
  M3 = Transpose(M2)
  M0 = MatAdd(M3, M0)

structure: unclassified  [a=0.998 b=0.218 c=-0.416 g=-0.009, erase c/a=0.417, R²=0.9505, 1408 steps]

train acc 0.615 ±0.014
test regime collision3: acc 0.636  margin 0.044  ±0.006
test d16 T12 ow0.3: acc 0.920  margin 0.249  ±0.004
test d16 T12 ow0.0: acc 0.908  margin 0.235  ±0.004
test d16 T12 ow0.6: acc 0.922  margin 0.235  ±0.005
test d32 T24 ow0.3: acc 0.984  margin 0.336  ±0.002
test d8 T6 ow0.3: acc 0.774  margin 0.102  ±0.009
test d16 T64 K8 ow0.3: acc 0.776  margin 0.113  ±0.009
test d16 T128 K8 ow0.3: acc 0.765  margin 0.103  ±0.013
```
