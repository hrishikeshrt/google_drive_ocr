#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'google_api_python_client>=2.9.0',
    'google_auth_oauthlib>=0.4.1',
    'tqdm>=4.60.0',
    'attrs>=21.2.0',
    'natsort>=7.0.1',
    'pdf2image>=1.15.1',
    'ConfigArgParse>=1.4.1'
]

test_requirements = ['pytest>=3', ]

setup(
    author="Hrishikesh Terdalkar",
    author_email='hrishikeshrt@linuxmail.org',
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: User Interfaces',
        'Topic :: Utilities',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9'
    ],
    description="Perform OCR using Google's Drive API v3",
    entry_points={
        'console_scripts': [
            'google-ocr=google_drive_ocr.cli:main',
        ],
    },
    install_requires=requirements,
    license="GNU General Public License v3",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='google_drive_ocr',
    name='google_drive_ocr',
    packages=find_packages(include=['google_drive_ocr', 'google_drive_ocr.*']),
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/hrishikeshrt/google_drive_ocr',
    version='0.2.5',
    zip_safe=False,
)
