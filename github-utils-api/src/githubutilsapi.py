# coding=utf-8
import requests
import base64
import json

class GithubUtilsApi:
    '''
    GithubUtilsClass, created to let other scripts to automate DevOps HelpDesk Support
    '''
    def __init__(self, user, token, github_url="https://api.github.com", proxies={}, verify=True):
        '''
        Contructor
        :params user: string; user account at github (email)
        :params token: string; auth personal token with enough permission provided (or password)
        :params github_url: string; for GitHub Enterprise take in cosinderation the following pattern http(s)://[hostname]/api/v3/
        :params proxies: proxies
        '''
        self.github_url = github_url
        self.__user = user
        self.__auth = "Basic "+ str(base64.b64encode(str(self.__user+":"+token).encode('ascii')), "utf-8")
        self.proxies = proxies
        self.verify=verify

    def __request(self, type, url, data):
        '''
        Request Method with Auth Header required by Github
        '''
        headers = {
            'accept': 'application/vnd.github.v3+json',
            'Authorization': self.__auth
        }
        body = json.dumps(data)
        return requests.request(type, url, headers=headers, data=body, proxies=self.proxies, verify=self.verify)
        

    def repository_org_create(self, organization_name=None, repository_name=None, visibility="private"):
        '''
        This method allows creating a repository in a defined Github organization
        According API docs: https://docs.github.com/en/rest/reference/repos#create-an-organization-repository
        :param organization_name: string; name of the current organization created at github
        :param repository_name: string; repository slug name
        :param visibility: private, public or internal
        :return: request
        '''
        params = {}
        if repository_name:
            params['name'] = repository_name
        if visibility:
            params['visibility'] = visibility
        url = self.github_url + "/orgs/" + organization_name + "/repos"
        return self.__request("POST", url, params)

    def repository_grant_team(self, organization_name=None, repository_name=None, repository_owner=None, team_slug_name=None, team_permission='push'):
        '''
        This methows allows granting a Github Team in an specific repository.
        According API docs: https://docs.github.com/en/rest/reference/teams#add-or-update-team-repository-permissions 
        :param organization_name: string; name of the current organization created at github
        :param repository_name: string; repository slug name
        :param repository_owner: string; organization/user owner
        :param team_slug_name: string; Github Team slug name
        :param team_permission: string; options available are -> pull, push, admin, maintain, triage
        :return: request
        '''
        params = {}
        if team_permission:
            params['permission'] = team_permission
        url = self.github_url + "/orgs/" + organization_name + "/teams/" + team_slug_name + "/repos/" + repository_owner + "/" + repository_name
        return self.__request("PUT", url, params)


    def team_create(self, organization_name=None, team_slug_name=None, team_privacy="closed"):
        '''
        This method allows creating a GitHub Team in a defined Github Organization
        According API docs: https://docs.github.com/en/rest/reference/teams#create-a-team
        :param organization_name: string; name of the current organization created at github
        :param team_slug_name: string; Github Team slug name
        :param team_privacy: string; options available -> "secret" (only member) or "closed" all organizational members
        :return: request
        '''
        params = {}
        if team_slug_name:
            params['name'] = team_slug_name
        if team_privacy:
            params['privacy'] = team_privacy
        url = self.github_url + "/orgs/" + organization_name + "/teams"
        return self.__request("POST", url, params)

    def team_grant_user(self, organization_name=None, team_slug_name=None, github_username=None, team_role="member"):
        '''
        This method allows granting a user in a GitHub organization Team  
        According API docs: https://docs.github.com/en/rest/reference/teams#add-or-update-team-membership-for-a-user
        :param organization_name: string; name of the current organization created at github
        :param team_slug_name: string; Github Team slug name
        :param github_username: string; Github Username
        :param team_role: values-> member or maintainer
        :return: request
        '''
        params = {}
        if team_role:
            params['role'] = team_role
        url = self.github_url + "/orgs/" + organization_name + "/teams/" + team_slug_name + "/memberships/" + github_username
        return self.__request("PUT", url, params)

    def team_remove_user(self, organization_name=None, team_slug_name=None, github_username=None):
        '''
        This method allows removing a user in a GitHub organization Team  
        According API docs: https://docs.github.com/en/rest/reference/teams#remove-team-membership-for-a-user
        :param organization_name: string; name of the current organization created at github
        :param team_slug_name: string; Github Team slug name
        :param github_username: string; Github Username
        :return: request
        '''
        params = {}
        url = self.github_url + "/orgs/" + organization_name + "/teams/" + team_slug_name + "/memberships/" + github_username
        return self.__request("DELETE", url, params)

    def list_repositories(self, organization_name=None, type="all", sort="created", per_page=30, page=1):
        '''
        This method allows listing all repositories in a GitHub organization
        According API docs: https://docs.github.com/es/rest/reference/repos#list-organization-repositories
        :param organization_name: string; name of the current organization created at github
        :param type: string; Specifies the types of repositories you want returned. Can be one of all, public, private, forks, sources, member, internal. Default: all
        :param sort: string; Can be one of created, updated, pushed, full_name. Default: created
        :param per_page: integer; Results per page (max 100). Default: 30
        :param page: integer; Page number of the results to fetch. Default: 1
        :return: request
        '''
        params = {}
        query = "?per_page="+str(per_page)+"&page="+str(page)+"&type="+type+"&sort="+sort
        url = self.github_url + "/orgs/" + organization_name + "/repos"+query
        return self.__request("GET", url, params)

    def repository(self, owner=None, repository_name=None):
        '''
        This method allows getting all repository's details
        According API docs: https://docs.github.com/es/rest/reference/repos#get-a-repository
        :param owner: string; name of the current organization created at github or the owner
        :param repository_name: string; repository slug name
        :return: request
        '''
        params = {}
        url = self.github_url + "/repos/" + owner + "/" + repository_name
        return self.__request("GET", url, params)

    def list_repository_branches(self, owner=None, repository_name=None, protected=None, per_page=30, page=1):
        '''
        This method allows listing all branches in a repository
        According API docs: https://docs.github.com/es/rest/reference/branches#list-branches
        :param owner: string; name of the current organization created at github or the owner
        :param repository_name: string; repository slug name
        :protected: string; Setting to true returns only protected branches. When set to false, only unprotected branches are returned. Omitting this parameter returns all branches.
        :param per_page: integer; Results per page (max 100). Default: 30
        :param page: integer; Page number of the results to fetch. Default: 1
        :return: request
        '''
        params = {}
        if protected:
            params['protected'] = protected
        query = "?per_page="+str(per_page)+"&page="+str(page)
        url = self.github_url + "/repos/" + owner + "/" + repository_name + "/branches" + query
        return self.__request("GET", url, params)

    def recursive_get_all_repository_branches(self, organization_name, repository_name, page=1):
        '''
        This is a recursive method to get all repository branches using the method self.list_repository_branches
        :param organization_name: string; name of the current organization created at github
        :param repository_name: string; repository slug name
        :param page: integer; Page number of the results to fetch. Default: 1
        :return: Array of branches
        '''
        page_size = 30
        list_branches = json.loads(self.list_repository_branches(owner=organization_name,repository_name=repository_name,per_page=page_size,page=page).text)
        if len(list_branches) == page_size:
            list_branches = list_branches + self.recursive_get_all_repository_branches(organization_name,repository_name,page+1)
        else:
            return list_branches
        return list_branches

    def repository_get_commit_details(self, owner, repository_name, reference, per_page=30, page=1):
        '''
        This method allows listing all details in a commit
        According API docs: https://docs.github.com/es/rest/reference/commits#get-a-commit
        :param owner: string; name of the current organization created at github or the owner
        :param repository_name: string; repository slug name
        :param reference: string; ref parameter
        :param per_page: integer; Results per page (max 100). Default: 30
        :param page: integer; Page number of the results to fetch. Default: 1
        :return: commit details
        '''
        params = {}
        query = "?per_page="+str(per_page)+"&page="+str(page)
        url = self.github_url + "/repos/" + owner + "/" + repository_name + "/commits/" + reference + query
        return self.__request("GET", url, params)

    def repository_comment_issue(self, owner, repository_name, pull_number, body_text):
        '''
        This method allows create a comment in a pull request issue
        According API docs: https://docs.github.com/en/rest/reference/pulls#create-a-review-comment-for-a-pull-request
        :param owner: string; name of the current organization created at github or the owner
        :param repository_name: string; repository slug name
        :param pull_number: int; pull request id number
        :param body_text: string; text of the review comment
        :return: requests details
        '''
        params = {}
        if body_text:
            params['body'] = body_text
        url = self.github_url + "/repos/" + owner + "/" + repository_name + "/issues/" + str(pull_number) + "/comments"
        return self.__request("POST", url, params)

