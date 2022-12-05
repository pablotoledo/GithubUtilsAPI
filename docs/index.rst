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

   gh = GithubUtilsApi(user='user', 
         token='token', 
         github_url='https://github.mycompany.com/api/v3', 
         github_url_graphql='https://github.mycompany.com/api/graphql')


Get organization members
------------------------
This method let you list GH users in an organization

Accorrding API docs: https://docs.github.com/en/rest/orgs/members#list-organization-members

.. code-block:: python

    # Get organization members
    member = gh.organization_members_list('organization_name')

Create a repository
-------------------
This method let you create a repository in an organization

Accorrding API docs: https://docs.github.com/en/rest/reference/repos#create-an-organization-repository

.. code-block:: python

    # Create a repository
    repo = gh.repository_org_create('organization_name', 
               'repository_name', 
               visibility='private, public or internal')

Grant Team access to a repository
---------------------------------
This method let you grant a team access to a repository

Accorrding API docs: https://docs.github.com/en/rest/reference/teams#add-or-update-team-repository-permissions

.. code-block:: python

    # Grant Team access to a repository
    repo = gh.repository_grant_team('organization_name', 
               'repository_name', 
               'repository_owner', 
               'team_slug_name', 
               permission='pull, push, admin, maintain or triage')

Grant user into the organization
--------------------------------
This method let you grant a user into the specified organization

Accorrding API docs: https://docs.github.com/en/rest/orgs/members

.. code-block:: python

    # Grant user into the organization
    repo = gh.organization_grant_user('organization_name', 
               'user_name')

Create a team
-------------
This method let you create a team into the specified organization

Accorrding API docs: https://docs.github.com/en/rest/reference/teams#create-a-team

.. code-block:: python

    # Create a team
    repo = gh.team_create('organization_name', 
               'team_name', 
               team_privacy='secret or closed')

Remove a user from a team
-------------------------
This method let you remove a user from a GitHub organization team

Accorrding API docs: https://docs.github.com/en/rest/reference/teams#remove-team-membership-for-a-user

.. code-block:: python

    # Remove a user from a team
    repo = gh.team_remove_user('organization_name', 
               'team_name', 
               'user_name')

List team users
---------------
This method let you list users in a GitHub organization team

Accorrding API docs: https://docs.github.com/en/rest/reference/teams#list-team-members

.. code-block:: python

    # List team members
    repo = gh.team_list_users('organization_name', 
               'team_name')

Create a discussion post on a team's page
-----------------------------------------
This method let you create a discussion post on a team's page

Accorrding API docs: https://docs.github.com/en/rest/reference/teams#create-a-discussion

.. code-block:: python

    # Create a discussion post on a team's page
    repo = gh.team_discussion_create('organization_name', 
               'team_name', 
               'discussion_title', 
               private='Boolean: True or False')

Get a discussion post on a team's page
--------------------------------------
This method let you get a discussion post on a team's page or create a new one if it does not exist

Accorrding API docs: https://docs.github.com/en/rest/teams/discussions#create-a-discussion

.. code-block:: python

    # Get a discussion post on a team's page or create a new one if it does not exist
    repo = gh.team_discussion_search('organization_name', 
               'team_name', 
               'discussion_title', 
               create_if_not_exists='Boolean: True or False', 
               private='Boolean: True or False')

List all discussions on a team's page
-------------------------------------
This method let you list all discussions on a team's page.

Accorrding API docs: https://docs.github.com/en/rest/teams/discussions#list-discussions

.. code-block:: python

    # List all discussions on a team's page
    repo = gh.team_discussion_list('organization_name', 'team_name')

Create a comment on a Team discussion post
------------------------------------------
This method let you create a comment on a Team discussion post.

Accorrding API docs: https://docs.github.com/en/rest/teams/discussion-comments#create-a-discussion-comment

.. code-block:: python

    # Create a comment on a Team discussion post
    repo = gh.team_discussion_create_comment('organization_name', 
               'team_name', 
               'discussion_id', 
               'comment_body')

