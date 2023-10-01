# How to contribute

You’re very welcome to make bug fixes or enhancements to this library.
This document lays out the guidelines for how to get those changes into
the main package repository.

## Getting Started

- [Fork the repository](#)
- Keep it synchronized while you are developing
- Install pyenv

```
pip install -r requirements.txt
```

## Mandatory conditions

1. If you are adding a new method
2. If you make changes in current methods

Please follow the code style and check the docs folder and **document your changes**.

## Before you raise a PR

Create the **Commit Header** with the relevant feature pre-fixed, examples below:

- GitHub: list repositories ✅
- [GitHub] Remove user from team ✅

## Using your changes before they’re live

You may want to use the changes you’ve made to this library before the
merging/review process has been completed. To do this you can install it
into the global python environment by running this command from the top
level directory.

```
pip install . --upgrade
```

The following command builds a package and uploads it to the PIP repository.

```
python setup.py sdist upload
```

An alternative way you can use the next command

```
python3 -m pip install git+yourrepository.git
```

## References

All methods are based on docs from: [GitHub Docs](https://docs.github.com/en/rest/orgs/members#list-organization-members)

## Credits

In addition to all the contributors, we would like to thank these companies:

- [GitHub](https://github.com/) for hosting our repository and continuous integration
