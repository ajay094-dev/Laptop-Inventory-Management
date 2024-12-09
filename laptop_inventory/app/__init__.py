from flask import Flask
from flask_mysqldb import MySQL
from pymongo import MongoClient
from flask_bcrypt import Bcrypt

mysql = MySQL()
mongo_client = None
bcrypt = Bcrypt()

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    # Initialize MySQL
    mysql.init_app(app)

    # Initialize MongoDB
    global mongo_client
    mongo_client = MongoClient(app.config['MONGO_URI'])

    # Initialize bcrypt
    bcrypt.init_app(app)

    # Register blueprints
    from .auth import auth_bp
    from .inventory_mysql import inventory_mysql_bp
    from .inventory_mongo import inventory_mongo_bp
    from .admin import admin_bp
    from .user import user_bp

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(inventory_mysql_bp, url_prefix='/mysql')
    app.register_blueprint(inventory_mongo_bp, url_prefix='/mongo')
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(user_bp, url_prefix='/user')

    return app