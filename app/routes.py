from flask import jsonify, request
from app import app
from app.data import inventory

# The decorator
# The function
# What to return 

@app.route("/")
def homepage():
    return ("Welcome to Milkah's inventory!")

@app.route("/inventory", methods=["GET"])
def inventory_list():
    return jsonify(inventory)

# How do you find one specific item from a list of dictionaries?
# What happens if the ID doesn't exist? 🤔

# @app.route("/events/<int:id>", methods=["GET"])
# def specific_event(id):
#     event = next(e.to_dict() for e in events if e.id == id)
#     if not event:
#         return "Event not found, please try a different id.", 404
#     return jsonify(event), 200 
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


