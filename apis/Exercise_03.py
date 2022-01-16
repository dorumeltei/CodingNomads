'''
Write the necessary code to make a POST request to:

    http://demo.codingnomads.co:8080/tasks_api/users

and create a user with your information.

Make a GET request to confirm that your user information has been saved.

'''

import requests
from pprint import pprint

url = "http://demo.codingnomads.co:8080/tasks_api/users"

new_user = {    
    "first_name": "dhoro",
    "last_name": "mlt",
    "email": "mlt@gmail.com"
}

response = requests.post(url, json=new_user)

check_data = requests.get(url)
check_data = check_data.json()
pprint(check_data['data'])
