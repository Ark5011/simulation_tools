from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import string
import random
import pytz

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root@127.0.0.1:8889/archive'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

def generate_random_id(length=6):
    characters = string.ascii_uppercase + string.digits
    random_id = ''.join(random.choice(characters) for _ in range(length))
    return random_id

class Archive(db.Model):
    __tablename__ = 'archive'

    archive_id = db.Column(db.String(6), primary_key=True, unique=True)
    timestamp = db.Column(db.DateTime, default=lambda: datetime.now(pytz.UTC), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    project = db.Column(db.String(100), nullable=False)
    factory = db.Column(db.String(100), nullable=False)
    line = db.Column(db.String(100), nullable=False)
    product = db.Column(db.String(100), nullable=False)
    plant = db.Column(db.String(100), nullable=False)

    def __init__(self, name, project, factory, line, product, plant, timestamp=None):
        self.archive_id = generate_random_id()
        self.name = name
        self.project = project
        self.factory = factory
        self.line = line
        self.product = product
        self.plant = plant
        self.timestamp = timestamp or datetime.now(pytz.UTC)

    def json(self):
        sg_timezone = pytz.timezone('Asia/Singapore')
        timestamp_sg = self.timestamp.astimezone(sg_timezone)
        return {
            "archive_id": self.archive_id,
            "timestamp": timestamp_sg.isoformat(),
            "name": self.name,
            "project": self.project,
            "factory": self.factory,
            "line": self.line,
            "product": self.product,
            "plant": self.plant
        }

@app.route("/archive", methods=['POST'])
def create_archive():
    data = request.get_json()

    archive = Archive(
        name=data['name'],
        project=data['project'],
        factory=data['factory'],
        line=data['line'],
        product=data['product'],
        plant=data['plant'],
        timestamp=datetime.strptime(data['timestamp'], '%Y-%m-%dT%H:%M:%S')
    )

    try:
        db.session.add(archive)
        db.session.commit()
    except Exception as e:
        return jsonify(
            {
                "code": 500,
                "message": "An error occurred creating the archive: " + str(e)
            }
        ), 500

    return jsonify(
        {
            "code": 201,
            "data": archive.json()
        }
    ), 201

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(port=5003, debug=True)
