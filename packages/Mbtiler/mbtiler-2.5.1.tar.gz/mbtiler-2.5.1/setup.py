#!/usr/bin/python3
# -*- coding: utf8 -*-
import os
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))

setup(
    name='Mbtiler',
    version='2.5.1',
    author='Elmeslmaney',
    author_email='mohamedelmeslmaney00@gmail.com',
    url='https://github.com/Elmeslmaney/Mbtiler',
    download_url="http://pypi.python.org/pypi/Mbtiler/",
    description="Mbtiler is a python toolbox to manipulate map tiles.",
    long_description=open(os.path.join(here, 'README.rst')).read() + '\n\n' +
                     open(os.path.join(here, 'CHANGES')).read(),
    license='LPGL, see LICENSE file.',
    install_requires = [
        'mbutil',
        'requests',
    ],
    extras_require = {
        'PIL':  ["Pillow"],
        'Mapnik': ["Mapnik >= 2.0.0"]
    },
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    keywords=['MBTiles', 'Mapnik'],
    classifiers=['Programming Language :: Python :: 3.5',
                 'Natural Language :: English',
                 'Topic :: Utilities',
                 'Development Status :: 5 - Production/Stable'],
)
