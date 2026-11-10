# Search seed 9

task: regime collision3  alphabet: 19 ops  readout: evolved  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 140558  time: 228s  pop: 500  tournament: 10

## Milestones (first candidate count where best train acc reached the reference rule)

- linear attention (acc 0.362): 25460 candidates
- delta rule (beta=1) (acc 0.578): not reached
- delta rule (beta=0.5) (acc 0.617): not reached
- gated delta (alpha=0.9) (acc 0.519): not reached

## Best rule

```
S' = (0.876·S + (v)⊗(k))
o = S·q

Effective program (4 instructions):
  M2 = Outer(V1, V0)
  s1 = 0.8763
  M0 = MatScale(s1, M0)
  M0 = MatAdd(M0, M2)

train acc 0.506
test regime collision3: acc 0.517  margin -0.042
test d16 T12 ow0.3: acc 0.734  margin 0.127
test d16 T12 ow0.0: acc 0.718  margin 0.113
test d16 T12 ow0.6: acc 0.727  margin 0.112
test d32 T24 ow0.3: acc 0.636  margin 0.097
test d8 T6 ow0.3: acc 0.645  margin 0.036
test d16 T64 K8 ow0.3: acc 0.582  margin -0.009
test d16 T128 K8 ow0.3: acc 0.561  margin -0.028
```
