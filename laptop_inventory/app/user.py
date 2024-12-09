from flask import Blueprint, session, jsonify
from app import mysql

user_bp = Blueprint('user', __name__)

@user_bp.route('/inventory', methods=['GET'])
def get_inventory():
    if session.get('role') != 'user':
        return jsonify({"error": "Users only"}), 403

    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM inventory WHERE user_id = %s", (session['user_id'],))
    inventory = cursor.fetchall()

    return jsonify({"inventory": inventory}), 200