"""Python driver for AutomationDirect (formerly Koyo) Ethernet ClickPLCs."""

from setuptools import setup

with open('README.md') as in_file:
    long_description = in_file.read()

setup(
    name='syscon_clickplc',
    version='0.0.4',
    description="Python driver for Koyo Ethernet ClickPLCs.",
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/SYSCON-International/syscon_clickplc',
    author='SYSCON International',
    author_email='dev@syscon-intl.com',
    packages=['syscon_clickplc'],
    entry_points={
        'console_scripts': [('syscon_clickplc = syscon_clickplc:command_line')]
    },
    install_requires=[
        'pymodbus>=2.4.0; python_version == "3.8"',
        'pymodbus>=2.4.0; python_version == "3.9"',
        'pymodbus>=3.0.2,<3.7.0; python_version >= "3.10"',
    ],
    extras_require={
        'test': [
            'pytest',
            'pytest-cov',
            'pytest-asyncio',
            'mypy==1.10.0',
            'ruff==0.4.2',
        ],
    },
    license='GPLv2',
    classifiers=[
        'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
        'Development Status :: 4 - Beta',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Topic :: Scientific/Engineering :: Human Machine Interfaces'
    ]
)
