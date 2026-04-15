import requests
from app.external_api import fetch_product
from validators import validate_expiry_date, validate_id, validate_price, validate_quantity

BASE_URL = "http://127.0.0.1:5000"


# wrapping requests safely 
def safe_request(method, url, **kwargs):
    try:
        response = requests.request(method, url, timeout=10, **kwargs)
        response.raise_for_status()

    except requests.exceptions.Timeout:
        return {"error": "Request timed out"}

    except requests.exceptions.ConnectionError:
        return {"error": "Could not connect to server"}

    except requests.exceptions.HTTPError as e:
        return {"error": f"HTTP error {e.response.status_code}"}

    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

    try:
        return response.json()
    except ValueError:
        return response.text



# mapping function that returns in json friendly format
def map_off_product(product, price, quantity, expiry_date):
    return {
        "product_name": product.get("product_name") or product.get("product_name_en", ""),
        "ingredients": product.get("ingredients_text", ""),
        "brand": product.get("brands", ""),
        "category": product.get("categories", ""),
        "price": price,
        "quantity": quantity,
        "expiry_date": expiry_date
    }



# main loop
while True:
    try:
        print("\n==== INVENTORY MENU ====")
        print("1. View all items")
        print("2. View specific item")
        print("3. Search + Add from OpenFoodFacts")
        print("4. Add item manually")
        print("5. Update item")
        print("6. Delete item")
        print("7. Exit")

        choice = input("Please input the option you would like to proceed with: ")

        
        # view all items
        if choice == "1":
            response = safe_request("GET", f"{BASE_URL}/inventory")
            print(response)

        
        # view single item
        elif choice == "2":
            item_id = validate_id("Please input the id of the item you want to view: ")
            if item_id is None:
                continue

            response = safe_request("GET", f"{BASE_URL}/inventory/{item_id}")
            print(response)

        
        # search & add
        elif choice == "3":
            search_term = input("Please input the product you want to search: ")
            
            results = fetch_product(search_term)

            if not results:
                    print("OpenFoodFacts is currently unavailable. Please try again later.")
                    continue
                
            products = results.get("products", [])

            if not products:
                    print("No matching products found")
                    continue

            product = products[0]

            print("\n--- PRODUCT FOUND ---")
            print("Name:", product.get("product_name"))
            print("Brand:", product.get("brands"))
            print("Ingredients:", product.get("ingredients_text"))

            confirm = input("\nWould you like to add this product? (yes/no): ")

            if confirm.lower() != "yes":
                    continue

            price = validate_price("Please input the price: ")
            if price is None:
                    continue

            quantity = validate_quantity("Please input the quantity: ")
            if quantity is None:
                    continue

            expiry_date = validate_expiry_date("Please input expiry date (DD.MM.YYYY): ")
            if expiry_date is None:
                    continue

            data = map_off_product(product, price, quantity, expiry_date)

            response = safe_request(
                    "POST",
                    f"{BASE_URL}/inventory",
                    json=data
                )

            if isinstance(response, dict) and "error" in response:
                print(f" Failed: {response['error']}")
            else:
                 print(response)
                 print("Product added successfully")

        
        # manual addition
        elif choice == "4":
            product_name = input("Product name: ")
            ingredients = input("Ingredients: ")
            brand = input("Brand: ")
            category = input("Category: ")

            price = validate_price("Price: ")
            if price is None:
                continue

            quantity = validate_quantity("Quantity: ")
            if quantity is None:
                continue

            expiry_date = validate_expiry_date("Expiry date (DD.MM.YYYY): ")
            if expiry_date is None:
                continue

            data = {
                "product_name": product_name,
                "ingredients": ingredients,
                "brand": brand,
                "category": category,
                "price": price,
                "quantity": quantity,
                "expiry_date": expiry_date
            }

            response = safe_request("POST", f"{BASE_URL}/inventory", json=data)
            
            if isinstance(response, dict) and "error" in response:
                print(f" Failed: {response['error']}")
            else:
                 print(response)
                 print("Product added successfully")


        
        # update
        elif choice == "5":
            item_id = validate_id("Enter item ID to update: ")
            if item_id is None:
                continue

                #added validation to this option
            allowed_fields = [
                "product_name",
                "ingredients",
                "brand",
                "category",
                "price",
                "quantity",
                "expiry_date"
            ]

            print("\nAllowed fields:")
            print(", ".join(allowed_fields))

            field = input("Which field do you want to update? ").strip()

            if field not in allowed_fields:
                print("Invalid field selected!")
                continue


            # placing validatable fields in a dictionary
            field_validators = {
                "price": validate_price,
                "quantity": validate_quantity,
                "expiry_date": validate_expiry_date
            }


            # handling all values using a conditional statement
            if field in field_validators:
                value = field_validators[field](f"Enter new {field}: ")
                if value is None:
                    continue
            else:
                value = input(f"Enter new {field}: ")


            # send patch request
            response = safe_request(
                "PATCH",
                f"{BASE_URL}/inventory/{item_id}",
                json={field: value}
            )

            print(response)
            

        
        # delete
        elif choice == "6":
            item_id = validate_id("Enter item ID to delete: ")
            if item_id is None:
                continue

            confirm = input("Are you sure? (yes/no): ")
            if confirm.lower() != "yes":
                continue

            response = safe_request(
                "DELETE",
                f"{BASE_URL}/inventory/{item_id}"
            )

            print(response)

        # exit
        elif choice == "7":
            break

        else:
            print("Invalid option selected.")

    

    except KeyboardInterrupt:
        print("\nExiting...")
        break

    except Exception as e:
        print(f"Unexpected error: {e}")