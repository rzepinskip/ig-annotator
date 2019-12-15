igannotator
===========

.. image:: https://img.shields.io/pypi/v/igannotator.svg
    :target: https://pypi.python.org/pypi/igannotator
    :alt: Latest PyPI version

.. image::  .png
   :target:  
   :alt: Latest Travis CI build status

Institutional Grammar annotator package.

Usage
-----

Installation
------------
1. Create a virtual environment::

    python -m venv .env

2. Activate the virtual environment::

    source .env/bin/activate

3. Install dependencies::

    pip install -r requirements.txt


Example 
-------

1. Run annotation for example (sentence are separated by empty line)::

    python ig_annotator.py data/simple_example.txt simple_example-ouput.xml

2. Run annotation for `nauka_1.txt` file::

    python stanfordForGoldStandard.py 

Authors
-------

``igannotator`` was written by the group of students during `Text Mining` course at Warsaw University of Technology.
