import os
from flask import Flask, jsonify, send_from_directory # Updated import
from crud import get_db_connection, TABLE_NAME # Import necessary functions/variables from crud.py

# Tell Flask where to find the static files (optional, but good for clarity)
# The static_folder defaults to 'static'
app = Flask(__name__, static_folder='static') 

# Serve the index.html from the root path
@app.route('/')
def index():
    # Use send_from_directory to explicitly serve a file from the static folder
    # This correctly points to your 'static/index.html'
    return send_from_directory(app.static_folder, 'index.html')


# Simple API endpoint for the frontend to call
@app.route('/api/items', methods=['GET'])
def get_items():
    connection = get_db_connection()
    if not connection:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        with connection.cursor() as cursor:
            sql = f"SELECT * FROM {TABLE_NAME}"
            cursor.execute(sql)
            items = cursor.fetchall()
            return jsonify(items)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        connection.close()

# C - CREATE a New Item
@app.route('/api/items', methods=['POST'])
def create_item():
    data = request.json
    name = data.get('name')
    description = data.get('description', '')
    quantity = data.get('quantity', 0)

    if not name:
        return jsonify({"error": "Name is required"}), 400

    connection = get_db_connection()
    if not connection:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        with connection.cursor() as cursor:
            sql = f"INSERT INTO {TABLE_NAME} (name, description, quantity) VALUES (%s, %s, %s)"
            cursor.execute(sql, (name, description, quantity))
            connection.commit()
            return jsonify({"message": "Item created successfully", "id": cursor.lastrowid}), 201
    except Exception as e:
        connection.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        connection.close()

# D - DELETE an Item (requires U - Update to complete the set, but D is a good test)
@app.route('/api/items/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    connection = get_db_connection()
    if not connection:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        with connection.cursor() as cursor:
            sql = f"DELETE FROM {TABLE_NAME} WHERE id = %s"
            result = cursor.execute(sql, (item_id,))
            connection.commit()
            
            if result == 0:
                 return jsonify({"message": f"Item with ID {item_id} not found"}), 404
                 
            return jsonify({"message": f"Item with ID {item_id} deleted successfully"}), 200
    except Exception as e:
        connection.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        connection.close()

if __name__ == '__main__':
    # Flask runs on port 5000 by default. 
    app.run(host='0.0.0.0', port=5000, debug=True)
