#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Console script for Google OCR (Drive API v3)
"""

###############################################################################

import re
import sys
import time
import logging

import configargparse

###############################################################################

from . import __version__
from .application import GoogleOCRApplication
from .utils import get_files, extract_pages

###############################################################################

root_logger = logging.getLogger()
root_logger.addHandler(logging.StreamHandler())

###############################################################################


def main():
    # ----------------------------------------------------------------------- #
    # Default Config

    class Config:
        image = None
        batch = None
        image_dir = None
        pdf = None

        pages = None
        client_secret = None
        upload_folder_id = None

    # ----------------------------------------------------------------------- #

    p = configargparse.ArgumentParser(
        default_config_files=['~/.gdo.cfg'],
        auto_env_var_prefix="GDO_",
        description="Google OCR using Drive API v3",
        args_for_setting_config_path=["-c", "--config"],
        config_arg_help_message="Read configuration from file",
        args_for_writing_out_config_file=["-w", "--write-config"],
        write_out_config_file_arg_help_message="Write configuration file"
    )
    p.add_argument("--client-secret", required=True,
                   help='Path to client secret file')
    p.add_argument("-i", "--image", help='Path to a single image file')
    p.add_argument("-b", "--batch", nargs='+', help='Paths image files')
    p.add_argument("-d", "--image-dir", help='Path to image directory')
    p.add_argument("-x", "--extension", default='.png',
                   help="Extension to look in image directory")
    p.add_argument("--pdf", help='Path to PDF file')
    p.add_argument("--pages", nargs='*',
                   help="Pages from PDF to extract and OCR")
    p.add_argument("--upload-folder-id",
                   help='Google Drive folder id to upload files to')
    p.add_argument("--workers", type=int, default=1,
                   help="Number of workers (multiprocessing)")
    p.add_argument("--no-keep", action='store_true',
                   help="Delete file from Google Drive after OCR is performed")
    p.add_argument("--verbose", action='store_true', help="Verbose output")
    p.add_argument("--debug", action='store_true', help="Debug mode")
    p.add_argument("--version", action='version',
                   version=f'%(prog)s {__version__}')

    p.parse_args(namespace=Config)

    # ----------------------------------------------------------------------- #

    disable_tqdm = True
    if Config.debug:
        root_logger.setLevel(logging.DEBUG)
    elif Config.verbose:
        root_logger.setLevel(logging.INFO)
    else:
        disable_tqdm = False

    # ----------------------------------------------------------------------- #

    root_logger.debug(Config.__dict__)

    # ----------------------------------------------------------------------- #

    if (
        Config.image is None
        and Config.batch is None
        and Config.image_dir is None
        and Config.pdf is None
    ):
        p.print_help()
        return 1

    # ----------------------------------------------------------------------- #
    # Create Application Instance

    app = GoogleOCRApplication(
        client_secret=Config.client_secret,
        upload_folder_id=Config.upload_folder_id,
        temporary_upload=Config.no_keep
    )

    # ----------------------------------------------------------------------- #
    # Single image file

    if Config.image is not None:
        t_start = time.time()
        status = app.perform_ocr(Config.image)
        t_finish = time.time()
        print(f"{status.value} ({t_finish-t_start:.4f} seconds)")
        output_path = app.get_output_path(Config.image)
        with open(output_path, "r", encoding="utf-8") as f:
            print(f.read())
        return 0

    # ----------------------------------------------------------------------- #
    # Multiple images

    image_files = []
    # Multiple images on command line
    if Config.batch is not None:
        image_files = Config.batch

    # Find images from a directory
    if Config.image_dir is not None:
        image_files = get_files(Config.image_dir, Config.extension)

    # Extract pages from a PDF file
    if Config.pdf is not None:
        if Config.pages is not None:
            pages = []
            for page in Config.pages:
                if page.isdigit():
                    pages.append(int(page))

                m = re.match(r'^(\d+)-(\d+)$', page)
                if m:
                    pages.extend(range(int(m.group(1)), int(m.group(2)) + 1))
        else:
            pages = None
        image_files = extract_pages(Config.pdf, pages=pages)

    if image_files:
        app.perform_ocr_batch(
            image_files,
            workers=Config.workers,
            disable_tqdm=disable_tqdm
        )
        return 0

    return 1

###############################################################################


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
