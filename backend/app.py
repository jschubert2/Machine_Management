from flask import Flask
from flask_cors import CORS
from models import db
from routes import register_routes

app = Flask(__name__)
CORS(app)  # Allows frontend to access backend

# Config de la base de données
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:admin@localhost:5432/mesdb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialisation de la base de données avec l'app Flask
db.init_app(app)

# Enregistrement des routes
register_routes(app)

# Création des tables au démarrage
with app.app_context():
    db.create_all()

# Lancement du serveur
if __name__ == '__main__':
    app.run(debug=False, port=5000)
