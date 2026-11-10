# Structural test on the final rule of every committed seed

Family by `src/classify.rs` (least-squares fit on real memory states, R² ≥ 0.99). "old count" is the
number of seeds whose summary says the accuracy level of delta rule beta=0.5 was reached, the
criterion used before 10 Nov 2026. For evolved-readout runs only the write rule is classified.

| tag | setting | seeds | delta family (structural) | old count (accuracy level) | linear attention family | unclassified | other |
|---|---|---|---|---|---|---|---|
| v1-noaddnode | base task, 48 train episodes, add-node off (3 Nov) | 1 | 0 | 0 | 0 | 1 | 0 |
| v2-local | base task, add-node on (3 Nov) | 2 | 1 | 1 | 0 | 1 | 0 |
| v2 | base task, add-node on | 16 | 5 | 6 | 8 | 3 | 0 |
| v2-noaddnode | base task, add-node off | 16 | 6 | 8 | 8 | 2 | 0 |
| base-recip | base task, add-node on, Recip in the alphabet (package B) | 16 | 4 | 5 | 11 | 1 | 0 |
| base-recip-noaddnode | base task, add-node off, Recip in the alphabet (package B) | 16 | 5 | 5 | 10 | 1 | 0 |
| v3 | task v3 (long episodes), add-node on | 16 | 11 | 12 | 4 | 1 | 0 |
| v3-extraops | task v3, ten extra ops | 16 | 6 | 9 | 1 | 9 | 0 |
| v3-nomatvec | task v3, without MatVec | 16 | 4 | 5 | 10 | 2 | 0 |
| 5a-A | collision3, fixed readout | 16 | 1 | 7 | 4 | 10 | 1 |
| 5a-B | collision3, evolved readout, ten extra ops | 16 | 2 | 4 | 2 | 12 | 0 |
| 5a-C | collision3, evolved readout | 16 | 1 | 2 | 11 | 4 | 0 |

## Per seed

