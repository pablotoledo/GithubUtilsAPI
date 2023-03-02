# coding=utf-8
import requests
import base64
import json

from ..exceptions import GithubUtilsException


class GithubUtilsApi:
    """
    GithubUtilsClass, created to let other scripts to automate DevOps HelpDesk Support
    """

    def __init__(self, user, token, github_url="https://api.github.com",
                 github_url_graphql="https://github.com/api/graphql", proxies=None, verify=True):
        """
        Constructor
        :params user: string; user account at GitHub (email)
        :params token: string; auth personal token with enough permission provided (or password)
        :params github_url: string; for GitHub Enterprise take in consideration the following pattern http(s)://[hostname]/api/v3/
        :params github_url_graphql: string; for GitHub Enterprise take in consideration the following pattern http(s)://[hostname]/api/graphql/
        :params proxies: proxies
        """
        self.github_url = github_url
        self.__user = user
        self.__token = token
        self.__auth = "Basic " + str(base64.b64encode(str(self.__user + ":" + token).encode('ascii')), "utf-8")
        self._auth_graphql = f"token {self.__token}"
        self.proxies = {} if proxies is None else proxies
        self.verify = verify
        self.github_url_graphql = github_url_graphql

    def _get_ids_branch_protection(self, input_tmp, input_repo):
        result = []
        if input_tmp['totalCount'] > 0:
            for node in input_tmp['nodes']:
                result.append(node['actor']['id'])
        if input_repo['totalCount'] > 0:
            for node in input_repo['nodes']:
                if node['actor']['id'] not in result:
                    result.append(node['actor']['id'])
        return result

    def _parse_github_error_message(self, json_response: dict) -> str:
        error_list = json_response['errors']
        error_messages = [f"Error {index + 1}: {x.get('message')}" for index, x in enumerate(error_list)]
        return '.\n'.join(error_messages)

    def _request(self, request_type, url, data, is_graphql=False):
        """
        Request Method with Auth Header required by GitHub
        """
        headers = {
            'accept': 'application/vnd.github.v3+json',
            'Authorization': self._auth_graphql if is_graphql else self.__auth
        }
        body = json.dumps(data)
        return requests.request(request_type, url, headers=headers, data=body, proxies=self.proxies, verify=self.verify)

    def _response_to_json(self, response):
        """
        This method let you parse request body to JSON
        :param response: request response object
        :return: Array result
        """
        if 200 <= response.status_code < 300:
            result = json.loads(response.content)
            if type(result) == dict and 'errors' in result.keys():
                raise GithubUtilsException(self._parse_github_error_message(result))
            return result
        else:
            body = response.content.decode('utf-8') if type(response.content) is bytes else response.content
            raise GithubUtilsException(body)

    def organization_members_list(self, organization_name, per_page=30, page=1):
        """
        This method let you list GH users in an organization
        According API docs: https://docs.github.com/en/rest/orgs/members#list-organization-members
        :param organization_name: string; name of the current organization created at GitHub
        :param per_page: int; users per page
        :param page: int; page
        :return: request
        """
        params = {}
        query = "?per_page=" + str(per_page) + "&page=" + str(page)
        url = self.github_url + "/orgs/" + organization_name + "/members" + query
        return self._request("GET", url, params)

    def repository_org_create(self, organization_name=None, repository_name=None, visibility="private"):
        """
        This method allows creating a repository in a defined GitHub organization
        According API docs: https://docs.github.com/en/rest/reference/repos#create-an-organization-repository
        :param organization_name: string; name of the current organization created at GitHub
        :param repository_name: string; repository slug name
        :param visibility: private, public or internal
        :return: request
        """
        params = {}
        if repository_name:
            params['name'] = repository_name
        if visibility:
            params['visibility'] = visibility
        url = self.github_url + "/orgs/" + organization_name + "/repos"
        return self._request("POST", url, params)

    def repository_grant_team(self, organization_name=None, repository_name=None, repository_owner=None,
                              team_slug_name=None, team_permission='push'):
        """
        This method allows granting a GitHub Team in a specific repository.
        According API docs: https://docs.github.com/en/rest/reference/teams#add-or-update-team-repository-permissions
        :param organization_name: string; name of the current organization created at GitHub
        :param repository_name: string; repository slug name
        :param repository_owner: string; organization/user owner
        :param team_slug_name: string; GitHub Team slug name
        :param team_permission: string; options available are -> pull, push, admin, maintain, triage
        :return: request
        """
        params = {}
        if team_permission:
            params['permission'] = team_permission
        url = self.github_url + "/orgs/" + organization_name + "/teams/" + team_slug_name + "/repos/" + repository_owner + "/" + repository_name
        return self._request("PUT", url, params)

    def organization_grant_user(self, organization_name=None, github_username=None):
        """
        This method allows granting a  GitHub Team in a specific repository.
        According API docs: https://docs.github.com/en/rest/orgs/members
        :param organization_name: string; name of the current organization created at GitHub
        :param github_username: string; Github Username
        :return: request
        """

        params = {}
        if github_username:
            params['role'] = 'member'
        url = self.github_url + "/orgs/" + organization_name + "/memberships/" + github_username
        return self._request("PUT", url, params)

    def team_create(self, organization_name=None, team_slug_name=None, team_privacy="closed"):
        """
        This method allows creating a GitHub Team in a defined GitHub Organization
        According API docs: https://docs.github.com/en/rest/reference/teams#create-a-team
        :param organization_name: string; name of the current organization created at GitHub
        :param team_slug_name: string; GitHub Team slug name
        :param team_privacy: string; options available -> "secret" (only member) or "closed" all organizational members
        :return: request
        """
        params = {}
        if team_slug_name:
            params['name'] = team_slug_name
        if team_privacy:
            params['privacy'] = team_privacy
        url = self.github_url + "/orgs/" + organization_name + "/teams"
        return self._request("POST", url, params)

    def team_grant_user(self, organization_name=None, team_slug_name=None, github_username=None, team_role="member"):
        """
        This method allows granting a user in a GitHub organization Team
        According API docs: https://docs.github.com/en/rest/reference/teams#add-or-update-team-membership-for-a-user
        :param organization_name: string; name of the current organization created at GitHub
        :param team_slug_name: string; GitHub Team slug name
        :param github_username: string; GitHub Username
        :param team_role: values-> member or maintainer
        :return: request
        """
        params = {}
        if team_role:
            params['role'] = team_role
        url = self.github_url + "/orgs/" + organization_name + "/teams/" + team_slug_name + "/memberships/" + github_username
        return self._request("PUT", url, params)

    def team_remove_user(self, organization_name=None, team_slug_name=None, github_username=None):
        """
        This method allows removing a user in a GitHub organization Team
        According API docs: https://docs.github.com/en/rest/reference/teams#remove-team-membership-for-a-user
        :param organization_name: string; name of the current organization created at GitHub
        :param team_slug_name: string; GitHub Team slug name
        :param github_username: string; Github Username
        :return: request
        """
        params = {}
        url = self.github_url + "/orgs/" + organization_name + "/teams/" + team_slug_name + "/memberships/" + github_username
        return self._request("DELETE", url, params)

    def team_list_users(self, organization_name=None, team_slug_name=None, per_page=30) -> list:
        """
        This method allows list all user in a GitHub organization Team
        According API docs: https://docs.github.com/en/rest/teams/members#list-team-members
        :param organization_name: string; name of the current organization created at GitHub
        :param team_slug_name: string; GitHub Team slug name
        :param per_page: int; users per page
        :return: request
        """
        page = 1
        url_base = self.github_url + "/orgs/" + organization_name + "/teams/" + team_slug_name + "/members"
        url_query = url_base + "?per_page=" + str(per_page) + "&page=" + str(page)
        result = self._response_to_json(self._request("GET", url_query, None))
        result_all = []
        while len(result) > 0:
            result_all.extend(result)
            page += 1
            url_query = url_base + "?per_page=" + str(per_page) + "&page=" + str(page)
            result = self._response_to_json(self._request("GET", url_query, None))
        return result_all

    def team_discussion_create(self, organization_name=None, team_slug_name=None, discussion_title=None, private=False):
        """
        This method creates a new discussion post on a team's page
        According API docs: https://docs.github.com/en/rest/teams/discussions#create-a-discussion
        :param organization_name: string; name of the current organization created at GitHub
        :param team_slug_name: string; GitHub Team slug name
        :param discussion_title: string; The discussion post's title
        :param private: boolean: Private posts are only visible to team members, organization owners, and team maintainers. Public posts are visible to all members of the organization. Set to true to create a private post.
        :return: request
        """
        body = {
            'title': discussion_title,
            'body': discussion_title,
            'private': private
        }
        url = self.github_url + "/orgs/" + organization_name + "/teams/" + team_slug_name + "/discussions"
        return self._request("POST", url, body)

    def team_discussion_search(self, organization_name=None, team_slug_name=None, discussion_title=None,
                               create_if_not_exists=False, private=False):
        """
        This method returns a discussion if exists, else None
        According API docs: https://docs.github.com/en/rest/teams/discussions#create-a-discussion
        :param organization_name: string; name of the current organization created at GitHub
        :param team_slug_name: string; GitHub Team slug name
        :param discussion_title: string; The discussion post's title
        :param create_if_not_exists: bool; If discussion does not exist, create one
        :param private: boolean; Private posts are only visible to team members, organization owners, and team maintainers. Public posts are visible to all members of the organization. Set to true to create a private post.
        :return: request
        """

        def _search_discussion(discussions: list, search_title: str):
            for discussion in discussions:
                if discussion['title'] == search_title:
                    return discussion

        index = 1

        discussions = self.team_discussion_list(organization_name, team_slug_name, page=index)
        if discussions.status_code >= 300:
            raise GithubUtilsException(discussions.text)
        discussions = json.loads(discussions.text)

        while len(discussions) > 0:
            discussion = _search_discussion(discussions, discussion_title)
            if discussion is not None:
                return discussion

            index += 1
            discussions = json.loads(self.team_discussion_list(organization_name, team_slug_name, page=index).text)

        if create_if_not_exists:
            return json.loads(
                self.team_discussion_create(organization_name, team_slug_name, discussion_title, private).text)

    def team_discussion_list(self, organization_name=None, team_slug_name=None, per_page=30, page=1):
        """
        This method list all discussions on a team's page.
        According API docs: https://docs.github.com/en/rest/teams/discussions#list-discussions
        :param organization_name: string; name of the current organization created at GitHub
        :param team_slug_name: string; GitHub Team slug name
        :param per_page: integer; Results per page (max 100). Default: 30
        :param page: integer; Page number of the results to fetch. Default: 1
        :return: request
        """
        body = {}
        query = "?per_page=" + str(per_page) + "&page=" + str(page)
        url = self.github_url + "/orgs/" + organization_name + "/teams/" + team_slug_name + "/discussions" + query
        return self._request("GET", url.lower(), body)

    def team_discussion_create_comment(self, organization_name=None, team_slug_name=None, discussion_number=None,
                                       comment_body=None):
        """
        This method creates a new comment on a team discussion.
        According API docs: https://docs.github.com/en/rest/teams/discussion-comments#create-a-discussion-comment
        :param organization_name: string; name of the current organization created at GitHub
        :param team_slug_name: string; GitHub Team slug name
        :param discussion_number: string; The number that identifies the discussion
        :param comment_body: string; The discussion comment's body text
        :return: request
        """
        body = {
            'body': comment_body
        }
        url = self.github_url + "/orgs/" + organization_name + "/teams/" + team_slug_name + "/discussions/" + str(
            discussion_number) + "/comments"
        return self._request("POST", url, body)

    def list_repositories(self, organization_name=None, type="all", sort="created", per_page=30, page=1):
        """
        This method allows retrieve paginated list in a request object of repositories in a GitHub organization
        According API docs: https://docs.github.com/es/rest/reference/repos#list-organization-repositories
        :param organization_name: string; name of the current organization created at GitHub
        :param type: string; Specifies the types of repositories you want returned. Can be one of all, public, private, forks, sources, member, internal. Default: all
        :param sort: string; Can be one of created, updated, pushed, full_name. Default: created
        :param per_page: integer; Results per page (max 100). Default: 30
        :param page: integer; Page number of the results to fetch. Default: 1
        :return: request
        """
        params = {}
        query = "?per_page=" + str(per_page) + "&page=" + str(page) + "&type=" + type + "&sort=" + sort
        url = self.github_url + "/orgs/" + organization_name + "/repos" + query
        return self._request("GET", url, params)

    def list_repositories_all(self, organization_name=None, repository_type="all", sort="created", per_page=30):
        """
        This method allows listing all repositories in a GitHub organization, without paginate option using the method self.list_repositories
        According API docs: https://docs.github.com/es/rest/reference/repos#list-organization-repositories
        :param organization_name: string; name of the current organization created at GitHub
        :param repository_type: string; Specifies the types of repositories you want returned. Can be one of all, public, private, forks, sources, member, internal. Default: all
        :param sort: string; Can be one of created, updated, pushed, full_name. Default: created
        :param per_page: integer; Results per page (max 100). Default: 30
        :return: Array of repositories
        TODO: Pending refactor with recursive approach to increase legibility and performance
        """
        page = 1
        result = self._response_to_json(
            self.list_repositories(organization_name, type=repository_type, sort=sort, per_page=per_page, page=page))
        result_all = []
        while len(result) > 0:
            page += 1
            result_all.extend(result)
            result = self._response_to_json(
                self.list_repositories(organization_name, type=repository_type, sort=sort, per_page=per_page,
                                       page=page))
        return result_all

    def repository(self, owner=None, repository_name=None):
        """
        This method allows getting all repository's details
        According API docs: https://docs.github.com/es/rest/reference/repos#get-a-repository
        :param owner: string; name of the current organization created at GitHub or the owner
        :param repository_name: string; repository slug name
        :return: request
        """
        params = {}
        url = self.github_url + "/repos/" + owner + "/" + repository_name
        return self._request("GET", url, params)

    def repository_branch_delete(self, owner=None, repository_name=None, branch_name=None):
        """
        This method allows remove a repository branch
        According non-documented API endpoint mentioned in https://github.community/t/how-to-delete-a-branch-through-the-api/211792
        curl -s -X DELETE -u username:${{secrets.GITHUB_TOKEN}} https://api.github.com/repos/${{ github.repository }}/git/refs/heads/${{ github.head_ref }}
        requests.delete(f"{API_URL}/repos/{OWNER}/{REPO}/git/refs/heads/{BRANCH_NAME}")
        :param owner: string; name of the current organization created at GitHub or the owner
        :param repository_name: string; repository slug name
        :param branch_name: string; branch name to be deleted from the repository
        :return: request
        """
        url = f"{self.github_url}/repos/{owner}/{repository_name}/git/refs/heads/{branch_name}"
        params = {}
        return self._request("DELETE", url, params)

    def list_repository_branches(self, owner=None, repository_name=None, protected=None, per_page=30, page=1):
        """
        This method allows retrieve paginated list in a request object of branches in a repository
        According API docs: https://docs.github.com/es/rest/reference/branches#list-branches
        :param owner: string; name of the current organization created at GitHub or the owner
        :param repository_name: string; repository slug name
        :param protected: string; Setting to true returns only protected branches. When set to false, only unprotected branches are returned. Omitting this parameter returns all branches
        :param per_page: integer; Results per page (max 100). Default: 30
        :param page: integer; Page number of the results to fetch. Default: 1
        :return: request
        """
        params = {}
        if protected:
            params['protected'] = protected
        query = "?per_page=" + str(per_page) + "&page=" + str(page)
        url = self.github_url + "/repos/" + owner + "/" + repository_name + "/branches" + query
        return self._request("GET", url, params)

    @PendingDeprecationWarning
    def list_repository_branches_all(self, owner=None, repository_name=None, protected=None, per_page=30):
        """
        DEPRECATED!
        This method allows listing all branches in a repository, without paginate option using the method self.list_repository_branches.
        According API docs: https://docs.github.com/es/rest/reference/branches#list-branches
        :param owner: string; name of the current organization created at GitHub or the owner
        :param repository_name: string; repository slug name
        :param protected: string; Setting to true returns only protected branches. When set to false, only unprotected branches are returned. Omitting this parameter returns all branches
        :param per_page: integer; Results per page (max 100). Default: 30
        :return: Array of branches
        """
        page = 1
        result = self._response_to_json(
            self.list_repository_branches(owner=owner, repository_name=repository_name, protected=protected,
                                          per_page=per_page, page=page))
        result_all = []
        while len(result) > 0:
            page += 1
            result_all.extend(result)
            result = self._response_to_json(
                self.list_repository_branches(owner=owner, repository_name=repository_name, protected=protected,
                                              per_page=per_page, page=page))
        return result_all

    def recursive_get_all_repository_branches(self, organization_name, repository_name, page=1):
        """
        This is a recursive method to get all repository branches using the method self.list_repository_branches
        :param organization_name: string; name of the current organization created at GitHub
        :param repository_name: string; repository slug name
        :param page: integer; Page number of the results to fetch. Default: 1
        :return: Array of branches
        """
        page_size = 100
        list_branches = json.loads(
            self.list_repository_branches(owner=organization_name, repository_name=repository_name, per_page=page_size,
                                          page=page).text)
        if len(list_branches) == page_size:
            list_branches = list_branches + self.recursive_get_all_repository_branches(organization_name,
                                                                                       repository_name, page + 1)
        else:
            return list_branches
        return list_branches

    def get_repository_branch(self, owner=None, repository_name=None, branch_name=None):
        """
        This method allows retrieve paginated list in a request object of branches in a repository
        According API docs: https://docs.github.com/en/rest/branches/branches?apiVersion=2022-11-28#get-a-branch
        :param owner: string; name of the current organization created at GitHub or the owner
        :param repository_name: string; repository slug name
        :param branch_name: string; The name of the branch. Cannot contain wildcard characters.
        :return: request
        """
        url = self.github_url + "/repos/" + owner + "/" + repository_name + "/branches/" + branch_name
        return self._response_to_json(self._request("GET", url, {}))

    def repository_get_commit_details(self, owner, repository_name, reference, per_page=30, page=1):
        """
        This method allows listing all details in a commit
        According API docs: https://docs.github.com/es/rest/reference/commits#get-a-commit
        :param owner: string; name of the current organization created at GitHub or the owner
        :param repository_name: string; repository slug name
        :param reference: string; ref parameter
        :param per_page: integer; Results per page (max 100). Default: 30
        :param page: integer; Page number of the results to fetch. Default: 1
        :return: commit details
        """
        params = {}
        query = "?per_page=" + str(per_page) + "&page=" + str(page)
        url = self.github_url + "/repos/" + owner + "/" + repository_name + "/commits/" + reference + query
        return self._request("GET", url, params)

    def repository_comment_issue(self, owner, repository_name, pull_number, body_text):
        """
        This method allows to create a comment in a pull request issue
        According API docs: https://docs.github.com/en/rest/reference/pulls#create-a-review-comment-for-a-pull-request
        :param owner: string; name of the current organization created at GitHub or the owner
        :param repository_name: string; repository slug name
        :param pull_number: int; pull request id number
        :param body_text: string; text of the review comment
        :return: requests details
        """
        params = {}
        if body_text:
            params['body'] = body_text
        url = self.github_url + "/repos/" + owner + "/" + repository_name + "/issues/" + str(pull_number) + "/comments"
        print(url)
        print(body_text)
        return self._request("POST", url, params)

    def user_details(self, user_name=None):
        """
        This method allows list all GitHub user properties
        According API docs: https://docs.github.com/es/rest/users/users#get-a-user
        :param user_name: string; Github User Name
        :return: request
        """
        params = {}
        url = self.github_url + "/users/" + user_name
        return self._request("GET", url, params)

    def repository_create_release(self, owner=None, repository_name=None, tag_name=None, release_name=None,
                                  release_body=None, generate_release_notes=False, is_pre_release=False):
        """
        This method creates a new comment on a team discussion.
        According API docs: https://docs.github.com/en/rest/releases/releases#create-a-release
        :param owner: string; The account owner of the repository. The name is not case-sensitive
        :param repository_name: string; The name of the repository. The name is not case-sensitive
        :param tag_name: string; The name of the tag
        :param release_name: string; The name of the release
        :param release_body: string; Text describing the contents of the tag
        :param generate_release_notes: bool; Whether to automatically generate the name and body for this release. If name is specified, the specified name will be used; otherwise, a name will be automatically generated. If body is specified, the body will be pre-pended to the automatically generated notes
        :param is_pre_release: bool; true to identify the release as a prerelease. false to identify the release as a full release.
        :return: request
        """
        body = {
            'tag_name': tag_name,
            'name': release_name,
            'body': release_body,
            'generate_release_notes': generate_release_notes,
            'prerelease': is_pre_release
        }
        url = self.github_url + "/repos/" + owner + "/" + repository_name + "/releases"
        return self._request("POST", url, body)

    def list_repository_teams(self, owner=None, repository_name=None, per_page=30, page=1):
        """
        This method allows retrieve paginated list in a request object branches in a repository
        According API docs: https://docs.github.com/es/rest/repos/repos#list-repository-teams
        :param owner: string; name of the current organization created at GitHub or the owner
        :param repository_name: string; repository slug name
        :param per_page: integer; Results per page (max 100). Default: 30
        :param page: integer; Page number of the results to fetch. Default: 1
        :return: request
        """
        params = {}
        query = "?per_page=" + str(per_page) + "&page=" + str(page)
        url = self.github_url + "/repos/" + owner + "/" + repository_name + "/teams" + query
        return self._request("GET", url, params)

    def list_repository_teams_all(self, owner=None, repository_name=None, per_page=30):
        """
        This method allows listing all branches in a repository, without paginate option using the method self.list_repository_teams.
        According API docs: https://docs.github.com/es/rest/repos/repos#list-repository-teams
        :param owner: string; name of the current organization created at GitHub or the owner
        :param repository_name: string; repository slug name
        :param per_page: integer; Results per page (max 100). Default: 30
        :return: Array of Teams
        TODO: This method is not working properly, it is not returning all teams
        """
        page = 1
        result = self._response_to_json(
            self.list_repository_teams(owner=owner, repository_name=repository_name, per_page=per_page, page=page))
        result_all = []
        while len(result) > 0:
            page += 1
            result_all.extend(result)
            result = self._response_to_json(
                self.list_repository_teams(owner=owner, repository_name=repository_name, per_page=per_page, page=page))
        return result_all

    def list_teams(self, owner=None, per_page=30, page=1):
        """
        This method allows retreive organization teams paginated list in a request object
        According API docs: https://docs.github.com/es/rest/teams/teams#list-teams
        :param owner: string; name of the current organization created at GitHub or the owner
        :param per_page: integer; Results per page (max 100). Default: 30
        :param page: integer; Page number of the results to fetch. Default: 1
        :return: request
        """
        params = {}
        query = "?per_page=" + str(per_page) + "&page=" + str(page)
        url = self.github_url + "/orgs/" + owner + "/teams" + query
        return self._request("GET", url, params)

    def list_teams_all(self, owner=None, per_page=30):
        """
        This method allows listing all teams in an organization, without paginate option using the method self.list_teams.
        According API docs: https://docs.github.com/es/rest/teams/teams#list-teams
        :param owner: string; name of the current organization created at GitHub or the owner
        :param per_page: integer; Results per page (max 100). Default: 30
        :return: Array of Teams
        TODO: Pending refactor with recursive approach to increase legibility and performance
        """
        page = 1
        result = self._response_to_json(self.list_teams(owner=owner, per_page=per_page, page=page))
        result_all = []
        while len(result) > 0:
            page += 1
            result_all.extend(result)
            result = self._response_to_json(self.list_teams(owner=owner, per_page=per_page, page=page))
        return result_all

    def team_by_name(self, owner=None, team_slug=None):
        """
        This method allows gets a team using the team's slug
        According API docs:  https://docs.github.com/es/rest/teams/teams#get-a-team-by-name
        :param owner: string; name of the current organization created at GitHub or the owner
        :param team_slug: string; team slug name
        :return: request
        """
        params = {}
        url = self.github_url + "/orgs/" + owner + "/teams/" + team_slug
        return self._request("GET", url, params)

    def list_repository_tags(self, owner=None, repository_name=None, per_page=30, page=1):
        """
        This method allows retrieve paginated list in a request object of tags in a repository
        According API docs: https://docs.github.com/en/rest/repos/repos#list-repository-tags
        :param owner: string; name of the current organization created at GitHub or the owner
        :param repository_name: string; repository slug name
        :param per_page: integer; Results per page (max 100). Default: 30
        :param page: integer; Page number of the results to fetch. Default: 1
        :return: request
        """
        params = {}
        query = "?per_page=" + str(per_page) + "&page=" + str(page)
        url = self.github_url + "/repos/" + owner + "/" + repository_name + "/tags" + query
        return self._request("GET", url, params)

    def list_repository_tags_all(self, owner=None, repository_name=None, per_page=30):
        """
        This method allows listing all tags in a repository, without paginate option using the method self.list_repository_tags.
        According API docs: https://docs.github.com/en/rest/repos/repos#list-repository-tags
        :param owner: string; name of the current organization created at GitHub or the owner
        :param repository_name: string; repository slug name
        :param per_page: integer; Results per page (max 100). Default: 30
        :return: Array of Tags
        TODO: Pending refactor with recursive approach to increase legibility and performance
        """
        page = 1
        result = self._response_to_json(
            self.list_repository_tags(owner=owner, repository_name=repository_name, per_page=per_page, page=page))
        result_all = []
        while len(result) > 0:
            page += 1
            result_all.extend(result)
            result = self._response_to_json(
                self.list_repository_tags(owner=owner, repository_name=repository_name, per_page=per_page, page=page))
        return result_all

    def list_repository_prs(self, owner=None, repository_name=None, per_page=30, page=1, state="all"):
        """
        This method allows retrieve paginated list in a request object of pull request in a repository by status
        According API docs: https://docs.github.com/en/rest/pulls/pulls#list-pull-requests
        :param owner: string; name of the current organization created at GitHub or the owner
        :param repository_name: string; repository slug name
        :param per_page: integer; Results per page (max 100). Default: 30
        :param page: integer; Page number of the results to fetch. Default: 1
        :param state: string options separated by comma; options: open, closed, or all
        :return: request
        """
        params = {}
        query = f"?per_page={str(per_page)}&page={str(page)}&state={state}"
        url = self.github_url + "/repos/" + owner + "/" + repository_name + "/pulls" + query
        return self._request("GET", url, params)

    def list_repository_prs_all(self, owner=None, repository_name=None, per_page=30, state="all"):
        """
        This method allows listing all pull request in a repository by status without paginate option using the method self.list_repository_prs.
        According API docs: https://docs.github.com/en/rest/pulls/pulls#list-pull-requests
        :param owner: string; name of the current organization created at GitHub or the owner
        :param repository_name: string; repository slug name
        :param per_page: integer; Results per page (max 100). Default: 30
        :param state: string options separated by comma; options: open, closed, or all
        :return: Array of Pull Request
        TODO: Pending refactor with recursive approach to increase legibility and performance
        """
        page = 1
        result = self._response_to_json(
            self.list_repository_prs(owner=owner, repository_name=repository_name, per_page=per_page, page=page,
                                     state=state))
        result_all = []
        while len(result) > 0:
            page += 1
            result_all.extend(result)
            result = self._response_to_json(
                self.list_repository_prs(owner=owner, repository_name=repository_name, per_page=per_page, page=page,
                                         state=state))
        return result_all

    def list_repository_collaborations(self, owner=None, repository_name=None, permission=None, affiliation=None,
                                       per_page=30, page=1):
        """
        This method allows retreive paginated list in a request object collaborations in a repository
        According API docs: https://docs.github.com/es/rest/collaborators/collaborators#list-repository-collaborators
        :param owner: string; name of the current organization created at GitHub or the owner
        :param repository_name: string; repository slug name
        :param permission: string; Can be one of: pull, triage, push, maintain, admin
        :param affiliation: string; Can be one of: outside, direct, all
        :param per_page: integer; Results per page (max 100). Default: 30
        :param page: integer; Page number of the results to fetch. Default: 1
        :return: request
        """
        params = {}
        query = "?per_page=" + str(per_page) + "&page=" + str(page) + "&permission=" + str(
            permission) + "&affiliation=" + str(affiliation)
        url = self.github_url + "/repos/" + owner + "/" + repository_name + "/collaborators" + query
        return self._request("GET", url, params)

    def list_repository_colllaborations_all(self, owner=None, repository_name=None, permission=None, affiliation=None,
                                            per_page=30):
        """
        This method allows listing all collaborations in a repository, without paginate option using the method self.list_repository_colllaborations_all.
        According API docs: https://docs.github.com/es/rest/collaborators/collaborators#list-repository-collaborators
        :param owner: string; name of the current organization created at GitHub or the owner
        :param repository_name: string; repository slug name
        :param permission: string; Can be one of: pull, triage, push, maintain, admin
        :param affiliation: string; Can be one of: outside, direct, all
        :param per_page: integer; Results per page (max 100). Default: 30
        :return: Array of Teams
        TODO: Pending refactor with recursive approach to increase legibility and performance
        """
        page = 1
        result = self._response_to_json(
            self.list_repository_collaborations(owner=owner, repository_name=repository_name, permission=permission,
                                                affiliation=affiliation, per_page=per_page, page=page))
        result_all = []
        while len(result) > 0:
            page += 1
            result_all.extend(result)
            result = self._response_to_json(
                self.list_repository_collaborations(owner=owner, repository_name=repository_name, permission=permission,
                                                    affiliation=affiliation, per_page=per_page, page=page))
        return result_all

    def list_commit_statuses(self, owner=None, repo=None,sha=None, per_page=30, page=1):
        '''
        This method allows retreive paginated list in a request object statuses check in a specific reference
        According API docs: https://docs.github.com/es/rest/commits/statuses?apiVersion=2022-11-28#list-commit-statuses-for-a-reference
        :param owner: string; name of the current organization created at github or the owner
        :param repo: string; repository slug name, required
        :param sha: string; ref parameter, required
        :param per_page: integer; Results per page (max 100). Default: 30
        :param page: integer; Page number of the results to fetch. Default: 1
        :return: request
        '''
        params = {}
        query = "?per_page="+str(per_page)+"&page="+str(page)
        url = self.github_url + "/repos/" + owner + "/" + repo + "/statuses/" + sha  + query
        return self._request("GET", url, params)
    
    def list_commit_statuses_all(self, owner=None, repo=None, sha=None, per_page=30):
        '''
        This method allows listing all statuses check in a specific reference , without paginate option using the method self.list_commit_statuses.
        According API docs: https://docs.github.com/es/rest/commits/statuses?apiVersion=2022-11-28#list-commit-statuses-for-a-reference
        :param owner: string; name of the current organization created at github or the owner
        :param repo: string; repository slug name
        :param sha: string; ref parameter, required
        :param per_page: integer; Results per page (max 100). Default: 30
        :return: Array of Statuses
        TODO: Pending refactor with recursive approach to increase legibility and performance
        '''
        page = 1
        result = self._response_to_json(self.list_commit_statuses(owner=owner, repo=repo,sha=sha,per_page=per_page,page=page))
        result_all = []
        while (len(result)>0):
            page +=1
            result_all.extend(result)
            result = self._response_to_json(self.list_commit_statuses(owner=owner, repo=repo,sha=sha,per_page=per_page,page=page))
        return result_all

    def list_reviews_for_pr(self, owner=None, repo=None, pull_number=None, per_page=30, page=1):
        '''
        This method allows retreive paginated list in a request object pr reviews
        According API docs: https://docs.github.com/en/rest/pulls/reviews?apiVersion=2022-11-28#list-reviews-for-a-pull-request
        :param owner: string; name of the current organization created at github or the owner
        :param repo: string; repository slug name. Required
        :param pull_number: integer; The number that identifies the pull request. Required
        :param per_page: integer; Results per page (max 100). Default: 30
        :param page: integer; Page number of the results to fetch. Default: 1
        :return: request
        '''
        params = {}
        query = "?per_page="+str(per_page)+"&page="+str(page)
        url = self.github_url + "/repos/" + owner + "/" + repo + "/pulls/" + str(pull_number) + "/reviews" + query
        return self._request("GET", url, params)

    def list_reviews_for_pr_all(self, owner=None, repo=None, pull_number=None, per_page=30):
        '''
        This method allows listing all statuses check in a specific reference , without paginate option using the method self.list_commit_statuses.
        According API docs: https://docs.github.com/en/rest/pulls/reviews?apiVersion=2022-11-28#list-reviews-for-a-pull-request
        :param owner: string; name of the current organization created at github or the owner
        :param repo: string; repository slug name
        :param pull_number: integer; The number that identifies the pull request. Required
        :param per_page: integer; Results per page (max 100). Default: 30
        :return: Array of Reviews
        '''
        page = 1
        result = self._response_to_json(self.list_reviews_for_pr(owner=owner, repo=repo,pull_number=pull_number,per_page=per_page,page=page))
        result_all = []
        while (len(result)>0):
            page +=1
            result_all.extend(result)
            result = self._response_to_json(self.list_reviews_for_pr(owner=owner, repo=repo,pull_number=pull_number,per_page=per_page,page=page))
        return result_all
    
    def organization_members_list_all(self, owner=None,per_page=30):
        """
        This method allows listing all organization members , without paginate option using the method self.organization_members_list.
        According API docs: https://docs.github.com/en/rest/orgs/members#list-organization-members
        :param owner: string; name of the current organization created at github or the owner
        :param per_page: integer; Results per page (max 100). Default: 30
        :return: Array of Members
        """
        page = 1
        result = self._response_to_json(self.organization_members_list(organization_name=owner,per_page=per_page,page=page))
        result_all = []
        while (len(result)>0):
            page +=1
            result_all.extend(result)
            result = self._response_to_json(self.organization_members_list(organization_name=owner,per_page=per_page,page=page))
        return result_all
    
    def list_repos_for_a_user(self, username=None, type="all",direction="asc", per_page=30, page=1):
        '''
        This method allows retreive paginated list repos for a user in a request object
        According API docs: https://docs.github.com/en/rest/repos/repos?apiVersion=2022-11-28#list-repositories-for-a-user
        :param username: string; login name of user
        :param type: string; Default: all. Can be one of: all, owner, member
        :param direction: string;Default: asc when using full_name, otherwise desc, Can be one of: asc, desc
        :param per_page: integer; Results per page (max 100). Default: 30
        :param page: integer; Page number of the results to fetch. Default: 1
        :return: request
        '''
        params = {}
        query = "?type="+str(type)+"&direction="+str(direction)+"&per_page="+str(per_page)+"&page="+str(page)
        url = self.github_url + "/users/" + username + "/repos" + query
        return self._request("GET", url, params)

    def list_repos_for_a_user_all(self, username=None, type="all",direction="asc", per_page=30):
        '''
        This method allows listing all repos for a user, without paginate option using the method self.list_repos_for_a_user.
        According API docs: https://docs.github.com/en/rest/repos/repos?apiVersion=2022-11-28#list-repositories-for-a-user
        :param username: string; login name of user
        :param type: string; Default: all. Can be one of: all, owner, member
        :param direction: string;Default: asc when using full_name, otherwise desc, Can be one of: asc, desc
        :param per_page: integer; Results per page (max 100). Default: 30
        :param page: integer; Page number of the results to fetch. Default: 1
        :return: Array of Repositories with permission assoc
        '''
        page = 1
        result = self._response_to_json(self.list_repos_for_a_user(username=username, type=type,direction=direction, per_page=per_page, page=page))
        result_all = []
        while (len(result)>0):
            page +=1
            result_all.extend(result)
            result = self._response_to_json(self.list_repos_for_a_user(username=username, type=type,direction=direction, per_page=per_page, page=page))
        return result_all

    def list_review_comments_on_a_pr(self,owner=None,repo=None,pull_number=None,direction="asc",per_page=30,page=1):
        '''
        This method allows retreive paginated list review comments for a PR in a request object
        According API docs: https://docs.github.com/en/rest/pulls/comments?apiVersion=2022-11-28#list-review-comments-on-a-pull-request
        :param owner: string; name of the current organization created at github or the owner
        :param repo: string; repository slug name
        :param pull_number: integer, pull request number
        :param direction: string;Default: asc when using full_name, otherwise desc, Can be one of: asc, desc
        :param per_page: integer; Results per page (max 100). Default: 30
        :param page: integer; Page number of the results to fetch. Default: 1
        :return: request
        '''
        params = {} 
        query = "?per_page="+str(per_page)+"&page="+str(page)
        url = self.github_url + "/repos/" + str(owner) + "/" + str(repo) + "/issues/" + str(pull_number) + "/comments" + query
        return self._request("GET", url, params)

    def list_review_comments_on_a_pr_all(self, owner=None, repo=None, pull_number=None,direction="asc", per_page=30):
        '''
        This method allows listing all review comments for a PR, without paginate option using the method self.list_review_comments_on_a_pr.
        According API docs: https://docs.github.com/en/rest/pulls/comments?apiVersion=2022-11-28#list-review-comments-on-a-pull-request
        :param owner: string; name of the current organization created at github or the owner
        :param repo: string; repository slug name
        :param pull_number: integer, pull request number
        :param direction: string;Default: asc when using full_name, otherwise desc, Can be one of: asc, desc
        :param per_page: integer; Results per page (max 100). Default: 30
        :return: Array of Review Comments for a PR
        '''
        page = 1
        result = self._response_to_json(self.list_review_comments_on_a_pr(owner=owner, repo=repo, pull_number=pull_number, direction=direction, per_page=1, page=page))
        result_all = []
        while (len(result)>0):
            page +=1
            result_all.extend(result)
            result = self._response_to_json(self.list_review_comments_on_a_pr(owner=owner, repo=repo, pull_number=pull_number, direction=direction, per_page=per_page, page=page))
        return result
    
    # GraphQL Endpoints

    def delete_repository_branch_protection_rule(self, repository_rule: dict) -> requests.Response:
        """
        This method allows to delete specific branch protection rule in a repository
        According API docs: https://docs.github.com/es/graphql/reference/mutations#deletebranchprotectionrule
        :param repository_rule: object deleteBranchProtectionRuleInput; https://docs.github.com/es/graphql/reference/input-objects#deletebranchprotectionruleinput
        :return: request
        """
        query = 'mutation{\
                    deleteBranchProtectionRule(input: { \
                                branchProtectionRuleId: "change_branchProtectionRuleId" \
                    })\
                    {\
                        clientMutationId \
                    }\
            }'

        query = query.replace("change_branchProtectionRuleId", str(repository_rule['id']))
        query = query.replace("\'", "\"")
        myjson = {'query': query}

        return self._request('POST', self.github_url_graphql, data=myjson, is_graphql=True)

    def list_repository_branch_protection_rules(self, owner=None, repository_name=None):
        """
        This method allows list all branch protection rules in a specific repository
        According Github docs: https://github.com/orgs/community/discussions/24596
        :param owner: string; name of the current organization created at GitHub or the owner
        :param repository_name: string; repository slug name
        :return: Array of branch rules
        """
        query = '{ repository ( owner:"org_name" , name: "repo_name" )\
            { \
                branchProtectionRules(first: 100) { \
                    nodes { \
                        id \
                        pattern \
                        isAdminEnforced \
                        allowsDeletions \
                        allowsForcePushes \
                        blocksCreations  \
                        bypassForcePushAllowances (first: 100) { \
                            totalCount \
                            nodes{  \
                                actor { \
                                    ... on Team { name id } \
                                    ... on User { login id } \
                                } \
                            } \
                        } \
                        bypassPullRequestAllowances (first: 100) { \
                            totalCount \
                            nodes{  \
                                actor { \
                                    ... on Team { name id } \
                                    ... on User { login id } \
                                } \
                            } \
                        } \
                        pushAllowances(first: 100) { \
                            totalCount \
                            nodes{  \
                                actor { \
                                    ... on Team { name id } \
                                    ... on User { login id } \
                                    ... on App { name id } \
                                } \
                            } \
                        } \
                        requiredApprovingReviewCount \
                        requiredStatusCheckContexts \
                        requiredStatusChecks{context} \
                        requiresApprovingReviews \
                        requiresCodeOwnerReviews \
                        requiresCommitSignatures \
                        requiresConversationResolution \
                        requiresStatusChecks \
                        requiresStrictStatusChecks \
                        restrictsPushes \
                        requiresLinearHistory \
                        restrictsReviewDismissals \
                        reviewDismissalAllowances(first: 100) { \
                            totalCount \
                            nodes{  \
                                actor { \
                                    ... on Team { name id } \
                                    ... on User { login id } \
                                } \
                            } \
                        } \
                    } \
                } \
            } \
        } '

        query = query.replace("org_name", owner)
        query = query.replace("repo_name", repository_name)

        myjson = {'query': query}

        response = self._request('POST', self.github_url_graphql, data=myjson, is_graphql=True)
        result = self._response_to_json(response)
        return result['data']['repository']['branchProtectionRules']['nodes']

    def create_repository_branch_protection_rule_by_template(self, rule_template, repo_github):
        """
        This method allows to create a branch protection rule defined in a repository template to a specific repository
        According Github docs: https://docs.github.com/es/graphql/reference/mutations#createbranchprotectionrule
        :param rule_template: Object Branch Protection Rule. Params in https://docs.github.com/es/graphql/reference/objects#branchprotectionrule
                              Use method self.list_repository_branch_protection_rules to get specific branch permission rule as a rule template
        :param repo_github: Object Repository; use self.repository to get content body Object (dictionary from JSON)
        :return: Array of branch rule created
        """
        query = 'mutation{\
                    createBranchProtectionRule(input: { \
                                repositoryId: "change_repositoryId" \
                                pattern: "change_pattern" \
                                allowsDeletions:  change_allowsDeletions\
                                allowsForcePushes: change_allowsForcePushes\
                                blocksCreations: change_blocksCreations\
                                bypassForcePushActorIds: change_bypassForcePushActorIds\
                                bypassPullRequestActorIds: change_bypassPullRequestActorIds\
                                isAdminEnforced: change_isAdminEnforced\
                                pushActorIds: change_pushActorIds\
                                dismissesStaleReviews: change_dismissesStaleReviews\
                                requiredApprovingReviewCount: change_requiredApprovingReviewCount\
                                requiredStatusCheckContexts: change_requiredStatusCheckContexts\
                                requiresApprovingReviews: change_requiresApprovingReviews\
                                requiresCodeOwnerReviews: change_requiresCodeOwnerReviews\
                                requiresCommitSignatures: change_requiresCommitSignatures\
                                requiresConversationResolution: change_requiresConversationResolution\
                                requiresLinearHistory: change_requiresLinearHistory\
                                requiresStatusChecks: change_requiresStatusChecks\
                                requiresStrictStatusChecks: change_requiresStrictStatusChecks\
                                restrictsPushes: change_restrictsPushes\
                                restrictsReviewDismissals: change_restrictsReviewDismissals\
                                reviewDismissalActorIds: change_reviewDismissalActorIds\
                    })\
                    {\
                        clientMutationId\
                        branchProtectionRule{pattern}\
                    }\
            }'

        repository_id = repo_github['node_id']
        query = query.replace("change_repositoryId", str(repository_id))

        pattern = rule_template["pattern"]  # String
        query = query.replace("change_pattern", pattern)

        allows_deletions = rule_template["allowsDeletions"]  # Boolean
        query = query.replace("change_allowsDeletions", str(allows_deletions).lower())

        allows_force_pushes = rule_template["allowsForcePushes"]  # Boolean
        query = query.replace("change_allowsForcePushes", str(allows_force_pushes).lower())

        blocks_creations = rule_template["blocksCreations"]  # Boolean
        query = query.replace("change_blocksCreations", str(blocks_creations).lower())

        bypass_force_push_actor_ids = self._get_ids_branch_protection(rule_template["bypassForcePushAllowances"],
                                                                      rule_template[
                                                                          "bypassForcePushAllowances"])  # IDs list
        query = query.replace("change_bypassForcePushActorIds", str(bypass_force_push_actor_ids))

        bypass_pull_request_actor_ids = self._get_ids_branch_protection(rule_template["bypassPullRequestAllowances"],
                                                                        rule_template[
                                                                            "bypassPullRequestAllowances"])  # IDs list
        query = query.replace("change_bypassPullRequestActorIds", str(bypass_pull_request_actor_ids))

        is_admin_enforced = rule_template["isAdminEnforced"]  # Boolean
        query = query.replace("change_isAdminEnforced", str(is_admin_enforced).lower())

        push_actor_ids = self._get_ids_branch_protection(rule_template["pushAllowances"],
                                                         rule_template["pushAllowances"])  # IDs list
        query = query.replace("change_pushActorIds", str(push_actor_ids))

        is_admin_enforced = rule_template.get("dismissesStaleReviews", True)  # Boolean
        query = query.replace("change_dismissesStaleReviews", str(is_admin_enforced).lower())

        required_approving_review_count = rule_template["requiredApprovingReviewCount"]  # int
        if required_approving_review_count is None:
            required_approving_review_count = 0
        query = query.replace("change_requiredApprovingReviewCount",
                              str(required_approving_review_count).lower())  # int

        requires_status_checks = rule_template["requiresStatusChecks"]  # Boolean
        query = query.replace("change_requiresStatusChecks", str(requires_status_checks).lower())  # int

        required_status_check_contexts = rule_template["requiredStatusCheckContexts"]  # [String!]
        query = query.replace("change_requiredStatusCheckContexts", str(required_status_check_contexts))

        requires_approving_reviews = rule_template["requiresApprovingReviews"]  # Boolean
        query = query.replace("change_requiresApprovingReviews", str(requires_approving_reviews).lower())

        requires_code_owner_reviews = rule_template["requiresCodeOwnerReviews"]  # Boolean
        query = query.replace("change_requiresCodeOwnerReviews", str(requires_code_owner_reviews).lower())

        requires_commit_signatures = rule_template["requiresCommitSignatures"]  # Boolean
        query = query.replace("change_requiresCommitSignatures", str(requires_commit_signatures).lower())

        requires_conversation_resolution = rule_template["requiresConversationResolution"]  # Boolean
        query = query.replace("change_requiresConversationResolution", str(requires_conversation_resolution).lower())

        requires_linear_history = rule_template["requiresLinearHistory"]  # Boolean
        query = query.replace("change_requiresLinearHistory", str(requires_linear_history).lower())

        requires_strict_status_checks = rule_template["requiresStrictStatusChecks"]  # Boolean
        query = query.replace("change_requiresStrictStatusChecks", str(requires_strict_status_checks).lower())

        restricts_pushes = rule_template["restrictsPushes"]  # Boolean
        query = query.replace("change_restrictsPushes", str(restricts_pushes).lower())

        restricts_review_dismissals_pushes = rule_template["restrictsReviewDismissals"]  # Boolean
        query = query.replace("change_restrictsReviewDismissals", str(restricts_review_dismissals_pushes).lower())

        review_dismissal_actor_ids = self._get_ids_branch_protection(rule_template["reviewDismissalAllowances"],
                                                                     rule_template[
                                                                         "reviewDismissalAllowances"])  # IDs list
        query = query.replace("change_reviewDismissalActorIds", str(review_dismissal_actor_ids))
        query = query.replace("\'", "\"")

        myjson = {'query': query}

        return self._response_to_json(self._request('POST', self.github_url_graphql, data=myjson, is_graphql=True))

    def update_required_status_check_context_to_branch_policy(self, branch_protection_rule_id,
                                                              status_check_contexts: list):
        """
        Update required status check contexts to branch policy
        According to: TODO: tbc by @jpardin1
        :param branch_protection_rule_id: Branch protection rule id
        :param status_check_contexts: List of status check contexts
        :return: Response
        """
        query = 'mutation{\
                    updateBranchProtectionRule(input: { \
                                branchProtectionRuleId: "change_branchProtectionRuleId" \
                                requiresStatusChecks: true \
                                requiresStrictStatusChecks: true \
                                dismissesStaleReviews: true \
                                requiredStatusCheckContexts: change_requiredStatusCheckContexts \
                                requiredStatusChecks: change_requiredStatusChecks \
                    })\
                    {\
                        clientMutationId\
                        branchProtectionRule{pattern}\
                    }\
            }'
        required_status_checks = ','.join(['{context: ' + f'"{x}"' + "}" for x in status_check_contexts])
        required_status_checks = '[' + required_status_checks + ']'
        query = query.replace("change_branchProtectionRuleId", branch_protection_rule_id)
        query = query.replace("change_requiredStatusCheckContexts", str(status_check_contexts).replace('\'', '"'))
        query = query.replace("change_requiredStatusChecks", required_status_checks)
        query = query.replace("\'", "\"")

        myjson = {'query': query}
        return self._response_to_json(self._request('POST', self.github_url_graphql, data=myjson, is_graphql=True))

    def change_branch_regex_pattern_policies(self, branch_protection_rule_id, new_pattern):
        """
        Change branch regex pattern policies
        According to: TODO: tbc by @jpardin1
        :param branch_protection_rule_id: Branch protection rule id
        :param new_pattern: New pattern
        :return: Response
        """
        query = 'mutation{\
                    updateBranchProtectionRule(input: { \
                                branchProtectionRuleId: "change_branchProtectionRuleId" \
                                pattern: "change_pattern" \
                    })\
                    {\
                        clientMutationId\
                        branchProtectionRule{pattern}\
                    }\
            }'

        query = query.replace("change_branchProtectionRuleId", branch_protection_rule_id)
        query = query.replace("change_pattern", new_pattern)
        query = query.replace("\'", "\"")

        myjson = {'query': query}
        return self._response_to_json(self._request('POST', self.github_url_graphql, data=myjson, is_graphql=True))

    def repository_list_hooks(self, organization_name=None, repository_name=None):
        """
        Lists webhooks for a repository. last response may return null if there have not been any deliveries within 30 days.
        According API docs: https://docs.github.com/en/rest/webhooks/repos?apiVersion=2022-11-28#list-repository-webhooks
        :param organization_name: string; name of the current organization created at GitHub
        :param repository_name: string; Repository name
        :return: request
        """
        params = {}
        url = self.github_url + "/repos/" + organization_name + f"/{repository_name}/" + "hooks"
        return self._request("GET", url, params)

    def repository_create_hook(self, organization_name: str, repository_name: str, hook_payload: dict):
        """
        Repositories can have multiple webhooks installed. Each webhook should have a unique config. Multiple webhooks can share the same config as long as those webhooks do not have any events that overlap.
        According API docs: https://docs.github.com/en/rest/webhooks/repos?apiVersion=2022-11-28#create-a-repository-webhook
        :param organization_name: string; name of the current organization created at GitHub
        :param repository_name: string; Repository name
        :return: request
        """
        url = self.github_url + "/repos/" + organization_name + f"/{repository_name}/" + "hooks"
        return self._request("POST", url=url, data=hook_payload)
