#!/usr/bin/env python3
"""Exact verification of the numerical certificates in Appendix A of
X.-N. Lu and M. Sawa, "Paired Constructions and Rational Gaussian Designs".

The data are read from data/appendix_data.json. All arithmetic is exact
(integers and fractions.Fraction). Run with --verbose to list every check.
"""

from fractions import Fraction
import json
from pathlib import Path
import sys

DATA = Path(__file__).resolve().parent / "data" / "appendix_data.json"
VERBOSE = "--verbose" in sys.argv[1:]


def check(condition, message):
    if not condition:
        sys.exit(f"FAIL: {message}")


def report(message):
    if VERBOSE:
        print(f"[OK] {message}")


def gaussian_moment(k):
    """k-th moment of exp(-x^2)/sqrt(pi) dx: (k-1)!!/2^(k/2) for even k, 0 for odd k."""
    if k % 2:
        return Fraction(0)
    double_factorial = 1
    for j in range(1, k, 2):
        double_factorial *= j
    return Fraction(double_factorial, 2 ** (k // 2))


def points_of(row):
    """X(A,d) = {+-a/d : a in A}, together with 0 when the order is odd (H(A,d))."""
    d = row["denominator"]
    points = {Fraction(s * a, d) for a in row["positive_numerators"] for s in (1, -1)}
    if row["order"] % 2:
        points.add(Fraction(0))
    return points


def verify_design(label, row, degree):
    """n distinct points, and 2^(r+1) sum_{a in A} a^(2r) = (2r-1)!! n d^(2r) for 2r <= degree.

    Odd moments vanish because the point set is antipodal.
    """
    n, d, A = row["order"], row["denominator"], row["positive_numerators"]
    check(len(points_of(row)) == n, f"{label}: not {n} distinct points")
    for k in range(2, degree + 1, 2):
        r = k // 2
        lhs = 2 ** (r + 1) * sum(a**k for a in A)
        rhs = gaussian_moment(k) * 2**r * n * d**k
        check(lhs == rhs, f"{label}: moment {k} is wrong")
    report(f"{label}: Gaussian {degree}-design with {n} points")


def verify_union(label, first, second, order, degree):
    """The two components are disjoint and their union has the Gaussian moments."""
    points = points_of(first) | points_of(second)
    check(len(points) == first["order"] + second["order"] == order,
          f"{label}: not a disjoint union with {order} points")
    for k in range(degree + 1):
        mean = sum((x**k for x in points), Fraction(0)) / order
        check(mean == gaussian_moment(k), f"{label}: moment {k} is wrong")
    report(f"{label}: Gaussian {degree}-design with {order} points")


def verify_paired(label, entry, degree, order, quarter_turn):
    """All mixed moments of total degree <= degree equal those of gamma x gamma."""
    d = entry["denominator"]
    points = set()
    for a, b in entry["integer_representatives"]:
        x, y = Fraction(a, d), Fraction(b, d)
        points |= {(x, y), (-x, -y)}
        if quarter_turn:
            points |= {(-y, x), (y, -x)}
    check(len(points) == order, f"{label}: not {order} distinct points")
    count = 0
    for r in range(degree + 1):
        for s in range(degree + 1 - r):
            mean = sum((u**r * v**s for u, v in points), Fraction(0)) / order
            check(mean == gaussian_moment(r) * gaussian_moment(s),
                  f"{label}: mixed moment ({r},{s}) is wrong")
            count += 1
    report(f"{label}: {order} points, {count} mixed moments")
    return count


def verify_orders(data, designs, table5_orders):
    """The finite ranges of orders used in the proofs of the main theorems."""
    # Degree 5: Table 1, Table 2, and the 7-designs used as 5-designs.
    five = ({row["order"] for row in data["table_1"].values()}
            | {u["order"] for u in data["table_2_unions"]}
            | {designs[label]["order"] for label in data["five_data_7_design_labels"]})
    check({n for n in five if 28 <= n <= 71} == {28, 32, 34} | set(range(36, 72)),
          "degree 5: orders 28, 32, 34 and 36..71 are not all covered")

    # Degree 7, orders 55..128: Table 3 (without the primed alternatives),
    # Table 4, and the projections of P7 (order 112); every order not in N.
    N = set(data["seven_nonexistence_orders_N"])
    seven = ({row["order"] for label, row in data["table_3"].items() if not label.endswith("p")}
             | {u["order"] for u in data["table_4_unions"]} | {112})
    check({n for n in seven if n <= 128} == set(range(55, 129)) - N,
          "degree 7: orders 55..128 outside N are not all covered")

    # Degree 7, orders 129..240: n - 112 from above, the direct designs, or Table 5.
    shifted = {n for n in range(129, 241) if n - 112 >= 55 and n - 112 not in N}
    direct = {designs[label]["order"] for label in data["seven_large_direct_labels"]}
    check(shifted | direct | table5_orders == set(range(129, 241)),
          "degree 7: orders 129..240 are not all covered")
    return len(N), len(shifted), len(direct), len(table5_orders)


def main():
    data = json.loads(DATA.read_text(encoding="utf-8"))
    five, seven = data["table_1"], data["table_3"]
    designs = {**five, **seven}

    for label, row in five.items():
        verify_design(label, row, 5)
    for label, row in seven.items():
        verify_design(label, row, 7)

    for table, degree in (("table_2_unions", 5), ("table_4_unions", 7)):
        for u in data[table]:
            a, b = u["components"]
            verify_union(f"{a} + {b}", designs[a], designs[b], u["order"], degree)

    table5 = []
    for rule in data["table_5_union_rules"]:
        a = rule["first"]
        for b in rule["seconds"]:
            n = seven[a]["order"] + seven[b]["order"]
            verify_union(f"{a} + {b}", seven[a], seven[b], n, 7)
            table5.append(n)

    p5 = verify_paired("P5", data["paired_P5"], 5, 36, quarter_turn=False)
    p7 = verify_paired("P7", data["paired_P7"], 7, 112, quarter_turn=True)
    excluded, shifted, direct, unions = verify_orders(data, designs, set(table5))

    n2, n4 = len(data["table_2_unions"]), len(data["table_4_unions"])
    print("PASS: exact verification of the certificates in Appendix A of Lu and Sawa")
    print(f"  Table 1: {len(five)} Gaussian 5-designs")
    print(f"  Table 3: {len(seven)} Gaussian 7-designs")
    print(f"  Tables 2, 4, 5: {n2 + n4 + len(table5)} disjoint unions ({n2} + {n4} + {len(table5)})")
    print(f"  P5: 36 distinct pairs, {p5} exact mixed moments")
    print(f"  P7: 112 distinct pairs, {p7} exact mixed moments")
    print("  Orders, degree 5: 28, 32, 34 and every order 36..71")
    print(f"  Orders, degree 7: every order 55..128 except the {excluded} orders in N")
    print(f"  Orders, degree 7: 129..240 = {shifted} shifted + {direct} direct + {unions} unions")


if __name__ == "__main__":
    main()
