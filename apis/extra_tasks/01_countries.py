'''
Use the countries API https://restcountries.com/ to fetch information
on your home country and the country you're currently in.

In your python program, parse and compare the data of the two responses:
* Which country has the larger population?
* How much does the are of the two countries differ?
* Print the native name of both countries, as well as their capitals

'''
from pprint import pprint
import requests

url = "https://restcountries.com/"
url_all = "https://restcountries.com/v3.1/all"
url_country = "https://restcountries.com/v3.1/name/romania"

def get_country(country):
    url_country = f"https://restcountries.com/v3.1/name/{country.lower()}"
    response = requests.get(url_country)
    return response.json()
    

romania_raw = get_country('romania')[1] #there is an error in the API. first record is Oman, for some reason
qatar_raw = get_country('qatar')[0]

def country(country, native):
    country_details = []
    country_details.append(country['population'])
    country_details.append(country['area'])
    country_details.append(country['name']['nativeName'][native]['official'])
    country_details.append(country['capital'][0])
    return country_details

romania = country(romania_raw, 'ron')
qatar = country(qatar_raw, 'ara')

if romania[0] > qatar[0]:
    print(f'Largest population: Romania - {romania[0]:,}')
else:
    print(f'Largest population: Qatar - {qatar[0]:,} km2')

print(f'Romania area: {int(romania[1]):,} km2\nQatar area in km: {int(qatar[1]):,} km2\
    \nThe area differnece is: {int(romania[1] - qatar[1]):,} km2')

print(f'Romania native name: {romania[2]}. It\'s capital is {romania[3]}.')
print(f'Qatar native name: {qatar[2]}. It\'s capital is {qatar[3]}.')
