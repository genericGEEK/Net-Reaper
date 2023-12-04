import json
import logging
import requests
from helpers import helpers
from config.config import *

requests.packages.urllib3.disable_warnings()


class AkipsAPI(requests.Session):

    def __init__(self):
        super(AkipsAPI, self).__init__()
        self.base_url = helpers.base_url(host=AKIPS_HOST)
        self.verify = False

    def request(self, method, path, api=None, data=None, **kwargs):
        """ Extends base class method to handle DNA Center JSON data"""
        url = self.base_url + api + '?password={};'.format(AKIPS_PASS) + path
        data = json.dumps(data).encode('utf-8') if data is not None else None
        response = super(AkipsAPI, self).request(method, url, data=data, **kwargs)

        try:
            json_obj = response.json(object_hook=JsonObj)
        except ValueError:
            logging.debug('Response is not JSON encoded')
            json_obj = response
        else:
            if 400 <= response.status_code < 600 and 'response' in json_obj:
                response.reason = _flatten(': ', json_obj.response, ['errorCode', 'message', 'detail'])
        response.raise_for_status()
        return json_obj

class TimeoutError(Exception):
    """ Custom exception raised when a task has timed out """
    pass

class TaskError(Exception):
    """ Custom exception raised when a task has failed """

    def __init__(self, *args, **kwargs):
        self.response = kwargs.pop('response', None)
        super(TaskError, self).__init__(*args, **kwargs)

class JsonObj(dict):
    """ Dictionary with attribute access """

    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__

    def __getattr__(self, name):
        """ x.__getattr__(y) <==> x.y """
        try:
            return self[name]
        except KeyError:
            raise AttributeError(name)

    def __str__(self):
        """ Serialize object to JSON formatted string with indents """
        return json.dumps(self, indent=1)

def _flatten(string, dct, keys):
    """ Helper function to join values of given keys existing in dict """
    return string.join(str(dct[k]) for k in set(keys) & set(dct.keys()))
