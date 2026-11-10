# Search seed 6

task: v3  alphabet: 29 ops, with extra ops  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 753890  time: 11263s  pop: 500  tournament: 10

## Milestones (first candidate count where best train acc reached the reference rule)

- linear attention (acc 0.571): 19828 candidates
- delta rule (beta=1) (acc 0.853): 746356 candidates
- delta rule (beta=0.5) (acc 0.901): not reached
- gated delta (alpha=0.9) (acc 0.713): 19828 candidates

## Best rule

```
S' = tanh((tanh(tanh(((tanh(tanh(tanh((S + 0)))) - (S + 0)))((((k + k) + (k ⊙ k)))⊗((k + k))))) + (tanh(((tanh(tanh(tanh((S + 0)))) - (S + 0)))((((k + k) + (k ⊙ k)))⊗((k + k)))) + ((((tanh(tanh(tanh((S + 0)))) - (S + 0)))((tanh(tanh(tanh((S + 0)))) - (S + 0))) + tanh(((v)⊗(k) + (S + 0)))) - (tanh(tanh(tanh((S + 0)))) - (S + 0))))))

Effective program (21 instructions):
  M3 = MatAdd(M0, M1)
  M0 = Outer(V1, V0)
  M1 = MatTanh(M3)
  M0 = MatAdd(M0, M3)
  M1 = MatTanh(M1)
  M2 = MatTanh(M1)
  V4 = Hadamard(V0, V0)
  M3 = MatSub(M2, M3)
  M1 = MatTanh(M0)
  M0 = MatMul(M3, M3)
  M1 = MatAdd(M0, M1)
  V3 = VecAdd(V0, V0)
  M1 = MatSub(M1, M3)
  V0 = VecAdd(V3, V4)
  M0 = Outer(V0, V3)
  M3 = MatMul(M3, M0)
  M2 = MatTanh(M3)
  M0 = MatAdd(M2, M1)
  M3 = MatTanh(M2)
  M1 = MatAdd(M3, M0)
  M0 = MatTanh(M1)

train acc 0.893
test d16 T12 ow0.3: acc 0.909  margin 0.238
test d16 T12 ow0.0: acc 0.909  margin 0.230
test d16 T12 ow0.6: acc 0.903  margin 0.218
test d32 T24 ow0.3: acc 0.950  margin 0.291
test d8 T6 ow0.3: acc 0.752  margin 0.084
test d16 T64 K8 ow0.3: acc 0.787  margin 0.144
test d16 T128 K8 ow0.3: acc 0.737  margin 0.103
```
