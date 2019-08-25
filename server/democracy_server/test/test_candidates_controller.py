# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from democracy_server.models.candidate import Candidate  # noqa: E501
from democracy_server.models.error import Error  # noqa: E501
from democracy_server.test import BaseTestCase


class TestCandidatesController(BaseTestCase):
    """CandidatesController integration test stubs"""

    def test_list_election_candidates(self):
        """Test case for list_election_candidates

        List candidates
        """
        response = self.client.open(
            '/v1/elections/{electionId}/candidates'.format(election_id=56),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_lookup_candidate(self):
        """Test case for lookup_candidate

        Lookup Candidate
        """
        response = self.client.open(
            '/v1/elections/{electionId}/candidates/{candidateId}'.format(election_id=56, candidate_id=56),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
