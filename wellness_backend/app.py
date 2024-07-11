from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask_cors import CORS
from flask_restful import Api
from models1 import db
from resource_1 import Login, Register, AppointmentResource, AppointmentDetailResource

app = Flask(__name__)
CORS(app)
api = Api(app)

# Configuration
app.config['SECRET_KEY'] = 'your_secret_key_here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Password%401@localhost:3306/example'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Ensure tables are created
with app.app_context():
    db.create_all()

# Add resources
api.add_resource(Login, '/login')
api.add_resource(Register, '/register')
api.add_resource(AppointmentResource, '/appointments')
api.add_resource(AppointmentDetailResource, '/appointments/<int:appointment_id>')

if __name__ == '__main__':
    app.run(debug=True)

