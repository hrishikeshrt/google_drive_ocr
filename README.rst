=========================
Google OCR (Drive API v3)
=========================


.. image:: https://img.shields.io/pypi/v/google_drive_ocr.svg
        :target: https://pypi.python.org/pypi/google_drive_ocr

.. image:: https://img.shields.io/travis/hrishikeshrt/google_drive_ocr.svg
        :target: https://travis-ci.com/hrishikeshrt/google_drive_ocr

.. image:: https://readthedocs.org/projects/google-drive-ocr/badge/?version=latest
        :target: https://google-drive-ocr.readthedocs.io/en/latest/?version=latest
        :alt: Documentation Status



Perform OCR using Google's Drive API v3


* Free software: GNU General Public License v3
* Documentation: https://google-drive-ocr.readthedocs.io.

Usage
-----

To use :code:`google_drive_ocr` in a project::

    from google_drive_ocr.application import GoogleOCRApplication
    app = GoogleOCRApplication('client_secret.json')
    # Single image
    app.perform_ocr('image.png')
    # Multiple images
    app.perform_batch_ocr(['image_1.png', 'image_2.png', 'image_3.png'])
    # Multiple Images using multiprocessing
    app.perform_batch_ocr(['image_1.png', 'image_3.png', 'image_2.png'], workers=2)

To use :code:`google_drive_ocr` from command line::

    google-ocr --client-secret client_secret.json \
    --upload-folder-id <google-drive-folder-id>  \
    --image-dir images/ --extension .jpg \
    --workers 4 --no-keep

    # Save configuration and exit
    # If configuration is written to ~/.gdo.cfg, we don't have to specify those
    # options again on the subsequent runs
    google-ocr --client-secret client_secret.json --write-config ~/.gdo.cfg

    # Read configuration from a custom location (if it was written to a custom location)
    google-ocr --config ~/.my_config_file ..

    # Examples (assuming client-secret is saved in configuration file)
    # Single image
    google-ocr -i image.png

    # Multiple images
    google-ocr -b image_1.png image_2.png image_3.png

    # All files from a directory
    google-ocr --image-dir images/ --extension .png

    # Multiple images using multiprocessing
    google-ocr -b image_1.png image_2.png image_3.png --workers 2

    # PDF files
    google-ocr --pdf document.pdf --pages 1-3 5 7-10 13

    # For more detailed Usage
    google-ocr --help


**Note**:
You must setup a Google application and download :code:`client_secrets.json` file before using :code:`google_drive_ocr`.

Setup Instructions
------------------

Create a project on Google Cloud Platform

**Wizard**: https://console.developers.google.com/start/api?id=drive

**Instructions**:

    * https://cloud.google.com/genomics/downloading-credentials-for-api-access
    * Select application type as "Installed Application"
    * Create credentials OAuth consent screen --> OAuth client ID
    * Save :code:`client_secret.json`

Features
--------

* Perform OCR using Google's Drive API v3
* Single, Batch and Parallel OCR
* Work on a PDF document directly
* Highly configurable CLI
* :code:`GoogleOCRApplication` class usable in a project

Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
