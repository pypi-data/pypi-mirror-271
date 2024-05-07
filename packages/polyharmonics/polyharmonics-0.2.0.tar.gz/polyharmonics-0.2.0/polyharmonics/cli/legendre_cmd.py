from time import time
from typing import List, Optional

import typer
from rich.console import Console
from sympy import Expr, Symbol, latex, pretty

from polyharmonics import legendre

from .colors import Color

SUB = str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉")
X = Symbol("x")
console = Console()


def legendre_command(
    n: str = typer.Argument(
        ...,
        help="""The degree of the polynomial(s).
        An integer or a comma-separated list of integers.""",
        metavar="DEGREE",
    ),
    print_latex: bool = typer.Option(
        False,
        "-l",
        "--latex",
        case_sensitive=False,
        help="Print the polynomial(s) in LaTeX format.",
    ),
    evaluate: str = typer.Option(
        None,
        "-x",
        "--eval",
        case_sensitive=False,
        help="""Print the polynomial(s) evaluated on the given numbers.
        Either a number or a comma-separated list of numbers.""",
    ),
    color: Optional[Color] = typer.Option(
        Color.white,
        "-c",
        "--color",
        case_sensitive=False,
        help="Color for print. White if not specified.",
    ),
    display_time: bool = typer.Option(
        False,
        "-t",
        "--time",
        case_sensitive=False,
        help="Display the time taken to calculate the function(s).",
    ),
) -> None:
    """Calculate and print the Legendre polynomial(s)."""

    # Convert the input to a list of integers
    try:
        n_values = [int(value) for value in n.split(",")]
        if any(i < 0 for i in n_values):
            raise typer.BadParameter("All integers must be greater or equal to 0.")
    except ValueError:
        raise typer.BadParameter(
            "n must be an integer or a comma-separated list of integers."
        )

    x_values = []
    if evaluate is not None and evaluate != "":
        try:
            if isinstance(evaluate, float):
                x_values.append(evaluate)
            else:
                for value in evaluate.split(","):
                    x_values.append(float(value))
        except ValueError:
            raise typer.BadParameter(
                "x must either be a number or a list of numbers separated by commas."
            )

    if display_time:
        t_start = time()

    # Calculate the Legendre polynomial(s)

    with console.status(
        status=(
            "[yellow1]Calculating Legendre polynomials.[/]"
            if len(n_values) > 1
            else "[yellow1]Calculating Legendre polynomial.[/]"
        ),
        spinner="dots",
    ):
        result: List[Expr] = [legendre(i) for i in n_values]

    if display_time:
        t_end = time()
        console.print(
            f"[bold green1]Done! [/][bold]Time taken: {t_end - t_start:.6f} seconds[/]\n"  # noqa: E501
        )

    for n, pol in zip(n_values, result):
        if print_latex:
            console.print(f"[bold {color}]P_{n}(x) = {latex(pol)}[/]\n")
        else:
            console.print(f"[bold {color}]P{str(n).translate(SUB)}(x) = [/]")
            console.print(f"[bold {color}] {pretty(pol)}[/]\n")
        if x_values:
            for x in x_values:
                console.print(
                    f"[bold {color}]P{str(n).translate(SUB)}({x}) = {pol.subs(X, x)}[/]\n"  # noqa: E501
                )

    raise typer.Exit()
