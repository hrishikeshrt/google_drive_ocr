=========================
Google OCR (Drive API v3)
=========================


.. image:: https://img.shields.io/pypi/v/google_drive_ocr?color=success
        :target: https://pypi.python.org/pypi/google_drive_ocr

.. image:: https://readthedocs.org/projects/google-drive-ocr/badge/?version=latest
        :target: https://google-drive-ocr.readthedocs.io/en/latest/?version=latest
        :alt: Documentation Status

.. image:: https://img.shields.io/pypi/pyversions/google_drive_ocr
        :target: https://pypi.python.org/pypi/google_drive_ocr
        :alt: Python Version Support

.. image:: https://img.shields.io/github/issues/hrishikeshrt/google_drive_ocr
        :target: https://github.com/hrishikeshrt/google_drive_ocr/issues
        :alt: GitHub Issues

.. image:: https://img.shields.io/github/followers/hrishikeshrt?style=social
        :target: https://github.com/hrishikeshrt
        :alt: GitHub Followers

.. image:: https://img.shields.io/twitter/follow/hrishikeshrt?style=social
        :target: https://twitter.com/hrishikeshrt
        :alt: Twitter Followers


Perform OCR using Google's Drive API v3


* Free software: GNU General Public License v3
* Documentation: https://google-drive-ocr.readthedocs.io.

Features
========

* Perform OCR using Google's Drive API v3
* Class :code:`GoogleOCRApplication()` for use in projects
* Highly configurable CLI
* Run OCR on a single image file
* Run OCR on multiple image files
* Run OCR on all images in directory
* Use multiple workers (:code:`multiprocessing`)
* Work on a PDF document directly

Usage
=====

Using in a Project
------------------

Create a :code:`GoogleOCRApplication` application instance:

.. code-block:: python

    from google_drive_ocr import GoogleOCRApplication

    app = GoogleOCRApplication('client_secret.json')

Perform OCR on a single image:

.. code-block:: python

    app.perform_ocr('image.png')


Perform OCR on mupltiple images:

.. code-block:: python

    app.perform_batch_ocr(['image_1.png', 'image_2.png', 'image_3.png'])

Perform OCR on multiple images using multiple workers (:code:`multiprocessing`):

.. code-block:: python

    app.perform_batch_ocr(['image_1.png', 'image_3.png', 'image_2.png'], workers=2)


Using Command Line Interface
----------------------------

Typical usage with several options:

.. code-block:: console

    google-ocr --client-secret client_secret.json \
    --upload-folder-id <google-drive-folder-id>  \
    --image-dir images/ --extension .jpg \
    --workers 4 --no-keep

Show help message with the full set of options:

.. code-block:: console

    google-ocr --help

Configuration
^^^^^^^^^^^^^

The default location for configuration is :code:`~/.gdo.cfg`.
If configuration is written to this location with a set of options,
we don't have to specify those options again on the subsequent runs.

Save configuration and exit:

.. code-block:: console

    google-ocr --client-secret client_secret.json --write-config ~/.gdo.cfg


Read configuration from a custom location (if it was written to a custom location):

.. code-block:: console

    google-ocr --config ~/.my_config_file ..

Performing OCR
^^^^^^^^^^^^^^

**Note**: It is assumed that the :code:`client-secret` option is saved in configuration file.

Single image file:

.. code-block:: console

    google-ocr -i image.png

Multiple image files:

.. code-block:: console

    google-ocr -b image_1.png image_2.png image_3.png

All image files from a directory with a specific extension:

.. code-block:: console

    google-ocr --image-dir images/ --extension .png

Multiple workers (:code:`multiprocessing`):

.. code-block:: console

    google-ocr -b image_1.png image_2.png image_3.png --workers 2

PDF files:

.. code-block:: console

    google-ocr --pdf document.pdf --pages 1-3 5 7-10 13


**Note**:
You must setup a Google application and download :code:`client_secrets.json` file before using :code:`google_drive_ocr`.

Setup Instructions
==================

Create a project on Google Cloud Platform

**Wizard**: https://console.developers.google.com/start/api?id=drive

**Instructions**:

    * https://cloud.google.com/genomics/downloading-credentials-for-api-access
    * Select application type as "Installed Application"
    * Create credentials OAuth consent screen --> OAuth client ID
    * Save :code:`client_secret.json`
