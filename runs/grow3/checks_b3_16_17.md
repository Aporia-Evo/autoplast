fresh draws: tuned DeltaNet 0.643, tuned Kalman delta 0.934

## runs/grow3/armB3_task16/best.json

```
S' = ((S + (v)⊗(k)) + (P2·(v + -0.385·(S + (v)⊗(k))·k))⊗(k))
P2' = (P2 + 0.010·|-0.385·(S + (v)⊗(k))·k|·(P1)ᵀ)

Effective program (15 instructions):
  M3 = Outer(V1, V0)
  M0 = MatAdd(M0, M3)
  V2 = MatVec(M0, V0)
  s0 = -0.3850
  V2 = VecScale(s0, V2)
  V1 = VecAdd(V1, V2)
  V1 = MatVec(M2, V1)
  M3 = Outer(V1, V0)
  M0 = MatAdd(M0, M3)
  s0 = Norm(V2)
  M3 = Transpose(M1)
  M3 = MatScale(s0, M3)
  s0 = 0.0100
  M3 = MatScale(s0, M3)
  M2 = MatAdd(M2, M3)

structure: delta rule  [a=1.000 b=1.729 c=-0.477 g=0.001, erase c/a=0.477, R²=0.9942, 1408 steps]

train acc 0.669 ±0.014
test regime collision3: acc 0.645  margin 0.053  ±0.006
test d16 T12 ow0.3: acc 0.921  margin 0.247  ±0.004
test d16 T12 ow0.0: acc 0.912  margin 0.236  ±0.004
test d16 T12 ow0.6: acc 0.923  margin 0.234  ±0.005
test d32 T24 ow0.3: acc 0.985  margin 0.335  ±0.002
test d8 T6 ow0.3: acc 0.776  margin 0.103  ±0.009
test d16 T64 K8 ow0.3: acc 0.851  margin 0.185  ±0.008
test d16 T128 K8 ow0.3: acc 0.858  margin 0.228  ±0.011
```
fresh draws: 0.650 (+0.007 ± 0.001, 12/12) against DeltaNet; 0.650 (-0.284 ± 0.003, 0/12) against Kalman delta
JAX float32 eps 1e-6:
  reference: linear attention: acc 0.3852 (2505/6503)
  reference: delta rule (beta=0.5): acc 0.6402 (4163/6503)
  runs/grow3/armB3_task16/best.json: acc 0.6451 (4195/6503)
JAX float64 eps 1e-9:
  reference: linear attention: acc 0.3852 (2505/6503)
  reference: delta rule (beta=0.5): acc 0.6402 (4163/6503)
  runs/grow3/armB3_task16/best.json: acc 0.6451 (4195/6503)
eps scale: runs/grow3/armB3_task16/best.json: median max|S|  eps 1e-6: 0.954  eps 1e-3: 0.954  ratio 1 

## runs/grow3/armB3_task17/best.json

```
S' = ((S + -0.418·(S·P2·k)⊗(P2·k)) + (v)⊗(P1·P2·k))
P1' = (P1 + -0.418·(P1·P1·P2·k)⊗(P1·P2·k))
P2' = ((P2 + -0.036·(P2·k)⊗(P2·k)) + 0.039·((P1 + -0.418·(P1·P1·P2·k)⊗(P1·P2·k)))ᵀ)

Effective program (21 instructions):
  V0 = MatVec(M2, V0)
  M3 = Outer(V0, V0)
  s0 = -0.0357
  M3 = MatScale(s0, M3)
  M2 = MatAdd(M2, M3)
  V2 = MatVec(M0, V0)
  M3 = Outer(V2, V0)
  V0 = MatVec(M1, V0)
  s0 = -0.4181
  M3 = MatScale(s0, M3)
  M0 = MatAdd(M0, M3)
  M3 = Outer(V1, V0)
  M0 = MatAdd(M0, M3)
  V1 = MatVec(M1, V0)
  M3 = Outer(V1, V0)
  M3 = MatScale(s0, M3)
  M1 = MatAdd(M1, M3)
  M3 = Transpose(M1)
  s0 = 0.0389
  M3 = MatScale(s0, M3)
  M2 = MatAdd(M2, M3)

structure: unclassified  [a=0.996 b=0.547 c=-0.591 g=-0.075, erase c/a=0.594, R²=0.7453, 1408 steps]

train acc 0.805 ±0.011
test regime collision3: acc 0.790  margin 0.178  ±0.005
test d16 T12 ow0.3: acc 0.921  margin 0.300  ±0.004
test d16 T12 ow0.0: acc 0.974  margin 0.322  ±0.002
test d16 T12 ow0.6: acc 0.863  margin 0.235  ±0.007
test d32 T24 ow0.3: acc 0.942  margin 0.389  ±0.004
test d8 T6 ow0.3: acc 0.801  margin 0.130  ±0.008
test d16 T64 K8 ow0.3: acc 0.971  margin 0.319  ±0.004
test d16 T128 K8 ow0.3: acc 0.989  margin 0.322  ±0.003
```
fresh draws: 0.797 (+0.154 ± 0.003, 12/12) against DeltaNet; 0.797 (-0.137 ± 0.001, 0/12) against Kalman delta
JAX float32 eps 1e-6:
  reference: linear attention: acc 0.3852 (2505/6503)
  reference: delta rule (beta=0.5): acc 0.6402 (4163/6503)
  runs/grow3/armB3_task17/best.json: acc 0.7896 (5135/6503)
JAX float64 eps 1e-9:
  reference: linear attention: acc 0.3852 (2505/6503)
  reference: delta rule (beta=0.5): acc 0.6402 (4163/6503)
  runs/grow3/armB3_task17/best.json: acc 0.7896 (5135/6503)
eps scale: runs/grow3/armB3_task17/best.json: median max|S|  eps 1e-6: 0.423  eps 1e-3: 0.423  ratio 1 