| tag | seed | family | a | erase c/a | R² | train acc | delta accuracy level reached |
|---|---|---|---|---|---|---|---|
| v1-noaddnode | 1 | unclassified | 0.931 | 0.001 | 0.9632 | 0.814 | no |
| v2-local | 1 | unclassified | 1.000 | 0.000 | 0.9397 | 0.853 | no |
| v2-local | 2 | gated delta rule | 1.098 | 0.725 | 1.0000 | 0.971 | yes |
| v2 | 1 | linear attention | 0.958 | 0.000 | 1.0000 | 0.814 | no |
| v2 | 2 | linear attention | 0.951 | 0.001 | 0.9960 | 0.817 | no |
| v2 | 3 | gated delta rule | 1.098 | 0.683 | 0.9969 | 0.975 | yes |
| v2 | 4 | linear attention | 0.952 | 0.001 | 0.9960 | 0.817 | no |
| v2 | 5 | linear attention | 0.958 | -0.000 | 1.0000 | 0.814 | no |
| v2 | 6 | gated delta rule | 1.153 | 0.763 | 0.9906 | 0.969 | yes |
| v2 | 7 | gated delta rule | 1.098 | 0.683 | 0.9969 | 0.975 | yes |
| v2 | 8 | unclassified | 1.055 | 0.624 | 0.9645 | 0.969 | yes |
| v2 | 9 | linear attention | 0.951 | 0.001 | 0.9960 | 0.817 | no |
| v2 | 10 | linear attention | 0.958 | -0.000 | 1.0000 | 0.814 | no |
| v2 | 11 | unclassified | 0.954 | 0.124 | 0.9088 | 0.836 | no |
| v2 | 12 | gated delta rule | 1.089 | 0.633 | 0.9984 | 0.973 | yes |
| v2 | 13 | linear attention | 0.958 | 0.000 | 1.0000 | 0.814 | no |
| v2 | 14 | linear attention | 0.952 | 0.001 | 0.9947 | 0.821 | no |
| v2 | 15 | unclassified | 0.955 | 0.137 | 0.8876 | 0.840 | no |
| v2 | 16 | gated delta rule | 1.108 | 0.696 | 0.9936 | 0.972 | yes |
| v2-noaddnode | 1 | linear attention | 0.951 | 0.001 | 0.9960 | 0.817 | no |
| v2-noaddnode | 2 | gated delta rule | 1.096 | 0.651 | 0.9982 | 0.975 | yes |
| v2-noaddnode | 3 | linear attention | 0.958 | 0.000 | 1.0000 | 0.814 | no |
| v2-noaddnode | 4 | unclassified | 1.111 | 0.569 | 0.9855 | 0.977 | yes |
| v2-noaddnode | 5 | gated delta rule | 1.122 | 0.718 | 0.9909 | 0.970 | yes |
| v2-noaddnode | 6 | gated delta rule | 1.101 | 0.726 | 1.0000 | 0.971 | yes |
| v2-noaddnode | 7 | gated delta rule | 1.141 | 0.834 | 0.9984 | 0.966 | yes |
| v2-noaddnode | 8 | linear attention | 0.951 | 0.001 | 0.9960 | 0.817 | no |
| v2-noaddnode | 9 | linear attention | 0.958 | 0.000 | 1.0000 | 0.814 | no |
| v2-noaddnode | 10 | linear attention | 0.958 | -0.000 | 1.0000 | 0.814 | no |
| v2-noaddnode | 11 | unclassified | 1.504 | 0.635 | 0.4417 | 0.954 | yes |
| v2-noaddnode | 12 | linear attention | 0.958 | -0.000 | 1.0000 | 0.814 | no |
| v2-noaddnode | 13 | gated delta rule | 1.100 | 0.647 | 0.9989 | 0.973 | yes |
| v2-noaddnode | 14 | linear attention | 0.951 | -0.000 | 0.9992 | 0.812 | no |
| v2-noaddnode | 15 | gated delta rule | 1.098 | 0.683 | 0.9969 | 0.975 | yes |
| v2-noaddnode | 16 | linear attention | 0.952 | 0.001 | 0.9956 | 0.817 | no |
| base-recip | 1 | linear attention | 0.951 | 0.001 | 0.9960 | 0.817 | no |
| base-recip | 2 | linear attention | 0.958 | -0.000 | 1.0000 | 0.814 | no |
| base-recip | 3 | unclassified | 1.114 | 0.720 | 0.9895 | 0.969 | yes |
| base-recip | 4 | gated delta rule | 1.097 | 0.750 | 0.9910 | 0.967 | yes |
| base-recip | 5 | gated delta rule | 1.125 | 0.777 | 0.9908 | 0.971 | yes |
| base-recip | 6 | linear attention | 0.956 | -0.002 | 0.9958 | 0.821 | no |
| base-recip | 7 | linear attention | 0.951 | 0.001 | 0.9960 | 0.817 | no |
| base-recip | 8 | linear attention | 0.952 | 0.001 | 0.9956 | 0.817 | no |
| base-recip | 9 | gated delta rule | 1.097 | 0.675 | 0.9977 | 0.973 | yes |
| base-recip | 10 | linear attention | 0.958 | -0.000 | 1.0000 | 0.814 | no |
| base-recip | 11 | linear attention | 0.958 | -0.000 | 1.0000 | 0.814 | no |
| base-recip | 12 | gated delta rule | 1.100 | 0.651 | 0.9971 | 0.975 | yes |
| base-recip | 13 | linear attention | 0.951 | 0.001 | 0.9960 | 0.817 | no |
| base-recip | 14 | linear attention | 0.951 | 0.001 | 0.9960 | 0.817 | no |
| base-recip | 15 | linear attention | 0.958 | -0.000 | 1.0000 | 0.814 | no |
| base-recip | 16 | linear attention | 0.951 | 0.000 | 0.9957 | 0.829 | no |
| base-recip-noaddnode | 1 | linear attention | 0.958 | -0.000 | 1.0000 | 0.814 | no |
| base-recip-noaddnode | 2 | gated delta rule | 1.108 | 0.709 | 0.9959 | 0.973 | yes |
| base-recip-noaddnode | 3 | linear attention | 0.952 | 0.001 | 0.9957 | 0.818 | no |
| base-recip-noaddnode | 4 | linear attention | 0.958 | -0.000 | 1.0000 | 0.814 | no |
| base-recip-noaddnode | 5 | linear attention | 0.958 | 0.000 | 1.0000 | 0.814 | no |
| base-recip-noaddnode | 6 | linear attention | 0.959 | 0.001 | 0.9991 | 0.819 | no |
| base-recip-noaddnode | 7 | linear attention | 0.958 | -0.000 | 1.0000 | 0.814 | no |
| base-recip-noaddnode | 8 | linear attention | 0.958 | 0.000 | 1.0000 | 0.814 | no |
| base-recip-noaddnode | 9 | linear attention | 0.951 | -0.000 | 0.9992 | 0.812 | no |
| base-recip-noaddnode | 10 | gated delta rule | 1.138 | 0.720 | 0.9982 | 0.967 | yes |
| base-recip-noaddnode | 11 | gated delta rule | 1.134 | 0.829 | 0.9968 | 0.965 | yes |
| base-recip-noaddnode | 12 | gated delta rule | 1.107 | 0.697 | 0.9981 | 0.973 | yes |
| base-recip-noaddnode | 13 | linear attention | 0.958 | -0.000 | 1.0000 | 0.814 | no |
| base-recip-noaddnode | 14 | unclassified | 0.970 | 0.054 | 0.9846 | 0.824 | no |
| base-recip-noaddnode | 15 | linear attention | 0.958 | 0.000 | 1.0000 | 0.814 | no |
| base-recip-noaddnode | 16 | gated delta rule | 1.107 | 0.722 | 0.9933 | 0.970 | yes |
| v3 | 1 | decayed linear attention | 0.907 | -0.000 | 1.0000 | 0.725 | no |
| v3 | 2 | unclassified | 1.000 | 0.586 | 0.9838 | 0.918 | yes |
| v3 | 3 | delta rule | 1.000 | 0.549 | 0.9949 | 0.914 | yes |
| v3 | 4 | decayed linear attention | 0.907 | -0.000 | 1.0000 | 0.725 | no |
| v3 | 5 | delta rule | 1.000 | 0.519 | 0.9924 | 0.918 | yes |
| v3 | 6 | delta rule | 1.000 | 0.556 | 0.9997 | 0.908 | yes |
| v3 | 7 | delta rule | 1.000 | 0.552 | 0.9953 | 0.911 | yes |
| v3 | 8 | decayed linear attention | 0.907 | -0.000 | 1.0000 | 0.725 | no |
| v3 | 9 | delta rule | 1.000 | 0.569 | 0.9983 | 0.911 | yes |
| v3 | 10 | delta rule | 1.000 | 0.600 | 0.9972 | 0.908 | yes |
| v3 | 11 | delta rule | 1.000 | 0.612 | 0.9981 | 0.907 | yes |
| v3 | 12 | delta rule | 1.000 | 0.554 | 0.9941 | 0.916 | yes |
| v3 | 13 | delta rule | 1.000 | 0.578 | 0.9918 | 0.908 | yes |
| v3 | 14 | decayed linear attention | 0.914 | 0.001 | 0.9964 | 0.721 | no |
| v3 | 15 | delta rule | 1.000 | 0.581 | 1.0000 | 0.905 | yes |
| v3 | 16 | delta rule | 1.015 | 0.669 | 0.9980 | 0.908 | yes |
| v3-extraops | 1 | delta rule | 1.000 | 0.599 | 0.9986 | 0.909 | yes |
| v3-extraops | 2 | delta rule | 1.000 | 0.651 | 0.9957 | 0.912 | yes |
| v3-extraops | 3 | unclassified | 0.868 | 0.027 | 0.9372 | 0.789 | no |
| v3-extraops | 4 | unclassified | 0.925 | 0.005 | 0.9842 | 0.720 | no |
| v3-extraops | 5 | delta rule | 1.000 | 0.612 | 0.9936 | 0.903 | yes |
| v3-extraops | 6 | unclassified | 1.011 | 0.600 | 0.9204 | 0.893 | no |
| v3-extraops | 7 | unclassified | 0.921 | 0.006 | 0.9833 | 0.724 | no |
| v3-extraops | 8 | unclassified | 1.000 | 0.613 | 0.9856 | 0.918 | yes |
| v3-extraops | 9 | decayed linear attention | 0.905 | 0.001 | 0.9981 | 0.727 | no |
| v3-extraops | 10 | delta rule | 1.000 | 0.605 | 0.9939 | 0.908 | yes |
| v3-extraops | 11 | delta rule | 1.000 | 0.562 | 0.9991 | 0.907 | yes |
| v3-extraops | 12 | unclassified | 0.909 | 0.085 | 0.9388 | 0.763 | no |
| v3-extraops | 13 | unclassified | 0.910 | 0.017 | 0.9545 | 0.730 | no |
| v3-extraops | 14 | unclassified | 0.999 | 0.634 | 0.9803 | 0.904 | yes |
| v3-extraops | 15 | delta rule | 1.000 | 0.585 | 0.9977 | 0.913 | yes |
| v3-extraops | 16 | unclassified | 1.000 | 0.574 | 0.9711 | 0.913 | yes |
| v3-nomatvec | 1 | delta rule | 1.004 | 0.596 | 1.0000 | 0.908 | yes |
| v3-nomatvec | 2 | delta rule | 1.000 | 0.599 | 0.9924 | 0.910 | yes |
| v3-nomatvec | 3 | delta rule | 1.000 | 0.610 | 0.9989 | 0.909 | yes |
| v3-nomatvec | 4 | decayed linear attention | 0.907 | -0.000 | 1.0000 | 0.725 | no |
| v3-nomatvec | 5 | decayed linear attention | 0.907 | -0.000 | 1.0000 | 0.725 | no |
| v3-nomatvec | 6 | decayed linear attention | 0.907 | 0.000 | 1.0000 | 0.728 | no |
| v3-nomatvec | 7 | unclassified | 1.007 | 0.643 | 0.9892 | 0.916 | yes |
| v3-nomatvec | 8 | decayed linear attention | 0.907 | -0.000 | 1.0000 | 0.725 | no |
| v3-nomatvec | 9 | decayed linear attention | 0.907 | -0.000 | 1.0000 | 0.725 | no |
| v3-nomatvec | 10 | unclassified | 0.951 | 0.106 | 0.9294 | 0.755 | no |
| v3-nomatvec | 11 | decayed linear attention | 0.907 | -0.000 | 1.0000 | 0.725 | no |
| v3-nomatvec | 12 | decayed linear attention | 0.907 | -0.000 | 1.0000 | 0.725 | no |
| v3-nomatvec | 13 | decayed linear attention | 0.907 | -0.000 | 1.0000 | 0.725 | no |
| v3-nomatvec | 14 | decayed linear attention | 0.907 | 0.000 | 1.0000 | 0.725 | no |
| v3-nomatvec | 15 | decayed linear attention | 0.907 | 0.000 | 1.0000 | 0.725 | no |
| v3-nomatvec | 16 | delta rule | 1.000 | 0.611 | 0.9981 | 0.908 | yes |
| 5a-A | 1 | unclassified | 0.862 | 0.000 | 0.9862 | 0.510 | no |
| 5a-A | 2 | unclassified | 1.000 | 0.454 | 0.9420 | 0.642 | yes |
| 5a-A | 3 | decayed linear attention | 0.857 | -0.000 | 0.9964 | 0.512 | no |
| 5a-A | 4 | decayed linear attention | 0.903 | 0.001 | 0.9915 | 0.512 | no |
| 5a-A | 5 | delta rule | 1.001 | 0.474 | 0.9907 | 0.625 | yes |
| 5a-A | 6 | decayed linear attention | 0.878 | 0.001 | 0.9952 | 0.511 | no |
| 5a-A | 7 | unclassified | 0.865 | -0.000 | 0.9817 | 0.511 | no |
| 5a-A | 8 | delta + Kronecker mix | 1.000 | 0.449 | 0.9951 | 0.632 | yes |
| 5a-A | 9 | decayed linear attention | 0.874 | 0.000 | 0.9955 | 0.509 | no |
| 5a-A | 10 | unclassified | 0.862 | 0.000 | 0.9862 | 0.510 | no |
| 5a-A | 11 | unclassified | 1.008 | 0.503 | 0.9874 | 0.624 | yes |
| 5a-A | 12 | unclassified | 1.000 | 0.476 | 0.9827 | 0.630 | yes |
| 5a-A | 13 | unclassified | 0.999 | 0.525 | 0.9887 | 0.623 | yes |
| 5a-A | 14 | unclassified | 0.862 | 0.000 | 0.9862 | 0.510 | no |
| 5a-A | 15 | unclassified | 1.000 | 0.518 | 0.9863 | 0.621 | yes |
| 5a-A | 16 | unclassified | 0.880 | -0.001 | 0.9808 | 0.511 | no |
| 5a-B | 1 | decayed linear attention | 0.914 | 0.013 | 0.9938 | 0.514 | no |
| 5a-B | 2 | unclassified | 0.991 | 0.471 | 0.9755 | 0.623 | yes |
| 5a-B | 3 | unclassified | 0.881 | 0.032 | 0.9751 | 0.520 | no |
| 5a-B | 4 | delta rule | 1.000 | 0.462 | 0.9903 | 0.624 | yes |
| 5a-B | 5 | unclassified | 0.913 | 0.027 | 0.9756 | 0.528 | no |
| 5a-B | 6 | unclassified | 0.970 | 0.379 | 0.9897 | 0.613 | yes |
| 5a-B | 7 | unclassified | 0.904 | 0.030 | 0.9776 | 0.513 | no |
| 5a-B | 8 | unclassified | 0.887 | 0.044 | 0.9398 | 0.518 | no |
| 5a-B | 9 | unclassified | 0.887 | 0.009 | 0.9695 | 0.519 | no |
| 5a-B | 10 | unclassified | 0.891 | 0.009 | 0.9747 | 0.520 | no |
| 5a-B | 11 | unclassified | 0.904 | 0.029 | 0.9783 | 0.510 | no |
| 5a-B | 12 | delta rule | 1.000 | 0.554 | 0.9917 | 0.631 | yes |
| 5a-B | 13 | decayed linear attention | 0.911 | 0.002 | 0.9939 | 0.515 | no |
| 5a-B | 14 | unclassified | 0.891 | 0.009 | 0.9747 | 0.520 | no |
| 5a-B | 15 | unclassified | 0.904 | 0.029 | 0.9775 | 0.516 | no |
| 5a-B | 16 | unclassified | 0.904 | 0.030 | 0.9776 | 0.509 | no |
| 5a-C | 1 | decayed linear attention | 0.894 | -0.002 | 0.9946 | 0.509 | no |
| 5a-C | 2 | decayed linear attention | 0.878 | 0.001 | 0.9971 | 0.513 | no |
| 5a-C | 3 | decayed linear attention | 0.869 | 0.000 | 0.9917 | 0.515 | no |
| 5a-C | 4 | decayed linear attention | 0.878 | 0.001 | 0.9966 | 0.512 | no |
| 5a-C | 5 | unclassified | 0.906 | 0.002 | 0.9818 | 0.512 | no |
| 5a-C | 6 | decayed linear attention | 0.884 | 0.000 | 0.9992 | 0.514 | no |
| 5a-C | 7 | delta rule | 1.000 | 0.498 | 0.9962 | 0.622 | yes |
| 5a-C | 8 | unclassified | 0.868 | -0.002 | 0.9742 | 0.509 | no |
| 5a-C | 9 | decayed linear attention | 0.876 | -0.000 | 1.0000 | 0.506 | no |
| 5a-C | 10 | decayed linear attention | 0.874 | 0.000 | 0.9955 | 0.509 | no |
| 5a-C | 11 | decayed linear attention | 0.880 | -0.001 | 0.9907 | 0.509 | no |
| 5a-C | 12 | decayed linear attention | 0.869 | 0.000 | 0.9918 | 0.510 | no |
| 5a-C | 13 | decayed linear attention | 0.873 | 0.000 | 0.9930 | 0.511 | no |
| 5a-C | 14 | unclassified | 0.907 | 0.152 | 0.9280 | 0.532 | no |
| 5a-C | 15 | decayed linear attention | 0.878 | 0.001 | 0.9934 | 0.512 | no |
| 5a-C | 16 | unclassified | 0.999 | 0.469 | 0.9716 | 0.625 | yes |
