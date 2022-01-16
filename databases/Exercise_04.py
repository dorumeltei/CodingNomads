'''

Please create a new Python application that interfaces with a brand new database.
This application must demonstrate the ability to:

    - create at least 3 tables
    - insert data to each table
    - update data in each table
    - select data from each table
    - delete data from each table
    - use at least one join in a select query

BONUS: Make this application something that a user can interact with from the CLI. Have options
to let the user decide what tables are going to be created, or what data is going to be inserted.
The more dynamic the application, the better!


'''
import sqlalchemy
from pprint import pprint

from sqlalchemy.sql.functions import current_timestamp

engine = sqlalchemy.create_engine('mysql+pymysql://root:pwd@localhost/equipment')
connection = engine.connect()
metadata = sqlalchemy.MetaData()

# - create at least 3 tables
table_user = sqlalchemy.Table('user', metadata,
                    sqlalchemy.Column('user_id', sqlalchemy.Integer(), autoincrement=True),
                    sqlalchemy.Column('f_name', sqlalchemy.String(50), nullable=False),
                    sqlalchemy.Column('l_name', sqlalchemy.String(50), nullable=False),
                    sqlalchemy.Column('username', sqlalchemy.String(20), nullable=False),
                    sqlalchemy.Column('salary', sqlalchemy.Integer(), nullable=True))
            

table_equipment = sqlalchemy.Table('equipment', metadata,
                    sqlalchemy.Column('equipment_id', sqlalchemy.Integer(), autoincrement=True),
                    sqlalchemy.Column('make', sqlalchemy.String(50), nullable=False),
                    sqlalchemy.Column('model', sqlalchemy.String(50), nullable=False),
                    sqlalchemy.Column('description', sqlalchemy.String(200), nullable=True),
                    sqlalchemy.Column('functional', sqlalchemy.Boolean(), default=True))
                 

table_lend = sqlalchemy.Table('lend', metadata,
                    sqlalchemy.Column('lend_id', sqlalchemy.Integer(), autoincrement=True),
                    sqlalchemy.Column('user_id', sqlalchemy.String(50), nullable=False),
                    sqlalchemy.Column('equipment_id', sqlalchemy.String(50), nullable=False),
                    sqlalchemy.Column('lend_date', sqlalchemy.DateTime()))
                   
metadata.create_all(engine)

table_user = sqlalchemy.Table('user', metadata, autoload=True, autoload_with=engine)
table_equipment = sqlalchemy.Table('equipment', metadata, autoload=True, autoload_with=engine)
table_lend = sqlalchemy.Table('lend', metadata, autoload=True, autoload_with=engine)

# - insert data to each table
query_insert_user = sqlalchemy.insert(table_user)
new_records_user = [{'f_name':'Doru', 'l_name':'Meltei', 'username':'dmeltei', 'salary': 2000},
               {'f_name':'Susana', 'l_name':'Garcia', 'username':'sgarcia', 'salary': 3000},]
result_query_insert_user = connection.execute(query_insert_user, new_records_user)

query_insert_equipment = sqlalchemy.insert(table_equipment)
new_records_equipment = [{'make':'LG', 'model':'SVS22', 'description':'55" TV, 4K resolution', 'functional':True},
               {'make':'JBL', 'model':'ABC556', 'description':'500 watts portable speaker with tripod', 'functional':True},
               {'make':'Nikon', 'model':'NK67', 'description':'DSLR camera with standard lens', 'functional':False},]
result_query_insert_equpment = connection.execute(query_insert_equipment, new_records_equipment)

query_insert_lend = sqlalchemy.insert(table_lend)
new_records_lend = [{'user_id':1, 'equipment_id': 4},
                {'user_id':2, 'equipment_id': 2}]
result_query_insert_user = connection.execute(query_insert_lend, new_records_lend)

# - update data in each table
query_update1 = sqlalchemy.update(table_user).values(salary=2800).where(table_user.columns.user_id == 1)
query_update2 = sqlalchemy.update(table_equipment).values(functional=False).where(table_equipment.columns.model == 'ABC556')
result_query_update1 = connection.execute(query_update1)
result_query_update2 = connection.execute(query_update2)

# - select data from each table
query_select1 = sqlalchemy.select([table_user])
query_select2 = sqlalchemy.select([table_equipment.columns.make, table_equipment.columns.model]).where(table_equipment.columns.functional == False)
result_query_select1 = connection.execute(query_select1).fetchall()
result_query_select2 = connection.execute(query_select2).fetchall()
pprint(result_query_select1)
pprint(result_query_select2)

# # - delete data from each table
query_delete1 = sqlalchemy.delete(table_user).where(table_user.columns.user_id == 3)
query_delete2 = sqlalchemy.delete(table_equipment).where(table_equipment.columns.make == 'Nikon')
result_query_delete1 = connection.execute(query_delete1)
result_query_delete2 = connection.execute(query_delete2)

# - use at least one join in a select query
query_join = table_user.join(table_lend, table_lend.columns.user_id == table_user.columns.user_id)\
                        .join(table_equipment, table_equipment.columns.equipment_id == table_lend.columns.equipment_id)
query_select_from_join = sqlalchemy.select([table_user.columns.user_id, table_user.columns.l_name, table_equipment.columns.make, table_equipment.columns.model]).select_from(query_join)
result_query_select_from_join = connection.execute(query_select_from_join).fetchall()
pprint(result_query_select_from_join)

