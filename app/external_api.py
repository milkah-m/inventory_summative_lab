import requests

def fetch_product(product_name):
    URL = "https://world.openfoodfacts.org/cgi/search.pl"

    headers = {
        "User-Agent": "InventoryApp/1.0 (learning project)",
        "Accept": "application/json"
    }

    params = {
        "search_terms": product_name,
        "json": 1,
        "page_size": 1
    }

    try:
        response = requests.get(URL, headers=headers, params=params, timeout=10)

        response.raise_for_status()

        return response.json()

    except requests.exceptions.HTTPError:
        print("Server returned an error response")
    except requests.exceptions.ConnectionError:
        print("Network error - check internet connection")
    except requests.exceptions.Timeout:
        print("Request timed out")
    except ValueError:
        print("Invalid JSON response")

    return {}

#how do i have fetch_product handling a server error cause it doesn't at the moment and so i am getting back an irrelevant error message
# value errors have nothing to do with the server, right? they are innate errors
#what exactly does a value error catch and in what cases would it be relevant and what are other types of errors used in conjunction with it? 
# how do i view the results of a url request in the cli?