from flask import jsonify, make_response
from apps.utils.status_code import SUCCESS_OK, ERROR_BAD_REQUEST


def success_response(data, msg=None, status=SUCCESS_OK):
    if not msg:
        msg = 'Success!'
    return make_response(jsonify({
        'msg': msg,
        'data': data
    }), status)


def fail_response(msg, status=ERROR_BAD_REQUEST):
    return make_response(jsonify({
        'msg': msg
    }), status)