# Search seed 30

task: regime collision3  alphabet: 20 ops, with Recip  readout: fixed o = S q  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 980800  time: 3677s  pop: 500  tournament: 10

commit: e979a8e  task seed: 1  train episodes: 144  persistent registers: 3 matrix, 0 vector, start identity  batch: 128

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* decayed linear attention: 2164 candidates
* unclassified: 2420 candidates
* linear attention: 5876 candidates
* delta rule: 192628 candidates
* linear, not error-correcting: 193268 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.362): 5876 candidates
- delta rule (beta=1) (acc 0.578): 192628 candidates
- delta rule (beta=0.5) (acc 0.617): 194420 candidates
- gated delta (alpha=0.9) (acc 0.519): 185588 candidates

## Best rule

```
S' = (((v)⊗(k) + S) + σ(0)·<tanh(tanh((k - P2·σ(0)·k))), (k - P2·σ(0)·k)>·|((v)⊗(k) + S)·tanh((k - P2·σ(0)·k))|·(0 - (((v)⊗(k) + S)·tanh((k - P2·σ(0)·k)))⊗(tanh(tanh((k - P2·σ(0)·k))))))
P1' = (|((v)⊗(k) + S)·tanh((k - P2·σ(0)·k))|·(0 - (((v)⊗(k) + S)·tanh((k - P2·σ(0)·k)))⊗(tanh(tanh((k - P2·σ(0)·k))))) - |((v)⊗(k) + S)·tanh((k - P2·σ(0)·k))|·(((k - P2·σ(0)·k) + ((v)⊗(k) + S)·tanh((k - P2·σ(0)·k))))⊗((tanh(tanh((k - P2·σ(0)·k))) - (k - P2·σ(0)·k))))
P2' = …

Effective program (23 instructions):
  s2 = Sigmoid(s2)
  V5 = VecScale(s2, V0)
  V2 = MatVec(M2, V5)
  M2 = Outer(V1, V0)
  M2 = MatAdd(M2, M0)
  V3 = VecSub(V0, V2)
  V0 = Tanh(V3)
  V2 = MatVec(M2, V0)
  V1 = Tanh(V0)
  V5 = VecSub(V1, V3)
  M1 = Outer(V2, V1)
  s0 = Dot(V1, V3)
  s3 = Norm(V2)
  M3 = MatSub(M3, M1)
  M1 = MatScale(s3, M3)
  V3 = VecAdd(V3, V2)
  M0 = MatScale(s0, M1)
  M3 = MatScale(s2, M0)
  M0 = MatAdd(M2, M3)
  M3 = Outer(V3, V5)
  M3 = MatScale(s3, M3)
  M1 = MatSub(M1, M3)
  M2 = MatMul(M1, M1)

structure: unclassified  [a=1.000 b=0.591 c=-0.427 g=-0.325, erase c/a=0.426, R²=0.9705, 1408 steps]

train acc 0.642 ±0.014
test regime collision3: acc 0.642  margin 0.050  ±0.006
test d16 T12 ow0.3: acc 0.916  margin 0.247  ±0.004
test d16 T12 ow0.0: acc 0.929  margin 0.243  ±0.003
test d16 T12 ow0.6: acc 0.917  margin 0.234  ±0.005
test d32 T24 ow0.3: acc 0.980  margin 0.344  ±0.002
test d8 T6 ow0.3: acc 0.740  margin 0.089  ±0.009
test d16 T64 K8 ow0.3: acc 0.808  margin 0.133  ±0.009
test d16 T128 K8 ow0.3: acc 0.800  margin 0.124  ±0.013
```
