from setuptools import find_packages, setup

__title__ = "ssllabsscan"
__version__ = "3.1.0"
__author__ = "Kay Hau"
__email__ = "virtualda@gmail.com"
__uri__ = "https://github.com/kyhau/ssllabs-scan"
__summary__ = "SSL Labs Analysis Reporting"

__requirements__ = [
    "requests>=2.13.0",
]

__entry_points__ = {
    "console_scripts": [
        "ssllabs-scan = ssllabsscan.main:main",
    ]
}

CLASSIFIERS = [
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
    "Programming Language :: Python :: 3 :: Only",
]

setup(
    author=__author__,
    author_email=__email__,
    classifiers=CLASSIFIERS,
    data_files=[
        ("", ["CHANGELOG.md"]),
    ],
    description=__summary__,
    entry_points=__entry_points__,
    install_requires=__requirements__,
    name=__title__,
    packages=find_packages(exclude=["tests"]),
    python_requires=">=3.9",
    url=__uri__,
    version=__version__,
    zip_safe=False,
)
