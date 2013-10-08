pyvka
=====

Python package for authorize and get access_token for `vkontakte api <http://vk.com/developers.php>`_.


Installation
------------

You can install from PyPI::

    $ pip install pyvka==0.1


Example Of Usage
----------------

You should be create `standalone-application <http://vk.com/editapp?act=create>`_, and copy this app ID.

Now, you can use it::

    >>> from pyvka import VKAuth
    >>> login = 'your@email.or.phone.number.here'
    >>> pwd = 'b19b00b5'
    >>> app_id = 123456789
    >>> scopes = ['wall', 'friends']
    >>> vk = VKAuth()
    >>> vk.auth(login, pwd, app_id, scopes)
    >>> access_token = vk.access_token
    >>> user_id = vk.user_id

After receiving access_token you can be using `vkontakte package <https://crate.io/packages/vkontakte/>`_


.. image:: https://d2weczhvl823v0.cloudfront.net/saippuakauppias/pyvka/trend.png
   :alt: Bitdeli badge
   :target: https://bitdeli.com/free

