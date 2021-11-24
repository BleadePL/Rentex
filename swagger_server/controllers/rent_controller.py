import connexion
import six

from swagger_server.models.empty import Empty  # noqa: E501
from swagger_server.models.inline_response2004 import InlineResponse2004  # noqa: E501
from swagger_server.models.inline_response4004 import InlineResponse4004  # noqa: E501
from swagger_server.models.inline_response4005 import InlineResponse4005  # noqa: E501
from swagger_server.models.rent_rent_body import RentRentBody  # noqa: E501
from swagger_server.models.rental import Rental  # noqa: E501
from swagger_server.models.reservation import Reservation  # noqa: E501
from swagger_server import util


def rent_rent_id_delete(id, session_token):  # noqa: E501
    """Konczy wynajem auta

     # noqa: E501

    :param id: Id wynajmu
    :type id: int
    :param session_token: Token sesji
    :type session_token: int

    :rtype: Empty
    """
    return 'do some magic!'


def rent_rent_id_get(id, session_token):  # noqa: E501
    """Pobiera wynajem auta

     # noqa: E501

    :param id: Id wynajmu
    :type id: int
    :param session_token: Token sesji
    :type session_token: int

    :rtype: Rental
    """
    return 'do some magic!'


def rent_rent_post(body, session_token):  # noqa: E501
    """Wynajmuje auto

     # noqa: E501

    :param body: 
    :type body: dict | bytes
    :param session_token: Token sesji
    :type session_token: int

    :rtype: Empty
    """
    if connexion.request.is_json:
        body = RentRentBody.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def rent_reservate_post(session_token, car_id):  # noqa: E501
    """Rezerwuje auto

     # noqa: E501

    :param session_token: Token sesji
    :type session_token: int
    :param car_id: Id auta
    :type car_id: int

    :rtype: InlineResponse2004
    """
    return 'do some magic!'


def rent_reservation_id_delete(session_token, id):  # noqa: E501
    """Zakoncza rezerwacje

     # noqa: E501

    :param session_token: Token sesji
    :type session_token: int
    :param id: Id rezerwacji
    :type id: int

    :rtype: None
    """
    return 'do some magic!'


def rent_reservation_id_get(id, session_token):  # noqa: E501
    """Pobiera szczegoly rezerwacji

     # noqa: E501

    :param id: Id rezerwacji
    :type id: int
    :param session_token: Token sesji
    :type session_token: int

    :rtype: Reservation
    """
    return 'do some magic!'


def user_card_id_delete(id, session_token):  # noqa: E501
    """Usuwa karte z konta

     # noqa: E501

    :param id: Id karty
    :type id: int
    :param session_token: Token sesji
    :type session_token: int

    :rtype: Empty
    """
    return 'do some magic!'
