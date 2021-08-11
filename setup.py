from setuptools import setup
from distutils.util import convert_path

meta = {}
exec(open(convert_path('vardautomation/_metadata.py')).read(), meta)


with open('README.md') as fh:
    long_description = fh.read()

with open("requirements.txt") as fh:
    install_requires = fh.read()

NAME = 'vardautomation'

setup(
    name=NAME,
    version=meta['__version__'],
    author=meta['__author__'].split()[0],
    author_email=meta['__author__'].split()[1][1:-1],
    description='Automatisation tools',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=['vardautomation'],
    package_data={
        'vardautomation': ['py.typed'],
    },
    url='https://github.com/Ichunjo/vardautomation',
    zip_safe=False,
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.9',
    install_requires=install_requires,
)
