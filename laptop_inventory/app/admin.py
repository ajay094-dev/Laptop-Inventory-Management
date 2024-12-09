from flask import Blueprint, session, jsonify, request
from app import mysql

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/users', methods=['GET'])
def list_users():
    if session.get('role') != 'admin':
        return jsonify({"error": "Admins only"}), 403

    cursor = mysql.connection.cursor()
    cursor.execute("SELECT id, username, email, role FROM users")
    users = cursor.fetchall()

    return jsonify({"users": users}), 200