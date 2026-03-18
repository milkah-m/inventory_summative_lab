# import requests
# import json

# class Search:
#     def get_by_search_term(self, search_term):
#         search_term_formatted = search_term.replace(" ", "+")
#         fields = ["title", "author_name"]
#         fields_formatted = ",".join(fields)
#         limit = 1

#         URL = f"https://openlibrary.org/search.json?title={search_term_formatted}&field={fields_formatted}&limit={limit}"
#         raw = requests.get(URL)
#         print(raw)
        

#         data = requests.get(URL).json()
#         response = f"Title: {data["docs"][0]["title"]} | Author: {data["docs"][0]["author_name"][0]} | Ebook Access: {data["docs"][0]["ebook_access"]} "
#         return response
    
# search_term = input("Please enter a book title: ")
# result = Search().get_by_search_term(search_term)
# print("Search Result: \n")
# print(result)

# Takes a search term (product name or barcode) as a parameter
# Makes a request to OpenFoodFacts using the requests library
# Returns the first matching product

import requests

def fetch_product(product_name):
    #url that includes the product name
    URL = f"https://world.openfoodfacts.org/cgi/search.pl?search_terms={product_name}&json=true"
    #get the data and convert it to json format
    data = requests.get(URL).json()
    #get the first product that matches
    if not data["products"]:
        return "This product does not exist, please check your spelling or try a different product."
    response = data["products"][0]
    #return this first product
    return response
