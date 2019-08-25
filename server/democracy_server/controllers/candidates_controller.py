import connexion
import six

from web3 import Web3
from flask import current_app
from democracy_server.ethereum.election import Ethereum
from democracy_server.models.candidate import Candidate  # noqa: E501
from democracy_server.models.error import Error  # noqa: E501
from democracy_server import util


def list_election_candidates(election_id):  # noqa: E501
    """List candidates

     # noqa: E501

    :param election_id: Id of the election
    :type election_id: int

    :rtype: Candidate
    """
    try:
        election_id = Web3.toChecksumAddress(election_id)
    except ValueError:
        message = ('Election ID %s is not an Ethereum address' %
                   election_id)
        error = Error(
            code=1,
            message=message
        )
        return error, 400
    contract = current_app.config['FACTORY_CONTRACT']
    if not contract.call('electionExist', [election_id]):
        message = ("Election with id %s does not exist" % election_id)
        error = Error(
            code=2,
            message=message
        )
        return error, 404
    provider = contract.provider
    election_abi = current_app.config['ELECTION_ABI']
    contract = Ethereum(provider, election_id, election_abi)
    candidates_number = contract.call('numCandidates')
    candidates = list()
    for index in range(candidates_number):
        candidates.append(lookup_candidate(election_id, index))

    return candidates


def lookup_candidate(election_id, candidate_id):  # noqa: E501
    """Lookup Candidate

     # noqa: E501

    :param election_id: Id of the election
    :type election_id: int
    :param candidate_id: Id of the candidate
    :type candidate_id: int

    :rtype: Candidate
    """
    try:
        election_id = Web3.toChecksumAddress(election_id)
    except ValueError:
        message = ('Election ID %s is not an Ethereum address' %
                   election_id)
        error = Error(
            code=1,
            message=message
        )
        return error, 400
    contract = current_app.config['FACTORY_CONTRACT']
    if not contract.call('electionExist', [election_id]):
        message = ("Election with id %s does not exist" % election_id)
        error = Error(
            code=2,
            message=message
        )
        return error, 404
    provider = contract.provider
    election_abi = current_app.config['ELECTION_ABI']
    contract = Ethereum(provider, election_id, election_abi)
    candidates_number = contract.call('numCandidates')
    if candidate_id < 0 or candidate_id > candidates_number:
        message = ("Candidate with id %s does not exist" % candidate_id)
        error = Error(
            code=2,
            message=message
        )
        return error, 404
    candidate = contract.call('candidates', [candidate_id])
    candidate_repr = Candidate(
        id=candidate_id,
        name=candidate[0],
        description=candidate[1],
        votes=candidate[2]
    )
    return candidate_repr
