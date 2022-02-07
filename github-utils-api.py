# coding=utf-8
import requests
import base64

class GithubUtilsApi:
    '''
    GithubUtilsClass, created to let other scripts to automate DevOps HelpDesk Support
    '''
    def __init__(self, user, token, github_url="https://api.github.com/"):
        '''
        Contructor
        :params user: string; user account at github (email)
        :params token: string; auth personal token with enough permission provided
        :params github_url: string; for GitHub Enterprise take in cosinderation the following pattern http(s)://[hostname]/api/v3/
        '''
        self.github_url = github_url
        self.__user = user
        self.__auth = "Basic "+ str(base64.b64encode(str(user+":"+token).encode('ascii')))

    def __request(self, type, url, data):
        '''
        Request Method with Auth Header required by Github
        '''
        headers = {
            'accept': 'application/vnd.github.v3+json',
            'Authorization': self.__auth
        }
        return requests.request(type, url, headers=headers, data=data)
        

    def repository_org_create(self, organization_name=None, repository_name=None):
        '''
        Allows to create a repository in a defined Github organization
        Using: https://docs.github.com/en/rest/reference/repos#create-an-organization-repository
        :param organization_name: string; name of the current organization created at github
        :param repository_name: string;
        :return: request
        '''
        params = {}
        if repository_name:
            params['repository_name'] = repository_name
        url = self.github_url + organization_name + "/repos"
        return self.__request("POST", url, params)

    #def repository_grant_team()
    #https://docs.github.com/en/rest/reference/teams#add-or-update-team-repository-permissions

    #def team_create()

    #def team_grant_user()