from flask import jsonify, request
from app import app
from app.data import inventory
from datetime import datetime, timedelta
from app.external_api import fetch_product
from validators import validate_expiry_date, validate_id, validate_price, validate_quantity

# The decorator
# The function
# What to return

def get_item_by_id(item_id):
    return next((item for item in inventory if item["id"] == item_id), None) 

@app.route("/")
def homepage():
    return ("Welcome to Milkah's inventory!")

@app.route("/inventory", methods=["GET"])
def inventory_list():
    return jsonify(inventory)


@app.route("/inventory/<int:id>", methods=["GET"])
def get_item(id):
    item = get_item_by_id(id)
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

@app.route("/inventory/fetch", methods=["POST"])
def fetch_item():
    data = request.get_json()
    item_name = data["product_name"]
    item = fetch_product(item_name)
    if isinstance(item, str):
        return item, 404
    new_id = max((i["id"] for i in inventory), default=0) + 1
    new_item = {
     "id": new_id, 
     "product_name": item.get("product_name", "N/A"),
     "ingredients": item.get("ingredients_text", "N/A"),
     "price": data["price"],
     "category": item.get("categories", "N/A"),
     "quantity": data["quantity"],
     "brand": item.get("brands", "N/A"),
     "expiry_date": data["expiry_date"]
     }

    inventory.append(new_item)
    return jsonify(new_item), 201


@app.route("/inventory/<int:item_id>", methods=["PATCH"])
def update_item(item_id):

    item = get_item_by_id(item_id)

    if not item:
        return jsonify({"error": "Item not found"}), 404

    data = request.get_json()

    if not data:
        return jsonify({"error": "No data provided"}), 400

    allowed_fields = [
        "product_name",
        "ingredients",
        "brand",
        "category",
        "price",
        "quantity",
        "expiry_date"
    ]

    validators = {
        "price": validate_price,
        "quantity": validate_quantity,
        "expiry_date": validate_expiry_date
    }

    for field, value in data.items():

        if field not in allowed_fields:
            return jsonify({"error": f"Invalid field: {field}"}), 400

        if field in validators:
            value = validators[field](value)
        if value is None:
            return jsonify({"error": f"Invalid value for {field}"}), 400

    item[field] = value

    return jsonify({
        "message": "Item updated successfully",
        "item": item
    }), 200


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
    return jsonify(low_stock) if low_stock else jsonify([]), 200

@app.route("/inventory/expiring-soon", methods=["GET"])
def check_expiry():
    to_expire = [item for item in inventory if (datetime.strptime(item["expiry_date"], "%d.%m.%Y")) <= (datetime.now()+ timedelta(days=30))]
    return jsonify(to_expire) if to_expire else jsonify([]), 200

#what eaxctly are these two doing and which one is right?
#why am i getting a value error for this? like why is it jumpint to value error?
#and what is the correct way to write the relevant post request?