'''
Using the Chuck Norris API in combination with the datamuse API
( https://api.chucknorris.io/ - https://www.datamuse.com/api/ )

* Query the chucknorris api for a sentence
* Use the last word of that sentence to send a query to the Datamuse API
  and use the rel_rhy (or rel_nry) query parameter to fetch a word that rhymes
* Repeat a coupe of times and store the sentences and rhyme words
* Synthesize the collected results into an avant-garde poem and post on the forum ;)

'''
import requests
from pprint import pprint

url1 = 'https://api.chucknorris.io/jokes/random'
url2 = ' https://api.datamuse.com/'

def get_joke_word():
  resp1 = requests.get(url1)
  resp1 = resp1.json()
  val1 = resp1['value'].split()
  joke_word = val1[-1]
  if not joke_word[-1].isalpha():
    joke_word = joke_word[:-1]
  return joke_word

poem = ''''''

for x in range(2):
  while True: 
    joke_word = get_joke_word()
    rhyme_url = f'{url2}words?rel_rhy={joke_word}'
    resp2 = requests.get(rhyme_url)
    resp2 = resp2.json()
    if resp2:
      rhyme_word = resp2[0]['word']
      break
    else:
      continue
  poem += f'{joke_word.capitalize()}\n{rhyme_word.capitalize()}\n'

print(poem)