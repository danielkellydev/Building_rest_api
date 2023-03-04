from flask import Flask

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:newPassword@localhost:5432/book'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


