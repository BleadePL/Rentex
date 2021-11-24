import connexion
import six

from swagger_server.models.admin_car_body import AdminCarBody  # noqa: E501
from swagger_server.models.admin_location_body import AdminLocationBody  # noqa: E501
from swagger_server.models.car_id_body import CarIdBody  # noqa: E501
from swagger_server.models.empty import Empty  # noqa: E501
from swagger_server.models.inline_response20010 import InlineResponse20010  # noqa: E501
from swagger_server.models.inline_response20011 import InlineResponse20011  # noqa: E501
from swagger_server.models.inline_response20012 import InlineResponse20012  # noqa: E501
from swagger_server.models.inline_response20013 import InlineResponse20013  # noqa: E501
from swagger_server.models.inline_response20014 import InlineResponse20014  # noqa: E501
from swagger_server.models.inline_response2005 import InlineResponse2005  # noqa: E501
from swagger_server.models.inline_response2006 import InlineResponse2006  # noqa: E501
from swagger_server.models.inline_response2007 import InlineResponse2007  # noqa: E501
from swagger_server.models.inline_response2008 import InlineResponse2008  # noqa: E501
from swagger_server.models.inline_response2009 import InlineResponse2009  # noqa: E501
from swagger_server.models.location_id_body import LocationIdBody  # noqa: E501
from swagger_server.models.user_id_body import UserIdBody  # noqa: E501
from swagger_server import util


def admin_car_get(session_token, location_lat=None, location_long=None, pagelength=None, startindex=None, distance=None,
                  details=None):  # noqa: E501
    """Pobiera liste aut

     # noqa: E501

    :param session_token: Token sesji
    :type session_token: int
    :param location_lat: Szerokosc geograficzna
    :type location_lat: str
    :param location_long: Dlugosc geograficzna
    :type location_long: str
    :param pagelength: Number of records to return
    :type pagelength: float
    :param startindex: Start index for paging
    :type startindex: float
    :param distance: Dystans w m, w jakim szukac. Wartosci wieksze od 2000m beda automatycznie zamieniane na 1km, mniejsze od 100m na 100m
    :type distance: int
    :param details: Szczegoly auta
    :type details: bool

    :rtype: InlineResponse2005
    """
    return 'do some magic!'


def admin_car_id_delete(session_token, id):  # noqa: E501
    """Usuwa auto z systemu

     # noqa: E501

    :param session_token: Token sesji
    :type session_token: int
    :param id: Id auta
    :type id: int

    :rtype: Empty
    """
    return 'do some magic!'


def admin_car_id_get(session_token, id):  # noqa: E501
    """Pobiera szczegoly auta

     # noqa: E501

    :param session_token: Token sesji
    :type session_token: int
    :param id: Id auta
    :type id: int

    :rtype: InlineResponse2007
    """
    return 'do some magic!'


def admin_car_id_patch(session_token, id, body=None):  # noqa: E501
    """Modyfikuje dane auta

     # noqa: E501

    :param session_token: Token sesji
    :type session_token: int
    :param id: Id auta
    :type id: int
    :param body: Co zmienic? Dawac w Jsonie tylko te wartosci, ktore chcesz zmienic (oczywiskie niektorych rzeczy sie nie da, np modyfikowanie ID)
    :type body: dict | bytes

    :rtype: Empty
    """
    if connexion.request.is_json:
        body = CarIdBody.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def admin_car_id_rentalhistory_get(id, session_token, startindex=None, pagelength=None):  # noqa: E501
    """Zwraca historie przejazdow

     # noqa: E501

    :param id: Id auta
    :type id: int
    :param session_token: Token sesji
    :type session_token: int
    :param startindex: Start index for paging
    :type startindex: float
    :param pagelength: Number of records to return
    :type pagelength: float

    :rtype: InlineResponse2008
    """
    return 'do some magic!'


def admin_car_id_reservationhistory_get(id, session_token, startindex=None, pagelength=None):  # noqa: E501
    """Zwraca historie rezerwacji

     # noqa: E501

    :param id: Id auta
    :type id: int
    :param session_token: Token sesji
    :type session_token: int
    :param startindex: Start index for paging
    :type startindex: float
    :param pagelength: Number of records to return
    :type pagelength: float

    :rtype: InlineResponse2009
    """
    return 'do some magic!'


def admin_car_post(body, session_token):  # noqa: E501
    """Dodaje nowe auto

     # noqa: E501

    :param body: Ignorujcie parametry &quot;bez sensu&quot; np last used, last rental itp, nie chce mi sie tworzyc specjalnie scheme na to XD
    :type body: dict | bytes
    :param session_token: Token sesji
    :type session_token: int

    :rtype: InlineResponse2006
    """
    if connexion.request.is_json:
        body = AdminCarBody.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def admin_location_get(session_token, location_lat=None, location_long=None, pagelength=None, startindex=None,
                       distance=None):  # noqa: E501
    """Pobiera liste lokacji

     # noqa: E501

    :param session_token: Token sesji
    :type session_token: int
    :param location_lat: Szerokosc geograficzna
    :type location_lat: str
    :param location_long: Dlugosc geograficzna
    :type location_long: str
    :param pagelength: Number of records to return
    :type pagelength: float
    :param startindex: Start index for paging
    :type startindex: float
    :param distance: Dystans w m, w jakim szukac. Wartosci wieksze od 2000m beda automatycznie zamieniane na 1km, mniejsze od 100m na 100m
    :type distance: int

    :rtype: InlineResponse20012
    """
    return 'do some magic!'


