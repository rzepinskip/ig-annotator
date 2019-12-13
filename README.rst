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

4. Generate CONLLU files::

    python stanfordForGoldStandard.py 

5. Annotate CONNLU files in specified directory::

    python ig_annotator.py data/conllu/goldStandard-stanford


Requirements
^^^^^^^^^^^^

Compatibility
-------------

Licence
-------

Authors
-------

`igannotator` was written by `Pawel Rzepinski, Ryszard Szymanski`.
