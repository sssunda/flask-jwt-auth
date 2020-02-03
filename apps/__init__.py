from flask import Flask
from models.database import init_db
from account.views import account
app = Flask(__name__)
init_db()
app.register_blueprint(account, url_prefix='/account/')

@app.route("/")
def hello():
    return "Hello, World!"

if __name__ == '__main__':
  app.run()
