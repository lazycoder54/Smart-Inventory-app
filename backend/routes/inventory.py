from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity
from app import db, socketio
from utils.nlp_parser import parse_command, speak_text
from sqlalchemy import func
from utils.voice_recognition import recognize_speech_from_mic, stop_recognition
import time

inventory_bp = Blueprint("inventory", __name__)


@inventory_bp.route("/add", methods=["POST"])
@jwt_required()
def add_item():
    from models import InventoryItem
    from sqlalchemy.exc import DataError
    data = request.json  

    name = data.get("name", "").strip().lower()
    quantity = data.get("quantity")
    unit = data.get("unit", "").strip().lower()
    
    if not name.isalpha():
        return jsonify(message="Item name must contain only alphabets."), 400

    if not isinstance(quantity, (int, float)) or quantity <= 0:
        return jsonify(message="Quantity must be a positive number."), 400

    SUPPORTED_UNITS = ["kg", "g", "lb", "oz", "pcs", "dozen", "pack", "ton", "bottle", "box", "liter"]
    if unit not in SUPPORTED_UNITS:
        return jsonify(message=f"Invalid unit '{unit}'. Supported units are: {', '.join(SUPPORTED_UNITS)}"), 400

    existing_item = InventoryItem.query.filter(
        func.lower(InventoryItem.name) == name,
        func.lower(InventoryItem.unit) == unit
    ).first()

    try:
        if existing_item:
           
            existing_item.quantity += quantity
            db.session.commit()
            socketio.emit("inventory_update", {
                "action": "update",
                "item": {
                    "id": existing_item.id,
                    "name": existing_item.name,
                    "quantity": existing_item.quantity,
                    "unit": existing_item.unit,
                }
            })
            return jsonify(message="Item quantity updated successfully", item_id=existing_item.id), 200

        new_item = InventoryItem(name=name, quantity=quantity, unit=unit)
        db.session.add(new_item)
        db.session.commit()
        socketio.emit("inventory_update", {
            "action": "add",
            "item": {
                "id": new_item.id,
                "name": new_item.name,
                "quantity": new_item.quantity,
                "unit": new_item.unit,
            }
        })
        return jsonify(message="New item added successfully", item_id=new_item.id), 201

    except DataError as e:
        db.session.rollback()
        return jsonify(message="Invalid data provided.", error=str(e)), 400

@inventory_bp.route("/update/<int:item_id>", methods=["PUT"])
@jwt_required()
def update_item(item_id):
    from models import InventoryItem
    
    data = request.json
    item = InventoryItem.query.get(item_id)
    if not item:
        return jsonify(message="Item not found"), 404
    item.quantity = data["quantity"]
    db.session.commit()
    
    socketio.emit("inventory_update", {"action": "update", "item": {"id": item_id,"name": item.name, "quantity": data["quantity"]}})
    return jsonify(message="Item updated successfully", name=item.name), 200

@inventory_bp.route("/delete/<int:item_id>", methods=["DELETE"])
@jwt_required()
def delete_item(item_id):
    from models import InventoryItem
    
    item = InventoryItem.query.get(item_id)
    if not item:
        return jsonify(message="Item not found"), 404

    db.session.delete(item)
    db.session.commit()
    socketio.emit("inventory_update", {"action": "delete", "item_id": item_id})
    return jsonify(message="Item deleted successfully"), 200

@inventory_bp.route("/list", methods=["GET"])
@jwt_required()
def list_items():
    from models import InventoryItem
    user_id = get_jwt_identity() 
    claims = get_jwt() 
    
    role = claims.get("role", "user")
    items = InventoryItem.query.all()
    item_list = [
        {"id": item.id, 
         "name": item.name, 
         "quantity": item.quantity, 
         "unit": item.unit} 
        for item in items
        ]
    return jsonify(items=item_list), 200

@inventory_bp.route("/restricted", methods=["GET"])
@jwt_required()
def restricted_area():
    claims = get_jwt()  
    role = claims.get("role", "user")
    if role != "admin":
        return jsonify(message="Admins only!"), 403
    return jsonify(message="Welcome to the admin area.")

