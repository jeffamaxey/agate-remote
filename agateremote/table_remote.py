#!/usr/bin/env python

"""
This module contains the Remote extension to :class:`Table <agate.table.Table>`.
"""

import agate
import requests
import six


def from_url(cls, url, callback=agate.Table.from_csv, binary=False, requests_encoding=None, **kwargs):
    """
    Download a remote file and pass it to a :class:`.Table` parser.

    :param url:
        URL to a file to load.
    :param callback:
        The method to invoke to create the table. Typically either
        :meth:`agate.Table.from_csv` or :meth:`agate.Table.from_json`, but
        it could also be a method provided by an extension.
    :param requests_encoding:
        An encoding to pass to requests for use when decoding the response
        content. (e.g. force use of 'utf-8-sig' when CSV has a BOM).
    :param binary:
        If :code:`False` the downloaded data will be processed as a string,
        otherwise it will be treated as binary data. (e.g. for Excel files)
    """
    r = requests.get(url)

    if requests_encoding:
        r.encoding = requests_encoding

    if binary:
        content = six.BytesIO(r.content)
    else:
        if six.PY2:
            content = six.StringIO(r.content.decode('utf-8'))
        else:
            content = six.StringIO(r.text)

    return callback(content, **kwargs)


agate.Table.from_url = classmethod(from_url)
