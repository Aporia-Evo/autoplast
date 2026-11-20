# Search seed 30

task: regime collision3  alphabet: 20 ops, with Recip  readout: fixed o = S q  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 890579  time: 2646s  pop: 500  tournament: 10

commit: 6c2f60a  task seed: 1  train episodes: 144  persistent registers: 3 matrix, 0 vector, start identity  batch: 128

search: regularized evolution  tune-consts: 0  select: lexicase  residual-insert: on

residual insert: 357187 attempts, 270864 blocks inserted, 295082 times dead instructions removed first

validation level (val > 0.651, T128 K8 val >= 0.838, train - val <= 0.03; checked every 50000 candidates): 250100 candidates

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* unclassified: 3444 candidates
* decayed linear attention: 3444 candidates
* linear attention: 4852 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.362): 4852 candidates
- delta rule (beta=1) (acc 0.578): 118260 candidates
- delta rule (beta=0.5) (acc 0.617): 118772 candidates
- gated delta (alpha=0.9) (acc 0.519): 34036 candidates

## Best rule

```
S' = ((S + (0.908·((((v + v) + -0.068·(0 + k)) + -0.246·(P1 + S)·k))⊗(norm(tanh(k))) + (σ(-0.246)·P1 + 0.908·((((v + v) + -0.068·(0 + k)) + -0.246·(P1 + S)·k))⊗(norm(tanh(k)))))) + ((σ(-0.246)·P1 + 0.908·((((v + v) + -0.068·(0 + k)) + -0.246·(P1 + S)·k))⊗(norm(tanh(k)))))(σ(-0.246)·P1))
P1' = (σ(-0.246)·P1 + (σ(-0.246)·P1 + 0.908·((((v + v) + -0.068·(0 + k)) + -0.246·(P1 + S)·k))⊗(norm(tanh(k)))))
P2' = (σ(-0.246)·P1 + 0.908·((((v + v) + -0.068·(0 + k)) + -0.246·(P1 + S)·k))⊗(norm(tanh(k))))

Effective program (23 instructions):
  V2 = VecAdd(V1, V1)
  M3 = MatAdd(M1, M0)
  V1 = MatVec(M3, V0)
  V4 = VecAdd(V3, V0)
  s1 = -0.0683
  V4 = VecScale(s1, V4)
  V2 = VecAdd(V2, V4)
  s2 = -0.2459
  V1 = VecScale(s2, V1)
  V2 = VecAdd(V2, V1)
  s0 = Sigmoid(s2)
  V3 = Tanh(V0)
  V5 = Normalize(V3)
  s1 = 0.9077
  M2 = Outer(V2, V5)
  M3 = MatScale(s1, M2)
  M1 = MatScale(s0, M1)
  M2 = MatAdd(M1, M3)
  M3 = MatAdd(M3, M2)
  M0 = MatAdd(M0, M3)
  M3 = MatMul(M2, M1)
  M0 = MatAdd(M0, M3)
  M1 = MatAdd(M1, M2)

structure: unclassified  [a=1.032 b=3.696 c=-0.475 g=0.000, erase c/a=0.461, R²=0.8744, 1408 steps]

train acc 0.686 ±0.013
test regime collision3: acc 0.681  margin 0.079  ±0.006
test d16 T12 ow0.3: acc 0.947  margin 0.270  ±0.003
test d16 T12 ow0.0: acc 0.940  margin 0.256  ±0.003
test d16 T12 ow0.6: acc 0.916  margin 0.239  ±0.005
test d32 T24 ow0.3: acc 0.983  margin 0.358  ±0.002
test d8 T6 ow0.3: acc 0.817  margin 0.124  ±0.008
test d16 T64 K8 ow0.3: acc 0.797  margin 0.146  ±0.009
test d16 T128 K8 ow0.3: acc 0.814  margin 0.150  ±0.012
```
