from typing import List, Union

from sympy import Expr, Rational, diff, expand, factorial, symbols

x, t = symbols("x t")

gen_Legendre: Expr = (1 - 2 * x * t + t**2) ** Rational(-1, 2)

# Where the differentiation of the generating function is stored when using legendre_def
LEGENDRE_DEF_STORE: List[Expr] = [
    (1 - 2 * x * t + t**2) ** Rational(-1, 2),
    -(1 / 2) * (2 * t - 2 * x) * (1 - 2 * x * t + t**2) ** Rational(-3, 2),
]

# Where the Legendre polynomials are stored when using legendre_rec
LEGENDRE_REC_STORE: List[Expr] = [x**0, x**1]


def legendre_def(n: int, store: bool = True, callback: bool = False):
    if n == 0:
        return x**0
    elif n == 1:
        return x**1
    else:
        if store:
            # If the previous polynomials are not stored, calculate and store them
            if len(LEGENDRE_DEF_STORE) <= n:
                if len(LEGENDRE_DEF_STORE) < n:
                    legendre_def(n - 1, store=True, callback=True)
                LEGENDRE_DEF_STORE.append(diff(LEGENDRE_DEF_STORE[n - 1], t, 1))
            # If the function is called by itself to store
            # the previous polynomials, don't return them
            if callback:
                return None
            else:
                # The fractions are converted to floats
                # subs is the problem but don't know why
                return expand(
                    (1 / factorial(n)) * LEGENDRE_DEF_STORE[n].subs(t, 0),
                    deep=True,
                    mul=True,
                    multinomial=False,
                    power_exp=False,
                    power_base=False,
                    log=False,
                )
        else:
            return expand(
                (1 / factorial(n)) * diff(gen_Legendre, t, n).subs(t, 0),
                deep=True,
                mul=True,
                multinomial=False,
                power_exp=False,
                power_base=False,
                log=False,
            )


def legendre_rec(n: int, store: bool = True, callback: bool = False):
    if n == 0:
        return x**0
    elif n == 1:
        if callback:
            return x**1, x**0
        else:
            return x**1
    else:
        if store:
            if len(LEGENDRE_REC_STORE) <= n:
                if len(LEGENDRE_REC_STORE) < n:
                    legendre_rec(n - 1, store=store)
                LEGENDRE_REC_STORE.append(
                    expand(
                        (
                            (2 * n - 1) * x * LEGENDRE_REC_STORE[n - 1]
                            - (n - 1) * LEGENDRE_REC_STORE[n - 2]
                        )
                        / n,
                        deep=True,
                        mul=True,
                        multinomial=False,
                        power_exp=False,
                        power_base=False,
                        log=False,
                    ),
                )
            return LEGENDRE_REC_STORE[n]
        else:
            curr_pol, prev_pol = legendre_rec(n - 1, store=store, callback=True)
            if callback:
                return (
                    expand(
                        ((2 * n - 1) * x * curr_pol - (n - 1) * prev_pol) / n,
                        deep=True,
                        mul=True,
                        multinomial=False,
                        power_exp=False,
                        power_base=False,
                        log=False,
                    ),
                    curr_pol,
                )
            else:
                return expand(
                    ((2 * n - 1) * x * curr_pol - (n - 1) * prev_pol) / n,
                    deep=True,
                    mul=True,
                    multinomial=False,
                    power_exp=False,
                    power_base=False,
                    log=False,
                )


def legendre(n: Union[int, List[int]]) -> Union[Expr, List[Expr]]:
    """
    Calculate the analytical expression of the Legendre polynomials

    Args:
        n (Union[int, List[int]]): The degree of the Legendre polynomial(s).
        Must be an integer or a list of integers greater than or equal to 0.

    Returns:
        Union[Expr, List[Expr]]: The Legendre polynomial(s) of the given degree(s).

    Examples:
        .. code:: python

            >>> legendre(1)
            x
            >>> legendre([0, 1])
            [1, x]
    """  # noqa: E501
    if isinstance(n, int):
        if n < 0:
            raise ValueError("Degree n must be greater than or equal to 0")
        return legendre_rec(n, store=False)
    elif isinstance(n, list):
        if any(i < 0 for i in n):
            raise ValueError("All degrees n must be greater than or equal to 0")
        store: bool = len(n) > 1
        return [legendre_rec(i, store=store) for i in n]
    else:
        raise TypeError("n must be an integer or a list of integers")
