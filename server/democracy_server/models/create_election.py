# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from democracy_server.models.base_model_ import Model
from democracy_server.models.create_candidate import CreateCandidate  # noqa: F401,E501
from democracy_server import util


class CreateElection(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """
    def __init__(self, name: str=None, description: str=None, candidates: List[CreateCandidate]=None, account: str=None, pkey: str=None):  # noqa: E501
        """CreateElection - a model defined in Swagger

        :param name: The name of this CreateElection.  # noqa: E501
        :type name: str
        :param description: The description of this CreateElection.  # noqa: E501
        :type description: str
        :param candidates: The candidates of this CreateElection.  # noqa: E501
        :type candidates: List[CreateCandidate]
        :param account: The account of this CreateElection.  # noqa: E501
        :type account: str
        :param pkey: The pkey of this CreateElection.  # noqa: E501
        :type pkey: str
        """
        self.swagger_types = {
            'name': str,
            'description': str,
            'candidates': List[CreateCandidate],
            'account': str,
            'pkey': str
        }

        self.attribute_map = {
            'name': 'name',
            'description': 'description',
            'candidates': 'candidates',
            'account': 'account',
            'pkey': 'pkey'
        }
        self._name = name
        self._description = description
        self._candidates = candidates
        self._account = account
        self._pkey = pkey

    @classmethod
    def from_dict(cls, dikt) -> 'CreateElection':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The CreateElection of this CreateElection.  # noqa: E501
        :rtype: CreateElection
        """
        return util.deserialize_model(dikt, cls)

    @property
    def name(self) -> str:
        """Gets the name of this CreateElection.


        :return: The name of this CreateElection.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name: str):
        """Sets the name of this CreateElection.


        :param name: The name of this CreateElection.
        :type name: str
        """
        if name is None:
            raise ValueError("Invalid value for `name`, must not be `None`")  # noqa: E501

        self._name = name

    @property
    def description(self) -> str:
        """Gets the description of this CreateElection.


        :return: The description of this CreateElection.
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description: str):
        """Sets the description of this CreateElection.


        :param description: The description of this CreateElection.
        :type description: str
        """

        self._description = description

    @property
    def candidates(self) -> List[CreateCandidate]:
        """Gets the candidates of this CreateElection.


        :return: The candidates of this CreateElection.
        :rtype: List[CreateCandidate]
        """
        return self._candidates

    @candidates.setter
    def candidates(self, candidates: List[CreateCandidate]):
        """Sets the candidates of this CreateElection.


        :param candidates: The candidates of this CreateElection.
        :type candidates: List[CreateCandidate]
        """

        self._candidates = candidates

    @property
    def account(self) -> str:
        """Gets the account of this CreateElection.


        :return: The account of this CreateElection.
        :rtype: str
        """
        return self._account

    @account.setter
    def account(self, account: str):
        """Sets the account of this CreateElection.


        :param account: The account of this CreateElection.
        :type account: str
        """
        if account is None:
            raise ValueError("Invalid value for `account`, must not be `None`")  # noqa: E501

        self._account = account

    @property
    def pkey(self) -> str:
        """Gets the pkey of this CreateElection.


        :return: The pkey of this CreateElection.
        :rtype: str
        """
        return self._pkey

    @pkey.setter
    def pkey(self, pkey: str):
        """Sets the pkey of this CreateElection.


        :param pkey: The pkey of this CreateElection.
        :type pkey: str
        """
        if pkey is None:
            raise ValueError("Invalid value for `pkey`, must not be `None`")  # noqa: E501

        self._pkey = pkey