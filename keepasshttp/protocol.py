import logging
import requests

from keepasshttp import common
from keepasshttp import crypto
from keepasshttp import password
from keepasshttp import util


logger = logging.getLogger(__name__)


DEFAULT_KEEPASS_URL = 'http://localhost:19455/'


def associate(requestor=None):
    """Send a new encryption key to keepass.

    Waits for user to accept and provide a name for the association.

    Returns:
        key: the new encryption key
        identifier: the name provided by the user
    """
    requestor = requestor or DEFAULT_REQUESTOR
    key = crypto.getRandomKey()
    input_data = {
        'RequestType': 'associate',
        'Key': key
    }
    output = requestor(key, input_data, None, {})
    return key, output['Id']


def testAssociate(id_, key, requestor=None):
    """Test that keepass has the given identifier and key"""
    requestor = requestor or DEFAULT_REQUESTOR
    input_data = {
        'RequestType': 'test-associate',
    }
    return requestor(key, input_data, id_)


def getLogins(url, id_, key, requestor=None, print_output=False):
    """Query keepass for entries that match `url`"""
    requestor = requestor or DEFAULT_REQUESTOR
    iv = crypto.getRandomIV()
    input_data = {
        'RequestType': 'get-logins',
        'Url': crypto.encrypt(url, key, iv)
    }
    output = requestor(key, input_data, id_, iv=iv)
    if print_output:
        print output
    decrypted = [
        crypto.decryptDict(entry, key, output['Nonce'])
        for entry in output.get('Entries', [])
    ]
    # replace passwords here so that we don't
    # accidently print them
    return [password.replace(e) for e in decrypted]


class Requestor(object):
    def __init__(self, url):
        self.url = url

    def __call__(self, key, input_data, id_, standard_data=None, iv=None):
        data = self.mergeData(key, input_data, id_, standard_data, iv)
        response = requests.post(self.url, json=data)
        return self.processResponse(response, key)

    def mergeData(self, key, input_data, id_, standard_data=None, iv=None):
        # standard_data can be set to {} so need to explicitly check
        # that it is equal to None
        if standard_data is None:
            iv = iv or crypto.getRandomIV()
            standard_data = {
                'Id': id_,
                'Nonce': iv,
                'Verifier': getVerifier(iv, key)
            }
        return util.merge(standard_data, input_data)

    def processResponse(self, response, key):
        if response.status_code != 200:
            raise common.RequestFailed('Failed to get a response', response)
        output = util.convertToStr(response.json())
        if not output['Success']:
            raise common.RequestFailed(
                'keepass returned a unsuccessful response', response)
        if not checkVerifier(key, output['Nonce'], output['Verifier']):
            raise common.RequestFailed('Failed to verify response', response)
        return output
DEFAULT_REQUESTOR = Requestor(DEFAULT_KEEPASS_URL)


def getVerifier(iv, key):
    return crypto.encrypt(iv, key, iv)


def checkVerifier(key, iv, verifier):
    return verifier == crypto.encrypt(iv, key, iv)
