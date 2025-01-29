from flask import Flask, jsonify, request
import pydapper
from database import get_db_connection
from models import User

app = Flask(__name__)

# Home route
@app.route('/')
def home():
    return jsonify({"message": "Welcome to the PyDapper Web API!"})

# Get all users
@app.route('/users', methods=['GET'])
def get_users():
    with pydapper.using(get_db_connection()) as commands:
        users = commands.query("SELECT * FROM users", model=User)
    return jsonify([user.__dict__ for user in users])

# Get user by ID
@app.route('/users/<int:id>', methods=['GET'])
def get_user_by_id(id):
    #print(id)
    sentinel = object()
    with pydapper.using(get_db_connection()) as commands:    
        user = commands.query_first("SELECT * FROM users WHERE id =?id?",param={"id": id}, model=User)
        
        #print(user)
    if user:
        return jsonify(user.__dict__)
    return jsonify({"error": "User not found"}), 404

# Add a new user
@app.route('/users', methods=['POST'])
def add_user():
    data = request.get_json()
    name = data.get('name')
    age = data.get('age')

    if not name or not age:
        return jsonify({"error": "Name and age are required"}), 400

    with pydapper.using(get_db_connection()) as commands:
        commands.execute("INSERT INTO users (name, age) VALUES (?name?, ?age?)", param={"name": name,"age":age})
        #commands.execute("INSERT INTO users (name, age) VALUES(?, ?)", (name, age))
        #commands.execute("INSERT INTO users (name, age) VALUES (?, ?)", (name, age))
        
    return jsonify({"message": "User added successfully!"}), 201

# Delete a user by ID
@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    with pydapper.using(get_db_connection()) as commands:
        commands.execute("DELETE FROM users WHERE id = ?", (user_id,))
    return jsonify({"message": "User deleted successfully!"})



if __name__ == '__main__':
    app.run(debug=True)
