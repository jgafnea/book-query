import argparse
import sys

from .display import console, display
from .search import search


def main():
    parser = argparse.ArgumentParser(
        description="Search LibGen and return download links"
    )
    parser.add_argument("title", type=str, help="Title of book to search for")

    args = parser.parse_args()
    book_title = args.title

    try:
        results = search(book_title)
        if not results:
            console.print(f"[bold yellow]No results: [/][bold]'{book_title}'[/]")
            sys.exit(1)

        display(results)

    except KeyboardInterrupt:
        console.print("[red]Search canceled by user.[/]")
        sys.exit(130)

    except Exception as e:
        console.print(f"[bold red]An error occurred:[/] {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
