# coding=utf-8
import requests
import base64

class GithubUtilsApi:
    '''GithubUtilsClass'''
    def __init__(self, user, token, github_url="https://api.github.com/"):
        self.github_url = github_url
        self.__user = user
        self.__auth = "Basic "+ str(base64.b64encode(str(user+":"+token).encode('ascii')))

    def __request(self, type, url, data):
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
        :return:
        '''
        params = {}