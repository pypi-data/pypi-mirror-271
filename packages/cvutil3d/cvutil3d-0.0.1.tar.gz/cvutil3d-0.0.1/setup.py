from setuptools import setup, find_packages
from os import path
from io import open

here = path.abspath(path.dirname(__file__))
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='cvutil3d',
    description='Set of auxiliary scripts for 3D computer vision tasks',
    url='https://github.com/osmr/cvutil3d',
    author='Oleg Sémery',
    author_email='osemery@gmail.com',
    license='MIT',
    long_description=long_description,
    long_description_content_type='text/markdown',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Topic :: Scientific/Engineering :: Image Processing',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
    ],
    keywords='datasets image video 3D processing',
    packages=find_packages(exclude=['others', '*.others', 'others.*', '*.others.*']),
    install_requires=['pyrender'],
    python_requires='>=3.10',
    include_package_data=True,
)
