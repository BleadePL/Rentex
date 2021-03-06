# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from swagger_server.models.base_model_ import Model
from swagger_server import util


class User(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    def __init__(self, login: str = None, email: str = None, name: str = None, surname: str = None,
                 account_type: str = None, status: str = None, balance: str = None):  # noqa: E501
        """User - a model defined in Swagger

        :param login: The login of this User.  # noqa: E501
        :type login: str
        :param email: The email of this User.  # noqa: E501
        :type email: str
        :param name: The name of this User.  # noqa: E501
        :type name: str
        :param surname: The surname of this User.  # noqa: E501
        :type surname: str
        :param account_type: The account_type of this User.  # noqa: E501
        :type account_type: str
        :param status: The status of this User.  # noqa: E501
        :type status: str
        :param balance: The balance of this User.  # noqa: E501
        :type balance: str
        """
        self.swagger_types = {
            'login': str,
            'email': str,
            'name': str,
            'surname': str,
            'account_type': str,
            'status': str,
            'balance': str
        }

        self.attribute_map = {
            'login': 'login',
            'email': 'email',
            'name': 'name',
            'surname': 'surname',
            'account_type': 'accountType',
            'status': 'status',
            'balance': 'balance'
        }
        self._login = login
        self._email = email
        self._name = name
        self._surname = surname
        self._account_type = account_type
        self._status = status
        self._balance = balance

    @classmethod
    def from_dict(cls, dikt) -> 'User':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The User of this User.  # noqa: E501
        :rtype: User
        """
        return util.deserialize_model(dikt, cls)

    @property
    def login(self) -> str:
        """Gets the login of this User.

        Login uzytkownika  # noqa: E501

        :return: The login of this User.
        :rtype: str
        """
        return self._login

    @login.setter
    def login(self, login: str):
        """Sets the login of this User.

        Login uzytkownika  # noqa: E501

        :param login: The login of this User.
        :type login: str
        """

        self._login = login

    @property
    def email(self) -> str:
        """Gets the email of this User.

        Email uzytkownika  # noqa: E501

        :return: The email of this User.
        :rtype: str
        """
        return self._email

    @email.setter
    def email(self, email: str):
        """Sets the email of this User.

        Email uzytkownika  # noqa: E501

        :param email: The email of this User.
        :type email: str
        """

        self._email = email

    @property
    def name(self) -> str:
        """Gets the name of this User.

        Imie  # noqa: E501

        :return: The name of this User.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name: str):
        """Sets the name of this User.

        Imie  # noqa: E501

        :param name: The name of this User.
        :type name: str
        """

        self._name = name

    @property
    def surname(self) -> str:
        """Gets the surname of this User.

        Nazwisko  # noqa: E501

        :return: The surname of this User.
        :rtype: str
        """
        return self._surname

    @surname.setter
    def surname(self, surname: str):
        """Sets the surname of this User.

        Nazwisko  # noqa: E501

        :param surname: The surname of this User.
        :type surname: str
        """

        self._surname = surname

    @property
    def account_type(self) -> str:
        """Gets the account_type of this User.

        PERSONAL - osoba prywatna, COMPANY - firma, ORGANISATION - organizacja, UNKNOWN - Inne  # noqa: E501

        :return: The account_type of this User.
        :rtype: str
        """
        return self._account_type

    @account_type.setter
    def account_type(self, account_type: str):
        """Sets the account_type of this User.

        PERSONAL - osoba prywatna, COMPANY - firma, ORGANISATION - organizacja, UNKNOWN - Inne  # noqa: E501

        :param account_type: The account_type of this User.
        :type account_type: str
        """

        self._account_type = account_type

    @property
    def status(self) -> str:
        """Gets the status of this User.

        ACTIVE - Aktywne konto, INACTIVE - nieaktwyne konto, DOCUMENTS - Brak dokumentow, PENDING - wyslano dokumenty, oczekiwanie na potwierdzenie, PAYMENT - Brak srodkow na koncie, LOCKED - konto zablokowane, DELETED - konto usuniete  # noqa: E501

        :return: The status of this User.
        :rtype: str
        """
        return self._status

    @status.setter
    def status(self, status: str):
        """Sets the status of this User.

        ACTIVE - Aktywne konto, INACTIVE - nieaktwyne konto, DOCUMENTS - Brak dokumentow, PENDING - wyslano dokumenty, oczekiwanie na potwierdzenie, PAYMENT - Brak srodkow na koncie, LOCKED - konto zablokowane, DELETED - konto usuniete  # noqa: E501

        :param status: The status of this User.
        :type status: str
        """

        self._status = status

    @property
    def balance(self) -> str:
        """Gets the balance of this User.

        stan konta w PLN.GR  # noqa: E501

        :return: The balance of this User.
        :rtype: str
        """
        return self._balance

    @balance.setter
    def balance(self, balance: str):
        """Sets the balance of this User.

        stan konta w PLN.GR  # noqa: E501

        :param balance: The balance of this User.
        :type balance: str
        """

        self._balance = balance
