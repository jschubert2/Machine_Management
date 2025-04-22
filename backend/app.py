from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity

app = Flask(__name__)
CORS(app)  # Allows frontend to access backend
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://mesuser:mespass@localhost:5432/mesdb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Machine Model
class Machine(db.Model):
    __tablename__ = 'machines' #new
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(50), nullable=False, default="Idle")

# Create database
#with app.app_context():
 #   db.create_all()

# API Endpoints
@app.route('/machines', methods=['GET'])
def get_machines():
    machines = Machine.query.all()
    return jsonify([{"id": m.id, "name": m.name, "status": m.status} for m in machines])

@app.route('/machines', methods=['POST'])
def add_machine():
    data = request.json
    new_machine = Machine(name=data['name'], status=data['status'])
    db.session.add(new_machine)
    db.session.commit()
    return jsonify({"message": "Machine added successfully!"})

if __name__ == '__main__':
    app.run(debug=True, port=5000)


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Strg+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
