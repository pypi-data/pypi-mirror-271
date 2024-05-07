# encoding: utf-8
from setuptools import setup, find_packages

SHORT = "client for openapi service."

__version__ = "0.0.1.17"
__author__ = 'fanqiangwei'
__email__ = 'fanqiangwei002@ke.com'
readme_path = 'README.md'

setup(
    name='ait_openapi',
    version=__version__,
    packages=find_packages('src'),
    package_dir={'': 'src'},
    install_requires=[
        'httpx>=0.10.0,<=0.26.0',
        'Werkzeug==3.0.1',
    ],
    url='',
    author=__author__,
    author_email=__email__,
    classifiers=[
        'Programming Language :: Python :: 3.5',
    ],
    include_package_data=True,
    package_data={'': ['*.py', '*.pyc']},
    zip_safe=False,
    platforms='any',

    description=SHORT,
    long_description=open(readme_path, encoding='utf-8').read(),
    long_description_content_type='text/markdown',
)
