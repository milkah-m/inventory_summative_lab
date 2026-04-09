

import requests

def fetch_product(product_name):
    URL = f"https://world.openfoodfacts.org/cgi/search.pl?search_terms={product_name}&json=true"

# i used headers because i had received a 403 error and wanted to communicate to the server that i am a safe individual cause 403 means forbidden. forbidden fruit  
    headers = {
        "User-Agent": "InventoryApp/1.0 (learning project)",
        "Accept": "application/json"
    }
    
    response = requests.get(URL, headers=headers)

    print("Status:", response.status_code)
    print("Response preview:", response.text[:200])

    # 1. Check status
    if response.status_code != 200:
        return "API request failed"

    # 2. Check empty response
    if not response.text:
        return "Empty response from API"

    # 3. Safely parse JSON
    try:
        data = response.json()
    except ValueError:
        return "Invalid JSON response"

    # 4. Check products exist
    if not data.get("products"):
        return "This product does not exist, please check your spelling."

    # 5. Return first product safely
    return data["products"][0]

    

#how do i have fetch_product handling a server error cause it doesn't at the moment and so i am getting back an irrelevant error message
# value errors have nothing to do with the server, right? they are innate errors
#what exactly does a value error catch and in what cases would it be relevant and what are other types of errors used in conjunction with it? 
# how do i view the results of a url request in the cli?