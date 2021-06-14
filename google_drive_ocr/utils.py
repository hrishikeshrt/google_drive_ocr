#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 14 22:29:54 2021

@author: Hrishikesh Terdalkar
"""

import os
from pdf2image import convert_from_path

###############################################################################


def get_files(topdir, extn):
    '''
    Search topdir recursively for all files with extension 'extn'

    extension is checked with endswith() call, instead of the supposedly better
    os.path.splitext(), in order to facilitate the search with multiple '.'
    i.e.
    >>> get_files(topdir, '.xyz.txt')
    works as expected which wouldn't have if splitext() was used.
    '''
    return (
        os.path.join(dirpath, name)
        for dirpath, dirnames, files in os.walk(topdir)
        for name in files
        if name.lower().endswith(extn.lower())
    )

###############################################################################


def extract_pages(pdf_file, pages=None):
    '''Extract pages from a PDF file

    Pages are saved beside the PDF file with
    '''
    images = convert_from_path(pdf_file)
    _name, _ext = os.path.splitext(pdf_file)

    if isinstance(pages, list):
        pages = [images[i] for i in pages if 0 <= i < len(pages)]

        for _idx in pages:
            if 0 <= _idx < len(pages):
                image = images[_idx]
                image.save(f'{_name}.page-{_idx}.png')

###############################################################################
