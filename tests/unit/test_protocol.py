import unittest

import mock

from keepasshttp import crypto
from keepasshttp import protocol


class TestProtocol(unittest.TestCase):
    def testAssociate(self):
        requestor = mock.Mock(return_value={'Id': 'new_id'})
        key, id_ = protocol.associate(requestor)
        self.assertEqual('new_id', id_)

    def testTestAssociate(self):
        requestor = mock.Mock(return_value=True)
        self.assertTrue(protocol.testAssociate('a', 'b', requestor))

    def testGetLogins(self):
        key = crypto.getRandomKey()
        iv = crypto.getRandomIV()
        requestor = mock.Mock(
            return_value={
                'Entries': [{'key': crypto.encrypt('test', key, iv)}],
                'Nonce': iv,
            }
        )
        logins = protocol.getLogins('a', 'b', key, requestor)
        self.assertEqual([{'key': 'test'}], logins)
