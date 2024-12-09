from flask import Blueprint, request, session, jsonify
from app import mysql

inventory_mysql_bp = Blueprint('inventory_mysql', __name__)

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
@inventory_mysql_bp.route('/items', methods=['POST'])
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

    cursor = mysql.connection.cursor()
    try:
        cursor.execute(
            "INSERT INTO inventory (user_id, item_name, description, quantity, price) VALUES (%s, %s, %s, %s, %s)",
            (session['user_id'], item_name, description, quantity, price)
        )
        mysql.connection.commit()
        return jsonify({"message": "Item created successfully in MySQL"}), 201
    finally:
        cursor.close()


# READ All Inventory Items
@inventory_mysql_bp.route('/items', methods=['GET'])
def read_items():
    if 'user_id' not in session:
        return jsonify({"error": "Unauthorized access"}), 403

    cursor = mysql.connection.cursor()
    try:
        cursor.execute("SELECT * FROM inventory WHERE user_id = %s", (session['user_id'],))
        items = cursor.fetchall()
        return jsonify({"items": items}), 200
    finally:
        cursor.close()


# READ Single Inventory Item by ID
@inventory_mysql_bp.route('/items/<int:item_id>', methods=['GET'])
def read_item(item_id):
    if 'user_id' not in session:
        return jsonify({"error": "Unauthorized access"}), 403

    cursor = mysql.connection.cursor()
    try:
        cursor.execute("SELECT * FROM inventory WHERE id = %s AND user_id = %s", (item_id, session['user_id']))
        item = cursor.fetchone()
        if not item:
            return jsonify({"error": "Item not found"}), 404
        return jsonify(item), 200
    finally:
        cursor.close()


# UPDATE Inventory Item
@inventory_mysql_bp.route('/items/<int:item_id>', methods=['PUT'])
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

    cursor = mysql.connection.cursor()
    try:
        cursor.execute(
            "UPDATE inventory SET item_name = %s, description = %s, quantity = %s, price = %s WHERE id = %s AND user_id = %s",
            (item_name, description, quantity, price, item_id, session['user_id'])
        )
        mysql.connection.commit()
        if cursor.rowcount == 0:
            return jsonify({"error": "Item not found or unauthorized"}), 404
        return jsonify({"message": "Item updated successfully in MySQL"}), 200
    finally:
        cursor.close()


# DELETE Inventory Item
@inventory_mysql_bp.route('/items/<int:item_id>', methods=['DELETE'])
@admin_required
def delete_item(item_id):
    if 'user_id' not in session:
        return jsonify({"error": "Unauthorized access"}), 403

    cursor = mysql.connection.cursor()
    try:
        cursor.execute("DELETE FROM inventory WHERE id = %s AND user_id = %s", (item_id, session['user_id']))
        mysql.connection.commit()
        if cursor.rowcount == 0:
            return jsonify({"error": "Item not found or unauthorized"}), 404
        return jsonify({"message": "Item deleted successfully from MySQL"}), 200
    finally:
        cursor.close()