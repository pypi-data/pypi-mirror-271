from typing import List, Union

from sympy import Expr, Rational, Symbol, diff, expand, factor, factorial, radsimp

from .legendre_polynomials import legendre_def, legendre_rec

x = Symbol("x")

LEGENDRE_FUNC_STORE_DEF: List[List[Expr]] = []
LEGENDRE_FUNC_STORE_REC: List[List[Expr]] = []


def associated_legendre_def(
    n: int, m: int, store: bool = True, use_legendre_def: bool = False
):
    if abs(m) > n:
        return x * 0

    if m < 0:
        return (
            (1 if m % 2 == 0 else -1)
            * factorial(n - m)
            / factorial(n + m)
            * associated_legendre_def(
                n, -m, store=store, use_legendre_def=use_legendre_def
            )
        )

    if store:
        for i in range(len(LEGENDRE_FUNC_STORE_DEF), n + 1):
            LEGENDRE_FUNC_STORE_DEF.append(
                [
                    (
                        legendre_rec(i, store=store)
                        if not use_legendre_def
                        else legendre_def(i, store=store)
                    )
                ]
            )
        for i in range(len(LEGENDRE_FUNC_STORE_DEF[n]), m + 1):
            LEGENDRE_FUNC_STORE_DEF[n].append(
                expand(diff(LEGENDRE_FUNC_STORE_DEF[n][i - 1], x, 1))
            )
        return expand((1 - x**2) ** Rational(m, 2) * LEGENDRE_FUNC_STORE_DEF[n][m])
    else:
        return expand(
            (1 - x**2) ** Rational(m, 2)
            * diff(
                (
                    legendre_rec(n, store=store)
                    if not use_legendre_def
                    else legendre_def(n, store=store)
                ),
                x,
                m,
            )
        )


# HIGHLY INNEFICIENT, USE ONLY FOR TESTING WITH SMALL VALUES OF n AND m
def associated_legendre_rec(
    n: int,
    m: int,
    store: bool = True,
    use_legendre_def: bool = False,
    callback: bool = False,
):
    if abs(m) > n:
        return x * 0

    if m == 0 or m == 1:
        if callback and m == 1:
            return (
                associated_legendre_def(
                    n, 1, store=store, use_legendre_def=use_legendre_def
                ),
                associated_legendre_def(
                    n, 0, store=store, use_legendre_def=use_legendre_def
                ),
            )

        else:
            return associated_legendre_def(
                n, m, store=store, use_legendre_def=use_legendre_def
            )

    elif m < 0:
        return (
            (1 if m % 2 == 0 else -1)
            * factorial(n - m)
            / factorial(n + m)
            * associated_legendre_rec(
                n, -m, store=store, use_legendre_def=use_legendre_def
            )
        )

    else:
        if store:
            for i in range(len(LEGENDRE_FUNC_STORE_REC), n + 1):
                LEGENDRE_FUNC_STORE_REC.append(
                    [
                        (
                            legendre_rec(i, store=store)
                            if not use_legendre_def
                            else legendre_def(i, store=store)
                        )
                    ]
                )
            for i in range(len(LEGENDRE_FUNC_STORE_REC[n]), m):
                LEGENDRE_FUNC_STORE_REC[n].append(
                    associated_legendre_rec(n, i, store=store)
                )
            LEGENDRE_FUNC_STORE_REC[n].append(
                expand(
                    (
                        2
                        * (m - 1)
                        * x
                        * (1 - x**2) ** Rational(-1, 2)
                        * LEGENDRE_FUNC_STORE_REC[n][m - 1]
                        - (n + m - 1) * (n - m + 2) * LEGENDRE_FUNC_STORE_REC[n][m - 2]
                    ),
                    deep=True,
                    mul=True,
                    multinomial=False,
                    power_exp=False,
                    power_base=False,
                    log=False,
                ),
            )
            return LEGENDRE_FUNC_STORE_REC[n][m]
        else:
            curr_fun, prev_fun = associated_legendre_rec(
                n, m - 1, store=store, callback=True
            )
            if callback:
                return (
                    expand(
                        (
                            2 * (m - 1) * x * (1 - x**2) ** Rational(-1, 2) * curr_fun
                            - (n + m - 1) * (n - m + 2) * prev_fun
                        ),
                        deep=True,
                        mul=True,
                        multinomial=False,
                        power_exp=False,
                        power_base=False,
                        log=False,
                    ),
                    curr_fun,
                )
            else:
                return expand(
                    (
                        2 * (m - 1) * x * (1 - x**2) ** Rational(-1, 2) * curr_fun
                        - (n + m - 1) * (n - m + 2) * prev_fun
                    ),
                    deep=True,
                    mul=True,
                    multinomial=False,
                    power_exp=False,
                    power_base=False,
                    log=False,
                )


def associated_legendre(
    n: Union[int, List[int]], m: Union[int, List[int]]
) -> Union[Expr, List[Expr]]:
    """
    Calculate the analytical expression of the Associated legendre function(s)

    Args:
        n (Union[int, List[int]]): The subscript of the function(s).
        Must be an integer or a list of integers greater than or equal to 0.
        m (Union[int, List[int]]): The superscript of the function(s).
        Must be an integer or a list of integers.

    Returns:
        Union[Expr, List[Expr]]: The Associated legendre function(s) of the given subscript(s) and superscript(s).

    Examples:
        .. code:: python

            >>> associated_legendre(1, 0)
            x
            >>> associated_legendre([1, 1], [0, 1])
            [x, (1 - x**2)**(1/2)]
    """  # noqa: E501
    if isinstance(n, int) and isinstance(m, int):
        if n < 0:
            raise ValueError("Subscript n must be greater than or equal to 0")
        return associated_legendre_def(n, m, store=False)
    elif isinstance(n, list) and isinstance(m, list) and len(n) == len(m):
        if any(i < 0 for i in n):
            raise ValueError("All subscripts n must be greater than or equal to 0")
        store: bool = len(n) > 1
        return [associated_legendre_def(i, j, store=store) for i, j in zip(n, m)]
    else:
        raise TypeError(
            "n and m must both be integers or lists of integers of the same length"
        )
