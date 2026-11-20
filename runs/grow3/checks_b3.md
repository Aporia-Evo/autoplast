fresh draws: tuned DeltaNet 0.643, tuned Kalman delta 0.934

## runs/grow3/armB3_task10/best.json

```
S' = (((S + -0.653·(S·k)⊗(P2·k)) + -0.137·σ(-0.653)·(S + -0.653·(S·k)⊗(P2·k))) + (v)⊗(P1·P2·k))
P1' = (P1 + -0.653·(P1·P2·k)⊗(tanh(P1·P2·k)))
P2' = (P2 + 0.104·|S·k|·((P1 + -0.653·(P1·P2·k)⊗(tanh(P1·P2·k))) - P2))

Effective program (24 instructions):
  V2 = MatVec(M0, V0)
  V0 = MatVec(M2, V0)
  M3 = Outer(V2, V0)
  V0 = MatVec(M1, V0)
  s0 = -0.6527
  M3 = MatScale(s0, M3)
  M0 = MatAdd(M0, M3)
  s1 = Sigmoid(s0)
  M3 = MatScale(s1, M0)
  s1 = -0.1374
  M3 = MatScale(s1, M3)
  M0 = MatAdd(M0, M3)
  M3 = Outer(V1, V0)
  M0 = MatAdd(M0, M3)
  V1 = Tanh(V0)
  M3 = Outer(V0, V1)
  M3 = MatScale(s0, M3)
  M1 = MatAdd(M1, M3)
  s0 = Norm(V2)
  M3 = MatSub(M1, M2)
  M3 = MatScale(s0, M3)
  s0 = 0.1042
  M3 = MatScale(s0, M3)
  M2 = MatAdd(M2, M3)

structure: unclassified  [a=0.953 b=0.338 c=-0.554 g=-0.062, erase c/a=0.581, R²=0.5701, 1408 steps]

train acc 0.825 ±0.011
test regime collision3: acc 0.804  margin 0.170  ±0.005
test d16 T12 ow0.3: acc 0.927  margin 0.306  ±0.004
test d16 T12 ow0.0: acc 0.984  margin 0.336  ±0.002
test d16 T12 ow0.6: acc 0.892  margin 0.240  ±0.006
test d32 T24 ow0.3: acc 0.950  margin 0.374  ±0.003
test d8 T6 ow0.3: acc 0.853  margin 0.156  ±0.007
test d16 T64 K8 ow0.3: acc 0.924  margin 0.201  ±0.006
test d16 T128 K8 ow0.3: acc 0.897  margin 0.183  ±0.009
```
fresh draws: 0.811 (+0.168 ± 0.003, 12/12) against DeltaNet; 0.811 (-0.124 ± 0.002, 0/12) against Kalman delta
JAX float32 eps 1e-6:
  reference: linear attention: acc 0.3852 (2505/6503)
  reference: delta rule (beta=0.5): acc 0.6402 (4163/6503)
  runs/grow3/armB3_task10/best.json: acc 0.8042 (5230/6503)
JAX float64 eps 1e-9:
  reference: linear attention: acc 0.3852 (2505/6503)
  reference: delta rule (beta=0.5): acc 0.6402 (4163/6503)
  runs/grow3/armB3_task10/best.json: acc 0.8042 (5230/6503)
eps scale: runs/grow3/armB3_task10/best.json: median max|S|  eps 1e-6: 0.257  eps 1e-3: 0.257  ratio 1 

## runs/grow3/armB3_task11/best.json

