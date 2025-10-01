from rich import box
from rich.console import Console
from rich.table import Table

console = Console()


def display(results) -> None:
    # https://rich.readthedocs.io/en/stable/appendix/colors.html
    table = Table(title="", box=box.SIMPLE_HEAD)

    table.add_column("Title", style="bright_cyan")
    table.add_column("Year", style="bright_magenta")
    table.add_column("Author", style="yellow")
    table.add_column("Ext", style="green")
    table.add_column("Size", style="dim", justify="right")
    table.add_column("Download", style="blue")

    for book in results:
        table.add_row(
            book.title,
            book.year,
            book.author,
            book.extension,
            book.size,
            book.download,
        )

    console.print(table)
