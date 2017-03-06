import gzip
import urllib2
from StringIO import StringIO

from helper import log


def get_url(request_url, header):
    log("http_helper", "request: " + request_url)
    request = urllib2.Request(request_url, None, header)
    response = urllib2.urlopen(request, timeout=10)
    if response.info().get('Content-Encoding') == 'gzip':
        buf = StringIO(response.read())
        f = gzip.GzipFile(fileobj=buf)
        data = f.read()
        return data
    else:
        raise IOError('get data error:' + request_url)
