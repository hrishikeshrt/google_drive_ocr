#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Utility Functions
"""

import os
import logging
from collections.abc import Iterable
from typing import Generator, Iterator, List, Set, Tuple

from pdf2image import convert_from_path
from pdf2image.generators import threadsafe

###############################################################################

LOGGER = logging.getLogger(__name__)

###############################################################################


def get_files(topdir: str, extn: str) -> Generator[str, None, None]:
    """
    Search :code:`topdir` recursively for all files with extension :code:`extn`

    extension is checked with :code:`str.endswith()`, instead of the supposedly
    better :code:`os.path.splitext()`, in order to facilitate the search with
    multiple dots in the :code:`extn`

    i.e.
    :code:`>>> get_files(topdir, ".xyz.txt")`
    wouldn't have worked as expected if :code:`splitext()` was used.

    Parameters
    ----------
    topdir : str
        Path of the directory to search files in
    extn : str
        Extension to look for

    Returns
    -------
    Generator[str, None, None]
        Matching file paths
    """
    return (
        os.path.join(dirpath, name)
        for dirpath, dirnames, files in os.walk(topdir)
        for name in files
        if name.lower().endswith(extn.lower())
    )


###############################################################################
# PDF Utils


def list_to_range(list_of_int: List[int]) -> List[Tuple[int, int]]:
    """Convert a list of integers into a list of ranges

    A range is tuple (start, end)

    Parameters
    ----------
    list_of_int : List[int]
        List of integers

    Returns
    -------
    List[Tuple[int, int]]
        List of ranges
    """
    ranges = []
    start, end = None, None
    last = None
    for current in sorted(set(list_of_int)):
        if current == int(current):
            current = int(current)
        else:
            continue
        if last is None:
            start = current
            last = current
        else:
            if current != last + 1:
                end = last
                ranges.append((start, end))
                start = current
            last = current
    ranges.append((start, last))
    return ranges


# Static Name Generator
@threadsafe
def static_generator(prefix):
    while True:
        yield prefix


def extract_pages(
    pdf_path: str,
    pages: Iterator[Tuple[int, int]] = None
) -> Set[str]:
    """Extract pages from a PDF file as image files

    Pages are saved in the same directory as the PDF file,
    with the suffix :code:`.page-[number].jpg`

    Parameters
    ----------
    pdf_path : str
        Path to the PDF file
    pages : Iterator[Tuple[int, int]], optional
        Page ranges to extract.
        If None, all pages will be extracted.
        The default is None.

    Returns
    -------
    Set[str]
        Set of paths to extracted pages
    """
    pdf_path = os.path.realpath(pdf_path)
    output_path = os.path.dirname(pdf_path)
    output_name, _ = os.path.splitext(os.path.basename(pdf_path))

    if isinstance(pages, Iterable):
        LOGGER.info(f"Extracting {len(pages)} pages from '{pdf_path}' ..")
        ranges = list_to_range(pages)
    else:
        LOGGER.info(f"Extracting all pages from '{pdf_path}' ..")
        ranges = [(None, None)]

    paths = set()
    for _start, _end in ranges:
        _paths = convert_from_path(
            pdf_path=pdf_path,
            output_folder=output_path,
            first_page=_start,
            last_page=_end,
            fmt="jpeg",
            jpegopt={"quality": 100, "progressive": True, "optimize": True},
            output_file=static_generator(f"{output_name}.page"),
            paths_only=True,
        )
        paths.update(_paths)
        if _start is not None and _end is not None:
            LOGGER.info(f"Extracted {len(_paths)} pages: {_start} to {_end}.")
        else:
            LOGGER.info(f"Extracted {len(_paths)} pages.")
    return paths


###############################################################################
