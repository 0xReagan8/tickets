import sys
import os
import requests
import json
from colorama import Fore, Style
from dotenv import load_dotenv

os.chdir(os.path.join(str(os.getcwd())))

# Load environment variables
load_dotenv(".env")

api_key = os.getenv("SENDOWL_KEY")
api_secret = os.getenv("SENDOWL_SECRET")


class SendOwlProduct:
    """
    A class to interact with the SendOwl Products API.
    
    Attributes:
        base_url (str): The base URL for the SendOwl Products API.
        auth (tuple): A tuple containing the API key and API secret for authentication.
    """
    
    def __init__(self):
        """
        Initializes the SendOwlProduct with necessary authentication details.
        
        Parameters:
            api_key (str): Your SendOwl API key.
            api_secret (str): Your SendOwl API secret.
        """
        self.base_url = "https://www.sendowl.com/api/v1/products"
        self.auth = (os.getenv("SENDOWL_KEY"), os.getenv("SENDOWL_SECRET"))
        self.product_type = 'digital'
        self.sales_limit = 1
        

    def get_products(self):
        """
        Retrieves all products from the SendOwl API.
        
        Returns:
            A JSON object containing all products.
        """
        response = requests.get(self.base_url, auth=self.auth)
        return response.json()

    def search_product(self, term):
        """
        Searches for products by name.
        
        Parameters:
            term (str): The search term to look for in product names.
            
        Returns:
            A JSON object containing products that match the search term.
        """
        response = requests.get(f"{self.base_url}/search?term={term}", auth=self.auth)
        return response.json()

    def get_product(self, product_id):
        """
        Retrieves a specific product by its ID.
        
        Parameters:
            product_id (int): The unique identifier for the product.
            
        Returns:
            A JSON object containing the details of the specified product.
        """
        response = requests.get(f"{self.base_url}/{product_id}", auth=self.auth)
        return response.json()

    def create_product(self, data):
        """
        Creates a new product.
        
        Parameters:
            product_data (dict): A dictionary containing the product details. For file uploads, use multipart/form-data encoding.
            
        Returns:
            A JSON object containing the newly created product details.
        """
        url = self.base_url + ".json"  # or ".json" if you prefer JSON
        auth = self.auth
        id  = data['id']
        files = {
                'product[attachment]': open(data['attachment'], 'rb')
                 }
        data = {
            'product[product_type]': self.product_type,
            'product[sales_limit]': self.sales_limit,
            'product[pdf_stamping]':True,
            'product[price]': data['event_price'],
            'product[name]': data['event_id'],
            'product[created_at]':data['created_at'],
        }
        response = requests.post(url, auth=auth, files=files, data=data)
        if response.status_code == 201:
            print(f"✨✨✨✨✨  Product: {id} created successfully. ✨✨✨✨✨")
            return response.content  # or response.json() if using JSON
        else:
            print(f"💩 Failed to create product. Status code: {response.status_code} 💩")
            return None

    def update_product(self, product_id, product_data):
        """
        Updates an existing product.
        
        Parameters:
            product_id (int): The unique identifier for the product to update.
            product_data (dict): A dictionary containing the updated product details.
            
        Returns:
            A JSON object containing the updated product details.
        """
        response = requests.put(f"{self.base_url}/{product_id}", auth=self.auth, data=product_data)
        return response.json()

    def delete_product(self, product_id):
        """
        Deletes a product.
        
        Parameters:
            product_id (int): The unique identifier for the product to delete.
            
        Returns:
            The HTTP status code of the delete request.
        """
        response = requests.delete(f"{self.base_url}/{product_id}", auth=self.auth)
        return response.status_code

    def issue_order(self, product_id, order_data):
        """
        Issues an order for a product. Useful for integrating with custom or third-party gateways.
        
        Parameters:
            product_id (int): The unique identifier for the product.
            order_data (dict): A dictionary containing the order details.
            
        Returns:
            A JSON object containing the issued order details.
        """
        response = requests.post(f"{self.base_url}/{product_id}/issue", auth=self.auth, data=order_data)
        return response.json()
    
    def test(self, var):
        print(f"works: {var}")

# Example usage
if __name__ == "__main__":
    uploader = SendOwlProduct()
    product_name = "Test Product 100"
    product_type = "digital"  # digital, software, tangible, service, or drip
    product_price = "12.50"
    attachment_path = "/home/sbellina/jobs/tickets/tickets_output/QR_Code_2.png"

    # Create a new product
    product_response = uploader.create_product(product_name, product_type, product_price, attachment_path)

    print()
