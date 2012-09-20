from HTMLParser import HTMLParser

from .exceptions import ParserError


class FormParser(HTMLParser):

    def __init__(self):
        HTMLParser.__init__(self)
        self.url = None
        self.params = {}
        self.in_form = False
        self.form_parsed = False
        self.method = ''

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
            self.method = attrs.get('method', 'GET').upper()
        elif tag == 'input' and 'type' in attrs and 'name' in attrs:
            if attrs['type'] in ['hidden', 'text', 'password', 'submit']:
                self.params[attrs['name']] = attrs.get('value', '')

    def handle_endtag(self, tag):
        tag = tag.lower()
        if tag == 'form':
            if not self.in_form:
                raise ParserError('Unexpected end of <form>')
            self.in_form = False
            self.form_parsed = True
