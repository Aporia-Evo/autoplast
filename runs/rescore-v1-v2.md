# Old runs re-scored with the structural test and the regime suites

Binary at commit 0d2543d plus the working tree of the following commit; `autoplast eval --prog <file> --no-recip`.

## runs/v1-noaddnode/seed1

```
S' = (((v)⊗(k))ᵀ + (2.523·((v)⊗(k) + (v)⊗(k)) + 0.932·S))

Effective program (9 instructions):
  M1 = Outer(V1, V0)
  M3 = MatAdd(M1, M1)
  s3 = 0.9315
  M0 = MatScale(s3, M0)
  s3 = 2.5231
  M3 = MatScale(s3, M3)
  M2 = MatAdd(M3, M0)
  M1 = Transpose(M1)
  M0 = MatAdd(M1, M2)

structure: unclassified  [a=0.931 b=5.109 c=-0.001 g=0.004, erase c/a=0.001, R²=0.9632, 384 steps]

train acc 0.814 ±0.014
test d16 T12 ow0.3: acc 0.782 ±0.006  margin 0.145
test d16 T12 ow0.0: acc 0.832 ±0.005  margin 0.169
test d16 T12 ow0.6: acc 0.670 ±0.009  margin 0.081
test d32 T24 ow0.3: acc 0.806 ±0.006  margin 0.198
test d8 T6 ow0.3: acc 0.622 ±0.010  margin 0.028
full T24: acc 0.557 ±0.007  margin -0.006
overload T48: acc 0.346 ±0.005  margin -0.194
rewrite8 T96: acc 0.504 ±0.011  margin -0.037
rewrite14 T96: acc 0.461 ±0.008  margin -0.091
clustered T12: acc 0.156 ±0.005  margin -0.273
clustered8 T48: acc 0.084 ±0.006  margin -0.351

```

## runs/v2-local/seed1

```
S' = (S + σ(<S·tanh((k + tanh(k))), S·tanh((k + tanh(k)))>·<S·tanh((k + tanh(k))), S·tanh((k + tanh(k)))>)·(v)⊗(k))

Effective program (10 instructions):
  V4 = Tanh(V0)
  V2 = VecAdd(V0, V4)
  V2 = Tanh(V2)
  V4 = MatVec(M0, V2)
  M1 = Outer(V1, V0)
  s0 = Dot(V4, V4)
  s1 = SMul(s0, s0)
  s1 = Sigmoid(s1)
  M1 = MatScale(s1, M1)
  M0 = MatAdd(M0, M1)

structure: unclassified  [a=1.000 b=0.618 c=-0.000 g=-0.075, erase c/a=0.000, R²=0.9397, 384 steps]

train acc 0.853 ±0.012
test d16 T12 ow0.3: acc 0.832 ±0.006  margin 0.151
test d16 T12 ow0.0: acc 0.919 ±0.003  margin 0.201
test d16 T12 ow0.6: acc 0.689 ±0.009  margin 0.067
test d32 T24 ow0.3: acc 0.932 ±0.004  margin 0.225
test d8 T6 ow0.3: acc 0.639 ±0.010  margin 0.040
full T24: acc 0.593 ±0.007  margin 0.013
overload T48: acc 0.364 ±0.005  margin -0.104
rewrite8 T96: acc 0.077 ±0.006  margin -0.367
rewrite14 T96: acc 0.117 ±0.005  margin -0.320
clustered T12: acc 0.154 ±0.005  margin -0.272
clustered8 T48: acc 0.045 ±0.005  margin -0.428

```

## runs/v2-local/seed2

```
S' = 1.098·(((v)⊗(k) + S) - 1.098·(((v)⊗(k) + S))((((v)⊗(k))ᵀ)(0.661·(v)⊗(k))))

Effective program (11 instructions):
  s1 = 0.6606
  M3 = Outer(V1, V0)
  s3 = 1.0975
  M0 = MatAdd(M3, M0)
  M2 = MatScale(s1, M3)
  M1 = Transpose(M3)
  M3 = MatMul(M1, M2)
  M2 = MatMul(M0, M3)
  M3 = MatScale(s3, M2)
  M3 = MatSub(M0, M3)
  M0 = MatScale(s3, M3)

structure: gated delta rule  [a=1.098 b=0.302 c=-0.796 g=-0.000, erase c/a=0.725, R²=1.0000, 384 steps]

train acc 0.971 ±0.006
test d16 T12 ow0.3: acc 0.967 ±0.003  margin 0.311
test d16 T12 ow0.0: acc 0.947 ±0.003  margin 0.281
test d16 T12 ow0.6: acc 0.964 ±0.004  margin 0.312
test d32 T24 ow0.3: acc 0.978 ±0.002  margin 0.366
test d8 T6 ow0.3: acc 0.836 ±0.008  margin 0.139
full T24: acc 0.780 ±0.006  margin 0.129
overload T48: acc 0.206 ±0.004  margin -0.273
rewrite8 T96: acc 0.031 ±0.004  margin -0.606
rewrite14 T96: acc 0.021 ±0.002  margin -0.630
clustered T12: acc 0.180 ±0.006  margin -0.296
clustered8 T48: acc 0.072 ±0.006  margin -0.509

```
