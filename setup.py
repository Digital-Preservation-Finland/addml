"""Install addml."""

from setuptools import setup, find_packages


def main():
    """Install premis"""
    setup(
        name='addml',
        packages=find_packages(exclude=['tests', 'tests.*']),
        version='0.1',
        install_requires=[
            'lxml',
            'xml_helpers'
        ],
        dependency_links=[
            'git+https://gitlab.csc.fi/dpres/xml-helpers.git'
            '@develop#egg=xml_helpers-0.0'
        ]
    )


if __name__ == '__main__':
    main()
