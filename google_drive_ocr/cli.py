#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Console script for Google OCR (Drive API v3)
"""

###############################################################################

import os
import sys
import stat
import time
import logging
import argparse

###############################################################################

from . import __version__
from .application import GoogleOCRApplication
from .utils import get_files

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

        name = None
        client_secret = None
        upload_folder_id = None

        extension = '.png'
        no_keep = False
        workers = 1

    # ----------------------------------------------------------------------- #

    p = argparse.ArgumentParser(description="Google OCR using Drive API v3")
    p.add_argument("-s", "--client-secret", help='Path to client secret file')
    p.add_argument("-i", "--image", help='Path to a single image file')
    p.add_argument("-b", "--batch", nargs='+', help='Paths image files')
    p.add_argument("--image-dir", help='Path to image directory')
    p.add_argument("--extension", help="Extension to look in image directory")
    p.add_argument("--no-keep", action='store_true',
                   help="Delete file from Google Drive after OCR is performed")
    p.add_argument("--workers", type=int,
                   help="Number of workers (multiprocessing)")
    p.add_argument("--name", help='Application Name')
    p.add_argument("--verbose", action='store_true', help="Verbose output")
    p.add_argument("--debug", action='store_true', help="Debug mode")
    p.add_argument("--version", action='version',
                   version=f'%(prog)s {__version__}')

    p.parse_args(namespace=Config)

    # ----------------------------------------------------------------------- #

    if Config.verbose:
        root_logger.setLevel(logging.INFO)

    if Config.debug:
        root_logger.setLevel(logging.DEBUG)

    # ----------------------------------------------------------------------- #

    if (
        Config.image is None and
        Config.batch is None and
        Config.image_dir is None
    ):
        p.print_help()
        sys.exit(1)

    # -----------------------------------------------------------
    # Config
    # TODO: Better Configuration

    config = {}
    home_dir = os.path.expanduser('~')
    config_file = os.path.join(home_dir, '.gdo.cfg')

    if os.path.isfile(config_file):
        with open(config_file) as f:
            lines = f.read().split('\n')
            for line in lines:
                if line.strip():
                    key, value = line.split('=')
                    config[key.strip()] = value.strip()

    name = (
        Config.name or
        os.environ.get('GDOCR_NAME') or
        config.get('name')
    )

    client_secret = (
        Config.client_secret or
        os.environ.get('GDOCR_CLIENT_SECRET') or
        config.get('client_secret')
    )

    upload_folder_id = (
        Config.upload_folder_id or
        os.environ.get('GDOCR_UPLOAD_FOLDER_ID') or
        config.get('upload_folder_id')
    )

    manual = not (name and client_secret and upload_folder_id)

    if not name:
        name = input('Application Name: ').strip()
        config['name'] = name
    if not client_secret:
        client_secret = input('Client-Secrets File: ').strip()
        config['client_secret'] = client_secret
    if not upload_folder_id:
        upload_folder_id = input(
            "Upload Folder ID: (Default: 'root'): "
        ).strip()
        if not upload_folder_id:
            upload_folder_id = 'root'
        config['upload_folder_id'] = upload_folder_id

    # ----------------------------------------------------------------------- #
    # Create Application Instance

    app = GoogleOCRApplication(
        name=name,
        client_secret=client_secret,
        upload_folder_id=upload_folder_id,
        temporary_upload=Config.no_keep
    )

    if manual:
        answer = input("Save configuration? (Y/n) ")
        if not answer or answer.lower()[0] == 'y':
            with open(config_file, 'w') as f:
                f.write(
                    '\n'.join([' = '.join((k, v)) for k, v in config.items()])
                )
            logging.info("Configuration saved!")
            os.chmod(config_file, stat.S_IREAD + stat.S_IWRITE)

    # ----------------------------------------------------------------------- #
    # Single image file

    if Config.image is not None:
        t_start = time.time()
        status = app.perform_ocr(Config.image)
        t_finish = time.time()
        print(f"{status.value} ({t_finish-t_start:.4f} seconds)")
        output_path = app.get_output_path(Config.image)
        with open(output_path, 'r') as f:
            print(f.read())
        sys.exit(0)

    # ----------------------------------------------------------------------- #
    # Multiple images

    image_files = []
    # Multiple images on command line
    if Config.batch is not None:
        image_files = Config.batch

    # Find images from a directory
    if Config.image_dir is not None:
        image_files = get_files(Config.image_dir, Config.extension)

    if image_files:
        app.perform_ocr_batch(image_files, workers=Config.workers)


###############################################################################


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
