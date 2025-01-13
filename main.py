import firebirdsql

# conn = firebirdsql.connect(
#     host='121706200748.IP-DYNAMIC.COM',
#     database=r'D:\OneSOS Ver 4.1\DataOneSOS\DataTEST.FDB',
#     port=3050,
#     user='sysdba',
#     password='masterkey'
# )


conn = firebirdsql.connect(
        host='localhost',
        database='C://Users//SHAN//Downloads//DataTEST (1)//DataTEST.fdb',
        port=3050,
        user='sysdba',
        password='masterkey'
    )




cur = conn.cursor()

cur.execute("select  * from KOSAL")
for c in cur.fetchall():
    print(c[1])
# print(cur.fetchall()[0])
conn.close()