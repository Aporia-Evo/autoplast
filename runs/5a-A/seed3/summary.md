# Search seed 3

task: regime collision3  alphabet: 19 ops  readout: fixed o = S q  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 644002  time: 900s  pop: 500  tournament: 10

## Milestones (first candidate count where best train acc reached the reference rule)

- linear attention (acc 0.362): 9972 candidates
- delta rule (beta=1) (acc 0.578): not reached
- delta rule (beta=0.5) (acc 0.617): not reached
- gated delta (alpha=0.9) (acc 0.519): not reached

## Best rule

```
S' = ((tanh(1.009·<tanh(k), tanh(k)>·v))⊗(tanh(k)) - σ((<tanh(k), tanh(k)> + <tanh(k), tanh(k)>))·(0 - S))

Effective program (12 instructions):
  M0 = MatSub(M3, M0)
  V3 = Tanh(V0)
  s2 = Dot(V3, V3)
  s0 = SAdd(s2, s2)
  s0 = Sigmoid(s0)
  M1 = MatScale(s0, M0)
  V2 = VecScale(s2, V1)
  s1 = 1.0094
  V4 = VecScale(s1, V2)
  V5 = Tanh(V4)
  M0 = Outer(V5, V3)
  M0 = MatSub(M0, M1)

train acc 0.512
test regime collision3: acc 0.511  margin -0.052
test d16 T12 ow0.3: acc 0.712  margin 0.114
test d16 T12 ow0.0: acc 0.680  margin 0.085
test d16 T12 ow0.6: acc 0.730  margin 0.114
test d32 T24 ow0.3: acc 0.614  margin 0.081
test d8 T6 ow0.3: acc 0.637  margin 0.029
test d16 T64 K8 ow0.3: acc 0.582  margin -0.017
test d16 T128 K8 ow0.3: acc 0.545  margin -0.038
```
