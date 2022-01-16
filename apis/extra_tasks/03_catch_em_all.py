'''
Using the PokéAPI https://pokeapi.co/docs/v2#pokemon-section
fetch the name and height of all 151 Pokémon of the main series.

Create a text document that describes each Pokémon using the information
available in the JSON response.
NOTE: only using 'height' is enough, but if you want more, go crazy.

BONUS: Using your script, create a folder and download the main 'front_default'
       sprites for each Pokémon using requests into that folder.
       Name the files appropriately using the name data from your response.

'''
import requests, json
from pprint import pprint
from pathlib import Path

parent_folder = "G:\My Drive\code\Python\learn\coding_nomads\python-201-main\\07_apis_databases\\apis\extra_tasks" 
path = Path(parent_folder)

pokemons = {}

# url = 'https://pokeapi.co/docs/v2#pokemon-section'
url = 'https://pokeapi.co/api/v2/pokemon'
response = requests.get(url)
response = response.json()
response = response['results']

for x in response:
       poke_url = x['url']
       req = requests.get(poke_url).json()
       height = req['height']
       front_update_url = req['sprites']['front_default']
       lib = {'height': height, 'front_update': front_update_url}
       pokemons.update({x['name']: lib})     

with open('cath_em_all.txt', 'w') as f:
       json.dump(pokemons, f, indent=4)


images_folder = Path(parent_folder + '\Pokemon_img')
images_folder.mkdir(exist_ok=True)

for k, v in pokemons.items():
       pokemon_url = v['front_update']
       get_image = requests.get(pokemon_url).content
       with open(f'Pokemon_img\\{k}.jpg', 'wb') as f:
              f.write(get_image)
