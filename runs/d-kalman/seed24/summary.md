# Search seed 24

task: regime collision3  alphabet: 20 ops, with Recip  readout: fixed o = S q  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 781567  time: 1775s  pop: 500  tournament: 10

commit: e979a8e  task seed: 1  train episodes: 144  persistent registers: 3 matrix, 0 vector, start identity  batch: 128

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* decayed linear attention: 628 candidates
* linear attention: 7796 candidates
* unclassified: 12148 candidates
* gated delta rule: 1092596 candidates
* delta rule: 1093108 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.362): 7796 candidates
- delta rule (beta=1) (acc 0.578): 1093108 candidates
- delta rule (beta=0.5) (acc 0.617): 1099508 candidates
- gated delta (alpha=0.9) (acc 0.519): 225780 candidates

## Best rule

```
S' = ((P2 - (tanh(P2·tanh(tanh(tanh(k)))))⊗(tanh(tanh(tanh(k))))) + σ(2.318)·(tanh(tanh(v)))⊗(norm(((tanh(tanh(v)) ⊙ (tanh(tanh(k)) ⊙ tanh(tanh(k)))) + tanh(tanh(tanh(k)))))))
P1' = σ(2.318)·(tanh(tanh(v)))⊗(norm(((tanh(tanh(v)) ⊙ (tanh(tanh(k)) ⊙ tanh(tanh(k)))) + tanh(tanh(tanh(k))))))
P2' = (σ(2.318)·(tanh(tanh(v)))⊗(norm(((tanh(tanh(v)) ⊙ (tanh(tanh(k)) ⊙ tanh(tanh(k)))) + tanh(tanh(tanh(k)))))) + ((P2 - (tanh(P2·tanh(tanh(tanh(k)))))⊗(tanh(tanh(tanh(k))))) + σ(2.318)·(tanh(tanh(v)))⊗(norm(((tanh(tanh(v)) ⊙ (tanh(tanh(k)) ⊙ tanh(tanh(k)))) + tanh(tanh(tanh(k))))))))

Effective program (19 instructions):
  V2 = Tanh(V0)
  V2 = Tanh(V2)
  V4 = Tanh(V2)
  V3 = MatVec(M2, V4)
  V5 = Tanh(V3)
  V0 = Hadamard(V2, V2)
  M3 = Outer(V5, V4)
  V2 = Tanh(V1)
  V3 = Tanh(V2)
  V5 = Hadamard(V3, V0)
  V4 = VecAdd(V5, V4)
  V5 = Normalize(V4)
  s1 = 2.3184
  s2 = Sigmoid(s1)
  M1 = Outer(V3, V5)
  M0 = MatSub(M2, M3)
  M1 = MatScale(s2, M1)
  M0 = MatAdd(M0, M1)
  M2 = MatAdd(M1, M0)

structure: unclassified  [a=1.023 b=0.825 c=-0.676 g=0.005, erase c/a=0.661, R²=0.6055, 1408 steps]

train acc 0.654 ±0.014
test regime collision3: acc 0.657  margin 0.056  ±0.006
test d16 T12 ow0.3: acc 0.912  margin 0.264  ±0.004
test d16 T12 ow0.0: acc 0.859  margin 0.214  ±0.004
test d16 T12 ow0.6: acc 0.944  margin 0.282  ±0.004
test d32 T24 ow0.3: acc 0.965  margin 0.356  ±0.003
test d8 T6 ow0.3: acc 0.740  margin 0.083  ±0.009
test d16 T64 K8 ow0.3: acc 0.860  margin 0.205  ±0.008
test d16 T128 K8 ow0.3: acc 0.866  margin 0.200  ±0.011
```
