from flask_restful import Api, reqparse


api = Api()


# login parser
login_parser = reqparse.RequestParser()
login_parser.add_argument('username', required=True)
login_parser.add_argument('password', required=True)


# create parser
create_parser = reqparse.RequestParser()
create_parser.add_argument('username', required=True)
create_parser.add_argument('password', required=True)
create_parser.add_argument('password_confirmed', required=True)
create_parser.add_argument('email', required=True)


# update parser
update_parser = reqparse.RequestParser()
update_parser.add_argument('password', required=True)
update_parser.add_argument('password_confirmed', required=True)
update_parser.add_argument('email', required=True)