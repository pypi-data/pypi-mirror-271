import requests

# Base URL of the Flask server
# Example base url - Needs to be set by the client - base_url = "http://localhost:5000"
url = None

# API key for authentication
apikey = None

# Create a SQLite database
def create_database(db_name):
    global url
    endpoint_url = f"{url}/create_db"
    headers = {'X-API-Key': apikey}
    data = {'db_name': db_name}
    response = requests.post(endpoint_url, json=data, headers=headers)
    print(response.text)

# Validate a user
def validate_user(db_name, username, password):
    global url
    endpoint_url = f"{url}/validate_user"
    headers = {'X-API-Key': apikey}
    data = {'db_name': db_name, 'username': username, 'password': password}
    response = requests.post(endpoint_url, json=data, headers=headers)
    print(response.text)

# Add a new user
def add_user(db_name, username, email, password, pro_status):
    global url
    endpoint_url = f"{url}/add_user"
    headers = {'X-API-Key': apikey}
    data = {'db_name': db_name, 'username': username, 'email': email, 'password': password, 'pro_status': pro_status}
    response = requests.post(endpoint_url, json=data, headers=headers)
    print(response.text)

# Delete a user
def delete_user(db_name, username):
    global url
    endpoint_url = f"{url}/delete_user"
    headers = {'X-API-Key': apikey}
    data = {'db_name': db_name, 'username': username}
    response = requests.post(endpoint_url, json=data, headers=headers)
    print(response.text)

# Edit user's pro status
def edit_user_pro_status(db_name, username, pro_status):
    global url
    endpoint_url = f"{url}/edit_user_pro_status"
    headers = {'X-API-Key': apikey}
    data = {'db_name': db_name, 'username': username, 'pro_status': pro_status}
    response = requests.post(endpoint_url, json=data, headers=headers)
    print(response.text)


def return_pro_status(db_name, username):
    global url
    endpoint_url = f"{url}/return_pro_status"
    headers = {'X-API-Key': apikey}
    data = {'db_name': db_name, 'username': username}
    response = requests.post(endpoint_url, json=data, headers=headers)
    result = response.json()  # Extract JSON content from response
    pro_status = result.get('pro_status')  # Get the value of 'pro_status' from the response
    if pro_status == [1]:  # Assuming 'pro_status' is a list containing a single integer
        print("True")
    else:
        print("False")

