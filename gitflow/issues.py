'''
Created on Apr 18, 2013

@author: pvicente
'''

class IssuesManager(object):
    @staticmethod
    def description():
        raise NotImplementedError()
    
    @staticmethod
    def configure():
        raise NotImplementedError()

class GitHubManager(IssuesManager):
    @staticmethod
    def description():
        return 'Manage Github Issues'
    
    @staticmethod
    def configure():
        pass

