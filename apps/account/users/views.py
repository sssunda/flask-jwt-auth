from flask_restplus import Resource
from apps.decorators.jwt_auth import jwt_token_required
from apps.account.views import api, create_parser, update_parser
from apps.models.user import User
from apps.models.database import get_session
from apps.utils.validate import check_username, check_password, check_email
from apps.utils.response import success_response, fail_response
from apps.utils.status_code import ERROR_UNAUTHORIZED


ns_users = api.namespace("users")


@ns_users.route('')
class Home(Resource):
    @jwt_token_required
    def get(self, **kwargs):
        auth_user = kwargs['auth_user']
        if not auth_user.is_staff:
            return fail_response('Not Permission. Only Staff', ERROR_UNAUTHORIZED)
        db = get_session()
        user_list = db.query(User).all()

        data = list()
        for user in user_list:
            data.append({
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'created_on': user.created_on,
                'last_login': user.last_login,
                'is_staff': user.is_staff
            })
        return success_response(data)

    def post(self):
        parser = create_parser
        args = parser.parse_args()

        try:
            db = get_session()
            if db.query(User).filter_by(username=args['username']).first():
                return fail_response('Already existed username')
            
            if db.query(User).filter_by(email=args['email']).first():
                return fail_response('Already existed email')

            is_valid, err_msg = check_username(args['username'])
            if not is_valid:
                return fail_response(err_msg)

            is_valid, err_msg = check_password(args['password'], args['password_confirmed'])
            if not is_valid:
                return fail_response(err_msg)

            is_valid, err_msg = check_email(args['email'])
            if not is_valid:
                return fail_response(err_msg)

            user = User(
                username=args['username'],
                password=args['password'],
                email=args['email']
            )
            db.add(user)
        except Exception as e:
            print(e)
            return db.rollback()

        db.commit()
        new_user = db.query(User).filter_by(username=args['username']).first()
        data = {
            'id': new_user.id,
            'username': new_user.username,
            'email': new_user.email,
            'created_on': new_user.created_on
            }
        return success_response(data)


@ns_users.route('/<username>')
class Username(Resource):
    @jwt_token_required
    def get(self, username, **kwargs):
        auth_user = kwargs['auth_user']
        if auth_user.is_staff or kwargs['jwt_username'] == username:
            db = get_session()
            user = db.query(User).filter_by(username=username).first()

            if user:
                auth_user = user
                data = {
                    'id': auth_user.id,
                    'username': auth_user.username,
                    'email': auth_user.email,
                    'created_on': auth_user.created_on,
                    'last_login': auth_user.last_login
                }
                return success_response(data)
            else:
                return fail_response(f'No entry for username. {username}')
        return fail_response('Not Permission', ERROR_UNAUTHORIZED)

    @jwt_token_required
    def put(self, username, **kwargs):
        auth_user = kwargs['auth_user']
        parser = update_parser
        args = parser.parse_args()
        if kwargs['jwt_username'] == username or auth_user.is_staff:
            try:
                db = get_session()
                user = db.query(User).filter_by(username=username).first()

                is_valid, err_msg = check_password(args['password'], args['password_confirmed'])
                if not is_valid:
                    return fail_response(err_msg)

                is_valid, err_msg = check_email(args['email'])
                if not is_valid:
                    return fail_response(err_msg)

                user.set_password(args['password'])
                user.email = args['email']
                db.commit()
            except Exception as e:
                print(e)
                db.rollback()
                return fail_response('Error while update user info')
            data = {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'created_on': user.created_on,
                'last_login': user.last_login
            }
            return success_response(data)
        return fail_response('Not Permission', ERROR_UNAUTHORIZED)

    @jwt_token_required
    def delete(self, username, **kwargs):
        auth_user = kwargs['auth_user']

        if kwargs['jwt_username'] == username or auth_user.is_staff:
            try:
                db = get_session()
                db.query(User).filter_by(username=username).delete()
                db.commit()
            except:
                db.rollback()
                return fail_response(f'Error while deleting user {username}')
            return success_response({'deleted_user': username}, f'success. delete user {username}')
        return fail_response('Not Permission', ERROR_UNAUTHORIZED)