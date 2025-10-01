from unittest.mock import patch

import pytest
from bq.cli import main


def test_no_arguments(capsys):
    """Test exit wth error if no argument is passed."""
    test_args = ["bq"]

    with patch("sys.argv", test_args):
        with pytest.raises(SystemExit) as e:
            main()

    assert e.value.code != 0

    captured_out, captured_err = capsys.readouterr()
    assert "usage:" in captured_out or captured_err


@patch("bq.cli.console.print")
@patch("bq.cli.search", return_value=[])
def test_book_not_found(mock_search, mock_print):
    test_args = ["bq", "Book 404"]

    with patch("sys.argv", test_args):
        with pytest.raises(SystemExit) as e:
            main()

    mock_search.assert_called_once_with("Book 404")
    mock_print.assert_called_once_with(
        "[bold yellow]No results: [/][bold]'Book 404'[/]"
    )
    assert e.value.code == 1


@patch("bq.cli.display")
@patch("bq.cli.search", return_value=[{"title": "Book 200"}])
def test_book_found(mock_search, mock_display):
    test_args = ["bq", "Book 200"]
    with patch("sys.argv", test_args):
        main()

    mock_search.assert_called_once_with("Book 200")
    mock_display.assert_called_once_with([{"title": "Book 200"}])


@patch("bq.cli.search", side_effect=KeyboardInterrupt)
@patch("bq.cli.console.print")
def test_keyboard_interrupt(mock_print, mock_search):
    test_args = ["bq", "Any Book"]
    with patch("sys.argv", test_args):
        with pytest.raises(SystemExit) as e:
            main()

    mock_print.assert_called_once_with("[red]Search canceled by user.[/]")
    assert e.value.code == 130


@patch("bq.cli.search", side_effect=Exception)
@patch("bq.cli.console.print")
def test_unhandled_exception(mock_print, mock_search):
    test_args = ["bq", "Any Book"]
    with patch("sys.argv", test_args):
        with pytest.raises(SystemExit) as e:
            main()

    mock_print.assert_called_once()
    assert "An error occurred:" in mock_print.call_args[0][0]
    assert e.value.code == 1
