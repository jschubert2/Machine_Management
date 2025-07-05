from flask import Flask
from flask_cors import CORS
from models import db
from routes import register_routes
from flasgger import Swagger


app = Flask(__name__)
CORS(app)  # Allows frontend to access backend

# Config of the database
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:admin@localhost:5432/mesdb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SWAGGER'] = {
    'title': 'Machine Management API',
    'uiversion': 3
}
swagger = Swagger(app)

# initiate the database with flask
db.init_app(app)

# register routes
register_routes(app)

# tables creation on startup
with app.app_context():
    db.create_all()
    
def print_swagger_url():
    print("\n" + "="*80)
    print("🌐 Swagger Interface for Endpoint Documentation")
    print("👉 http://localhost:5000/apidocs/#/")
    print("="*80 + "\n")

# launch the app
if __name__ == '__main__':
    print_swagger_url()
    app.run(debug=False, port=5000)