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
