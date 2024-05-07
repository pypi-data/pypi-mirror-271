from typing import List

from sympy import Expr, Rational, diff, expand, factorial, symbols

x, t = symbols("x t")
gen_Legendre: Expr = (1 - 2 * x * t + t**2) ** Rational(-1, 2)


class LegendreStore:
    def __init__(self):
        self.reset()

    def reset(self, definition=True, recursion=True):
        # Stores differentiation of the generating function when using def
        if definition:
            self.definition: List[Expr] = [
                (1 - 2 * x * t + t**2) ** Rational(-1, 2),
                -Rational(1, 2)
                * (2 * t - 2 * x)
                * (1 - 2 * x * t + t**2) ** Rational(-3, 2),
            ]

        # Stores the Legendre polynomials when using recursion
        if recursion:
            self.recursion: List[Expr] = [x**0, x**1]


legendre_store = LegendreStore()


def legendre_def(n: int, store: bool = True, callback: bool = False):
    if n == 0:
        return x**0
    elif n == 1:
        return x**1
    else:
        if store:
            # If the previous polynomials are not stored, calculate and store them
            if len(legendre_store.definition) <= n:
                if len(legendre_store.definition) < n:
                    legendre_def(n - 1, store=True, callback=True)
                legendre_store.definition.append(
                    diff(legendre_store.definition[n - 1], t, 1)
                )
            # If the function is called by itself to store
            # the previous polynomials, don't return them
            if callback:
                return None
            else:
                return expand(
                    (1 / factorial(n)) * legendre_store.definition[n].subs(t, 0),
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
            if len(legendre_store.recursion) <= n:
                if len(legendre_store.recursion) < n:
                    legendre_rec(n - 1, store=store)
                legendre_store.recursion.append(
                    expand(
                        (
                            (2 * n - 1) * x * legendre_store.recursion[n - 1]
                            - (n - 1) * legendre_store.recursion[n - 2]
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
            return legendre_store.recursion[n]
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


def legendre(n: int) -> Expr:
    """
    Calculate the analytical expression of the Legendre polynomial

    Args:
        n (int): The degree of the Legendre polynomial.
        Must be an integer greater than or equal to 0.

    Returns:
        Expr: The Legendre polynomial of the given degree.

    Examples:
        .. code:: python

            >>> legendre(0)
            1
            >>> legendre(1)
            x
    """  # noqa: E501
    if isinstance(n, int):
        if n < 0:
            raise ValueError("n must be greater than or equal to 0")
        return legendre_rec(n, store=True)
    else:
        raise TypeError("n must be an integer")
