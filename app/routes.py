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

# @app.route("/events", methods=["POST"])
# def create_event():
#     data = request.get_json()
#     highest_id = max((e.id for e in events), default=0) + 1
#     new_event = Event(id=highest_id, title=data["title"])
#     events.append(new_event)
#     return jsonify(new_event.to_dict()), 201

# How do you get the data the user is sending?
# How do you generate a new unique ID?
# How do you add the new item to your inventory list? 
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


