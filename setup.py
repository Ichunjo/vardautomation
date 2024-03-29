from pathlib import Path
from typing import Any, Dict

from setuptools import setup

meta: Dict[str, Any] = {}
exec(Path('vardautomation/_metadata.py').read_text(), meta := dict[str, str]())

with open('README.md', encoding='utf-8') as fh:
    long_description = fh.read()

with open('requirements.txt', encoding='utf-8') as fh:
    install_requires = fh.read()

NAME = 'vardautomation'

setup(
    name=NAME,
    version=meta['__version__'],
    author=meta['__author__'],
    author_email=meta['__email__'],
    description='Encoding automation tools via Vapoursynth',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=['vardautomation', 'vardautomation.tooling', 'vardautomation._logging'],
    package_data={
        'vardautomation': ['py.typed', 'logo.txt'],
    },
    url='https://github.com/Ichunjo/vardautomation',
    zip_safe=False,
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.11',
    install_requires=install_requires,
)
