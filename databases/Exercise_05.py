'''
Using the API from the API section, write a program that makes a request to
get all of the users and all of their tasks.

Create tables in a new local database to model this data.

Think about what tables are required to model this data. Do you need two tables? Three?

Persist the data returned from the API to your database.

NOTE: If you run this several times you will be saving the same information in the table.
To prevent this, you should add a check to see if the record already exists before inserting it.

'''

import requests, sqlalchemy
from pprint import pprint

url = "http://demo.codingnomads.co:8080/tasks_api/"

def get_data (base_url, page):
    url = base_url + page
    api_response = requests.get(url)
    api_data = api_response.json()['data']
    return api_data

users_raw = get_data(url, 'users')
tasks_raw = get_data(url, 'tasks')

#rename "id" key to "user_id"
users = []
for item in users_raw:
    id = item['id']
    del item['id']
    item['user_id'] = id
    users.append(item)

#rename "id" key to "taks_id" and "userID" to "user_id"    
tasks = []
for item in tasks_raw:
    task_id = item['id']
    user_id = item['userId']
    del item['id']
    del item['userId']
    item['task_id'] = task_id
    item['user_id'] = user_id
    tasks.append(item)

engine = sqlalchemy.create_engine('mysql+pymysql://root:pwd@localhost/tasks')
connection = engine.connect()
metadata = sqlalchemy.MetaData()

# - create at least 3 tables
table_users = sqlalchemy.Table('users', metadata,
                    sqlalchemy.Column('user_id', sqlalchemy.Integer()),
                    sqlalchemy.Column('first_name', sqlalchemy.String(50), nullable=False),
                    sqlalchemy.Column('last_name', sqlalchemy.String(50), nullable=False),
                    sqlalchemy.Column('email', sqlalchemy.String(50), nullable=False),
                    sqlalchemy.Column('createdAt', sqlalchemy.BigInteger(), nullable=False),
                    sqlalchemy.Column('updatedAt', sqlalchemy.BigInteger(), nullable=False))                    
            

table_tasks = sqlalchemy.Table('tasks', metadata,
                    sqlalchemy.Column('task_id', sqlalchemy.Integer()),
                    sqlalchemy.Column('user_id', sqlalchemy.Integer()),
                    sqlalchemy.Column('name', sqlalchemy.String(50), nullable=False),
                    sqlalchemy.Column('description', sqlalchemy.String(200), nullable=True),
                    sqlalchemy.Column('completed', sqlalchemy.Boolean(), default=True),
                    sqlalchemy.Column('createdAt', sqlalchemy.BigInteger(), nullable=False),
                    sqlalchemy.Column('updatedAt', sqlalchemy.BigInteger(), nullable=False))                   
                  
metadata.create_all(engine)

table_users = sqlalchemy.Table('users', metadata, autoload=True, autoload_with=engine)
table_tasks = sqlalchemy.Table('tasks', metadata, autoload=True, autoload_with=engine)

query_insert_user = sqlalchemy.insert(table_users)
result_query_insert_user = connection.execute(query_insert_user, users)

query_insert_tasks = sqlalchemy.insert(table_tasks)
result_query_insert_tasks = connection.execute(query_insert_tasks, tasks)
