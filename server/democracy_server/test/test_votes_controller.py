# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from democracy_server.models.error import Error  # noqa: E501
from democracy_server.models.object import Object  # noqa: E501
from democracy_server.test import BaseTestCase


class TestVotesController(BaseTestCase):
    """VotesController integration test stubs"""

    def test_create_candidate_vote(self):
        """Test case for create_candidate_vote

        Vote for a candidate
        """
        response = self.client.open(
            '/v1/elections/{electionId}/candidates/{candidateId}/votes'.format(election_id=56, candidate_id=56),
            method='POST')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_candidate_votes(self):
        """Test case for get_candidate_votes

        Get votes for a candidate
        """
        response = self.client.open(
            '/v1/elections/{electionId}/candidates/{candidateId}/votes'.format(election_id=56, candidate_id=56),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
