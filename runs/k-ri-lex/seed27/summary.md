# Search seed 27

task: regime collision3  alphabet: 20 ops, with Recip  readout: fixed o = S q  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 875383  time: 5979s  pop: 500  tournament: 10

commit: 6c2f60a  task seed: 1  train episodes: 144  persistent registers: 3 matrix, 0 vector, start identity  batch: 128

search: regularized evolution  tune-consts: 0  select: lexicase  residual-insert: on

residual insert: 357742 attempts, 299990 blocks inserted, 315525 times dead instructions removed first

validation level (val > 0.651, T128 K8 val >= 0.838, train - val <= 0.03; checked every 50000 candidates): not reached

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* unclassified: 3828 candidates
* linear, not error-correcting: 6132 candidates
* gated Kronecker delta rule: 6132 candidates
* linear attention: 7540 candidates
* decayed linear attention: 9204 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.362): 7540 candidates
- delta rule (beta=1) (acc 0.578): 60532 candidates
- delta rule (beta=0.5) (acc 0.617): 267380 candidates
- gated delta (alpha=0.9) (acc 0.519): 20980 candidates

## Best rule

```
S' = …
P1' = (((v)⊗((k + -0.058·norm((0 + v)))) + (v)⊗((k + -0.058·norm((0 + v))))))(((S)ᵀ + -0.011·P2))
P2' = -0.203·((((((v)⊗((k + -0.058·norm((0 + v)))) + (v)⊗((k + -0.058·norm((0 + v))))))(((S)ᵀ + -0.011·P2)))ᵀ + (((v)⊗((k + -0.058·norm((0 + v)))) + (v)⊗((k + -0.058·norm((0 + v))))))(((S)ᵀ + -0.011·P2))))((((((S)ᵀ + -0.011·P2))ᵀ + (v)⊗((k + -0.058·norm((0 + v))))) + -0.010·((((S)ᵀ + -0.011·P2))ᵀ + (v)⊗((k + -0.058·norm((0 + v)))))))

Effective program (23 instructions):
  V2 = VecAdd(V3, V1)
  M3 = Transpose(M0)
  s1 = -0.0111
  M2 = MatScale(s1, M2)
  M3 = MatAdd(M3, M2)
  s2 = -0.0105
  M2 = Transpose(M3)
  V2 = Normalize(V2)
  s3 = -0.0581
  V2 = VecScale(s3, V2)
  V0 = VecAdd(V0, V2)
  M0 = Outer(V1, V0)
  M1 = MatAdd(M0, M0)
  M1 = MatMul(M1, M3)
  M0 = MatAdd(M2, M0)
  M3 = MatScale(s2, M0)
  M0 = MatAdd(M0, M3)
  M3 = Transpose(M1)
  M3 = MatAdd(M3, M1)
  s1 = -0.2031
  M2 = MatMul(M3, M0)
  M2 = MatScale(s1, M2)
  M0 = MatAdd(M0, M2)

structure: unclassified  [a=0.989 b=0.742 c=-0.407 g=-0.468, erase c/a=0.412, R²=0.8988, 1408 steps]

train acc 0.645 ±0.014
test regime collision3: acc 0.636  margin 0.049  ±0.006
test d16 T12 ow0.3: acc 0.900  margin 0.246  ±0.004
test d16 T12 ow0.0: acc 0.949  margin 0.264  ±0.003
test d16 T12 ow0.6: acc 0.879  margin 0.218  ±0.006
test d32 T24 ow0.3: acc 0.950  margin 0.330  ±0.003
test d8 T6 ow0.3: acc 0.759  margin 0.099  ±0.009
test d16 T64 K8 ow0.3: acc 0.743  margin 0.103  ±0.010
test d16 T128 K8 ow0.3: acc 0.725  margin 0.092  ±0.014
```
