#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Utility Functions
"""

import os
import logging
from collections.abc import Iterable

from pdf2image import convert_from_path
from pdf2image.generators import threadsafe

###############################################################################

logger = logging.getLogger(__name__)

###############################################################################


def get_files(topdir, extn):
    """
    Search topdir recursively for all files with extension 'extn'

    extension is checked with endswith() call, instead of the supposedly better
    os.path.splitext(), in order to facilitate the search with multiple '.'
    i.e.
    >>> get_files(topdir, '.xyz.txt')
    works as expected which wouldn't have if splitext() was used.
    """
    return (
        os.path.join(dirpath, name)
        for dirpath, dirnames, files in os.walk(topdir)
        for name in files
        if name.lower().endswith(extn.lower())
    )


###############################################################################
# PDF Utils


def list_to_range(list_of_int):
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


def extract_pages(pdf_path, pages=None):
    """Extract pages from a PDF file

    Pages are saved beside the PDF file with
    """
    pdf_path = os.path.realpath(pdf_path)
    output_path = os.path.dirname(pdf_path)
    output_name, _ = os.path.splitext(os.path.basename(pdf_path))

    if isinstance(pages, Iterable):
        logger.info(f"Extracting {len(pages)} pages from '{pdf_path}' ..")
        ranges = list_to_range(pages)
    else:
        logger.info(f"Extracting all pages from '{pdf_path}' ..")
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
            logger.info(f"Extracted {len(_paths)} pages: {_start} to {_end}.")
        else:
            logger.info(f"Extracted {len(_paths)} pages.")
    return paths


###############################################################################
