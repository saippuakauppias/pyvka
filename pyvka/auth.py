from urlparse import urlparse, parse_qsl
from urllib import urlencode, unquote_plus

import requests

from .parser import FormParser
from .exceptions import AuthError


class VKAuth(object):

    def __init__(self, login, pwd, app_id, scopes, form_parser_class=None):
        self._login = login
        self._pwd = pwd
        self._app_id = app_id
        self._scopes = scopes
        self._form_parser_class = form_parser_class or FormParser
        self._cookies = {}
        self.access_token = ''
        self.used_id = 0
        self._get_access_token()

    def _get_access_token(self):
        auth_sended_page = self._auth()
        if urlparse(auth_sended_page.url).path != '/blank.html':
            authorized_page = self._get_app_access(auth_sended_page.content)
            self._parse_authorized_url(authorized_page.url)
        else:
            self._parse_authorized_url(auth_sended_page.url)

    def _auth(self):
        auth_url = self._generate_auth_url()
        auth_page = requests.get(auth_url)
        parser = self._form_parser_class()
        parser.feed(auth_page.content)
        parser.close()
        checker = [not parser.form_parsed, parser.url is None,
                   'pass' not in parser.params, 'email' not in parser.params]
        if any(checker):
            raise AuthError('Not found form in auth page')
        parser.params['email'] = self._login
        parser.params['pass'] = self._pwd
        auth_sended_page = self._send_request(parser.method, parser.url,
                                              parser.params)
        self._cookies = auth_sended_page.cookies
        return auth_sended_page

    def _parse_authorized_url(self, url):
        url = urlparse(url)
        params = dict(parse_qsl(url.fragment or url.query))
        if 'error' in params:
            e = '{0}: {1}'.format(params['error'],
                                  unquote_plus(params['error_description']))
            raise AuthError(e)
        self.access_token = params['access_token']
        self.used_id = params['user_id']

    def _get_app_access(self, page_data):
        parser = self._form_parser_class()
        parser.feed(page_data)
        parser.close()
        if not parser.form_parsed or parser.url is None:
            raise AuthError('Not found form in get application access page')
        app_access_sended_page = self._send_request(parser.method, parser.url,
                                                    parser.params)
        return app_access_sended_page

    def _send_request(self, method, url, data):
        if method == 'POST':
            page = requests.post(url, data=data, allow_redirects=True,
                                 cookies=self._cookies)
        else:
            url = '{0}?{1}'.format(url, urlencode(data))
            page = requests.get(url, cookies=self._cookies)
        return page

    def _generate_auth_url(self):
        query_params = {
            'client_id': self._app_id,
            'redirect_uri': 'http://oauth.vk.com/blank.html',
            'display': 'wap',
            'scope': ','.join(self._scopes),
            'response_type': 'token'
        }
        query_params = urlencode(query_params)
        return 'http://oauth.vk.com/authorize?{0}'.format(query_params)
