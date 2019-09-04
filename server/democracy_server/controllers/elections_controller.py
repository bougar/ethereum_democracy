"""
Controller for elections method
"""
import connexion
import logging
from flask import current_app
from web3 import Web3

from democracy_server.ethereum.election import Ethereum
from democracy_server.models.create_election import CreateElection  # noqa: E501
from democracy_server.models.created_election import CreatedElection
from democracy_server.models.election import Election  # noqa: E501
from democracy_server.models.election import Candidate  # noqa: E501
from democracy_server.models.elections import Elections  # noqa: E501
from democracy_server.models.error import Error  # noqa: E501


def create_election():  # noqa: E501
    """
    Create an election on the voting systemd

    Returns:
        :obj:`~democracy_server.models.election.Election`: Created election
            representation
    """
    if connexion.request.is_json:
        election = CreateElection.from_dict(connexion.request.get_json())
    factory = current_app.config['FACTORY_CONTRACT']
    account = election.account
    pkey = election.pkey
    name = election.name
    candidates = election.candidates
    election = factory.call('electionNames', [name])
    if len(candidates) < 2:
        message = ('At least two candidates are needed to start an election.'
                   '%s provided' % str(len(candidates)))
        error = Error(
            code=5,
            message=message
        )
        return error, 400
    if election != "0x0000000000000000000000000000000000000000":
        message = ('Election with name \'%s\' already exists on the system'
                   % name)
        error = Error(
            code=3,
            message=message
        )
        return error, 400
    try:
        factory.send('createElection', account, pkey, [name])
    except ValueError as transact_error:
        message = str(transact_error)
        error = Error(
            code=100,
            message=message
        )
        return error, 500
    election = factory.call('electionNames', [name])
    provider = factory.provider
    election_abi = current_app.config['ELECTION_ABI']
    contract = Ethereum(provider, election, election_abi)
    for candidate in candidates:
        contract.send('addCandidate', account, pkey, [candidate.name])
    contract.send('commit', account, pkey)

    return CreatedElection(id=election)


def list_elections(limit=None):  # noqa: E501
    """List elections

     # noqa: E501

    :param limit: How many items to return at one time (max 100)
    :type limit: int

    :rtype: Elections
    """
    contract = current_app.config['FACTORY_CONTRACT']
    elections = contract.call('getElections')
    elections_repr = list()
    for election in elections:
        elections_repr.append(show_election_by_id(election))
    return Elections.from_dict(elections_repr)


def show_election_by_id(election_id):  # noqa: E501
    """Lookup election

     # noqa: E501

    :param election_id: The id of the election to retrieve
    :type election_id: str

    :rtype: Election
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
        candidate = contract.call('candidates', [index])
        name = candidate[0]
        votes = candidate[1]
        candidates.append(
            Candidate(
                name=name,
                votes=votes
            )
        )
    election = Election(
        id=election_id,
        name=contract.call('name'),
        candidates=candidates
    )
    return election
