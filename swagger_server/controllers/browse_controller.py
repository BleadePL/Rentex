import connexion
import six

from swagger_server.models.car import Car  # noqa: E501
from swagger_server.models.empty import Empty  # noqa: E501
from swagger_server.models.inline_response2002 import InlineResponse2002  # noqa: E501
from swagger_server.models.inline_response2003 import InlineResponse2003  # noqa: E501
from swagger_server.models.location import Location  # noqa: E501
from swagger_server import util


def browse_car_id_get(id, session_token):  # noqa: E501
    """Zwraca konkretne auto po ID

     # noqa: E501

    :param id: Car ID
    :type id: int
    :param session_token: Token sesji
    :type session_token: int

    :rtype: Car
    """
    return 'do some magic!'


def browse_location_id_get(id, session_token):  # noqa: E501
    """Zwraca konkretna lokalizacje po ID

     # noqa: E501

    :param id: Location ID
    :type id: int
    :param session_token: Token sesji
    :type session_token: int

    :rtype: Location
    """
    return 'do some magic!'


def browse_nearestcars_get(session_token, location_lat=None, location_long=None, distance=None):  # noqa: E501
    """Zwraca lokalizacje najblizszych aut

     # noqa: E501

    :param session_token: Token sesji
    :type session_token: int
    :param location_lat: Szerokosc geograficzna
    :type location_lat: str
    :param location_long: Dlugosc geograficzna
    :type location_long: str
    :param distance: Dystans w m, w jakim szukac. Wartosci wieksze od 2000m beda automatycznie zamieniane na 1km, mniejsze od 100m na 100m
    :type distance: int

    :rtype: InlineResponse2002
    """
    return 'do some magic!'


def browse_nearestlocations_get(session_token, location_lat=None, location_long=None, distance=None):  # noqa: E501
    """Zwraca liste najblizszych lokalizacji

     # noqa: E501

    :param session_token: Token sesji
    :type session_token: int
    :param location_lat: Szerokosc geograficzna
    :type location_lat: str
    :param location_long: Dlugosc geograficzna
    :type location_long: str
    :param distance: Dystans w m, w jakim szukac. Wartosci wieksze od 2000m beda automatycznie zamieniane na 1km, mniejsze od 100m na 100m
    :type distance: int

    :rtype: InlineResponse2003
    """
    return 'do some magic!'
