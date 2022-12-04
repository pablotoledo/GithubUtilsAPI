GitHub Utils API - documentation
================================

This package is used to provide a **simple** python interface for interacting with GitHub.
It is based on the official public Rest API documentation and private methods discovered by the community.

This project is documented at https://githubutilsapi.readthedocs.io/

Getting started
---------------

Install package using pip:

``pip install github-utils-api``

Import the package and create a conection.

.. code-block:: python

   from github_utils_api import GitHub

   gh = GithubUtilsApi(user='user', token='token')

In case you need to connect to a GitHub Enterprise instance, you can pass the url as a parameter.

.. code-block:: python
   
   from github_utils_api import GitHub

   gh = GithubUtilsApi(user='user', token='token', github_url='https://github.mycompany.com/api/v3', github_url_graphql='https://github.mycompany.com/api/graphql')





   
Contents
--------
.. toctree::
   :maxdepth: 2

   api


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
