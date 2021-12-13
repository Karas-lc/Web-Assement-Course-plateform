from flask_wtf.csrf import  CSRFProtect

csrf = CSRFProtect()
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)


from appdir import routes, models


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1')
