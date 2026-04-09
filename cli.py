
import requests
from datetime import datetime
from app.external_api import fetch_product

# What needs improvements:

# Missing input validation
# In the CLI code, you assume that the API calls will always return a valid response. In reality, other HTTP methods might fail due to network issues or server errors. 
# Handling these errors would improve robustness.
# Reduce duplication in the CLI code
 

# What's missing:

# you have implemented a function to fetch from external API, but how do I interact with it from the CLI

#but i am already handling the errors with the exception at the bottom of this page, no?
# how do i handle api request failures in a try-except block?
# except apierror as status code?
# 



BASE_URL = "http://127.0.0.1:5000"

def validate_id(prompt):
    try:
        id = int(input(prompt))
        if id <= 0:
            raise ValueError
        return id
    except ValueError:
        print("ID must be a positive number!")
        return None
    
def validate_price(prompt):
    try:
        price = float(input(prompt))
        if price <= 0:
            raise ValueError
        return price
    except ValueError:
        print("Price must be a positive float!")
        return None
    
def validate_quantity(prompt):
    try:
        quantity = int(input(prompt))
        if quantity <= 0:
            raise ValueError
        return quantity
    except ValueError:
                print("Quantity must be a positive integer!")
                return None

def validate_expiry_date(prompt):
    expiry_date = input(prompt)
    try:
        datetime.strptime(expiry_date, "%d.%m.%Y")
        return expiry_date
    except ValueError:
        print("Invalid date format! Please use DD.MM.YYYY")
        return None


def safe_request(method, url, **kwargs):
    try:
        response = requests.request(method, url, timeout=10, **kwargs)
        response.raise_for_status() 

    except requests.exceptions.Timeout:
        return "Request timed out."

    except requests.exceptions.ConnectionError:
        return "Could not connect to server."

    except requests.exceptions.HTTPError as e:
        return f"HTTP error: {e.response.status_code}"

    except requests.exceptions.RequestException as e:
        return f"Request failed: {e}"

    # Try parsing JSON
    try:
        return response.json()
    except ValueError:
        return response.text
        
while (True):
    try:
        print("1. View all items")
        print("2. View specific item")
        print("3. View specific item on OpenFoodFacts")
        print("4. Add item manually")
        print("5. Add item from OpenFoodFacts")
        print("6. Update item")
        print("7. Delete item")
        print("8. Exit")

        choice = input("Please input the option you would like to proceed with: ")


#the reason i have removed the json is because i am now handling it inside safe_request
        if choice == "1":
            response = safe_request("GET", f"{BASE_URL}/inventory")
            print(response)
            
        elif choice == "2":
            id = validate_id("Please input the id of the item you want to view")
            if id is None:
               continue
            response = safe_request("GET", f"{BASE_URL}/inventory/{int(id)}")
            print(response)

# you have implemented a function to fetch from external API, but how do I interact with it from the CLI
        elif choice == "3":
           search_term = input("Please input the product you want to view ")
           response = fetch_product(search_term)
           print(response)
            #why do we need to use requests.get? why can't we just 
            #okay but since fetch product already incorporates requests why can't we just call the function and then print the
            #response. why do we still need to incoporate requests on the elif?
            
        elif choice == "4":
            product_name = input("Please input the name of the item ")
            ingredients = input("Please input the ingredients of the item" )
            price = validate_price("Please input the price of the item ")
            if price is None:
                continue
            category = input("Please input the category of the item ")
            quantity = validate_quantity("Please input the quantity of the item ")
            if quantity is None:
                continue
            brand = input("Please input the brand of the item ")
            expiry_date = validate_expiry_date("Please input the expiry date of the item ")
            if expiry_date is None:
                continue
            response = safe_request("POST", f"{BASE_URL}/inventory", json={
        "product_name": product_name,
        "ingredients": ingredients,
        "price": price,
        "category": category,
        "quantity": quantity,
        "brand": brand,
        "expiry_date": expiry_date
        })
            print(response)

        #do i need validation for name, ingredients, category, and brand? why or why not? well, i think i don't need validation for these because i am the one deciding what 
        # they get to be... so for the ones that i am specifically checking, they are not strings and for expiry date it is the formatting. this is why these specific fields need 
        # validation...
        elif choice == "5":
            product_name = input("Please input the name of the item ")
            price = validate_price("Please input the price of the item ")
            if price is None:
                continue
            quantity = validate_quantity("Please input the quantity of the item ")
            if quantity is None:
                continue
            expiry_date = validate_expiry_date("Please input the expiry date of the item ")
            if expiry_date is None:
                continue
            response = safe_request("POST", f"{BASE_URL}/inventory", json={
        "product_name": product_name,
        "price": price,
        "quantity": quantity,
        "expiry_date": expiry_date
        })
            print(response)

        elif choice == "6":
            id = validate_id("Please input the id of the item you want to update ")
            if id is None:
               continue
            field = input("Which field do you want to update? ")
            value = input("Enter new value: ")
            response = safe_request("PATCH", f"{BASE_URL}/inventory/{int(id)}", json={
        field: value
        })
            print(response)


        elif choice == "7":
            id = validate_id("Please input the id of the item you want to delete ")
            if id is None:
               continue
            response = safe_request("DELETE", f"{BASE_URL}/inventory/{int(id)}")
            print(response)

        elif choice == "8":
            break
    
    except Exception as e:
        print(f"Something went wrong: {e}")

#why am i getting the value error, not the exception? what value does fetch product except?