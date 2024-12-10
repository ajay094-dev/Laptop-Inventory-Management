from flask import Blueprint, request, session, jsonify
from bson import ObjectId
from app import mongo_client

inventory_mongo_bp = Blueprint('inventory_mongo', __name__)

def validate_item_data(data):
    """Validate item data for CRUD operations."""
    errors = []
    if not data.get('item_name'):
        errors.append("Item name is required.")
    if not isinstance(data.get('quantity'), int) or data.get('quantity') <= 0:
        errors.append("Quantity must be a positive integer.")
    if not isinstance(data.get('price'), (int, float)) or data.get('price') <= 0:
        errors.append("Price must be a positive number.")
    return errors


def admin_required(func):
    """Decorator to ensure only admins can access a route."""
    def wrapper(*args, **kwargs):
        if session.get('role') != 'admin':
            return jsonify({"error": "Unauthorized access. Admins only."}), 403
        return func(*args, **kwargs)
    wrapper.__name__ = func.__name__
    return wrapper

# CREATE Inventory Item
@inventory_mongo_bp.route('/items', methods=['POST'])
@admin_required
def create_item():
    if 'user_id' not in session:
        return jsonify({"error": "Unauthorized access"}), 403

    data = request.get_json()
    validation_errors = validate_item_data(data)
    if validation_errors:
        return jsonify({"errors": validation_errors}), 400

    item_name = data['item_name']
    description = data.get('description', '')
    quantity = data['quantity']
    price = data['price']

    inventory = mongo_client.laptop_inventory.inventory
    result = inventory.insert_one({
        "user_id": session['user_id'],
        "item_name": item_name,
        "description": description,
        "quantity": quantity,
        "price": price
    })

    return jsonify({"message": "Item created successfully in MongoDB", "id": str(result.inserted_id)}), 201


# READ All Inventory Items
@inventory_mongo_bp.route('/items', methods=['GET'])
def read_items():
    if 'user_id' not in session:
        return jsonify({"error": "Unauthorized access"}), 403

    inventory = mongo_client.laptop_inventory.inventory

    if session['role'] == 'admin':
        # Admins can only view items they created
        items = list(inventory.find({"user_id": session['user_id']}, {"_id": 1, "item_name": 1, "description": 1, "quantity": 1, "price": 1}))
    elif session['role'] == 'user':
        # Users can view all items
        items = list(inventory.find({}, {"_id": 1, "item_name": 1, "description": 1, "quantity": 1, "price": 1}))
    else:
        return jsonify({"error": "Unauthorized role"}), 403

    # Convert ObjectId to string for JSON serialization
    for item in items:
        item['_id'] = str(item['_id'])

    return jsonify({"items": items}), 200



# READ Single Inventory Item by ID
@inventory_mongo_bp.route('/items/<string:item_id>', methods=['GET'])
def read_item(item_id):
    if 'user_id' not in session:
        return jsonify({"error": "Unauthorized access"}), 403

    inventory = mongo_client.laptop_inventory.inventory

    if session['role'] == 'admin':
        # Admins can only view items they created
        item = inventory.find_one({"_id": ObjectId(item_id), "user_id": session['user_id']})
    elif session['role'] == 'user':
        # Users can view any item
        item = inventory.find_one({"_id": ObjectId(item_id)})
    else:
        return jsonify({"error": "Unauthorized role"}), 403

    if not item:
        return jsonify({"error": "Item not found"}), 404

    # Convert ObjectId to string for JSON serialization
    item['_id'] = str(item['_id'])

    return jsonify(item), 200


# UPDATE Inventory Item
@inventory_mongo_bp.route('/items/<string:item_id>', methods=['PUT'])
@admin_required
def update_item(item_id):
    if 'user_id' not in session:
        return jsonify({"error": "Unauthorized access"}), 403

    data = request.get_json()
    validation_errors = validate_item_data(data)
    if validation_errors:
        return jsonify({"errors": validation_errors}), 400

    item_name = data['item_name']
    description = data.get('description', '')
    quantity = data['quantity']
    price = data['price']

    inventory = mongo_client.laptop_inventory.inventory
    result = inventory.update_one(
        {"_id": ObjectId(item_id), "user_id": session['user_id']},
        {"$set": {"item_name": item_name, "description": description, "quantity": quantity, "price": price}}
    )

    if result.matched_count == 0:
        return jsonify({"error": "Item not found or unauthorized"}), 404

    return jsonify({"message": "Item updated successfully in MongoDB"}), 200


# DELETE Inventory Item
@inventory_mongo_bp.route('/items/<string:item_id>', methods=['DELETE'])
@admin_required
def delete_item(item_id):
    if 'user_id' not in session:
        return jsonify({"error": "Unauthorized access"}), 403

    inventory = mongo_client.laptop_inventory.inventory
    result = inventory.delete_one({"_id": ObjectId(item_id), "user_id": session['user_id']})

    if result.deleted_count == 0:
        return jsonify({"error": "Item not found or unauthorized"}), 404

    return jsonify({"message": "Item deleted successfully from MongoDB"}), 200