How to contribute
=================

You’re very welcome to make bug fixes or enhancements to this library.
This document lays out the guidelines for how to get those changes into
the main package repository.

Getting Started
---------------

* Fork_ repository
* Keep it sync_'ed while you are developing
* Install pyenv_

::

   pip install -r requirements.txt


Mandatory conditions
--------------------

1. If you adding new method
2. If you make changes in current methods

Please follow the code style.


Before you raise a PR
---------------------

Create the **Commit Header** with the relevant feature pre-fixed, examples below,

* GitHub: list repositories           :heavy_check_mark:
* [GitHub] Remove user from team       :heavy_check_mark:


Using your changes before they’re live
--------------------------------------

You may want to use the changes you’ve made to this library before the
merging/review process has been completed. To do this you can install it
into the global python environment by running this command from the top
level directory.

::

   pip install . --upgrade

The following command builds a package and uploads it to PIP repository.

::

   python setup.py sdist upload

An alternative way you can use next command

::

   python3 -m pip install git+yourrepository.git


References
----------

All methods based on docs from: https://docs.github.com/en/rest/orgs/members#list-organization-members


Credits
-------
In addition to all the contributors we would like to thank to these companies:

* GitHub_ for hosting our repository and continuous integration
.. _GitHub: https://github.com/