@inventory_bp.route("/add-nlp", methods=["POST"])
@jwt_required()
def add_item_nlp():
    from models import InventoryItem
    
    data = request.json
    command = data.get("command")
    
    try:
        parsed_data = parse_command(command)
        existing_item = InventoryItem.query.filter_by(name=parsed_data["name"], unit=parsed_data["unit"]).first()
        if existing_item:
            existing_item.quantity += parsed_data["quantity"]
        else:
            new_item = InventoryItem(
                name=parsed_data["name"],
                quantity=parsed_data["quantity"],
                unit=parsed_data["unit"]
            )
            db.session.add(new_item)
        db.session.commit() 
        socketio.emit("inventory_update", {"action": "add", "item": parsed_data})

        return jsonify(message="Item processed and added successfully"), 201
    except ValueError as e:
        return jsonify(message=str(e)), 400

    
@inventory_bp.route("/add-voice", methods=["POST"])
@jwt_required()
def add_item_voice():
    from models import InventoryItem 
    try:
        
        command = recognize_speech_from_mic()
        if not command:
            return jsonify(message="Failed to recognize speech"), 400
        
        start_time = time.time()
        parsed_data = parse_command(command)
        parsed_data["name"] = parsed_data["name"].lower()

        if parsed_data['action'] == 'add':
            existing_item = InventoryItem.query.filter(
                db.func.lower(InventoryItem.name) == parsed_data["name"],
                InventoryItem.unit == parsed_data["unit"]
            ).first()
            if existing_item:    
                existing_item.quantity += parsed_data["quantity"]
            else:
                new_item = InventoryItem(
                    name=parsed_data["name"],
                    quantity=parsed_data["quantity"],
                    unit=parsed_data["unit"]
                )
                db.session.add(new_item) 
            db.session.commit()
            
            speak_text(f"Item '{parsed_data['name']}' added successfully.")
            response_message = f'{command}'
            return jsonify(message=response_message), 201

        elif parsed_data['action'] == 'update':
            
            existing_item = InventoryItem.query.filter(
                db.func.lower(InventoryItem.name) == parsed_data["name"],
                InventoryItem.unit == parsed_data["unit"]
            ).first()

            if existing_item:
                existing_item.quantity = parsed_data["quantity"]
                db.session.commit()
                speak_text(f"Item '{parsed_data['name']}' updated successfully.")
                response_message = f'{command}'
                return jsonify(message=response_message), 200
            else:
                speak_text(f"Item '{parsed_data['name']}' not found.")
                response_message = f"Item '{parsed_data['name']}' not found."
                return jsonify(message=response_message), 404

        elif parsed_data['action'] == 'remove':
            response_message = None 
            try:
                existing_item = InventoryItem.query.filter(
                db.func.lower(InventoryItem.name) == parsed_data["name"].lower(),
                InventoryItem.unit == parsed_data["unit"]
                ).first()

                if existing_item:
                    existing_item.quantity -= parsed_data["quantity"]
                    if existing_item.quantity <= 0:
                        warning_message = (
                            f"Item '{parsed_data['name']}' will be removed completely as the quantity "
                            f"after removing {parsed_data['quantity']} {parsed_data['unit']} will be nil. "
                            "Are you sure you want to delete it?"
                        )
                        speak_text(warning_message)
                        response_message = warning_message 
                
                        return jsonify(message=response_message, action_required="confirm_deletion"), 409
                    else:
                        response_message = (
                            f"Item '{parsed_data['name']}' updated with reduced quantity: "
                            f"{existing_item.quantity} {existing_item.unit} remaining."
                        )
                
                    db.session.commit()
                    response_message = f"{command}"
                else:        
                
                    response_message = f"Item '{parsed_data['name']}' not found in inventory."
                
                if response_message:  
                    speak_text(response_message)
                    return jsonify(message=response_message), (200 if existing_item else 404)
                else:
                    
                    raise ValueError("Unexpected error: response_message is not set.")
        
            except Exception as e:
                # Handle unexpected errors
                error_message = f"An unexpected error occurred: {str(e)}"
                
                speak_text("An error occurred while processing your request.")
                return jsonify(message=error_message), 500    

        elif parsed_data['action'] == 'search':
            # Logic for searching an item by name
            item_name = parsed_data["name"]
            item = InventoryItem.query.filter(
                db.func.lower(InventoryItem.name) == item_name
            ).first()

            if item:
                speak_text(f"Item '{item.name}' found with quantity {item.quantity} {item.unit}.")
                return jsonify(item={"name": item.name, "quantity": item.quantity, "unit": item.unit}), 200
            else:
                speak_text(f"Item '{item_name}' not found.")
                return jsonify(message="Item not found"), 404

        else:
            speak_text("Unknown action.")
            return jsonify(message="Unknown action"), 400

    except ValueError as ve:
        
        speak_text(f"Error: {str(ve)}")
        return jsonify({"error": str(ve)}), 400
    except Exception as e:     
        return jsonify({"error": "An unexpected error occurred. Please try again later."}), 500


