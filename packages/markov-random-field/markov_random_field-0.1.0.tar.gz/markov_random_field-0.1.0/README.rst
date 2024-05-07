===================
Markov Random Field
===================


.. image:: https://img.shields.io/pypi/v/markov_random_field.svg
        :target: https://pypi.python.org/pypi/markov_random_field

.. image:: https://img.shields.io/travis/jhaberbe/markov_random_field.svg
        :target: https://travis-ci.com/jhaberbe/markov_random_field

.. image:: https://readthedocs.org/projects/markov-random-field/badge/?version=latest
        :target: https://markov-random-field.readthedocs.io/en/latest/?version=latest
        :alt: Documentation Status




Markov Random Field for Image Segmentation


* Free software: MIT license
* Documentation: https://markov-random-field.readthedocs.io.


Features
--------

* TODO

Credits
-------

This package borrows almost everything from this repository:
        https://github.com/lucananni93/Hidden-Markov-Random-Fields/blob/master/image_segmentation/main.py

I made small QoL improvements (using scipy.signal.convolve2d instead of iterating through all the pixels to make this faster). 


As a small benchmark, an image of size (14930, 20226) with 4 classes takes 20m 40.7s to run on a cluster with 20 cores and 100 GB of RAM. 
Likely it doesn't require that much memory to run, however your mileage will vary.



This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
