import abc
from abc import ABC, abstractmethod
from amsdal_data.connections.base import ConnectionBase as ConnectionBase
from amsdal_utils.models.data_models.address import Address as Address
from typing import Any

class StateConnectionBase(ConnectionBase, ABC, metaclass=abc.ABCMeta):
    @abstractmethod
    def insert(self, address: Address, data: dict[str, Any]) -> None:
        """
        Inserts data to in scope of transaction.

        :param address: the address of the object
        :type address: Address
        :param data: the object data to write
        :type data: dict[str, Any]
        :return: None
        """
    @abstractmethod
    def bulk_insert(self, data: list[tuple[Address, dict[str, Any]]]) -> None:
        """
        Inserts data to in scope of transaction.

        :param data: list of tuples with address and data to write
        :type data: list[tuple[Address, dict[str, Any]]]
        :return: None
        """
    @abstractmethod
    def update(self, address: Address, data: dict[str, Any]) -> None:
        """
        Updates data to in scope of transaction.

        :param address: the address of the object
        :type address: Address
        :param data: the object data to write
        :type data: dict[str, Any]
        :return: None
        """
    @abstractmethod
    def bulk_update(self, data: list[tuple[Address, dict[str, Any]]]) -> None:
        """
        Updates data to in scope of transaction.

        :param data: list of tuples with address and data to write
        :type data: list[tuple[Address, dict[str, Any]]]
        :return: None
        """
    @abstractmethod
    def delete(self, address: Address) -> None:
        """
        Deletes data to in scope of transaction.

        :param address: the address of the object
        :type address: Address
        :return: None
        """
    @abstractmethod
    def bulk_delete(self, addresses: list[Address]) -> None:
        """
        Deletes data to in scope of transaction.

        :param addresses: list of addresses to delete
        :type addresses: list[Address]
        :return: None
        """