List repositories in an organization
------------------------------------
This method let you list repositories in an organization. Paginated method with filter options.

Accorrding API docs: https://docs.github.com/en/rest/reference/repos#list-organization-repositories

.. code-block:: python

    # List repositories in an organization
    repo = gh.list_repositories('organization_name', 
               type='all, public, private, forks, sources, member, internal', 
               sort='full_name, created, updated, pushed, size, stargazers_count, watchers_count, forks_count, open_issues_count, default_branch, score', 
               sort='created, updated, pushed, full_name' 
               per_page='1-100', 
               page='1-100')

List all repositories in an organization
----------------------------------------
This method let you list all repositories in an organization. Retrieve all repositories.

Accorrding API docs: https://docs.github.com/en/rest/reference/repos#list-organization-repositories

.. code-block:: python

    # List all repositories in an organization
    repo = gh.list_repositories_all('organization_name', 
               type='all, public, private, forks, sources, member, internal', 
               sort='created, updated, pushed, full_name', 
               per_page='1-100')

Get repository details
----------------------
This method let you get repository details.

Accorrding API docs: https://docs.github.com/en/rest/reference/repos#get-a-repository

.. code-block:: python

    # Get repository details
    repo = gh.get_repository('organization_name_or_owner', 'repository_name')

Delete a repository branch
--------------------------
This method let you delete a repository branch.

Accorrding non-documented API endpoint. Mentioned in https://github.community/t/how-to-delete-a-branch-through-the-api/211792

.. code-block:: python

    # Delete a repository branch
    repo = gh.repository_branch_delete('organization_name_or_owner', 
               'repository_name', 
               'branch_name')

List repository branches
------------------------
This method allows retrieve paginated list in a request object of branches in a repository

Accorrding API docs: https://docs.github.com/en/rest/reference/repos#list-branches

.. code-block:: python

    # List repository branches
    repo = gh.repository_branch_list('organization_name_or_owner', 
               'repository_name', 
               protected='Boolean: True or False',
               per_page='1-100', 
               page='1-100')

List all repository branches
----------------------------
This method allows listing all branches in a repository, without paginate option using the method self.list_repository_branches.

Accorrding API docs: https://docs.github.com/en/rest/reference/repos#list-branches

.. code-block:: python

    # List all repository branches
    repo = gh.recursive_get_all_repository_branches('organization_name_or_owner', 'repository_name')

Get repository branch details
-----------------------------
This method let you get repository branch details.

Accorrding API docs: https://docs.github.com/en/rest/branches/branches?apiVersion=2022-11-28#get-a-branch

.. code-block:: python

    # Get repository branch details
    repo = gh.get_repository_branch(
               'organization_name_or_owner', 
               'repository_name', 
               'branch_name')

Get repository commit details
-----------------------------
This method let you get repository commit details.

Accorrding API docs: https://docs.github.com/en/rest/reference/repos#get-a-commit

.. code-block:: python

    # Get repository commit details
    repo = gh.repository_get_commit_details(
               'organization_name_or_owner', 
               'repository_name', 
               'commit_sha')

Comment a pull request or issue
-------------------------------
This method let you comment a pull request or issue.

Accorrding API docs: https://docs.github.com/en/rest/reference/issues#create-a-review-comment-for-a-pull-request

.. code-block:: python

    # Comment a pull request or issue
    repo = gh.repository_comment_issue(
               'organization_name_or_owner', 
               'repository_name', 
               'pull_request_number', 
               'comment_body')

Get user details
----------------
This method let you get user details.

Accorrding API docs: https://docs.github.com/en/rest/reference/users#get-a-user

.. code-block:: python

    # Get user details
    repo = gh.user_details('user_name')

Create a repository release
---------------------------
This method let you create a repository release.

Accorrding API docs: https://docs.github.com/en/rest/reference/repos#list-repository-teams

.. code-block:: python

    # Create a repository release
    repo = gh.repository_create_release(
               'organization_name_or_owner', 
               'repository_name', 
               'tag_name', 
               'release_name', 
               'release_body',
               'generate_release_notes')

