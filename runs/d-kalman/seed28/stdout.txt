# Search seed 28

task: regime collision3  alphabet: 20 ops, with Recip  readout: fixed o = S q  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 949134  time: 1606s  pop: 500  tournament: 10

commit: e979a8e  task seed: 1  train episodes: 144  persistent registers: 3 matrix, 0 vector, start identity  batch: 128

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* unclassified: 884 candidates
* decayed linear attention: 1524 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.362): 18676 candidates
- delta rule (beta=1) (acc 0.578): not reached
- delta rule (beta=0.5) (acc 0.617): not reached
- gated delta (alpha=0.9) (acc 0.519): 626932 candidates

## Best rule

```
S' = ((P2 - P1))ᵀ
P1' = (0 - (P2 - P1))
P2' = ((0.121·((v - -1.971·k) - (tanh((((P2 - P1))ᵀ·k + k)) + (((P2 - P1))ᵀ·k + k))) + (0.121·((v - -1.971·k) - (tanh((((P2 - P1))ᵀ·k + k)) + (((P2 - P1))ᵀ·k + k))) + (norm(tanh((((P2 - P1))ᵀ·k + k))) + tanh((((P2 - P1))ᵀ·k + k))))))⊗(0.121·((v - -1.971·k) - (tanh((((P2 - P1))ᵀ·k + k)) + (((P2 - P1))ᵀ·k + k))))

Effective program (18 instructions):
  s0 = -1.9709
  M0 = MatSub(M2, M1)
  M1 = MatSub(M3, M0)
  M0 = Transpose(M0)
  V4 = VecScale(s0, V0)
  V1 = VecSub(V1, V4)
  V2 = MatVec(M0, V0)
  V2 = VecAdd(V2, V0)
  s1 = 0.1210
  V5 = Tanh(V2)
  V0 = VecAdd(V5, V2)
  V4 = VecSub(V1, V0)
  V1 = Normalize(V5)
  V0 = VecAdd(V1, V5)
  V5 = VecScale(s1, V4)
  V3 = VecAdd(V5, V0)
  V1 = VecAdd(V5, V3)
  M2 = Outer(V1, V5)

structure: unclassified  [a=0.940 b=0.001 c=-0.033 g=-0.010, erase c/a=0.035, R²=0.0010, 1408 steps]

train acc 0.572 ±0.014
test regime collision3: acc 0.578  margin -0.032  ±0.006
test d16 T12 ow0.3: acc 0.823  margin 0.156  ±0.006
test d16 T12 ow0.0: acc 0.845  margin 0.176  ±0.005
test d16 T12 ow0.6: acc 0.766  margin 0.073  ±0.008
test d32 T24 ow0.3: acc 0.930  margin 0.292  ±0.004
test d8 T6 ow0.3: acc 0.629  margin -0.059  ±0.010
test d16 T64 K8 ow0.3: acc 0.700  margin 0.021  ±0.010
test d16 T128 K8 ow0.3: acc 0.665  margin 0.010  ±0.015
```
