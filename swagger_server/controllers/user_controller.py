import connexion
import six

from swagger_server.models.credit_card import CreditCard  # noqa: E501
from swagger_server.models.empty import Empty  # noqa: E501
from swagger_server.models.gps_location import GPSLocation  # noqa: E501
from swagger_server.models.inline_response4002 import InlineResponse4002  # noqa: E501
from swagger_server.models.inline_response4003 import InlineResponse4003  # noqa: E501
from swagger_server.models.rental import Rental  # noqa: E501
from swagger_server.models.user import User  # noqa: E501
from swagger_server.models.user_cards_body import UserCardsBody  # noqa: E501
from swagger_server.models.user_changepasswd_body import UserChangepasswdBody  # noqa: E501
from swagger_server import util


def user_card_id_get(id, session_token):  # noqa: E501
    """Info na temat konkretnej karty

     # noqa: E501

    :param id: Id karty
    :type id: int
    :param session_token: Token sesji
    :type session_token: int

    :rtype: CreditCard
    """
    return 'do some magic!'


def user_cards_get(session_token):  # noqa: E501
    """Lista kart przypisanych do konta

     # noqa: E501

    :param session_token: Token sesji
    :type session_token: int

    :rtype: List[CreditCard]
    """
    return 'do some magic!'


def user_cards_post(body, session_token):  # noqa: E501
    """Dodaj karte do konta

     # noqa: E501

    :param body: Json Application with given schema
    :type body: dict | bytes
    :param session_token: Token sesji
    :type session_token: int

    :rtype: List[CreditCard]
    """
    if connexion.request.is_json:
        body = UserCardsBody.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def user_changepasswd_post(session_token, body=None):  # noqa: E501
    """Zmien haslo

     # noqa: E501

    :param session_token: Token sesji
    :type session_token: int
    :param body: 
    :type body: dict | bytes

    :rtype: Empty
    """
    if connexion.request.is_json:
        body = UserChangepasswdBody.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def user_details_get(session_token):  # noqa: E501
    """Pobiera informacje o uzytkowniku

     # noqa: E501

    :param session_token: Token sesji
    :type session_token: int

    :rtype: User
    """
    return 'do some magic!'


def user_history_get(session_token, pagelength=None, startindex=None):  # noqa: E501
    """Zwraca historie wypozyczen

     # noqa: E501

    :param session_token: Token sesji
    :type session_token: int
    :param pagelength: Number of records to return
    :type pagelength: float
    :param startindex: Start index for paging
    :type startindex: float

    :rtype: List[Rental]
    """
    return 'do some magic!'


def user_updatelocation_post(session_token, body=None):  # noqa: E501
    """Updates user location

     # noqa: E501

    :param session_token: Token sesji
    :type session_token: int
    :param body: 
    :type body: dict | bytes

    :rtype: Empty
    """
    if connexion.request.is_json:
        body = GPSLocation.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'
