# Search seed 13

task: v3  alphabet: 29 ops, with extra ops  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 582674  time: 6394s  pop: 500  tournament: 10

## Milestones (first candidate count where best train acc reached the reference rule)

- linear attention (acc 0.571): 31092 candidates
- delta rule (beta=1) (acc 0.853): not reached
- delta rule (beta=0.5) (acc 0.901): not reached
- gated delta (alpha=0.9) (acc 0.713): 33524 candidates

## Best rule

```
S' = (tanh(tanh(tanh(((v)⊗(k) + tanh(tanh(tanh(S))))))) + ((tanh(tanh(tanh(((v)⊗(k) + tanh(tanh(tanh(S))))))) - tanh(tanh(tanh(S)))) ⊙ tanh(tanh(tanh(((v)⊗(k) + tanh(tanh(tanh(S)))))))))

Effective program (11 instructions):
  M1 = Outer(V1, V0)
  M0 = MatTanh(M0)
  M3 = MatTanh(M0)
  M3 = MatTanh(M3)
  M0 = MatAdd(M1, M3)
  M1 = MatTanh(M0)
  M1 = MatTanh(M1)
  M0 = MatTanh(M1)
  M3 = MatSub(M0, M3)
  M3 = MatHadamard(M3, M0)
  M0 = MatAdd(M0, M3)

train acc 0.730
test d16 T12 ow0.3: acc 0.786  margin 0.147
test d16 T12 ow0.0: acc 0.820  margin 0.163
test d16 T12 ow0.6: acc 0.710  margin 0.099
test d32 T24 ow0.3: acc 0.878  margin 0.225
test d8 T6 ow0.3: acc 0.619  margin 0.022
test d16 T64 K8 ow0.3: acc 0.566  margin -0.006
test d16 T128 K8 ow0.3: acc 0.552  margin -0.019
```
