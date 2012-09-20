from urllib import urlencode

import requests

from .parser import FormParser
from .exceptions import ParserError


class VKAuth(object):

    def __init__(self, login, pwd, app_id, scopes, form_parser_class=None):
        self.login = login
        self.pwd = pwd
        self.app_id = app_id
        self.scopes = scopes
        self.form_parser_class = form_parser_class or FormParser

    def get_access_token(self):
        auth_url = self._generate_auth_url()
        auth_page = requests.get(auth_url)
        parser = self.form_parser_class()
        parser.feed(auth_page.content)
        parser.close()
        checker = [not parser.form_parsed, parser.url is None,
                   'pass' not in parser.params, 'email' not in parser.params]
        if  any(checker):
            raise ParserError('Not found form in auth page')

    def _generate_auth_url(self):
        query_params = {
            'client_id': self.app_id,
            'redirect_uri': 'http://oauth.vk.com/blank.html',
            'display': 'wap',
            'scope': ','.join(self.scopes),
            'response_type': 'token'
        }
        query_params = urlencode(query_params)
        return 'http://oauth.vk.com/authorize?{0}'.format(query_params)
