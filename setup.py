import setuptools

with open('README.md', encoding='utf-8') as fh:
    long_description = fh.read()

with open('requirements.txt', encoding='utf-8') as fh:
    install_requires = fh.read()

NAME = 'vardautomation'
VERSION = '0.5.0'

setuptools.setup(
    name=NAME,
    version=VERSION,
    author='Ichunjo',
    author_email='ichunjo.le.terrible@gmail.com',
    description='Encoding automation tools via Vapoursynth',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=['vardautomation'],
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
    python_requires='>=3.9',
    install_requires=install_requires,
)
