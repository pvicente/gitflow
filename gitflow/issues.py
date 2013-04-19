'''
Created on Apr 18, 2013

@author: pvicente
'''

from gitflow.util import itersubclasses
from gitflow.core import GitFlow
import re

class IssuesManager(object):
    def __init__(self):
        self._flow = None
    
    @property
    def configured(self):
        return bool(self.flow.get('issues.configured', False))
    
    @configured.setter
    def configured(self, value):
        self.flow.set('issues.configured', value)
    
    @property
    def flow(self):
        if self._flow is None:
            self._flow = GitFlow()
        return self._flow
    
    @property
    def registered(self):
        '''
        Return a list of available classes to manage Issues
        '''
        return [i for i in itersubclasses(self.__class__)]
    
    def configure(self):
        configured = False
        ids = range(len(self.registered))
        while not configured:
            print 'Select the issue manager to configure:'
            print self
            number = raw_input('Type number: ')
            if not number.isdigit() or not int(number) in ids:
                print 'selection error, type a right number'
                continue
            number = int(number)
            configurator_class = self.registered[number]
            configured = configurator_class().configure()
    
    def __str__(self):
        module_description = [str(i()) for i in self.registered]
        index = range(len(self.registered))
        return '\n'.join('%s. %s'%(j,s) for j,s in zip(index, module_description))

class GitHubIssuesManager(IssuesManager):
    RESTRING='git@github.com:(\S+)/(\S+)|git://github.com/(\S+)/(\S+)|https://github.com/(\S+)/(\S+)'
    REGEX = re.compile(RESTRING)
    
    def __init__(self):
        IssuesManager.__init__(self)
        self._url = ''
        self._project = ''
        self._organization = ''
    
    def _extract_organization_proyect(self, url):
        '''
        Return a tuple with the name of organization and project of url
        '''
        r = self.REGEX.match(url)
        if r is None:
            return ('','')
        values = [value for value in r.groups() if not value is None]
        return tuple(values)
        
    
    def __str__(self):
        return "%s\t\t%s"%(self.__class__.__name__, 'Manage issues in Github')
    
    @property
    def url(self):
        ret = ''
        try:
            ret = self.flow.get('remote.origin.url', '')
        except Exception:
            pass
        finally:
            return ret
    
    @property
    def project(self):
        if self._project:
            return self._project
        _, self._project = self._extract_organization_proyect(self.url)
        return self._project
    
    @property
    def organization(self):
        if self._organization:
            return self._organization
        self._organization, _ = self._extract_organization_proyect(self.url)
        return self._organization
    
    def configure(self):
        pass
    
if __name__ == '__main__':
    g = GitHubIssuesManager()
    print g.project, g.organization

