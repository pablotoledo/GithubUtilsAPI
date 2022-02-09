# coding=utf-8
import requests
import base64

class GithubUtilsApi:
    '''
    GithubUtilsClass, created to let other scripts to automate DevOps HelpDesk Support
    '''
    def __init__(self, user, token, github_url="https://api.github.com/", proxies={}):
        '''
        Contructor
        :params user: string; user account at github (email)
        :params token: string; auth personal token with enough permission provided
        :params github_url: string; for GitHub Enterprise take in cosinderation the following pattern http(s)://[hostname]/api/v3/
        :params proxies: proxies
        '''
        self.github_url = github_url
        self.__user = user
        self.__auth = "Basic "+ str(base64.b64encode(str(user+":"+token).encode('ascii')))
        self.proxies = proxies

    def __request(self, type, url, data):
        '''
        Request Method with Auth Header required by Github
        '''
        headers = {
            'accept': 'application/vnd.github.v3+json',
            'Authorization': self.__auth
        }
        return requests.request(type, url, headers=headers, data=data, proxies=self.proxies)
        

    def repository_org_create(self, organization_name=None, repository_name=None):
        '''
        Allows to create a repository in a defined Github organization
        According API docs: https://docs.github.com/en/rest/reference/repos#create-an-organization-repository
        :param organization_name: string; name of the current organization created at github
        :param repository_name: string; repository slug name
        :return: request
        '''
        params = {}
        if repository_name:
            params['repository_name'] = repository_name
        url = self.github_url + "/orgs/" + organization_name + "/repos"
        return self.__request("POST", url, params)

    def repository_grant_team(self, organization_name=None, repository_name=None, repository_owner=None, team_slug_name=None, team_permission='push'):
        '''
        This methows allows to grant a Github Team in an specific repository.
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


    def team_create(self, organization_name=None, team_slug_name=None):
        '''
        This method allows to create a GitHub Team in a defined Github Organization
        According API docs: https://docs.github.com/en/rest/reference/teams#create-a-team
        :param organization_name: string; name of the current organization created at github
        :param team_slug_name: string; Github Team slug name
        :return: request
        '''
        params = {}
        if team_slug_name:
            params['name'] = team_slug_name
        url = self.github_url + "/orgs/" + organization_name + "/teams"
        self.__request("POST", url, params)

    #def team_grant_user()
    #https://docs.github.com/en/rest/reference/teams#add-or-update-team-membership-for-a-user