def admin_location_id_delete(session_token, id):  # noqa: E501
    """Usuwa lokacje z systemu

     # noqa: E501

    :param session_token: Token sesji
    :type session_token: int
    :param id: Id lokacji
    :type id: int

    :rtype: Empty
    """
    return 'do some magic!'


def admin_location_id_get(session_token, id):  # noqa: E501
    """Pobiera szczegoly lokacji

     # noqa: E501

    :param session_token: Token sesji
    :type session_token: int
    :param id: Id lokacji
    :type id: int

    :rtype: InlineResponse20014
    """
    return 'do some magic!'


def admin_location_id_patch(session_token, id, body=None):  # noqa: E501
    """Modyfikuje dane Lokacji

     # noqa: E501

    :param session_token: Token sesji
    :type session_token: int
    :param id: Id lokacji
    :type id: int
    :param body: Co zmienic? Dawac w Jsonie tylko te wartosci, ktore chcesz zmienic (oczywiskie niektorych rzeczy sie nie da, np modyfikowanie ID)
    :type body: dict | bytes

    :rtype: Empty
    """
    if connexion.request.is_json:
        body = LocationIdBody.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def admin_location_post(body, session_token):  # noqa: E501
    """Dodaje nową lokację

     # noqa: E501

    :param body: Ignorujcie parametry &quot;bez sensu&quot; itp, nie chce mi sie tworzyc specjalnie scheme na to XD
    :type body: dict | bytes
    :param session_token: Token sesji
    :type session_token: int

    :rtype: InlineResponse20013
    """
    if connexion.request.is_json:
        body = AdminLocationBody.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def admin_user_get(session_token, startindex=None, pagelength=None, details=None, filter=None):  # noqa: E501
    """Zwraca liste uzytkownikow

     # noqa: E501

    :param session_token: Token sesji
    :type session_token: int
    :param startindex: Start index for paging
    :type startindex: float
    :param pagelength: Number of records to return
    :type pagelength: float
    :param details: Szczegoly auta
    :type details: bool
    :param filter: Login lub imie lub nazwisko lub email usera
    :type filter: str

    :rtype: InlineResponse20010
    """
    return 'do some magic!'


def admin_user_id_activate_post(session_token, id):  # noqa: E501
    """Aktywuje konto usera

     # noqa: E501

    :param session_token: Token sesji
    :type session_token: int
    :param id: Id usera
    :type id: int

    :rtype: Empty
    """
    return 'do some magic!'


def admin_user_id_delete(session_token, id):  # noqa: E501
    """Usuwa usera z systemu

     # noqa: E501

    :param session_token: Token sesji
    :type session_token: int
    :param id: Id usera
    :type id: int

    :rtype: Empty
    """
    return 'do some magic!'


def admin_user_id_documents_delete(session_token, id):  # noqa: E501
    """Odrzuca dokumenty uzytkowniika

     # noqa: E501

    :param session_token: Token sesji
    :type session_token: int
    :param id: Id usera
    :type id: int

    :rtype: Empty
    """
    return 'do some magic!'


def admin_user_id_documents_get(session_token, id, side=None):  # noqa: E501
    """Zwraca dokumenty uzytkownika w systemie

     # noqa: E501

    :param session_token: Token sesji
    :type session_token: int
    :param id: Id usera
    :type id: int
    :param side: F - przod, S - tyl
    :type side: str

    :rtype: str
    """
    return 'do some magic!'


def admin_user_id_documents_put(session_token, id):  # noqa: E501
    """Potwierdza dokumety uzytkownika

     # noqa: E501

    :param session_token: Token sesji
    :type session_token: int
    :param id: Id usera
    :type id: int

    :rtype: Empty
    """
    return 'do some magic!'


def admin_user_id_get(session_token, id):  # noqa: E501
    """Pobiera szczegoly uzytkownika

     # noqa: E501

    :param session_token: Token sesji
    :type session_token: int
    :param id: Id usera
    :type id: int

    :rtype: InlineResponse20011
    """
    return 'do some magic!'


def admin_user_id_patch(session_token, id, body=None):  # noqa: E501
    """Modyfikuje dane usera

     # noqa: E501

    :param session_token: Token sesji
    :type session_token: int
    :param id: Id usera
    :type id: int
    :param body: Co zmienic? Dawac w Jsonie tylko te wartosci, ktore chcesz zmienic (oczywiskie niektorych rzeczy sie nie da, np modyfikowanie ID). Nie modyfikowac np aktywacji lub licencji, od tego jest inne api
    :type body: dict | bytes

    :rtype: Empty
    """
    if connexion.request.is_json:
        body = UserIdBody.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def admin_user_id_rentalhistory_get(id, session_token, startindex=None, pagelength=None):  # noqa: E501
    """Zwraca historie przejazdow

     # noqa: E501

    :param id: Id usera
    :type id: int
    :param session_token: Token sesji
    :type session_token: int
    :param startindex: Start index for paging
    :type startindex: float
    :param pagelength: Number of records to return
    :type pagelength: float

    :rtype: InlineResponse2008
    """
    return 'do some magic!'


def admin_user_id_reservationhistory_get(id, session_token, startindex=None, pagelength=None):  # noqa: E501
    """Zwraca historie rezerwacji

     # noqa: E501

    :param id: Id usera
    :type id: int
    :param session_token: Token sesji
    :type session_token: int
    :param startindex: Start index for paging
    :type startindex: float
    :param pagelength: Number of records to return
    :type pagelength: float

    :rtype: InlineResponse2009
    """
    return 'do some magic!'
