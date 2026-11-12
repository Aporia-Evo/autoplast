# Search seed 12

task: regime collision3  alphabet: 20 ops, with Recip  readout: fixed o = S q  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 1007543  time: 2084s  pop: 500  tournament: 10

commit: e979a8e  task seed: 1  train episodes: 144  persistent registers: 3 matrix, 0 vector, start identity  batch: 128

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* unclassified: 3572 candidates
* decayed linear attention: 4212 candidates
* gated delta rule: 9076 candidates
* delta + Kronecker mix: 14964 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.362): 9460 candidates
- delta rule (beta=1) (acc 0.578): 11636 candidates
- delta rule (beta=0.5) (acc 0.617): 14964 candidates
- gated delta (alpha=0.9) (acc 0.519): 11636 candidates

## Best rule

```
S' = ((P2)(S) - ((norm((<norm(S·k), ((S·k - tanh(v)) + S·k)> + <S·k, k>)·tanh(tanh((norm(tanh(((tanh(v) - (S·k - tanh(v))) + S·k))) - norm(S·k))))) - (tanh(v) - (S·k - tanh(v)))))⊗(k))
P1' = (P2)(S)

Effective program (21 instructions):
  M1 = MatMul(M2, M0)
  V4 = MatVec(M0, V0)
  V1 = Tanh(V1)
  V5 = VecSub(V4, V1)
  V1 = VecSub(V1, V5)
  V3 = Normalize(V4)
  V2 = VecAdd(V5, V4)
  s2 = Dot(V4, V0)
  s3 = Dot(V3, V2)
  V2 = VecAdd(V1, V4)
  s3 = SAdd(s3, s2)
  V5 = Tanh(V2)
  V2 = Normalize(V5)
  V2 = VecSub(V2, V3)
  V2 = Tanh(V2)
  V3 = Tanh(V2)
  V4 = VecScale(s3, V3)
  V3 = Normalize(V4)
  V1 = VecSub(V3, V1)
  M0 = Outer(V1, V0)
  M0 = MatSub(M1, M0)

structure: unclassified  [a=1.000 b=1.232 c=-0.472 g=-0.252, erase c/a=0.472, R²=0.9560, 1408 steps]

train acc 0.648 ±0.014
test regime collision3: acc 0.653  margin 0.041  ±0.006
test d16 T12 ow0.3: acc 0.931  margin 0.225  ±0.004
test d16 T12 ow0.0: acc 0.913  margin 0.208  ±0.004
test d16 T12 ow0.6: acc 0.939  margin 0.227  ±0.005
test d32 T24 ow0.3: acc 0.991  margin 0.320  ±0.001
test d8 T6 ow0.3: acc 0.728  margin 0.074  ±0.009
test d16 T64 K8 ow0.3: acc 0.827  margin 0.149  ±0.008
test d16 T128 K8 ow0.3: acc 0.819  margin 0.144  ±0.012
```