```
S' = (((S + -0.642·(S·k)⊗(P2·k)) + -0.157·σ(-0.642)·(S + -0.642·(S·k)⊗(P2·k))) + (v)⊗(P1·P2·k))
P1' = (P1 + -0.642·(tanh(P1·P2·k))⊗(P1·P2·k))
P2' = (P2 + 0.100·|P1·P2·k|·((P1 + -0.642·(tanh(P1·P2·k))⊗(P1·P2·k)) - P2))

Effective program (24 instructions):
  V2 = MatVec(M0, V0)
  V0 = MatVec(M2, V0)
  M3 = Outer(V2, V0)
  V0 = MatVec(M1, V0)
  s0 = -0.6423
  M3 = MatScale(s0, M3)
  M0 = MatAdd(M0, M3)
  s1 = Sigmoid(s0)
  M3 = MatScale(s1, M0)
  s1 = -0.1571
  M3 = MatScale(s1, M3)
  M0 = MatAdd(M0, M3)
  M3 = Outer(V1, V0)
  M0 = MatAdd(M0, M3)
  V1 = Tanh(V0)
  M3 = Outer(V1, V0)
  M3 = MatScale(s0, M3)
  M1 = MatAdd(M1, M3)
  s0 = Norm(V0)
  M3 = MatSub(M1, M2)
  M3 = MatScale(s0, M3)
  s0 = 0.0998
  M3 = MatScale(s0, M3)
  M2 = MatAdd(M2, M3)

structure: unclassified  [a=0.944 b=0.339 c=-0.514 g=0.013, erase c/a=0.544, R²=0.5580, 1408 steps]

train acc 0.800 ±0.011
test regime collision3: acc 0.800  margin 0.168  ±0.005
test d16 T12 ow0.3: acc 0.887  margin 0.293  ±0.005
test d16 T12 ow0.0: acc 0.989  margin 0.341  ±0.001
test d16 T12 ow0.6: acc 0.852  margin 0.226  ±0.007
test d32 T24 ow0.3: acc 0.897  margin 0.355  ±0.005
test d8 T6 ow0.3: acc 0.830  margin 0.148  ±0.008
test d16 T64 K8 ow0.3: acc 0.928  margin 0.215  ±0.006
test d16 T128 K8 ow0.3: acc 0.899  margin 0.195  ±0.009
```
fresh draws: 0.805 (+0.162 ± 0.003, 12/12) against DeltaNet; 0.805 (-0.129 ± 0.001, 0/12) against Kalman delta
JAX float32 eps 1e-6:
  reference: linear attention: acc 0.3852 (2505/6503)
  reference: delta rule (beta=0.5): acc 0.6402 (4163/6503)
  runs/grow3/armB3_task11/best.json: acc 0.7998 (5201/6503)
JAX float64 eps 1e-9:
  reference: linear attention: acc 0.3852 (2505/6503)
  reference: delta rule (beta=0.5): acc 0.6402 (4163/6503)
  runs/grow3/armB3_task11/best.json: acc 0.7998 (5201/6503)
eps scale: runs/grow3/armB3_task11/best.json: median max|S|  eps 1e-6: 0.252  eps 1e-3: 0.252  ratio 1 

## runs/grow3/armB3_task12/best.json

