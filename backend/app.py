from flask import Flask
from flask_cors import CORS
from models import db
from routes import register_routes

app = Flask(__name__)
CORS(app)  # Allows frontend to access backend

# Config of the database
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:admin@localhost:5432/mesdb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# initiate the database with flask
db.init_app(app)

# register routes
register_routes(app)

# tables creation on startup
with app.app_context():
    db.create_all()

# launch the app
if __name__ == '__main__':
    app.run(debug=False, port=5000)
