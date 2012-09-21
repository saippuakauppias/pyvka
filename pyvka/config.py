from .parser import FormParser


CONFIG = {
    'auth_url': 'http://oauth.vk.com/authorize',
    'redirect_uri': 'http://oauth.vk.com/blank.html',
    'display': 'wap',
    'response_type': 'token',
    'form_parser_class': FormParser
}
