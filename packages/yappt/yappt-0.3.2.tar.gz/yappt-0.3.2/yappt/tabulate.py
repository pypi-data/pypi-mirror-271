"tabulate (print in a grid) an iterable of either dataclass objects, or Sequences"

import sys
from dataclasses import fields, is_dataclass
from itertools import chain, islice, zip_longest
from typing import Any, Callable, Iterable, Optional, Sequence, TextIO, TypeVar

from .grid import GridStyle, iter_with_grid
from .types import Column, HAlign
from .util import DEFAULT_FMTSPEC

T = TypeVar("T")


def tabulate(
    rows: Iterable[Sequence[Any] | Any],
    headers: Optional[Sequence[str]] = None,
    types: Optional[Sequence[type]] = None,
    *,
    peek: int = 200,
    default_fmtspc: dict[type, str] = DEFAULT_FMTSPEC,
    grid_style: Optional[GridStyle] = None,
    default_grid_style: Optional[GridStyle] = None,
    file: TextIO = sys.stdout,
) -> None:
    """
    pretty print rows of data in tabular form

    Args:
        rows: iterable of dataclass instances or Sequences. All rows must be of same type
        headers: column titles, defaults to column number. valid only when row is a Sequence
        types: list of types, defaults to types from the first row. valid only when row is a Sequence
        peek: number of rows to look ahead to determine column widths, 0 to use the actual width. (default: 200 rows)
        default_fmtspec: a mapping of type to format-spec strings to serve as default format-spec by types
        grid_style: grid style to use. cannot be overriden using $GRID_SYTLE
        default_grid_style: grid style to use when $GRID_STYLE is not set

    Returns:
        None
    """
    for line in tabulate_iter(
        rows,
        headers,
        types,
        peek=peek,
        default_fmtspc=default_fmtspc,
        grid_style=grid_style,
        default_grid_style=default_grid_style,
    ):
        print(line, file=file)


def tabulate_iter(
    rows: Iterable[Sequence[Any] | Any],
    headers: Optional[Sequence[str]] = None,
    types: Optional[Sequence[type]] = None,
    *,
    peek: int = 200,
    default_fmtspc: dict[type, str] = DEFAULT_FMTSPEC,
    grid_style: Optional[GridStyle] = None,
    default_grid_style: Optional[GridStyle] = None,
) -> Iterable[str]:
    """
    accepts an Iterable of either dataclass instances or Sequences, and returns an Iterable of strings of data in a grid

    Args:
        rows: iterable of dataclass instances or Sequences. All rows must be of same type
        headers: column titles, defaults to column number. valid only when row is a Sequence
        types: list of types, defaults to types from the first row. valid only when row is a Sequence
        peek: number of rows to look ahead to determine column widths, 0 to use the actual width. (default: 200 rows)
        default_fmtspec: a mapping of type to format-spec strings to serve as default format-spec by types
        grid_style: grid style to use. cannot be overriden using $GRID_SYTLE
        default_grid_style: grid style to use when $GRID_STYLE is not set

    Returns:
        Iterable over formatted, aligned and tabulated strings
    """
    it = iter(rows)
    try:
        first = next(it)
    except StopIteration:
        return

    it = chain([first], it)
    if is_dataclass(first):
        cols, formatted_rows = formatted_obj_iter(it, first.__class__, default_fmtspc)  # type: ignore
    elif isinstance(first, Sequence):
        cols, formatted_rows = formatted_seq_iter(it, types or [type(c) for c in first], headers, default_fmtspc)
    else:
        raise TypeError(f"Input to tabulate() must be an Iterable of either dataclass or a Sequnce, not {type(first)}")

    it = chain([[m.title for m in cols]], formatted_rows)
    if peek > 0:
        it = aligned_seq_iter(it, [m.alignment for m in cols], peek + 1)  # +1 to adjust for the header row
    it = iter_with_grid(iter(it), num_headers=1, grid_style=grid_style, default_grid_style=default_grid_style)

    yield from it


def formatted_seq_iter(
    rows: Iterable[Sequence[Any]],
    types: Sequence[type[Any]],
    headers: Optional[Sequence[str]] = None,
    default_fmtspec: dict[type, str] = DEFAULT_FMTSPEC,
) -> tuple[list[Column[Any]], Iterable[Sequence[str]]]:
    if headers is None:
        headers = [f"_{e}" for e, _ in enumerate(types, start=1)]
    cols = [Column.from_type(h, t, default_fmtspec=default_fmtspec) for h, t in zip(headers, types)]
    xs = [(c.format, e) for e, c in enumerate(cols)]

    def as_seq(o: Sequence[str]) -> list[str]:
        return [f(o[e]) for f, e in xs]

    return (cols, (as_seq(o) for o in rows))


def formatted_obj_iter(
    rows: Iterable[T], DC_Type: type[T], default_fmtspec: dict[type, str] = {}
) -> tuple[list[Column[Any]], Iterable[Sequence[str]]]:
    cols = Column.from_dataclass(DC_Type, default_fmtspec)
    attrs = [f.name for f in fields(DC_Type)]  # type: ignore
    xs = [(c.format, n) for c, n in zip(cols, attrs)]

    def as_seq(o: T) -> list[str]:
        return [f(getattr(o, a)) for f, a in xs]

    return (cols, (as_seq(o) for o in rows))


def aligned_seq_iter(rows: Iterable[Sequence[str]], alignments: list[HAlign], peek: int = 200) -> Iterable[list[str]]:
    "Accepts an Iterable of sequences of text, and returns an iterable of sequence of aligned texts"

    def splitcols(row: Sequence[str]) -> Iterable[Sequence[str]]:
        return zip_longest(*(col.split("\n") for col in row), fillvalue="")

    def aligner(a: HAlign, w: int) -> Callable[[str], str]:
        def wrapped(v: str) -> str:
            return a.align(v, w)

        return wrapped

    buffered = [y for x in islice(rows, 0, peek) for y in splitcols(x)]
    widths = [max(map(len, c)) for c in zip(*buffered)]
    _rows = chain(buffered, (y for x in rows for y in splitcols(x)))

    aligners = [aligner(a, w) for a, w in zip(alignments, widths)]
    yield from ([f(c) for f, c in zip(aligners, r)] for r in _rows)
