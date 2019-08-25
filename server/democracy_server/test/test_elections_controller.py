# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from democracy_server.models.create_election import CreateElection  # noqa: E501
from democracy_server.models.election import Election  # noqa: E501
from democracy_server.models.elections import Elections  # noqa: E501
from democracy_server.models.error import Error  # noqa: E501
from democracy_server.test import BaseTestCase


class TestElectionsController(BaseTestCase):
    """ElectionsController integration test stubs"""

    def test_create_election(self):
        """Test case for create_election

        Create an election
        """
        body = CreateElection()
        response = self.client.open(
            '/v1/elections',
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_list_elections(self):
        """Test case for list_elections

        List elections
        """
        query_string = [('limit', 56)]
        response = self.client.open(
            '/v1/elections',
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_show_election_by_id(self):
        """Test case for show_election_by_id

        Lookup election
        """
        response = self.client.open(
            '/v1/elections/{electionId}'.format(election_id='election_id_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
