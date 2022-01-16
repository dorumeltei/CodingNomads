'''
Write a program that makes a PUT request to update your user information to a new first_name, last_name and email.

Again make a GET request to confirm that your information has been updated.

'''
import requests
from pprint import pprint

url = "http://demo.codingnomads.co:8080/tasks_api/users"

id = "593"
update_user = {
    "id": id,
    "first_name": "dhorooo",
    "last_name": "mlt",
    "email": "mlt@gmail.com"
}
response = requests.put(url, json=update_user)
print(response.status_code)

check_data = requests.get(url)
check_data = check_data.json()
check_data = check_data['data']
pprint(check_data[-1])