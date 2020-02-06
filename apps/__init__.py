from flask import Flask, session
from models.database import init_db
from account.views import account, api

app = Flask(__name__)
init_db()

api.init_app(account)
app.register_blueprint(account, url_prefix='/account')
app.secret_key = 'super secret key'

@app.route("/")
def hello():
    try:
        if session['logged_in']:
            return "Success Login"
    except:
        return "Hello, World! Please Login!"

if __name__ == '__main__':
  app.run()
