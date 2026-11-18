# Search seed 19

task: regime collision3  alphabet: 20 ops, with Recip  readout: fixed o = S q  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 878838  time: 3062s  pop: 500  tournament: 10

commit: 50c2d10  task seed: 1  train episodes: 144  persistent registers: 3 matrix, 0 vector, start identity  batch: 128

search: regularized evolution  tune-consts: 0  select: lexicase

validation level (val > 0.651, T128 K8 val >= 0.838, train - val <= 0.03; checked every 50000 candidates): not reached

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* unclassified: 1780 candidates
* linear attention: 3188 candidates
* decayed linear attention: 5492 candidates
* delta + Kronecker mix: 61684 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.362): 3188 candidates
- delta rule (beta=1) (acc 0.578): 54644 candidates
- delta rule (beta=0.5) (acc 0.617): 61684 candidates
- gated delta (alpha=0.9) (acc 0.519): 53876 candidates

## Best rule

```
S' = (((P2 + P1) + S) + (((0 - ((P2 + P1) + S)·k) + tanh(tanh(v))))⊗(σ(0.074)·norm((tanh(tanh(v)) + ((((P2 + P1) + S)·k + k) + (((P2 + P1) + S)·k + k))))))
P1' = (0)⊗(0)
P2' = ((((0 - ((P2 + P1) + S)·k) + tanh(tanh(v))))⊗(σ(0.074)·norm((tanh(tanh(v)) + ((((P2 + P1) + S)·k + k) + (((P2 + P1) + S)·k + k))))))(((((P2 + P1) + S) + (((0 - ((P2 + P1) + S)·k) + tanh(tanh(v))))⊗(σ(0.074)·norm((tanh(tanh(v)) + ((((P2 + P1) + S)·k + k) + (((P2 + P1) + S)·k + k)))))) - σ(0.074)·(P2 + P1)))

Effective program (20 instructions):
  s3 = 0.0742
  M2 = MatAdd(M2, M1)
  M0 = MatAdd(M2, M0)
  M1 = Outer(V2, V5)
  V4 = MatVec(M0, V0)
  s1 = Sigmoid(s3)
  V3 = VecSub(V2, V4)
  V4 = VecAdd(V4, V0)
  V0 = VecAdd(V4, V4)
  M2 = MatScale(s1, M2)
  V2 = Tanh(V1)
  V4 = Tanh(V2)
  V1 = VecAdd(V3, V4)
  V0 = VecAdd(V4, V0)
  V3 = Normalize(V0)
  V2 = VecScale(s1, V3)
  M3 = Outer(V1, V2)
  M0 = MatAdd(M0, M3)
  M2 = MatSub(M0, M2)
  M2 = MatMul(M3, M2)

structure: unclassified  [a=0.991 b=0.392 c=-0.459 g=-0.024, erase c/a=0.463, R²=0.1070, 1408 steps]

train acc 0.699 ±0.013
test regime collision3: acc 0.683  margin 0.085  ±0.006
test d16 T12 ow0.3: acc 0.793  margin 0.183  ±0.006
test d16 T12 ow0.0: acc 0.779  margin 0.153  ±0.005
test d16 T12 ow0.6: acc 0.789  margin 0.169  ±0.008
test d32 T24 ow0.3: acc 0.890  margin 0.290  ±0.005
test d8 T6 ow0.3: acc 0.600  margin -0.009  ±0.010
test d16 T64 K8 ow0.3: acc 0.721  margin 0.090  ±0.010
test d16 T128 K8 ow0.3: acc 0.694  margin 0.082  ±0.014
```
