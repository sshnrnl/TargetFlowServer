#############################################
#                                           #
#                FBD Module                 #
#                                           #
#  Author: Shan                             #
#                                           #
#############################################

import firebirdsql # type: ignore

def connect():
    return firebirdsql.connect(
        host='121706200748.IP-DYNAMIC.COM',
        database='D:/OneSOS Ver 4.1/DataOneSOS/DataTEST.FDB',
        port=3050,
        user='sysdba',
        password='masterkey'
    )

# def connect():
#     return firebirdsql.connect(
#         host='localhost',
#         database='C:/User s/SHAN/Downloads/DataTEST/data.FDB',
#         port=3050,
#         user='sysdba',
#         password='masterkey'
#     )


def select(tables, selection='*', condition='',connect='', order='', order_mode='ASC'):
    cursor=connect.cursor()
    '''print(f'SELECT {selection} FROM {tables}{condition if not condition else f" WHERE {condition}"}')'''
    cursor.execute(f'SELECT {selection} FROM {tables}{condition if not condition else f" WHERE {condition}"} {order if not order else f"ORDER BY "+order+" "+order_mode}')
    a=cursor.fetchall()
    return a



def select_range(tables, start=0, end=0, selection="*", condition='', connect='', order='', order_mode='ASC'):
    cursor=connect.cursor()
    print(f'SELECT {selection} FROM {tables}{condition if not condition else f" WHERE {condition}"} ROWS {start} TO {end} {order if not order else f"ORDER BY "+order+" "+order_mode}')
    cursor.execute(f'SELECT {selection} FROM {tables}{condition if not condition else f" WHERE {condition}"} {order if not order else f"ORDER BY "+order+" "+order_mode} ROWS {start} TO {end}')
    a=cursor.fetchall()
    return a

