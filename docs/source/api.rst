API - GithubUtilsApi
====================

Get organization members
------------------------
This method let you list GH users in an organization
According API docs: https://docs.github.com/en/rest/orgs/members#list-organization-members

.. code-block:: python

    # Get organization members
    member = gh.organization_members_list('organization_name')

Create a repository
-------------------
This method let you create a repository in an organization
According API docs: https://docs.github.com/en/rest/reference/repos#create-an-organization-repository

.. code-block:: python

    # Create a repository
    repo = gh.repository_org_create('organization_name', 'repository_name', visibility='private, public or internal')

.. autosummary::
   :toctree: generated

   
