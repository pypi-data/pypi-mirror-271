from setuptools import setup, find_packages

setup(
    name = 'scrapkit',
    version = '2.0',
    description = 'WebScrapping in 3 lines of code',
    long_description = open('README.md').read(),
    long_description_content_type = 'text/markdown',
    author = 'Ali Lodhi',
    author_email = 'alilodhibusiness@gmail.com',
    packages = ['scrapkit'],
    install_requires = [
        'requests == 2.31.0',
        'bs4 == 0.0.2',
    ],
)