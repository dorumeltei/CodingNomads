'''
Consider each of the tasks below as a separate database query. Using SQLAlchemy, which is the necessary code to:

- Select all the actors with the first name of your choice

- Select all the actors and the films they have been in

- Select all the actors that have appeared in a category of a comedy of your choice

- Select all the comedic films and sort them by rental rate

- Using one of the statements above, add a GROUP BY statement of your choice

- Using one of the statements above, add a ORDER BY statement of your choice

'''

import sqlalchemy
from pprint import pprint

engine = sqlalchemy.create_engine('mysql+pymysql://root:pwd@localhost/sakila')
connection = engine.connect()
metadata = sqlalchemy.MetaData()

table_actor = sqlalchemy.Table('actor', metadata, autoload=True, autoload_with=engine)
table_film = sqlalchemy.Table('film', metadata, autoload=True, autoload_with=engine)
table_film_actor = sqlalchemy.Table('film_actor', metadata, autoload=True, autoload_with=engine)
table_category = sqlalchemy.Table('category', metadata, autoload=True, autoload_with=engine)
table_film_category = sqlalchemy.Table('film_category', metadata, autoload=True, autoload_with=engine)

# - Select all the actors with the first name of your choice
query_select_an_actor = sqlalchemy.select([table_actor]).where(table_actor.columns.first_name == 'penelope')
result_query1 = connection.execute(query_select_an_actor)
for actor in result_query1:
    fname = actor['first_name']
    lname = actor['last_name']
    # print(f'{fname.capitalize()} {lname.capitalize()}')

# - Select all the actors and the films they have been in
join_tables_actor_film = table_actor.join(table_film_actor, table_film_actor.columns.actor_id == table_actor.columns.actor_id)\
                                    .join(table_film, table_film.columns.film_id == table_film_actor.columns.film_id)
query_select_actor_films = sqlalchemy.select([table_actor.columns.first_name, 
                                            table_actor.columns.last_name, 
                                            table_film.columns.title])\
                                    .select_from(join_tables_actor_film)
result_query_actor_film = connection.execute(query_select_actor_films).fetchall()
for item in result_query_actor_film:
    fname, lname, film = item
    # print (f'{fname.capitalize()} {lname.capitalize()} - {film.capitalize()}')

# - Select all the actors that have appeared in a category of a comedy of your choice
film_search = 'WARDROBE PHANTOM'
for actor in result_query_actor_film:
    fname, lname, film = actor    
    # if film == film_search:
    #     print (f'{fname.capitalize()} {lname.capitalize()}')

# - Select all the comedic films and sort them by rental rate
join_film_category = table_film.join(table_film_category, table_film_category.columns.film_id == table_film.columns.film_id)\
                                    .join(table_category, table_category.columns.category_id == table_film_category.columns.category_id)
query_select_films = sqlalchemy.select([table_film.columns.title, table_film.columns.rental_rate])\
                        .select_from(join_film_category).where(table_category.columns.name == 'Comedy')\
                        .order_by(sqlalchemy.desc(table_film.columns.rental_rate))
result = connection.execute(query_select_films).fetchall()
print('All comedic films, sorted by rental rates:')
for items in result:
    film, rent = items
    # print(f'{film.capitalize()} - {float(rent)}')

# - Using one of the statements above, add a GROUP BY statement of your choice
query_actor_films_quantity = sqlalchemy.select([table_actor.columns.first_name,
                                            table_actor.columns.last_name,
                                           sqlalchemy.func.count(table_actor.columns.actor_id)])\
                                    .select_from(join_tables_actor_film)\
                                    .group_by(table_actor.columns.actor_id)\
                                    .order_by(sqlalchemy.desc(sqlalchemy.func.count(table_actor.columns.actor_id)))
result_query_actor_film = connection.execute(query_actor_films_quantity).fetchall()

for item in result_query_actor_film:
    fname, lname, films = item
    # print (f'{fname.capitalize()} {lname.capitalize()} - {films}')

# - Using one of the statements above, add a ORDER BY statement of your choice
query_order_by_last_name = query_select_actor_films.order_by(sqlalchemy.asc(table_actor.columns.last_name))
result_query = connection.execute(query_order_by_last_name).fetchall()
# pprint(result_query)


