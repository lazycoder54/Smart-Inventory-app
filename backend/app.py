from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate 
from flask_socketio import SocketIO
from flask_cors import CORS  
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
app.config.from_object("config.Config")

CORS(app, supports_credentials=True)

db = SQLAlchemy(app)
migrate = Migrate(app, db)
jwt = JWTManager(app)
socketio = SocketIO(app, cors_allowed_origins="http://localhost:5173")  

@socketio.on('connect')
def handle_connect():
    print("Client connected")

@socketio.on('disconnect')
def handle_disconnect():
    print("Client disconnected")
    

from routes.auth import auth_bp
from routes.inventory import inventory_bp

app.register_blueprint(auth_bp, url_prefix="/auth")
app.register_blueprint(inventory_bp, url_prefix="/inventory")

from models import User, InventoryItem, InventoryMovement

if __name__ == "__main__":
    socketio.run(app)
