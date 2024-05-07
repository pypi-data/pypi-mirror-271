from typing import List

from sympy import (
    Expr,
    Rational,
    Symbol,
    cos,
    diff,
    expand,
    factorial,
    sin,
    trigsimp,
)

from .legendre_polynomials import legendre_def, legendre_rec

x = Symbol("x")
th = Symbol("θ")


class AssLegendreStore:
    def __init__(self):
        self.reset()

    def reset(self, definition=True, recursion=True):
        # Stores differentiation of the Legendre polynomials when using def
        if definition:
            self.definition: List[List[Expr]] = []

        # Stores the Legendre functions when using rec
        if recursion:
            self.recursion: List[List[Expr]] = []


ass_legendre_store = AssLegendreStore()


def associated_legendre_def(
    n: int,
    m: int,
    polar: bool = False,
    store: bool = True,
    use_legendre_def: bool = False,
):
    if abs(m) > n:
        return x * 0

    if m < 0:
        return (
            (1 if m % 2 == 0 else -1)
            * factorial(n - m)
            / factorial(n + m)
            * associated_legendre_def(n, -m, store=store, use_legendre_def=use_legendre_def)
        )

    fun: Expr = None
    if store:
        for i in range(len(ass_legendre_store.definition), n + 1):
            ass_legendre_store.definition.append(
                [
                    (
                        legendre_rec(i, store=store)
                        if not use_legendre_def
                        else legendre_def(i, store=store)
                    )
                ]
            )
        for i in range(len(ass_legendre_store.definition[n]), m + 1):
            ass_legendre_store.definition[n].append(
                expand(diff(ass_legendre_store.definition[n][i - 1], x, 1))
            )
        fun = expand((1 - x**2) ** Rational(m, 2) * ass_legendre_store.definition[n][m])
    else:
        fun = expand(
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

    if polar:
        return trigsimp(fun.subs((1 - x**2) ** Rational(1, 2), sin(th)).subs(x, cos(th)))
    else:
        return fun


def associated_legendre_rec(
    n: int,
    m: int,
    polar: bool = False,
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
                    n, 1, polar=False, store=store, use_legendre_def=use_legendre_def
                ),
                associated_legendre_def(
                    n, 0, polar=False, store=store, use_legendre_def=use_legendre_def
                ),
            )

        else:
            fun: Expr = associated_legendre_def(
                n, m, polar=polar, store=store, use_legendre_def=use_legendre_def
            )
            if (
                store
                and len(ass_legendre_store.recursion) > n
                and len(ass_legendre_store.recursion[n]) == m
            ):
                ass_legendre_store.recursion[n].append(fun)
            return fun

    elif m < 0:
        return (
            (1 if m % 2 == 0 else -1)
            * factorial(n - m)
            / factorial(n + m)
            * associated_legendre_rec(
                n, -m, polar=polar, store=store, use_legendre_def=use_legendre_def
            )
        )

    else:
        if store:
            for i in range(len(ass_legendre_store.recursion), n + 1):
                ass_legendre_store.recursion.append(
                    [
                        associated_legendre_def(
                            i,
                            0,
                            polar=False,
                            store=store,
                            use_legendre_def=use_legendre_def,
                        )
                    ]
                )
            for i in range(len(ass_legendre_store.recursion[n]), m):
                associated_legendre_rec(
                    n,
                    i,
                    polar=False,
                    store=store,
                    use_legendre_def=use_legendre_def,
                )
            ass_legendre_store.recursion[n].append(
                expand(
                    (
                        2
                        * (m - 1)
                        * x
                        * (1 - x**2) ** Rational(-1, 2)
                        * ass_legendre_store.recursion[n][m - 1]
                        - (n + m - 1) * (n - m + 2) * ass_legendre_store.recursion[n][m - 2]
                    ),
                    deep=True,
                    mul=True,
                    multinomial=False,
                    power_exp=False,
                    power_base=False,
                    log=False,
                ),
            )
            if polar:
                return trigsimp(
                    ass_legendre_store.recursion[n][m]
                    .subs((1 - x**2) ** Rational(1, 2), sin(th))
                    .subs(x, cos(th))
                )
            else:
                return ass_legendre_store.recursion[n][m]
        else:
            curr_fun, prev_fun = associated_legendre_rec(
                n, m - 1, polar=False, store=store, callback=True
            )
            fun: Expr = expand(
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
            if polar and not callback:
                fun = trigsimp(
                    fun.subs((1 - x**2) ** Rational(1, 2), sin(th)).subs(x, cos(th))
                )
            elif callback:
                return (
                    fun,
                    curr_fun,
                )
            else:
                return fun


def associated_legendre(n: int, m: int, polar: bool = False) -> Expr:
    """
    Calculate the analytical expression of the Associated legendre function

    Args:
        n (int): The subscript of the function.
        Must be an integer greater than or equal to 0.
        m (int): The superscript of the function.
        Must be an integer.
        polar (bool): If True, the function is returned in polar coordinates.

    Returns:
        Expr: The Associated legendre function for the given subscript and superscript.

    Examples:
        .. code:: python

            >>> associated_legendre(1, 0)
            x
            >>> associated_legendre(1, 1, polar=True)
            sin(θ)
    """  # noqa: E501
    if isinstance(n, int) and isinstance(m, int):
        if n < 0:
            raise ValueError("n must be greater than or equal to 0")
        return associated_legendre_def(n, m, polar=polar, store=True)
    else:
        raise TypeError("n and m must both be integers")
