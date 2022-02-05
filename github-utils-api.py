# coding=utf-8
import requests

class GithubUtilsApi:
    '''GithubUtilsClass'''
    def __init__(self, github_url="https://api.github.com/"):
        self.github_url = github_url

    def repository_org_create(self):
        '''
        Allows to create a repository in a defined Github organization
        '''