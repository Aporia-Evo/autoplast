# Search seed 22

task: regime collision3  alphabet: 20 ops, with Recip  readout: fixed o = S q  add-node mutation: on  candidates: 1500076  real evaluations (after cache): 1176305  time: 3784s  pop: 500  tournament: 10

commit: ad31161  task seed: 1  train episodes: 144  persistent registers: 3 matrix, 0 vector, start identity  batch: 128

search: regularized evolution  tune-consts: 8  select: fitness

validation level (val > 0.651, T128 K8 val >= 0.838, train - val <= 0.03; checked every 50000 candidates): not reached

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* unclassified: 4852 candidates
* decayed linear attention: 6260 candidates
* linear attention: 17460 candidates
* delta rule: 542364 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.362): 17460 candidates
- delta rule (beta=1) (acc 0.578): 528460 candidates
- delta rule (beta=0.5) (acc 0.617): 542996 candidates
- gated delta (alpha=0.9) (acc 0.519): 51364 candidates

## Best rule

```
S' = (((v)⊗(((k + P1·k) + (k + P1·k))) - (P2)((tanh(tanh(k)))⊗(norm(tanh(tanh(k)))))) + (S + ((v)⊗(((k + P1·k) + (k + P1·k))) - (P2)((tanh(tanh(k)))⊗(norm(tanh(tanh(k))))))))
P1' = -0.150·(P2)((tanh(tanh(k)))⊗(norm(tanh(tanh(k)))))
P2' = 0.275·(S + ((v)⊗(((k + P1·k) + (k + P1·k))) - (P2)((tanh(tanh(k)))⊗(norm(tanh(tanh(k)))))))

Effective program (16 instructions):
  s3 = 0.2754
  s0 = -0.1505
  V4 = Tanh(V0)
  V5 = MatVec(M1, V0)
  V0 = VecAdd(V0, V5)
  V4 = Tanh(V4)
  V5 = Normalize(V4)
  M1 = Outer(V4, V5)
  M2 = MatMul(M2, M1)
  V0 = VecAdd(V0, V0)
  M3 = Outer(V1, V0)
  M3 = MatSub(M3, M2)
  M0 = MatAdd(M0, M3)
  M1 = MatScale(s0, M2)
  M2 = MatScale(s3, M0)
  M0 = MatAdd(M3, M0)

structure: unclassified  [a=1.000 b=4.133 c=-0.457 g=0.002, erase c/a=0.457, R²=0.9544, 1408 steps]

train acc 0.633 ±0.014
test regime collision3: acc 0.640  margin 0.041  ±0.006
test d16 T12 ow0.3: acc 0.900  margin 0.241  ±0.004
test d16 T12 ow0.0: acc 0.907  margin 0.237  ±0.004
test d16 T12 ow0.6: acc 0.910  margin 0.230  ±0.005
test d32 T24 ow0.3: acc 0.972  margin 0.340  ±0.003
test d8 T6 ow0.3: acc 0.731  margin 0.080  ±0.009
test d16 T64 K8 ow0.3: acc 0.819  margin 0.143  ±0.009
test d16 T128 K8 ow0.3: acc 0.802  margin 0.137  ±0.012
```
