from HTMLParser import HTMLParser

from .exceptions import ParserError


class FormParser(HTMLParser):

    def __init__(self):
        HTMLParser.__init__(self)
        self.url = None
        self.params = {}
        self.in_form = False
        self.form_parsed = False
        self.method = 'GET'

    def handle_starttag(self, tag, attrs):
        tag = tag.lower()
        if tag == 'form':
            if self.form_parsed:
                raise ParserError('Second form on page')
            if self.in_form:
                raise ParserError('Already in form')
            self.in_form = True
        if not self.in_form:
            return
        attrs = dict((name.lower(), value) for name, value in attrs)
        if tag == 'form':
            self.url = attrs['action']
            if 'method' in attrs:
                self.method = attrs['method']
        elif tag == 'input' and 'type' in attrs and 'name' in attrs:
            if attrs['type'] in ['hidden', 'text', 'password']:
                if 'value' in attrs:
                    self.params[attrs['name']] = attrs['value']
                else:
                    self.params[attrs['name']] = ''

    def handle_endtag(self, tag):
        tag = tag.lower()
        if tag == 'form':
            if not self.in_form:
                raise ParserError('Unexpected end of <form>')
            self.in_form = False
            self.form_parsed = True
