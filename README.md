Simple flask based AD password changer
======================================

Change ldaps/AD password via a webform for those without
direct access to the ldap service.

To install:
-----------

Install dependencies:
```
$ sudo apt-get install python-flask
```

Install web-dependencies:
```
$ (cd static ; ./get.sh)
```

Adjust config.py:
```
$ vi config.py
```

Configure apache to use "chpasswd.wsgi"


To run the tests:
-----------------
```
$ PYTHONPATH=. python test/test_app.py
```

To do:
------

- make the html pretty *cough*
- implement javascript for PW security indicator
- implement auto-discovery via _ldap._tcp.$DOMAIN SRV records
