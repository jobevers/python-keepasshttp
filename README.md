[![Build Status](https://travis-ci.org/jobevers/python-keepasshttp.svg?branch=master)](https://travis-ci.org/jobevers/python-keepasshttp)
[![Coverage Status](https://coveralls.io/repos/github/jobevers/python-keepasshttp/badge.svg?branch=master)](https://coveralls.io/github/jobevers/python-keepasshttp?branch=master)


# python-keepasshttp
Access passwords stored in keepass using the http plugin 

## Usage

```python
import keepasshttp

session = keepasshttp.start('my_app_name')
logins = session.getLogins('http://www.amazon.com')
print logins
```

Which will output something like:

```
[{u'Login': 'bezos@amzn.com',
  u'Name': 'Amazon',
  u'Password': Password(*****),
  u'Uuid': '0da19f691e4ab51c11433f809695c84e'}]
```

The password field is protected with a thin wrapper so that it
isn't accidently printed.  The actual value of the password can
be accessed like

```python
logins[0]['Password'].value
```

## Installation

`pip install git+https://github.com/jobevers/python-keepasshttp.git`

## Notes

This library is based based off of the keepasshttp author's
[Protocol Summary](https://github.com/pfn/keepasshttp#protocol)
and the
[Javascript Client Implementation](https://github.com/pfn/passifox/blob/master/chromeipass/background/keepass.js)

I kept a copy of the notebook I used while playing around with the
protocol
[Keepass Protocol](https://github.com/jobevers/python-keepasshttp/blob/master/Keepass%20Protocol.ipynb)
for reference.

## Installing http server for keepassx

Versions of keepassx have been written that port the functionality of
the keepasshttp plugin. Check out
https://github.com/keepassx/keepassx/pull/111 for the latest info.

## Related projects

https://github.com/ccryx/python-keephasshttpc
