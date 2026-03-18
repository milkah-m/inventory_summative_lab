from flask import jsonify, request
from app import app
from app.data import inventory
from datetime import datetime, timedelta

# The decorator
# The function
# What to return 

@app.route("/")
def homepage():
    return ("Welcome to Milkah's inventory!")

@app.route("/inventory", methods=["GET"])
def inventory_list():
    return jsonify(inventory)


@app.route("/inventory/<int:id>", methods=["GET"])
def get_item(id):
    item = next((i for i in inventory if i["id"] == id), None) 
    return jsonify(item) if item else ("Item not found!", 404)

@app.route("/inventory", methods=["POST"])
def create_item():
    data = request.get_json()
    new_id = max((i["id"] for i in inventory), default=0) + 1
    new_item = {
     "id": new_id, 
     "product_name": data["product_name"],
     "ingredients": data["ingredients"],
     "price": data["price"],
     "category": data["category"],
     "quantity": data["quantity"],
     "brand": data["brand"],
     "expiry_date": data["expiry_date"]
     }
    inventory.append(new_item)
    return jsonify(new_item), 201

@app.route("/inventory/<int:id>", methods=["PATCH"])
def update_item(id):
    data = request.get_json()
    item = next((i for i in inventory if i["id"] == id), None)
    if not item:
        return "Item not found!", 404
    for key in data:
     item[key] = data[key]
    return jsonify(item)

@app.route("/inventory/<int:id>", methods=["DELETE"])
def delete_item(id):
    global inventory
    item = next((i for i in inventory if i["id"] == id), None)
    if not item:
        return "Item not found!", 404
    inventory = [i for i in inventory if i["id"] != id]
    return "Item deleted successfully", 200

@app.route("/inventory/category/<string:category>", methods=["GET"])
def categorize(category):
    item = [i for i in inventory if i["category"] == category]
    return jsonify(item) if item else ("Item not found!", 404)


@app.route("/inventory/low-stock", methods=["GET"])
def check_stock():
    low_stock = [i for i in inventory if i["quantity"] <= 5]
    return jsonify(low_stock) if low_stock else ("All items are well stocked!", 404)

@app.route("/inventory/expiring-soon", methods=["GET"])
def check_expiry():
    to_expire = [item for item in inventory if (datetime.strptime(item["expiry_date"], "%d.%m.%Y")) <= (datetime.now()+ timedelta(days=30))]
    return jsonify(to_expire) if to_expire else ("No items expiring soon", 404)