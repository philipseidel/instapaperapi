#!/usr/bin/env python
from distutils.core import setup
#http://bashelton.com/2009/04/setuptools-tutorial/#setting_up

setup (
    name = "instapaperapi",
    version = "0.1",
    description="API for managing Instapaper accounts.",
    long_description=open('README.md').read(),
    author="Philip Seidel",
    author_email="info@philipseidel.com",
    url="http://www.philipseidel.com/",
    packages=['instapaperapi'],
    package_data = {'instapaperapi': ['*.xml']},
    download_url = "http://www.philipseidel.com/download/",
    zip_safe = True
)