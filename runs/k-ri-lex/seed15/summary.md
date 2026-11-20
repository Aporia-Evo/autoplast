# Search seed 15

task: regime collision3  alphabet: 20 ops, with Recip  readout: fixed o = S q  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 958200  time: 3130s  pop: 500  tournament: 10

commit: 6c2f60a  task seed: 1  train episodes: 144  persistent registers: 3 matrix, 0 vector, start identity  batch: 128

search: regularized evolution  tune-consts: 0  select: lexicase  residual-insert: on

residual insert: 357815 attempts, 246047 blocks inserted, 266008 times dead instructions removed first

validation level (val > 0.651, T128 K8 val >= 0.838, train - val <= 0.03; checked every 50000 candidates): 300020 candidates

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* unclassified: 1140 candidates
* decayed linear attention: 1780 candidates
* gated Kronecker delta rule: 2548 candidates
* linear attention: 3700 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.362): 3700 candidates
- delta rule (beta=1) (acc 0.578): 60660 candidates
- delta rule (beta=0.5) (acc 0.617): 181108 candidates
- gated delta (alpha=0.9) (acc 0.519): 46964 candidates

## Best rule

```
S' = ((-0.426·(-0.426·(P1 - P2) + (S + P2))·k)⊗(k) + ((((S + P2) + (-0.426·(-0.426·(P1 - P2) + (S + P2))·k)⊗(k)) + -0.426·(P1 - P2)) + (v)⊗(k)))
P1' = (0.216 + <k, v>)·(-0.426·(P1 - P2) + -0.015·(((-0.426·(P1 - P2) + (v)⊗(k)) + -0.426·(P1 - P2)) - ((-0.426·(-0.426·(P1 - P2) + (S + P2))·k)⊗(k) + ((((S + P2) + (-0.426·(-0.426·(P1 - P2) + (S + P2))·k)⊗(k)) + -0.426·(P1 - P2)) + (v)⊗(k)))))
P2' = ((-0.426·(P1 - P2) + (v)⊗(k)) + -0.426·(P1 - P2))

Effective program (23 instructions):
  M0 = MatAdd(M0, M2)
  s0 = -0.4264
  M1 = MatSub(M1, M2)
  M1 = MatScale(s0, M1)
  M3 = MatAdd(M1, M0)
  V4 = MatVec(M3, V0)
  V4 = VecScale(s0, V4)
  M3 = Outer(V4, V0)
  s0 = 0.2156
  M0 = MatAdd(M0, M3)
  s3 = Dot(V0, V1)
  s0 = SAdd(s0, s3)
  M0 = MatAdd(M0, M1)
  M2 = Outer(V1, V0)
  M0 = MatAdd(M0, M2)
  M2 = MatAdd(M1, M2)
  M0 = MatAdd(M3, M0)
  M2 = MatAdd(M2, M1)
  M3 = MatSub(M2, M0)
  s3 = -0.0151
  M3 = MatScale(s3, M3)
  M1 = MatAdd(M1, M3)
  M1 = MatScale(s0, M1)

structure: unclassified  [a=1.073 b=1.001 c=-0.907 g=-0.000, erase c/a=0.846, R²=0.7936, 1408 steps]

train acc 0.736 ±0.013
test regime collision3: acc 0.721  margin 0.110  ±0.006
test d16 T12 ow0.3: acc 0.946  margin 0.283  ±0.003
test d16 T12 ow0.0: acc 0.940  margin 0.268  ±0.003
test d16 T12 ow0.6: acc 0.932  margin 0.254  ±0.005
test d32 T24 ow0.3: acc 0.973  margin 0.365  ±0.002
test d8 T6 ow0.3: acc 0.838  margin 0.138  ±0.008
test d16 T64 K8 ow0.3: acc 0.857  margin 0.191  ±0.008
test d16 T128 K8 ow0.3: acc 0.880  margin 0.196  ±0.010
```
