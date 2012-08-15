from urllib import urlencode
from urllib2 import urlopen
try:
    import json
except ImportError:
    try:
        import simplejson as json
    except ImportError:
        from django.utils import simplejson as json

from geopy.geocoders.base import Geocoder,GeocoderResultError
from geopy import util

class DataScienceToolkit(Geocoder):
    """Geocoder using the DataScienceToolkit API."""

    def __init__(self,domain='www.datasciencetoolkit.org', format_string='%s'):
        if domain == 'www.datasciencetoolkit.org':
            from warnings import warn
            warn('The Data Science Toolkit Website should only be used for testing. '
                 'Deploying the toolkit on your own network is highly recommended.')

        self.domain = domain
        self.format_string = format_string

    @property
    def url(self):
        domain = self.domain.strip('/')
        return "http://%s/street2coordinates" % domain

    def geocode(self, string):
        params = json.dumps([string])
        url = self.url
        page = urlopen(url, params)

        return self.parse_json(page)

    def parse_json(self, page):
        if not isinstance(page, basestring):
            page = util.decode_page(page)
        doc = json.loads(page)
        result = doc.items()[0]

        if not result[1]:
            raise GeocoderResultError("No geographic location was found for the given address")

        def parse_result(result):
            location = result[0]
            latitude = result[1]['latitude']
            longitude = result[1]['longitude']
            return (location,(latitude,longitude))

        return parse_result(result)
