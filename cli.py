
import requests
        
try:
    while (True):
        print("1. View all items")
        print("2. View specific item")
        print("3. Add item manually")
        print("4. Add item from OpenFoodFacts")
        print("5. Update item")
        print("6. Delete item")
        print("7. Exit")

        choice = input("Please input the option you would like to proceed with ")


        if choice == "1":
            response = requests.get("http://127.0.0.1:5000/inventory").json()
            print(response)
            
        elif choice == "2":
            id = input("Please input the id of the item you want to view ")
            response = requests.get(f"http://127.0.0.1:5000/inventory/{int(id)}").json()
            print(response)
            
        elif choice == "3":
            product_name = input("Please input the name of the item ")
            ingredients = input("Please input the ingredients of the item" )
            price = input("Please input the price of the item ")
            category = input("Please input the category of the item ")
            quantity = input("Please input the quantity of the item ")
            brand = input("Please input the brand of the item ")
            expiry_date = input("Please input the expiry date of the item ")
            response = requests.post("http://127.0.0.1:5000/inventory", json={
        "product_name": product_name,
        "ingredients": ingredients,
        "price": price,
        "category": category,
        "quantity": quantity,
        "brand": brand,
        "expiry_date": expiry_date
        }).json()
            print(response)

        elif choice == "4":
            product_name = input("Please input the name of the item ")
            price = input("Please input the price of the item ")
            quantity = input("Please input the quantity of the item ")
            expiry_date = input("Please input the expiry date of the item ")
            response = requests.post("http://127.0.0.1:5000/inventory/fetch", json={
        "product_name": product_name,
        "price": price,
        "quantity": quantity,
        "expiry_date": expiry_date
        }).json()
            print(response)

        elif choice == "5":
            id = input("Please input the id of the item you want to update ")
            field = input("Which field do you want to update? ")
            value = input("Enter new value: ")
            response = requests.patch(f"http://127.0.0.1:5000/inventory/{int(id)}", json={field: value}).json()
            print(response)

        elif choice == "6":
            id = input("Please input the id of the item you want to delete ")
            response = requests.delete(f"http://127.0.0.1:5000/inventory/{int(id)}").text
            print(response)

        elif choice == "7":
            break
except ValueError:
    print("Invalid input, please enter a valid number!")
except Exception as e:
    print(f"Something went wrong: {e}")