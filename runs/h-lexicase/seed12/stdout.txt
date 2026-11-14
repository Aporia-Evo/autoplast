# Search seed 12

task: v2  alphabet: 19 ops  readout: fixed o = S q  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 855233  time: 1399s  pop: 500  tournament: 10

commit: ad31161  task seed: 1  train episodes: 96  persistent registers: 1 matrix, 0 vector, start zero  batch: 128

search: regularized evolution  tune-consts: 0  select: lexicase

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* unclassified: 2164 candidates
* linear attention: 11892 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.772): 11892 candidates
- delta rule (beta=1) (acc 0.858): 30452 candidates
- delta rule (beta=0.5) (acc 0.932): 52852 candidates
- gated delta (alpha=0.9) (acc 0.729): 11892 candidates

## Best rule

```
S' = (((v)⊗(k) + S) + ((|tanh(S·k)|·σ(<S·k, S·k>)·(0 - (v)⊗(k)) + ((v)⊗(k) + S)))((((0 - (v)⊗(k)))ᵀ)((((v)⊗(k) + S) - (|tanh(S·k)|·σ(<S·k, S·k>)·(0 - (v)⊗(k)) + ((v)⊗(k) + S))))))

Effective program (16 instructions):
  M3 = Outer(V1, V0)
  V5 = MatVec(M0, V0)
  s3 = Dot(V5, V5)
  V0 = Tanh(V5)
  s1 = Norm(V0)
  M1 = MatAdd(M3, M0)
  s0 = Sigmoid(s3)
  s1 = SMul(s1, s0)
  M0 = MatSub(M2, M3)
  M3 = MatScale(s1, M0)
  M2 = MatAdd(M3, M1)
  M3 = Transpose(M0)
  M0 = MatSub(M1, M2)
  M0 = MatMul(M3, M0)
  M3 = MatMul(M2, M0)
  M0 = MatAdd(M1, M3)

structure: unclassified  [a=1.000 b=0.831 c=-0.524 g=0.055, erase c/a=0.524, R²=0.9783, 384 steps]

train acc 0.958 ±0.007
test d16 T12 ow0.3: acc 0.946  margin 0.271  ±0.003
test d16 T12 ow0.0: acc 0.937  margin 0.244  ±0.003
test d16 T12 ow0.6: acc 0.952  margin 0.278  ±0.004
test d32 T24 ow0.3: acc 0.992  margin 0.358  ±0.001
test d8 T6 ow0.3: acc 0.813  margin 0.120  ±0.008
test d16 T64 K8 ow0.3: acc 0.839  margin 0.182  ±0.008
test d16 T128 K8 ow0.3: acc 0.836  margin 0.179  ±0.012
```
