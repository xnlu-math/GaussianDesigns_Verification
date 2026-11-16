# Exact verification for *Paired Constructions and Rational Gaussian Designs*

This repository contains the numerical certificates for the explicit
examples in Appendix A of the paper

> Xiao-Nan Lu and Masanori Sawa,
> *Paired Constructions and Rational Gaussian Designs*, 2026.

It also contains a short, independent verifier that uses only exact arithmetic.
Every certificate checked here is listed explicitly in the paper, and the
verifier checks these certificates directly.

## Quick start

Requires **Python 3.9 or later**. No third-party packages are needed.

```sh
python3 verify_appendix.py
```

If every check succeeds, the script prints `PASS` with the verification counts.
If a check fails, it prints `FAIL` with the reason. To list every design and
union as it is checked:

```sh
python3 verify_appendix.py --verbose
```

## What is verified

The target probability measure is

$$
d\gamma(x) = \frac{e^{-x^2}}{\sqrt{\pi}} dx, \qquad
m_{2r}(\gamma) = \frac{(2r-1)!!}{2^r}, \qquad
m_{2r+1}(\gamma) = 0.
$$

For a set $A$ of positive integers and a positive integer $d$, Appendix A
defines

$$
\mathcal{X}(A,d) = \lbrace \pm a/d : a \in A \rbrace, \qquad
\mathcal{H}(A,d) = \lbrace 0 \rbrace \cup \mathcal{X}(A,d),
$$

with $n = 2|A|$ or $n = 2|A|+1$ points, respectively. For each design, the
verifier checks the order and the distinctness of the points, and then checks
the following identities in exact integer arithmetic:

$$
4\sum_{a \in A} a^2 = n d^2, \qquad
8\sum_{a \in A} a^4 = 3 n d^4, \qquad
16\sum_{a \in A} a^6 = 15 n d^6 \quad \text{(degree 7 only)}.
$$

Verification scope:

| Source in the paper | Certificates / checks |
| --- | ---: |
| Table 1 | 26 distinct degree-5 designs; exact moments through degree 5 |
| Table 3 | 55 distinct degree-7 designs; exact moments through degree 7 |
| Table 2 | 10 disjoint unions, including their exact moments |
| Table 4 | 6 disjoint unions, including their exact moments |
| Table 5 | 54 disjoint unions, including their exact moments |
| Proposition 4.1 | All 21 joint moment identities with $r+s \leq 5$ on the 36-point set $P_5$ |
| Proposition 5.1 | All 36 joint moment identities with $r+s \leq 7$ on the 112-point set $P_7$ |
| Theorems 1.1 and 1.2 | The complete degree-5 base interval $36 \leq n \leq 71$ and all permitted degree-7 orders $55 \leq n \leq 240$ |

For each union of two designs of orders $n_1$ and $n_2$, the verifier checks
that the two point sets are disjoint, that is, that the union has exactly
$n_1 + n_2$ points. It then computes every moment of the union up to the
relevant degree with exact fractions.

Coverage of the base orders is checked as follows:

- Degree 5: the initial orders 28, 32, 34 and every order from 36 to 71.
  The paper proves that these extend in steps of 36.
- Degree 7: every order from 55 to 128 except the 25 excluded orders listed in
  Theorem 1.2. As in the paper, order 112 is supplied by Theorem 5.2 (from
  $P_7$) rather than by an explicit example. The interval from 129 to 240 is
  split into 49 orders $n$ for which $n - 112$ is already covered, 9 direct
  examples, and 54 unions from Table 5. The paper proves that these extend in
  steps of 112.

Table, proposition, and theorem numbers refer to the version of the
paper that accompanies release `v1.0.0` of this repository.

## Repository contents

- `verify_appendix.py`: the verifier
- `data/appendix_data.json`: numerators, denominators, the point sets of
  Propositions 4.1 and 5.1, and the union recipes
- `CITATION.cff`: citation information
- `LICENSE`: MIT License

## Data format

Designs are referred to by their labels in the paper. For example, `X28` is
$X_{28}$ and `H37` is $H_{37}$. The label `X32tilde` denotes
$\widetilde{X}_{32}$, and a suffix `p` denotes a primed alternative, so `Z60p`
is $Z'_{60}$.

`data/appendix_data.json` contains the following entries:

- `table_1`, `table_3`: the designs of Tables 1 and 3. Each entry gives the
  order $n$, the denominator $d$, and the positive numerators $A$. The design
  is $\mathcal{X}(A,d)$ when $n$ is even and $\mathcal{H}(A,d)$ when $n$ is odd.
- `table_2_unions`, `table_4_unions`: the unions in Tables 2 and 4, each given
  by its order and its two components.
- `table_5_union_rules`: the rows of Table 5. In each row, the design `first`
  is combined with each design listed in `seconds`.
- `paired_P5`, `paired_P7`: the integer points $D_5$ and $D_7$ and the
  denominators $6$ and $30$ from Propositions 4.1 and 5.1.
- `seven_nonexistence_orders_N`: the 25 excluded orders $\mathcal{N}$ of
  Theorem 1.2.
- `seven_large_direct_labels`: the nine designs $Z_{129}, \dots, Z_{176}$ used
  directly for orders between 129 and 240.
- `five_data_7_design_labels`: the degree-7 designs $Z_{55}$, $Z_{56}$,
  $Z_{59}$, $Z_{63}$ from Table 3, which are also used as degree-5 designs.

## Citation

When referring to the examples or the certificates, please cite the paper
above. GitHub shows citation metadata from the included `CITATION.cff`.

## License

The code and data in this repository are released under the MIT License.
See [`LICENSE`](LICENSE) for the full text.
