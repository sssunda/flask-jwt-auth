import re


def check_username(username):
    is_valid = True
    err_msg = ""

    # check length
    length = len(username)
    if length < 6 or length > 20:
        err_msg += "length of username should be 6 ~ 20\n"
        is_valid = False

    # check Uppercase
    regex = r"^[a-z0-9]*$"
    if re.match(regex, username) is None:
        err_msg += "Contains invalid character(Do not allows uppercase and special characters in username)\n"
        is_valid = False

    # check only number
    regex = r"^[0-9]*$"
    if re.match(regex, username):
        err_msg += "username should have at least one lowercase letter"
        is_valid = False

    return is_valid, err_msg


def check_password(password, password_confirmed):
    is_valid = True
    err_msg = ""

    # check length
    length = len(password)
    if length < 6 or length > 20:
        err_msg += "password length should be 6 ~ 20\n"
        is_valid = False

    # check value
    if password != password_confirmed:
        err_msg += "Input same password"
        is_valid = False

    return is_valid, err_msg


def check_email(email):
    is_valid = True

    regex = r"^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    if re.match(regex, email) is None:
        is_valid = False
        return is_valid, "Invalid email address"
    return is_valid, ""