```
S' = (((S + -0.642·(S·k)⊗(P2·k)) + 0.080·-0.642·(S + -0.642·(S·k)⊗(P2·k))) + (v)⊗(P1·P2·k))
P1' = (P1 + -0.642·(P1·P2·k)⊗(tanh(P1·P2·k)))
P2' = (P2 + 0.098·|P1·P2·k|·((P1 + -0.642·(P1·P2·k)⊗(tanh(P1·P2·k))) - P2))

Effective program (23 instructions):
  V2 = MatVec(M0, V0)
  V0 = MatVec(M2, V0)
  M3 = Outer(V2, V0)
  V0 = MatVec(M1, V0)
  s0 = -0.6416
  M3 = MatScale(s0, M3)
  M0 = MatAdd(M0, M3)
  M3 = MatScale(s0, M0)
  s1 = 0.0800
  M3 = MatScale(s1, M3)
  M0 = MatAdd(M0, M3)
  M3 = Outer(V1, V0)
  M0 = MatAdd(M0, M3)
  V1 = Tanh(V0)
  M3 = Outer(V0, V1)
  M3 = MatScale(s0, M3)
  M1 = MatAdd(M1, M3)
  s0 = Norm(V0)
  M3 = MatSub(M1, M2)
  M3 = MatScale(s0, M3)
  s0 = 0.0981
  M3 = MatScale(s0, M3)
  M2 = MatAdd(M2, M3)

structure: unclassified  [a=0.949 b=0.334 c=-0.519 g=-0.087, erase c/a=0.547, R²=0.5604, 1408 steps]

train acc 0.802 ±0.011
test regime collision3: acc 0.799  margin 0.167  ±0.005
test d16 T12 ow0.3: acc 0.884  margin 0.292  ±0.005
test d16 T12 ow0.0: acc 0.989  margin 0.342  ±0.001
test d16 T12 ow0.6: acc 0.841  margin 0.224  ±0.007
test d32 T24 ow0.3: acc 0.893  margin 0.354  ±0.005
test d8 T6 ow0.3: acc 0.829  margin 0.147  ±0.008
test d16 T64 K8 ow0.3: acc 0.931  margin 0.209  ±0.006
test d16 T128 K8 ow0.3: acc 0.901  margin 0.189  ±0.009
```
fresh draws: 0.805 (+0.162 ± 0.003, 12/12) against DeltaNet; 0.805 (-0.130 ± 0.001, 0/12) against Kalman delta
JAX float32 eps 1e-6:
  reference: linear attention: acc 0.3852 (2505/6503)
  reference: delta rule (beta=0.5): acc 0.6402 (4163/6503)
  runs/grow3/armB3_task12/best.json: acc 0.7986 (5193/6503)
JAX float64 eps 1e-9:
  reference: linear attention: acc 0.3852 (2505/6503)
  reference: delta rule (beta=0.5): acc 0.6402 (4163/6503)
  runs/grow3/armB3_task12/best.json: acc 0.7986 (5193/6503)
eps scale: runs/grow3/armB3_task12/best.json: median max|S|  eps 1e-6: 0.255  eps 1e-3: 0.255  ratio 1 

## runs/grow3/armB3_task13/best.json

```
S' = (((S + -0.047·(S)(P1)) + -0.570·((S + -0.047·(S)(P1))·k)⊗(k)) + (v)⊗((P1 + -0.003·|(S + -0.047·(S)(P1))·k|·(P1 - P2))·k))
P1' = ((P1 + -0.003·|(S + -0.047·(S)(P1))·k|·(P1 - P2)) + 1.059·(-0.570·(P1 + -0.003·|(S + -0.047·(S)(P1))·k|·(P1 - P2))·k)⊗((P1 + -0.003·|(S + -0.047·(S)(P1))·k|·(P1 - P2))·k))

Effective program (23 instructions):
  M3 = MatMul(M0, M1)
  s0 = -0.0466
  M3 = MatScale(s0, M3)
  M0 = MatAdd(M0, M3)
  V2 = MatVec(M0, V0)
  s0 = Norm(V2)
  M3 = MatSub(M1, M2)
  M3 = MatScale(s0, M3)
  s0 = -0.0030
  M3 = MatScale(s0, M3)
  M1 = MatAdd(M1, M3)
  M3 = Outer(V2, V0)
  V0 = MatVec(M1, V0)
  s0 = -0.5695
  M3 = MatScale(s0, M3)
  M0 = MatAdd(M0, M3)
  M3 = Outer(V1, V0)
  M0 = MatAdd(M0, M3)
  V1 = VecScale(s0, V0)
  M3 = Outer(V1, V0)
  s1 = 1.0589
  M3 = MatScale(s1, M3)
  M1 = MatAdd(M1, M3)

structure: unclassified  [a=0.978 b=0.379 c=-0.555 g=-0.075, erase c/a=0.568, R²=0.6458, 1408 steps]

train acc 0.800 ±0.011
test regime collision3: acc 0.773  margin 0.153  ±0.005
test d16 T12 ow0.3: acc 0.915  margin 0.295  ±0.004
test d16 T12 ow0.0: acc 0.983  margin 0.324  ±0.002
test d16 T12 ow0.6: acc 0.873  margin 0.236  ±0.006
test d32 T24 ow0.3: acc 0.951  margin 0.368  ±0.003
test d8 T6 ow0.3: acc 0.819  margin 0.142  ±0.008
test d16 T64 K8 ow0.3: acc 0.899  margin 0.209  ±0.007
test d16 T128 K8 ow0.3: acc 0.907  margin 0.210  ±0.009
```
fresh draws: 0.776 (+0.133 ± 0.002, 12/12) against DeltaNet; 0.776 (-0.158 ± 0.002, 0/12) against Kalman delta
JAX float32 eps 1e-6:
  reference: linear attention: acc 0.3852 (2505/6503)
  reference: delta rule (beta=0.5): acc 0.6402 (4163/6503)
  runs/grow3/armB3_task13/best.json: acc 0.7730 (5027/6503)
