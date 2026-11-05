| rule | train acc | test regime noisyq | test d16 T12 ow0.3 | test d16 T12 ow0.0 | test d16 T12 ow0.6 | test d32 T24 ow0.3 | test d8 T6 ow0.3 | test d16 T64 K8 ow0.3 | test d16 T128 K8 ow0.3 |
|---|---|---|---|---|---|---|---|---|---|
| no-write (start of search) | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| linear attention | 0.735 | 0.724 | 0.750 | 0.917 | 0.549 | 0.828 | 0.615 | 0.104 | 0.062 |
| delta rule (beta=1) | 0.821 | 0.841 | 0.862 | 0.788 | 0.922 | 0.948 | 0.744 | 0.831 | 0.844 |
| delta rule (beta=0.5) | 0.900 | 0.899 | 0.924 | 0.900 | 0.941 | 0.987 | 0.793 | 0.840 | 0.828 |
| gated delta (alpha=0.9) | 0.691 | 0.694 | 0.714 | 0.620 | 0.837 | 0.639 | 0.685 | 0.665 | 0.662 |

no-write (start of search): S' = S
linear attention: S' = (S + (v)⊗(k))
delta rule (beta=1): S' = (S + ((v - S·k))⊗(k))
delta rule (beta=0.5): S' = (S + 0.500·((v - S·k))⊗(k))
gated delta (alpha=0.9): S' = (0.900·S + ((v - 0.900·S·k))⊗(k))
