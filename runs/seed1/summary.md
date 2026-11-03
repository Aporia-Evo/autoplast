# Search seed 1

candidates: 1500020  real evaluations (after cache): 331720  time: 611s  pop: 500  tournament: 10

## Milestones (first candidate count where best train acc reached the reference rule)

- linear attention (acc 0.772): 11444 candidates
- delta rule (beta=1) (acc 0.858): 1028212 candidates
- delta rule (beta=0.5) (acc 0.932): not reached
- gated delta (alpha=0.9) (acc 0.729): 11444 candidates

## Best rule

```
S' = (S + σ(<S·tanh((k + tanh(k))), S·tanh((k + tanh(k)))>·<S·tanh((k + tanh(k))), S·tanh((k + tanh(k)))>)·(v)⊗(k))

Effective program (10 instructions):
  V4 = Tanh(V0)
  V2 = VecAdd(V0, V4)
  V2 = Tanh(V2)
  V4 = MatVec(M0, V2)
  M1 = Outer(V1, V0)
  s0 = Dot(V4, V4)
  s1 = SMul(s0, s0)
  s1 = Sigmoid(s1)
  M1 = MatScale(s1, M1)
  M0 = MatAdd(M0, M1)

train acc 0.853
test d16 T12 ow0.3: acc 0.832  margin 0.151
test d16 T12 ow0.0: acc 0.919  margin 0.201
test d16 T12 ow0.6: acc 0.689  margin 0.067
test d32 T24 ow0.3: acc 0.932  margin 0.225
test d8 T6 ow0.3: acc 0.639  margin 0.040
```