@inventory_bp.route("/process-command", methods=["POST"])
@jwt_required()
def process_command():
    from models import InventoryItem 
    data = request.json
    command = data.get("command")
    
    if not command:
        return jsonify(message="No command provided"), 400
    try:
        parsed_data = parse_command(command)
        parsed_data["name"] = parsed_data["name"].lower()
        if parsed_data['action'] == 'add':
            existing_item = InventoryItem.query.filter(
                db.func.lower(InventoryItem.name) == parsed_data["name"],
                InventoryItem.unit == parsed_data["unit"]
            ).first()

            if existing_item:
                
                existing_item.quantity += parsed_data["quantity"]
            else:
                new_item = InventoryItem(
                    name=parsed_data["name"],
                    quantity=parsed_data["quantity"],
                    unit=parsed_data["unit"]
                )
                db.session.add(new_item)
            db.session.commit()
    
            return jsonify(message="Item processed and added successfully"), 201
        
        elif parsed_data['action'] == 'update':
            try:   
                query = InventoryItem.query.filter(
                    db.func.lower(InventoryItem.name) == parsed_data["name"],
                )
                if "unit" in parsed_data:
                    query = query.filter(InventoryItem.unit == parsed_data["unit"])
                existing_item = query.first()

                if existing_item:
                    existing_item.quantity = parsed_data["quantity"]
                    db.session.commit()
                    speak_text(f"Item '{parsed_data['name']}' updated successfully.")
                    return jsonify(message="Item updated successfully"), 200
                else:
                    speak_text(f"Item '{parsed_data['name']}' not found.")
                    return jsonify(message="Item not found"), 404
            except Exception as e:
                error_message = f"An unexpected error occurred: {str(e)}"
                
                return jsonify(message=error_message), 500   

        elif parsed_data['action'] == 'remove':
            
            existing_item = InventoryItem.query.filter(
                db.func.lower(InventoryItem.name) == parsed_data["name"],
                InventoryItem.unit == parsed_data["unit"]
            ).first()

            if existing_item:
                existing_item.quantity -= parsed_data["quantity"]
                if existing_item.quantity <= 0:
                    db.session.delete(existing_item)
                    speak_text(f"Item '{parsed_data['name']}' removed from inventory.")
                else:
                    speak_text(f"Item '{parsed_data['name']}' updated with reduced quantity.")
                db.session.commit()
                return jsonify(message="Item removed successfully"), 200
            else:
                speak_text(f"Item '{parsed_data['name']}' not found.")
                return jsonify(message="Item not found"), 404
        
        elif parsed_data['action'] == 'show_stock':
            
            items = InventoryItem.query.all()
            if items:
                stock_list = [{"name": item.name, "quantity": item.quantity, "unit": item.unit} for item in items]
                speak_text("Current inventory stock shown.")
                return jsonify(stock_list=stock_list), 200
            else:
                speak_text("Inventory is empty.")
                return jsonify(message="No items in inventory"), 404
        
        elif parsed_data['action'] == 'search':
            
            item_name = parsed_data["name"]
            item = InventoryItem.query.filter(
                db.func.lower(InventoryItem.name) == item_name
            ).first()

            if item:
                speak_text(f"Item '{item.name}' found with quantity {item.quantity} {item.unit}.")
                return jsonify(item={"name": item.name, "quantity": item.quantity, "unit": item.unit}), 200
            else:
                speak_text(f"Item '{item_name}' not found.")
                return jsonify(message="Item not found"), 404

        else:
            speak_text("Unknown action.")
            return jsonify(message="Unknown action"), 400

    except ValueError as e:
        
        speak_text(f"Error: {str(e)}")
        return jsonify(message=str(e)), 400
    except Exception as e:
        
        speak_text("An unexpected error occurred.")
        return jsonify(message="An unexpected error occurred"), 500

    
