# Search seed 17

task: regime collision3  alphabet: 20 ops, with Recip  readout: fixed o = S q  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 750627  time: 2050s  pop: 500  tournament: 10

commit: e979a8e  task seed: 1  train episodes: 144  persistent registers: 3 matrix, 0 vector, start identity  batch: 128

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* decayed linear attention: 884 candidates
* unclassified: 4084 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.362): 7412 candidates
- delta rule (beta=1) (acc 0.578): 822004 candidates
- delta rule (beta=0.5) (acc 0.617): 879988 candidates
- gated delta (alpha=0.9) (acc 0.519): 70644 candidates

## Best rule

```
S' = ((P1 - P2) + (tanh(v))⊗(tanh(norm(tanh(tanh(k))))))
P1' = (|tanh(norm(tanh(tanh(k))))|·(tanh(v))⊗(tanh(norm(tanh(tanh(k))))) + (P1 - P2))
P2' = ((P1 - P2)·|tanh(norm(tanh(tanh(k))))|·tanh(tanh(k)))⊗(tanh(tanh(|tanh(norm(tanh(tanh(k))))|·tanh(tanh(k)))))

Effective program (16 instructions):
  M2 = MatSub(M1, M2)
  V0 = Tanh(V0)
  V4 = Tanh(V0)
  V1 = Tanh(V1)
  V5 = Normalize(V4)
  V5 = Tanh(V5)
  M1 = Outer(V1, V5)
  s1 = Norm(V5)
  M0 = MatAdd(M2, M1)
  M3 = MatScale(s1, M1)
  M1 = MatAdd(M3, M2)
  V4 = VecScale(s1, V4)
  V2 = MatVec(M2, V4)
  V4 = Tanh(V4)
  V4 = Tanh(V4)
  M2 = Outer(V2, V4)

structure: unclassified  [a=0.909 b=0.902 c=-0.043 g=0.002, erase c/a=0.047, R²=0.7566, 1408 steps]

train acc 0.623 ±0.014
test regime collision3: acc 0.634  margin 0.024  ±0.006
test d16 T12 ow0.3: acc 0.903  margin 0.253  ±0.004
test d16 T12 ow0.0: acc 0.865  margin 0.217  ±0.004
test d16 T12 ow0.6: acc 0.905  margin 0.255  ±0.006
test d32 T24 ow0.3: acc 0.969  margin 0.352  ±0.003
test d8 T6 ow0.3: acc 0.739  margin 0.088  ±0.009
test d16 T64 K8 ow0.3: acc 0.817  margin 0.179  ±0.009
test d16 T128 K8 ow0.3: acc 0.818  margin 0.173  ±0.012
```