List repository teams
---------------------
This method let you list repository teams. Paginated method.

Accorrding API docs: https://docs.github.com/es/rest/repos/repos#list-repository-teams

.. code-block:: python

    # List repository teams
    repo = gh.list_repository_teams(
               'organization_name_or_owner', 
               'repository_name', 
               'per_page', 
               'page')

List all repository teams
-------------------------
This method let you list all repository teams. Retrieve all repository teams.

Accorrding API docs: https://docs.github.com/es/rest/repos/repos#list-repository-teams

.. code-block:: python

    # List all repository teams
    repo = gh.list_repository_teams_all(
               'organization_name_or_owner', 
               'repository_name')

List teams in an organization
-----------------------------
This method let you list teams in an organization. Paginated.

Accorrding API docs: https://docs.github.com/es/rest/reference/teams#list-teams

.. code-block:: python

    # List teams in an organization
    repo = gh.list_teams(
               'organization_name_or_owner', 
               'per_page', 
               'page')

List all teams in an organization
---------------------------------
This method let you list all teams in an organization. Retrieve all teams.

Accorrding API docs: https://docs.github.com/es/rest/reference/teams#list-teams

.. code-block:: python

    # List all teams in an organization
    repo = gh.list_teams_all(
               'organization_name_or_owner'
               'per_page',
               )

Get team by name
----------------
This method let you get team by name.

Accorrding API docs: https://docs.github.com/es/rest/reference/teams#get-a-team-by-name

.. code-block:: python

    # Get team by name
    repo = gh.team_by_name(
               'organization_name_or_owner', 
               'team_name')

List repository tags
--------------------
This method let you list repository tags. Paginated.

Accorrding API docs: https://docs.github.com/es/rest/reference/repos#list-repository-tags

.. code-block:: python

    # List repository tags
    repo = gh.list_repository_tags(
               'organization_name_or_owner', 
               'repository_name', 
               'per_page', 
               'page')

List all repository tags
------------------------
This method let you list all repository tags. Retrieve all repository tags.

Accorrding API docs: https://docs.github.com/es/rest/reference/repos#list-repository-tags

.. code-block:: python

    # List all repository tags
    repo = gh.list_repository_tags_all(
               'organization_name_or_owner', 
               'repository_name')

List repository pull requests
-----------------------------
This method let you list repository pull requests. Paginated.

Accorrding API docs: https://docs.github.com/es/rest/reference/pulls#list-pull-requests

.. code-block:: python

    # List repository pull requests
    repo = gh.list_repository_prs(
               'organization_name_or_owner', 
               'repository_name', 
               'per_page', 
               'page',
               state='open, closed, all'
               )

List all repository pull requests
---------------------------------
This method let you list all repository pull requests. Retrieve all repository pull requests.

Accorrding API docs: https://docs.github.com/es/rest/reference/pulls#list-pull-requests

.. code-block:: python

    # List all repository pull requests
    repo = gh.list_repository_prs_all(
               'organization_name_or_owner', 
               'repository_name',
               'per_page',
               state='open, closed, all'
               )

List repository collaborators
-----------------------------
This method let you list repository collaborators. Paginated.

Accorrding API docs: https://docs.github.com/es/rest/collaborators/collaborators#list-repository-collaborators

.. code-block:: python

    # List repository collaborators
    repo = gh.list_repository_collaborations(
               'organization_name_or_owner', 
               'repository_name', 
               permission='pull, push, admin, maintain, triage',
               affiliation='outside, direct, all',
               'per_page', 
               'page')

List all repository collaborators
---------------------------------
This method let you list all repository collaborators. Retrieve all repository collaborators.

Accorrding API docs: https://docs.github.com/es/rest/collaborators/collaborators#list-repository-collaborators

.. code-block:: python

    # List all repository collaborators
    repo = gh.list_repository_collaborations_all(
               'organization_name_or_owner', 
               'repository_name', 
               permission='pull, push, admin, maintain, triage',
               affiliation='outside, direct, all',
               'per_page')



Contents
--------
.. toctree::
   :maxdepth: 2

   index


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
