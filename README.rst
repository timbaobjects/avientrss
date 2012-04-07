Avient RSS
==========

Avient RSS is utility web application that scrapes the contents of the Avient package tracking website and converts it into an RSS feed that can be used in numerous applications.

Every shipment has an AWB prefix and AWB number that can be used for online tracking. Using this information, Avient RSS will extract the tracking information from the Avient website and generate an RSS feed. This RSS feed can be used with a service like ifttt to provide SMS, Email and even a phone call notification on tracking updates.

You can inspect an ifttt recipe using an instance of this application here: http://ifttt.com/recipes/28483

Dependencies
============

* `Python <http://python.org/>`_
* `Flask <http://flask.pocoo.org/>`_
* `Requests <http://www.python-requests.org/>`_
* `Beautiful Soup <http://www.crummy.com/software/BeautifulSoup/>`_
* `PyRSS2Gen <http://www.dalkescientific.com/Python/PyRSS2Gen.html>`_