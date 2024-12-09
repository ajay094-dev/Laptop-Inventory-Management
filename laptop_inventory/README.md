
## Laptop Inventory Management System

A backend application for managing laptop inventory built with Flask, integrated with MySQL and MongoDB, and featuring role-based access control for users and admins.

**Features**

	•	Authentication: User registration and login with password hashing.
	•	Role-Based Access Control:
	•	Users can only view inventory items.
	•	Admins can perform all CRUD operations (Create, Read, Update, Delete) on inventory items.
	•	Inventory Management:
	•	MySQL: Structured relational database for user and inventory data.
	•	MongoDB: NoSQL database for flexible inventory data storage.
	•	Validation: Ensures valid data input for all operations.
	•	Session Management: Secures user sessions with cookies and Flask sessions.
	•	API Endpoints: RESTful APIs for seamless interaction.

**Technologies Used**

	•	Backend Framework: Flask
	•	Database: MySQL and MongoDB
	•	Authentication: Flask-Session and Flask-Bcrypt
	•	Validation: Python Regex
	•	Environment Configuration: Python Dotenv
	•	Testing: Postman

**Installation**

Prerequisites

	•	Python 3.7 or later
	•	MySQL
	•	MongoDB
	•	Virtual Environment (optional but recommended)

Steps

	1.	Clone the Repository:

git clone <https://github.com/ajay094-dev/Laptop-Inventory-Management.git>
cd laptop_inventory


	2.	Create a Virtual Environment:

python3 -m venv venv
source venv/bin/activate


	3.	Install Dependencies:

pip install -r requirements.txt


	4.	Set Up Databases:
	•	MySQL:

CREATE DATABASE laptop_inventory;
USE laptop_inventory;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    role ENUM('admin', 'user') DEFAULT 'user',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE inventory (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    item_name VARCHAR(100) NOT NULL,
    description TEXT,
    quantity INT NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);


	•	MongoDB:

use laptop_inventory;

db.users.createIndex({ username: 1 }, { unique: true });
db.inventory.createIndex({ user_id: 1 });


	5.	Set Up Environment Variables:
Create a .env file in the project root:

SECRET_KEY=your_secret_key
MYSQL_HOST=localhost
MYSQL_USER=root
MYSQL_PASSWORD=your_password
MYSQL_DB=laptop_inventory
MONGO_URI=mongodb://localhost:27017


	6.	Run the Application:

python3 run.py


	7.	Access the Application:
	•	Server URL: http://127.0.0.1:5000

API Endpoints

Authentication

	•	Register User: POST /auth/register
	•	Login User: POST /auth/login
	•	Logout User: POST /auth/logout

**Inventory Management**

MySQL

	•	View All Items (Users and Admins): GET /mysql/items
	•	Create Item (Admins only): POST /mysql/items
	•	Update Item (Admins only): PUT /mysql/items/<item_id>
	•	Delete Item (Admins only): DELETE /mysql/items/<item_id>

MongoDB

	•	View All Items (Users and Admins): GET /mongo/items
	•	Create Item (Admins only): POST /mongo/items
	•	Update Item (Admins only): PUT /mongo/items/<item_id>
	•	Delete Item (Admins only): DELETE /mongo/items/<item_id>

Testing

Using Postman

	1.	Import the API endpoints into Postman.
	2.	Test all endpoints for both users and admins.
	3.	Example test cases:
	•	User registration with missing fields.
	•	Login with incorrect credentials.
	•	Attempting unauthorized CRUD operations as a regular user.

Project Structure

laptop_inventory/
├── app/
│   ├── __init__.py        # Initialize Flask app and database connections
│   ├── auth.py            # Authentication routes and logic
│   ├── inventory_mysql.py # CRUD operations for MySQL
│   ├── inventory_mongo.py # CRUD operations for MongoDB
│   ├── admin.py           # Admin-specific routes
│   ├── user.py            # User-specific routes
│   ├── models.py          # Common database utilities
├── config.py              # Configuration for Flask and databases
├── run.py                 # Entry point for the application
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables
├── README.md              # Project documentation

Contributing

	1.	Fork the repository.
	2.	Create a new branch:

git checkout -b feature-branch-name


	3.	Commit your changes:

git commit -m "Description of changes"


	4.	Push to your branch:

git push origin feature-branch-name


	5.	Open a pull request.

