'''
Write a program that makes a DELETE request to remove the user your create in a previous example.

Again, make a GET request to confirm that information has been deleted.

'''

import requests
from pprint import pprint

url = "http://demo.codingnomads.co:8080/tasks_api/users"

id = "/593"
response = requests.delete(url + id)

check_data = requests.get(url)

check_data = check_data.json()['data']

pprint(check_data)