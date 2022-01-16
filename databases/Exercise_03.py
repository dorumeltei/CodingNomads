'''
Update all films in the film table to a rental_duration value of 10,
if the length of the movie is more than 150.

'''

import sqlalchemy
from pprint import pprint

engine = sqlalchemy.create_engine('mysql+pymysql://root:pwd@localhost/sakila')
connection = engine.connect()
metadata = sqlalchemy.MetaData()

table_film = sqlalchemy.Table('film', metadata, autoload=True, autoload_with=engine)
qry = sqlalchemy.update(table_film).values(rental_duration=10).where(table_film.columns.length > 150)

result = connection.execute(qry)



