from flask import Flask
from models.database import init_db

app = Flask(__name__)
init_db()

@app.route("/")
def hello():
    return "Hello, World!"

if __name__ == '__main__':
  app.run()
