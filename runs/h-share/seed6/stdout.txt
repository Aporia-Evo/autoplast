# Search seed 6

task: v2  alphabet: 19 ops  readout: fixed o = S q  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 920264  time: 1175s  pop: 500  tournament: 10

commit: ad31161  task seed: 1  train episodes: 96  persistent registers: 1 matrix, 0 vector, start zero  batch: 128

search: regularized evolution  tune-consts: 0  select: share (radius 0.05)

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* decayed linear attention: 1012 candidates
* linear, not error-correcting: 1268 candidates
* unclassified: 3444 candidates
* linear attention: 22260 candidates
* delta rule: 44916 candidates
* gated delta rule: 62836 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.772): 22260 candidates
- delta rule (beta=1) (acc 0.858): 60916 candidates
- delta rule (beta=0.5) (acc 0.932): 61812 candidates
- gated delta (alpha=0.9) (acc 0.729): 22260 candidates

## Best rule

```
S' = ((0 + (0 + -2.209))·0·(k)⊗(norm(k)) - (((S + ((v + 0))⊗(k)) + -2.209·(S + ((v + 0))⊗(k))) + (S)((k)⊗(norm(k)))))

Effective program (15 instructions):
  s1 = -2.2093
  V4 = VecAdd(V1, V5)
  M3 = Outer(V4, V0)
  V4 = Normalize(V0)
  M1 = MatAdd(M0, M3)
  M2 = Outer(V0, V4)
  M3 = MatMul(M0, M2)
  s2 = SAdd(s0, s1)
  M0 = MatScale(s1, M1)
  s1 = SAdd(s0, s2)
  M2 = MatScale(s0, M2)
  M0 = MatAdd(M1, M0)
  M0 = MatAdd(M0, M3)
  M1 = MatScale(s1, M2)
  M0 = MatSub(M1, M0)

structure: gated delta rule  [a=1.209 b=1.209 c=-1.000 g=-0.000, erase c/a=0.827, R²=1.0000, 384 steps]

train acc 0.954 ±0.007
test d16 T12 ow0.3: acc 0.950  margin 0.301  ±0.003
test d16 T12 ow0.0: acc 0.934  margin 0.269  ±0.003
test d16 T12 ow0.6: acc 0.942  margin 0.300  ±0.004
test d32 T24 ow0.3: acc 0.680  margin 0.120  ±0.007
test d8 T6 ow0.3: acc 0.854  margin 0.153  ±0.007
test d16 T64 K8 ow0.3: acc 0.000  margin 0.000  ±0.000
test d16 T128 K8 ow0.3: acc 0.000  margin 0.000  ±0.000
```
