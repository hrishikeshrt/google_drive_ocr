=====
Usage
=====

To use **Google OCR (Drive API v3)** in a project::

    from google_drive_ocr.application import GoogleOCRApplication
    app = GoogleOCRApplication('Google OCR', 'client_secrets.json')
    # Single image
    app.perform_ocr('image.png')
    # Multiple images
    app.perform_batch_ocr(['image_1.png', 'image_2.png', 'image_3.png'])
    # Multiple Images using multiprocessing
    app.perform_batch_ocr(['image_1.png', 'image_3.png', 'image_2.png'], workers=2)

To use **Google OCR (Drive API v3)** from command line::

    google-ocr --client-secret client_secret.json \
    --upload-folder-id <google-drive-folder-id>  \
    --image-dir images/ --extension .jpg \
    --workers 4 --no-keep

    # Save configuration and exit
    # If configuration is written to ~/.gdo.cfg, we don't have to specify those
    # options again on the subsequent runs
    google-ocr --client-secret client_secret.json --write-config ~/.gdo.cfg

    # Read configuration from a custom location
    # If configuration is written to a custom location, that can still be readthedocs
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
