#############################################
#                                           #
#               MySQL Module                #
#                                           #
#  Author: Shan                             #
#                                           #
#############################################

# Importing necessary library
import mysql.connector

# Connecting to SQL Database
def sqlconnect():
    return mysql.connector.connect(
        host="103.145.227.148",
        user="rajawa19_mks",
        password="nDYsy}*F[u7v",
        database="rajawa19_mks",
    )
    
# Comitting changes to SQL Database
def sqlcommit(connection):
    connection.commit()

# Inserting row to SQl Database
def sqlinsert(cursor,tables,values):
    return cursor.execute(f'INSERT INTO {tables} VALUES ({values})')

# Deleting row from SQL Database
def sqldelete(cursor,tables, condition):
    return cursor.execute(f'DELETE FROM {tables} WHERE {condition}')

# Select from SQL Database (Filter: Descending)
def sqlselect_desc(cursor, tables, selection='*', condition='', group=''):
    '''print(f'SELECT {selection} FROM {tables}{condition if not condition else f" WHERE {condition}"}')'''
    cursor.execute(f'SELECT {selection} FROM {tables}{condition if not condition else f" WHERE {condition}"} group by {group} desc')
    return cursor.fetchall()

# Select from SQL Database (Filter: Descending)
def sqlselect_sort(cursor, tables, selection='*', condition='', key='',sort=''):
    '''print(f'SELECT {selection} FROM {tables}{condition if not condition else f" WHERE {condition}"}')'''
    cursor.execute(f'SELECT {selection} FROM {tables}{condition if not condition else f" WHERE {condition}"} order by {key} {sort}')
    return cursor.fetchall()

# Select from SQL Database
def sqlselect(cursor, tables, selection='*', condition=''):
    '''print(f'SELECT {selection} FROM {tables}{condition if not condition else f" WHERE {condition}"}')'''
    cursor.execute(f'SELECT {selection} FROM {tables}{condition if not condition else f" WHERE {condition}"}')
    return cursor.fetchall()

# Update if row exist and insert if row doesnt exist
def sqlupdate_or_insert(cursor, tables, values, todo):
    cursor.execute(f'INSERT INTO {tables} VALUES ({values}) ON DUPLICATE KEY UPDATE {todo}')
    # print(f'INSERT INTO {tables} VALUES ({values}) ON DUPLICATE KEY UPDATE {todo}')

# Update row values from SQL Database
def sqlupdate(cursor, tables,todo, condition=''):
    cursor.execute(f"update {tables} SET {todo} WHERE {condition}")
    # print(f"update {tables} SET {todo} WHERE {condition}")