JAX float64 eps 1e-9:
  reference: linear attention: acc 0.3852 (2505/6503)
  reference: delta rule (beta=0.5): acc 0.6402 (4163/6503)
  runs/grow3/armB3_task13/best.json: acc 0.7730 (5027/6503)
eps scale: runs/grow3/armB3_task13/best.json: median max|S|  eps 1e-6: 0.294  eps 1e-3: 0.294  ratio 1 

## runs/grow3/armB3_task14/best.json

```
S' = (((S + -0.064·(S)(P1)) + -0.613·((S + -0.064·(S)(P1))·k)⊗(P2·k)) + (tanh(v))⊗(P1·P2·k))
P1' = (P1 + -0.613·(P1·P2·k)⊗(P1·P2·k))
P2' = (P2 + 0.032·|P1·P2·k|·((P1 + -0.613·(P1·P2·k)⊗(P1·P2·k)) - P2))

Effective program (23 instructions):
  M3 = MatMul(M0, M1)
  s0 = -0.0640
  M3 = MatScale(s0, M3)
  M0 = MatAdd(M0, M3)
  V2 = MatVec(M0, V0)
  V0 = MatVec(M2, V0)
  M3 = Outer(V2, V0)
  V0 = MatVec(M1, V0)
  s0 = -0.6134
  M3 = MatScale(s0, M3)
  M0 = MatAdd(M0, M3)
  V2 = Tanh(V1)
  M3 = Outer(V2, V0)
  M0 = MatAdd(M0, M3)
  M3 = Outer(V0, V0)
  M3 = MatScale(s0, M3)
  M1 = MatAdd(M1, M3)
  s0 = Norm(V0)
  M3 = MatSub(M1, M2)
  M3 = MatScale(s0, M3)
  s0 = 0.0324
  M3 = MatScale(s0, M3)
  M2 = MatAdd(M2, M3)

structure: unclassified  [a=0.969 b=0.341 c=-0.548 g=-0.016, erase c/a=0.566, R²=0.6110, 1408 steps]

train acc 0.794 ±0.012
test regime collision3: acc 0.782  margin 0.153  ±0.005
test d16 T12 ow0.3: acc 0.907  margin 0.295  ±0.004
test d16 T12 ow0.0: acc 0.982  margin 0.327  ±0.002
test d16 T12 ow0.6: acc 0.873  margin 0.234  ±0.006
test d32 T24 ow0.3: acc 0.935  margin 0.359  ±0.004
test d8 T6 ow0.3: acc 0.828  margin 0.144  ±0.008
test d16 T64 K8 ow0.3: acc 0.902  margin 0.179  ±0.007
test d16 T128 K8 ow0.3: acc 0.845  margin 0.133  ±0.011
```
fresh draws: 0.788 (+0.145 ± 0.002, 12/12) against DeltaNet; 0.788 (-0.146 ± 0.002, 0/12) against Kalman delta
