from dataclasses import dataclass
from typing import Dict, List

from libgen_api import LibgenSearch
from pyshorteners import Shortener
from rich.progress import Progress

CONFIG = {
    "LANG_FILTER": {"Language": "English"},
    "FILE_FILTER": ("epub", "pdf"),
    # Limit to 5 for faster search and cleaner documentation.
    "MAX_RESULTS": 5,
}


@dataclass
class Book:
    title: str
    year: int
    author: str
    extension: str
    size: str
    download: str


def filter(results: List[Dict]) -> List[Dict]:
    """
    Filter and sort search results.
    """
    filtered = [
        r for r in results if r.get("Extension").lower() in CONFIG["FILE_FILTER"]
    ]
    filtered.sort(key=lambda r: r["Year"], reverse=True)

    return filtered[: CONFIG["MAX_RESULTS"]]


def search(query: str) -> List[Book]:
    """
    Search LibGen and return list of books.
    """
    libgen = LibgenSearch()

    initial = libgen.search_title_filtered(query, CONFIG["LANG_FILTER"])
    filtered = filter(initial)

    # Kinda silly but "results" makes more sense later on than "filtered".
    results = filtered

    books: List[Book] = []

    with Progress(transient=True) as progress:
        # Use len(results) for "work" so progress updates correctly.
        task = progress.add_task("Searching…", total=len(results))

        for book_data in results:
            try:
                # Resolve download link from mirror and shorten it.
                resolved = libgen.resolve_download_links(book_data)["GET"]
                download = Shortener().tinyurl.short(resolved)
            except Exception:
                # If no download link is found, skip book.
                continue

            # Add download link to book data. This could probably be done below but keeping it here for clarity.
            book_data["Download"] = download

            # Create new Book objects and add to list.
            book = Book(
                title=book_data.get("Title", ""),
                year=book_data.get("Year", 0),
                author=book_data.get("Author", ""),
                extension=book_data.get("Extension", ""),
                size=book_data.get("Size", ""),
                download=book_data.get("Download", ""),
            )
            books.append(book)

            # Update progress after each book.
            progress.update(task, advance=1)

    return books
