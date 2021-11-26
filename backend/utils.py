import math
import re


def parse_required_fields(json, fields):
    parsed = {}
    for f in fields:
        if f not in json:
            return None
        else:
            parsed[f] = json[f]
    return parsed


# SOURCE: https://stackoverflow.com/questions/40688156/python-credit-card-validation
def validate_card(card_num):
    """
    Input: Card number, integer or string
    Output: Valid?, boolean
    """
    double = 0
    total = 0

    digits = str(card_num)

    for i in range(len(digits) - 1, -1, -1):
        for c in str((double + 1) * int(digits[i])):
            total += int(c)
        double = (double + 1) % 2

    return (total % 10) == 0


def execute_card_verification(card, cvv):
    """
    Perform external card verification. We don't do this here, so just return true for confirmed
    :rtype: object
    """
    return True


# Source https://stackoverflow.com/questions/3518504/regular-expression-for-matching-latitude-longitude-coordinates

latitude_validator_regex = re.compile("^(\+|-)?(?:90(?:(?:\.0{1,10})?)|(?:[0-9]|[1-8][0-9])(?:(?:\.[0-9]{1,10})?))$")
longitude_validator_regex = re.compile(
    "^(\+|-)?(?:180(?:(?:\.0{1,10})?)|(?:[0-9]|[1-9][0-9]|1[0-7][0-9])(?:(?:\.[0-9]{1,10})?))$")


def is_latitude_valid(latitude):
    return latitude_validator_regex.match(latitude) is not None


def is_longitude_valid(longitude):
    return longitude_validator_regex.match(longitude) is not None


def calculate_gps_distance(coord1, coord2):
    R = 6372800  # Earth radius in meters
    lat1, lon1 = coord1
    lat2, lon2 = coord2

    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)

    a = math.sin(dphi / 2) ** 2 + \
        math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2

    return 2 * R * math.atan2(math.sqrt(a), math.sqrt(1 - a))
