"""Install addml."""

from setuptools import setup, find_packages
from version import get_version


def main():
    """Install premis"""
    setup(
        name='addml',
        packages=find_packages(exclude=['tests', 'tests.*']),
        include_package_data=True,
        version=get_version(),
        install_requires=[
            'lxml',
            'six',
            'xml_helpers@git+https://gitlab.csc.fi/dpres/xml-helpers.git'
            '@develop'
        ]
    )


if __name__ == '__main__':
    main()
