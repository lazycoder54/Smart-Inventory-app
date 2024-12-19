from datetime import datetime
from app import db  

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(20), default="user")
    firebase_uid = db.Column(db.String(120), unique=True, nullable=False)  
    email = db.Column(db.String(120), unique=True, nullable=False)  
    
class InventoryItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Float, nullable=False)
    unit = db.Column(db.String(20), nullable=False) 

class InventoryMovement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey("inventory_item.id"), nullable=False)
    source_location = db.Column(db.String(100), nullable=False)  
    destination_location = db.Column(db.String(100), nullable=False)  
    change = db.Column(db.Float, nullable=False)  
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)  

