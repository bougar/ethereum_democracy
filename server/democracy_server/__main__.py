#!/usr/bin/env python3
"""
Flask entrypoint module
"""

import argparse
import os
import json
import connexion
import logging
from web3 import Web3

from democracy_server.ethereum.election import Ethereum
from democracy_server import encoder


def main():
    logging.basicConfig(level=logging.INFO)
    """
    Swagger server entrypoint function. It makes use of argparse library to
    build a beatiful command line
    """
    python_dir = os.path.dirname(os.path.relpath(__file__))
    specification_dir = os.path.join(python_dir, 'swagger')
    swagger_file = os.path.abspath(
        os.path.join(specification_dir, 'swagger.yaml')
    )
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--factory-abi',
        dest='factory',
        required=True,
        help='Smart contract Factory JSON interface'
    )
    parser.add_argument(
        '--election-abi',
        dest='election',
        required=True,
        help='Smart contract Election JSON interface'
    )
    parser.add_argument(
        '--address',
        required=True,
        help='Smart contract address'
    )
    parser.add_argument(
        '--infura',
        required=True,
        help='Infure URL to build the provider'
    )
    parser.add_argument(
        '-p',
        '--port',
        type=int,
        default=8080,
        help='Port to run the API'
    )
    parser.add_argument(
        '--swagger-file',
        dest='swagger_file',
        default=swagger_file
    )
    parser.add_argument(
        '-d',
        '--debug',
        action='store_true',
        default=False
    )
    args = parser.parse_args()
    swagger_file = os.path.abspath(args.swagger_file)
    if args.debug:
        logging.basicConfig(level=logging.DEBUG)
    app = connexion.FlaskApp(
        __name__,
        specification_dir=os.path.dirname(swagger_file),
        debug=args.debug
    )

    with open(args.factory, 'r') as _file:
        json_repr = json.loads(_file.read())
        if isinstance(json_repr, dict) and 'abi' in json_repr:
            factory_abi = json_repr['abi']
        else:
            factory_abi = json_repr
    with open(args.election, 'r') as _file:
        json_repr = json.loads(_file.read())
        if isinstance(json_repr, dict) and 'abi' in json_repr:
            election_abi = json_repr['abi']
        else:
            election_abi = json_repr

    provider = Web3.HTTPProvider(args.infura)
    factory_contract = Ethereum(provider, args.address, factory_abi)
    app.app.json_encoder = encoder.JSONEncoder
    app.add_api(
        os.path.basename(swagger_file),
        arguments={'title': 'Ethereum Voting'},
        pythonic_params=True
    )
    app.app.config['FACTORY_CONTRACT'] = factory_contract
    app.app.config['ELECTION_ABI'] = election_abi
    app.run(port=args.port)


if __name__ == '__main__':
    main()
