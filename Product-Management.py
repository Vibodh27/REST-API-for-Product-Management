from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)
DB_NAME = "products.db"

# ---------- Database Setup ----------
def init_db():
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute('''CREATE TABLE IF NOT EXISTS products (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            name TEXT NOT NULL,
                            price REAL NOT NULL,
                            quantity INTEGER NOT NULL
                        );''')

# ---------- Routes ----------
@app.route('/products', methods=['GET'])
def get_products():
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.execute("SELECT * FROM products")
        products = [
            {"id": row[0], "name": row[1], "price": row[2], "quantity": row[3]}
            for row in cursor.fetchall()
        ]
    return jsonify(products)

@app.route('/products', methods=['POST'])
def add_product():
    data = request.get_json()
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute("INSERT INTO products (name, price, quantity) VALUES (?, ?, ?)",
                     (data['name'], data['price'], data['quantity']))
    return jsonify({"message": "Product added successfully!"}), 201

@app.route('/products/<int:id>', methods=['PUT'])
def update_product(id):
    data = request.get_json()
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute("UPDATE products SET name=?, price=?, quantity=? WHERE id=?",
                     (data['name'], data['price'], data['quantity'], id))
    return jsonify({"message": "Product updated successfully!"})

@app.route('/products/<int:id>', methods=['DELETE'])
def delete_product(id):
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute("DELETE FROM products WHERE id=?", (id,))
    return jsonify({"message": "Product deleted successfully!"})

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
