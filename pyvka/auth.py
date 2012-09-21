from urlparse import urlparse, parse_qsl
from urllib import urlencode, unquote_plus

import requests

from .config import CONFIG
from .exceptions import AuthError


class VKAuth(object):

    def __init__(self, config={}):
        self.access_token = ''
        self.used_id = 0
        self._cookies = {}
        self.config = CONFIG.update(config)

    def auth(self, login, pwd, app_id, scopes):
        self._login = login
        self._pwd = pwd
        self._app_id = app_id
        self._scopes = scopes
        self._get_access_token()

    def _get_access_token(self):
        auth_sended_page = self._auth()
        if urlparse(auth_sended_page.url).path != '/blank.html':
            authorized_page = self._get_app_access(auth_sended_page.content)
            self._parse_authorized_url(authorized_page.url)
        else:
            self._parse_authorized_url(auth_sended_page.url)

    def _auth(self):
        auth_params = self._generate_auth_params()
        auth_page = self._send_request(self.config['auth_url'], auth_params)
        parser = self.config['form_parser_class']()
        parser.feed(auth_page.content)
        parser.close()
        checker = [not parser.form_parsed, parser.url is None,
                   'pass' not in parser.params, 'email' not in parser.params]
        if any(checker):
            raise AuthError('Not found form in auth page')
        parser.params['email'] = self._login
        parser.params['pass'] = self._pwd
        auth_sended_page = self._send_request(parser.url, parser.params,
                                              parser.method)
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
        parser = self.config['form_parser_class']()
        parser.feed(page_data)
        parser.close()
        if not parser.form_parsed or parser.url is None:
            raise AuthError('Not found form in get application access page')
        app_access_sended_page = self._send_request(parser.url, parser.params,
                                                    parser.method)
        return app_access_sended_page

    def _send_request(self, url, data, method='GET'):
        if method == 'POST':
            page = requests.post(url, data=data, allow_redirects=True,
                                 cookies=self._cookies)
        else:
            url = '{0}?{1}'.format(url, urlencode(data))
            page = requests.get(url, cookies=self._cookies)
        self._cookies.update(page.cookies.items())
        return page

    def _generate_auth_params(self):
        return {
            'client_id': self._app_id,
            'redirect_uri': self.config['redirect_uri'],
            'display': self.config['display'],
            'scope': ','.join(self._scopes),
            'response_type': self.config['response_type']
        }
