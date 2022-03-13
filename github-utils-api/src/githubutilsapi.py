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
        :params token: string; auth personal token with enough permission provided
        :params github_url: string; for GitHub Enterprise take in cosinderation the following pattern http(s)://[hostname]/api/v3/
        :params proxies: proxies
        '''
        self.github_url = github_url
        self.__user = user
        self.__auth = "Basic "+ str(base64.b64encode(str(user+":"+token).encode('ascii')), "utf-8")
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

    def list_repositories(self, organization_name=None, type="all", sort="created", per_page=None, page=None):
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
        if type:
            params['type'] = type
        if sort:
            params['sort'] = sort
        if per_page:
            params['per_page'] = per_page
        if page:
            params['page'] = page
        url = self.github_url + "/orgs/" + organization_name + "/repos"
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
        query = "?per_page="+per_page+"&page="+page
        url = self.github_url + "/repos/" + owner + "/" + repository_name + "/branches"+query
        return self.__request("GET", url, params)