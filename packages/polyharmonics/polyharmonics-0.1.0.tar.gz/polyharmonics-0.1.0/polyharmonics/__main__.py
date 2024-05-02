# type: ignore[attr-defined]
from enum import Enum
from time import time
from typing import Optional

import typer
from rich.console import Console
from sympy import Symbol, latex, limit, pretty

from polyharmonics import associated_legendre, legendre, version

SUB = str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉")
SUP = str.maketrans("-0123456789", "⁻⁰¹²³⁴⁵⁶⁷⁸⁹")
X = Symbol("x")


class Color(str, Enum):
    white = "white"
    red1 = "red"
    cyan1 = "cyan"
    magenta1 = "magenta"
    yellow1 = "yellow"
    green1 = "green"


app = typer.Typer(
    name="polyharmonics",
    help="Ortogonal Polynomials in the unit sphere.",
    add_completion=False,
)
console = Console()


def version_callback(print_version: bool) -> None:
    """Print the version of the package."""
    if print_version:
        console.print(f"[yellow]polyharmonics[/] version: [bold blue]{version}[/]")
        raise typer.Exit()


@app.callback()
def main(
    version: Optional[bool] = typer.Option(
        None,
        "-v",
        "--version",
        callback=version_callback,
        is_eager=True,
        help="Prints the version of the polyharmonics package.",
    ),
):
    pass


@app.command(name="legendre")
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
    result = legendre(n_values)

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


@app.command(name="associated-legendre")
def associated_legendre_command(
    nm: str = typer.Argument(
        ...,
        help="""The corresponding subscript and superscript of the function(s).
        Either a pair of integers separated by ':' or a comma-separated list of such pairs.""",  # noqa: E501
        metavar="SUB:SUP",
    ),
    print_latex: bool = typer.Option(
        False,
        "-l",
        "--latex",
        case_sensitive=False,
        help="Print the function(s) in LaTeX format.",
    ),
    evaluate: str = typer.Option(
        None,
        "-x",
        "--eval",
        case_sensitive=False,
        help="""Print the function(s) evaluated on the given numbers.
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
    """Calculate and print the Associated Legendre function(s)."""

    # Convert the input to two lists of integers
    try:
        n_values = []
        m_values = []
        for value in nm.split(","):
            n, m = value.split(":")
            n_values.append(int(n))
            m_values.append(int(m))
        if n is None or m is None or n == "" or m == "":
            raise typer.BadParameter(
                "Between each ',' must be a pair of integers separated by ':'."
            )
        if any(i < 0 for i in n_values):
            raise typer.BadParameter("All subscripts must be greater or equal to 0.")
    except ValueError:
        raise typer.BadParameter(
            "nm must either be a pair of integers separated by ':' or a list of such pairs separated by commas."  # noqa: E501
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

    # Calculate the Associated Legendre function(s)
    result = associated_legendre(n_values, m_values)

    if display_time:
        t_end = time()
        console.print(
            f"[bold green1]Done! [/][bold]Time taken: {t_end - t_start:.6f} seconds[/]\n"  # noqa: E501
        )

    for n, m, fun in zip(n_values, m_values, result):
        if print_latex:
            console.print(f"[bold {color}]P_{n}^{m}(x) = {latex(fun)}[/]\n")
        else:
            console.print(
                f"[bold {color}]P{str(n).translate(SUB)}{str(m).translate(SUP)}(x) = [/]"  # noqa: E501
            )
            console.print(
                f"[bold {color}] {pretty(fun)}[/]\n",
            )
        if x_values:
            for x in x_values:
                if abs(x) != 1:
                    console.print(
                        f"[bold {color}]P{str(n).translate(SUB)}{str(m).translate(SUP)}({x}) = {fun.subs(X, x)}[/]\n"  # noqa: E501
                    )
                else:
                    console.print(
                        f"[bold {color}]P{str(n).translate(SUB)}{str(m).translate(SUP)}({x}) = {limit(fun, X, x)}[/]\n"  # noqa: E501
                    )


if __name__ == "__main__":
    app()
