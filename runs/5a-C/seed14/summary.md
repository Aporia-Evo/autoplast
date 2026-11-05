# Search seed 14

task: regime collision3  alphabet: 19 ops  readout: evolved  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 285718  time: 1400s  pop: 500  tournament: 10

## Milestones (first candidate count where best train acc reached the reference rule)

- linear attention (acc 0.362): 33652 candidates
- delta rule (beta=1) (acc 0.578): not reached
- delta rule (beta=0.5) (acc 0.617): not reached
- gated delta (alpha=0.9) (acc 0.519): 480628 candidates

## Best rule

```
S' = ((0.907·(S + (v)⊗(k)) - (1.177·((S)((v)⊗(k)))((v)⊗(k)) + ((S)((v)⊗(k)))((v)⊗(k)))) + (1.177·((S)((v)⊗(k)))((v)⊗(k)))(1.177·((S)((v)⊗(k)))((v)⊗(k))))
o = S·q

Effective program (12 instructions):
  M1 = Outer(V1, V0)
  M3 = MatMul(M0, M1)
  s2 = 1.1774
  s1 = 0.9069
  M2 = MatAdd(M0, M1)
  M0 = MatScale(s1, M2)
  M1 = MatMul(M3, M1)
  M3 = MatScale(s2, M1)
  M1 = MatAdd(M3, M1)
  M0 = MatSub(M0, M1)
  M3 = MatMul(M3, M3)
  M0 = MatAdd(M0, M3)

train acc 0.532
test regime collision3: acc 0.537  margin -0.034
test d16 T12 ow0.3: acc 0.765  margin 0.141
test d16 T12 ow0.0: acc 0.751  margin 0.125
test d16 T12 ow0.6: acc 0.762  margin 0.131
test d32 T24 ow0.3: acc 0.730  margin 0.158
test d8 T6 ow0.3: acc 0.627  margin 0.021
test d16 T64 K8 ow0.3: acc 0.624  margin 0.018
test d16 T128 K8 ow0.3: acc 0.584  margin -0.002
```
