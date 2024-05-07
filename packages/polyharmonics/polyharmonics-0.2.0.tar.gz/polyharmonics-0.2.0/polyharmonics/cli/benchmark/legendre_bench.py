import time
from multiprocessing import Process

import typer
from prettytable import PrettyTable
from rich.console import Console
from rich.status import Status

from polyharmonics.legendre_polynomials import (
    legendre_def,
    legendre_rec,
    legendre_store,
)

SUB = str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉")
console = Console()


def legendre_bench_command(
    n: str = typer.Argument(
        ...,
        help="""Calculate the Legendre polynomials from 0 to the given degree.
        An integer or a comma-separated list of integers.""",
        metavar="DEGREE",
    ),
    max_time: float = typer.Option(
        60.0,
        "--max-time",
        case_sensitive=False,
        help="Maximum execution time in seconds for each calculation. Default is 60 seconds.",  # noqa: E501
    ),
    csv: str = typer.Option(
        None,
        "--csv",
        case_sensitive=False,
        help="""Save the results in a CSV file with the given name.
        File extension must not be specified.""",
    ),
) -> None:
    """Benchmark the calculation of Legendre polynomials and display the time taken."""  # noqa: E501

    # Convert the Legendre input to a list of integers
    try:
        n_values = sorted([int(value) for value in n.split(",")])
        if any(i < 0 for i in n_values):
            raise typer.BadParameter(
                "All integers must be greater or equal to 0."  # noqa: E501
            )
    except ValueError:
        raise typer.BadParameter(
            "n must be an integer or a comma-separated list of integers."  # noqa: E501
        )

    with console.status(status="", spinner="dots") as status:
        status: Status
        table = PrettyTable()
        n_tests = 4
        table.field_names = [
            "N",
            "Definition w storage",
            "Definition w/o storage",
            "Recursion w storage",
            "Recursion w/o storage",
        ]

        # List for each test to indicate if it timed out
        timed_out = [False for _ in range(n_tests)]
        for i in n_values:
            # List of tests to run for each n of n_values
            tests = [
                {
                    "fun": calculate_legendre,
                    "args": (i, True, True),
                    "text": (
                        "Calculating all Legendre polynomials "
                        f"from P{str(0).translate(SUB)}(x) to P{str(i).translate(SUB)}(x) "
                        "with definition and storage."
                    ),
                },
                {
                    "fun": calculate_legendre,
                    "args": (i, True, False),
                    "text": (
                        "Calculating all Legendre polynomials "
                        f"from P{str(0).translate(SUB)}(x) to P{str(i).translate(SUB)}(x) "
                        "with definition but no storage."
                    ),
                },
                {
                    "fun": calculate_legendre,
                    "args": (i, False, True),
                    "text": (
                        "Calculating all Legendre polynomials "
                        f"from P{str(0).translate(SUB)}(x) to P{str(i).translate(SUB)}(x) "
                        "with recursion and storage."
                    ),
                },
                {
                    "fun": calculate_legendre,
                    "args": (i, False, False),
                    "text": (
                        "Calculating all Legendre polynomials "
                        f"from P{str(0).translate(SUB)}(x) to P{str(i).translate(SUB)}(x) "
                        "with recursion but no storage."
                    ),
                },
            ]
            assert len(tests) == n_tests
            row = [i]
            for n_test, test in enumerate(tests):
                status.update(f"[yellow1]{test['text']}[/]")
                if timed_out[n_test]:
                    row.append("TIMEOUT")
                else:
                    legendre_calc = Process(target=test["fun"], args=test["args"])
                    t_start = time.time()
                    legendre_calc.start()
                    while legendre_calc.is_alive():
                        if time.time() - t_start > max_time:
                            legendre_calc.terminate()
                            row.append("TIMEOUT")
                            timed_out[n_test] = True
                            break

                    if len(row) == n_test + 1:
                        row.append(time.time() - t_start)

            table.add_row(row)

    if csv is None:
        console.print("[bold green]LEGENDRE POLYNOMIALS UP TO N[/]")
        console.print(table)
    else:
        # Open the file in binary mode to avoid having multiple newlines
        with open(csv + ".csv", "wb") as f:
            f.write(table.get_csv_string().encode("utf-8"))

    raise typer.Exit()


def calculate_legendre(n: int, use_legendre_def: bool, store: bool):
    if store:
        # Reset the store to avoid following calculations to be faster than expected
        legendre_store.reset(definition=use_legendre_def, recursion=not use_legendre_def)
    values = range(n + 1)
    for i in values:
        if use_legendre_def:
            legendre_def(i, store=store)
        else:
            legendre_rec(i, store=store)
