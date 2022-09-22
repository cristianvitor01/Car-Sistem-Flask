from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ce4288ac61ec58ef3cb244e94d46ec8c'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


@app.route('/')
def home_view():
    return 'Hello Word!'


if __name__ == '__main__':
    app.run(debug=True)
