import connexion
import six

from swagger_server.models.empty import Empty  # noqa: E501
from swagger_server.models.inline_response200 import InlineResponse200  # noqa: E501
from swagger_server.models.inline_response2001 import InlineResponse2001  # noqa: E501
from swagger_server.models.inline_response400 import InlineResponse400  # noqa: E501
from swagger_server.models.inline_response4001 import InlineResponse4001  # noqa: E501
from swagger_server.models.login_login_body import LoginLoginBody  # noqa: E501
from swagger_server.models.register_data import RegisterData  # noqa: E501
from swagger_server import util


def login_activate_post(session_token, activation_token=None):  # noqa: E501
    """Aktywacja konta

    Aktywuje konto w systemie # noqa: E501

    :param session_token: Token sesji
    :type session_token: int
    :param activation_token: Token aktywacyjny z maila, losowy pin 6 znakow 
    :type activation_token: str

    :rtype: Empty
    """
    return 'do some magic!'


def login_login_post(body=None):  # noqa: E501
    """Loguje do systemu

    Loguje uzytkownka do systemu # noqa: E501

    :param body: 
    :type body: dict | bytes

    :rtype: InlineResponse200
    """
    if connexion.request.is_json:
        body = LoginLoginBody.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def login_logout_post(session_token):  # noqa: E501
    """Wyloguj z systemu

     # noqa: E501

    :param session_token: Token sesji
    :type session_token: int

    :rtype: Empty
    """
    return 'do some magic!'


def login_register_post(body):  # noqa: E501
    """Rejestruje uzytkownika do systemu

    Rejestruje uzytkownika do systemu # noqa: E501

    :param body: Registration data
    :type body: dict | bytes

    :rtype: Empty
    """
    if connexion.request.is_json:
        body = RegisterData.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def login_send_token_post(session_token):  # noqa: E501
    """Wysyla token aktywacyjny

     # noqa: E501

    :param session_token: Token sesji
    :type session_token: int

    :rtype: Empty
    """
    return 'do some magic!'


def login_status_get(session_token):  # noqa: E501
    """Pobierz status konta

     # noqa: E501

    :param session_token: Token sesji
    :type session_token: int

    :rtype: InlineResponse2001
    """
    return 'do some magic!'


def login_upload_photos_post(body, session_token, side=None):  # noqa: E501
    """Upload images!

     # noqa: E501

    :param body: 
    :type body: dict | bytes
    :param session_token: Token sesji
    :type session_token: int
    :param side: F jezeli przod, B jezeli tył
    :type side: str

    :rtype: Empty
    """
    if connexion.request.is_json:
        body = Object.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'