@inventory_bp.route('/stop-listening', methods=['POST'])
@jwt_required()
def stop_listening():
    stop_recognition() 
    return jsonify({"message": "Stopped listening"}), 200        
    

@inventory_bp.route("/move", methods=["POST"])
@jwt_required()
def move_item():
    from models import InventoryItem, InventoryMovement
    data = request.json

    item_id = data.get("item_id")
    source_location = data.get("source_location")
    destination_location = data.get("destination_location")
    change = data.get("change")

    if not all([item_id, source_location, destination_location, change]):
        return jsonify({"message": "Missing required fields"}), 400
    item = InventoryItem.query.get(item_id)
    if not item:
        return jsonify({"message": "Item not found"}), 404
    if item.quantity + change < 0:
        return jsonify({"message": "Insufficient stock"}), 400

    movement = InventoryMovement(
        item_id=item_id,
        source_location=source_location,
        destination_location=destination_location,
        change=change
    )
    db.session.add(movement)

    item.quantity += change
    db.session.commit()
    
    socketio.emit("inventory_update", {
    "action": "move",
    "item": {  
        "id": item.id,
        "name": item.name,  
        "quantity": item.quantity,
        "unit": item.unit
    },
    "source_location": source_location,
    "destination_location": destination_location,
    "change": change,
    "new_quantity": item.quantity
})
    return jsonify({"message": "Stock moved successfully", "item_id": item.id, "new_quantity": item.quantity}), 200


@inventory_bp.route("/show-stock", methods=["GET"])
@jwt_required()
def show_stock():
    from models import InventoryItem
    items = InventoryItem.query.all()
    if items:
        
        stock_list = [
            {"id": item.id, "name": item.name, "quantity": item.quantity, "unit": item.unit}
            for item in items
        ]
        return jsonify(stock_list=stock_list), 200
        
    else:
        return jsonify(message="No items in inventory"), 404

@inventory_bp.route("/search", methods=["POST"])
@jwt_required()
def search_stock(query=None):
    from models import InventoryItem
    
    if query is None:  
        data = request.json
        query = data.get("query", "").strip().lower()  
    
    if not query:
        return jsonify(message="No search query provided"), 400
    results = InventoryItem.query.filter(
        (func.lower(InventoryItem.name).contains(query)) |  
        (func.cast(InventoryItem.id, db.String).like(f"%{query}%")) |  
        (func.cast(InventoryItem.quantity, db.String).like(f"%{query}%"))  
    ).all()

    if results:
        result_list = [
            {"id": item.id, "name": item.name, "quantity": item.quantity, "unit": item.unit}
            for item in results
        ]
        return jsonify(results=result_list), 200
    else:
        return jsonify(message="No matching items found"), 404

    
@inventory_bp.route("/process-voice-command", methods=["POST"])
@jwt_required()
def process_voice_command():
    try:
        command = recognize_speech_from_mic()
        if not command:
            return jsonify(message="Failed to recognize speech"), 400

        parsed_data = parse_command(command)
        action = parsed_data.get("action")
        query = parsed_data.get("query")
        
        if action == "show":
            return show_stock()
        elif action == "search" and query:    
            return search_stock(query=query)
        else:
            return jsonify(message=f"Unsupported action: {action}"), 400
    except ValueError as e:
        return jsonify(message=str(e)), 400
    
