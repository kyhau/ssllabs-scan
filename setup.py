from __future__ import absolute_import, division, print_function
from setuptools import setup, find_packages


__title__ = "ssllabsscan"
__version__ = "0.2.0"
__author__ = "Kayan Hau"
__email__ = "virtualda@gmail.com"
__uri__ = "https://github.com/kyhau/ssllabs-scan"
__summary__ = "SSL Labs Analysis Reporting"

__requirements__ = [
    'requests>=2.13.0',
]

__entry_points__ = {
    'console_scripts': [
        'ssllabs-scan = ssllabsscan.main:main',
    ]
}

setup(
    name=__title__,
    version=__version__,
    description=__summary__,
    packages=find_packages(exclude=['tests']),
    author=__author__,
    author_email=__email__,
    url=__uri__,
    zip_safe=False,
    entry_points=__entry_points__,
    install_requires=__requirements__,
    data_files=[
        ('', ['ReleaseNotes.md']),
    ],
)
