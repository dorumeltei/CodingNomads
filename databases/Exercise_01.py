'''

All of the following exercises should be done using sqlalchemy.

Using the provided database schema, write the necessary code to print information about the film and category table.

'''
import sqlalchemy
from pprint import pprint

engine = sqlalchemy.create_engine('mysql+pymysql://root:pwd@localhost/sakila')
connection = engine.connect()
metadata = sqlalchemy.MetaData()

table_film = sqlalchemy.Table('film', metadata, autoload=True, autoload_with=engine)
table_category = sqlalchemy.Table('category', metadata, autoload=True, autoload_with=engine)
table_film_category = sqlalchemy.Table('film_category', metadata, autoload=True, autoload_with=engine)

join_film_category = table_film.join(table_film_category, table_film_category.columns.film_id == table_film.columns.film_id)\
                                    .join(table_category, table_category.columns.category_id == table_film_category.columns.category_id)
query_select_from_join = sqlalchemy.select([table_film.columns.title, table_category.columns.name])\
                        .select_from(join_film_category)
result = connection.execute(query_select_from_join).fetchall()
pprint(result)

