pyvka
=====

Python package for authorize and get access_token for `vkontakte api <http://vk.com/developers.php>`_.


Installation
------------

You can install from PyPI::

    $ pip install pyvka==0.1


Example Of Usage
----------------

You should be add `standalone-application <http://vk.com/editapp?act=create>`_, and copy this app ID.

Now, you can use it::
    >>> import pyvka
    >>> vk_login = 'your@mail.or.phonenumber.here'
    >>> vk_password = 'b19b00b5'
    >>> app_id = 123456789
    >>> scopes = ['wall', 'friends']
    >>> access_token = pyvka.get_access_token(vk_login, vk_password, app_id, scopes)
