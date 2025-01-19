from api.index import app, connect, sqlselect, jwt, request, jsonify, token_required
import os
from datetime import datetime, timedelta, timezone
SECRET_KEY = os.getenv("SECRET_KEY")

@app.route('/api/v1/sales/post-so', methods=['post'])
@token_required
def post_sales_order():
    
    #getting auth header
    auth_header = request.headers.get('Authorization')
    request_data = request.json
    token = auth_header.split(" ")[1] if len(auth_header.split()) > 1 else None
    decoded_token = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])

    #making connection to the database
    conn = connect()
    cursor = conn.cursor()

    #retrieve kosal and nobuk for customer's and item's detail sake
    kosal=decoded_token["id"]
    nobuk=generate_mso(decoded_token["id"], cursor)

    #getting customer's and item's detail
    customer_detail=get_customer_details(request_data.get('customer_id'), cursor)
    items_detail=convert_item(request_data.get('items', []), nobuk, cursor, kosal)
    
    # uncomment to debug
    # print(nobuk, customer_detail, items_detail)


    #Variables for querying
    ####################################################
    NOBUK=nobuk  # Kode Sales + 0 + 2.Tahun + 5.Urut (Structur)
    KODE='CC'
    NOIDP='MKS'
    # TGL="CURRENT_DATE"  # Date bukan datetime
    TGLKIRIM=None
    TGLEXPIRE=None
    NOCTRL=None
    NOREF=None
    NOSO=None
    NOPO=None
    KOCUS=customer_detail['KOCUS']
    NAMCUS=customer_detail['NAMCUS']
    KOWIL=customer_detail['KOWIL']
    KOSEG='' #None
    KOSAL=kosal
    KOEXP=''
    KOASJ=''
    KOMAT=''
    FAKTOR=1
    KURS=1
    JUMLAH=items_detail["JUMLAH"]
    KURSTAX=1
    DISC=''
    PDISC=0
    JDISC=0
    PPN=customer_detail["KOTAX"] # biasa PPN atau P
    PPNINCL='T'
    PPPN=customer_detail["PPPN"]  # ambil dari kocus bs berupa 10 atau 11
    JPPN=items_detail["JUMLAH"] * PPPN / 100 # jumlah * pppn/100
    OTAX=''
    OTAXINCL='F'
    POTAX=0
    JOTAX=0
    FREIGHT=0
    NET=items_detail["JUMLAH"]
    DP=0
    JDP=0
    NODP=None
    TGLDP=None
    NOFP=None
    TGLFP=None
    KOSER=None
    JTEMPO=customer_detail["JTEMPO"]  # ambil dari kolom kocus berupa 28 atau 14
    STATUS=None
    KONSINYASI='F'
    TEMPLATE='F'
    OTORISASI='T'
    OTOUSR=''
    # OTOSTAMP="CURRENT_TIMESTAMP"  # datetime
    PRINTED=0
    PRFPAJAK=0
    CLOSED='F'
    CLOSEDUSR=None
    CLOSEDSTAMP=None
    BATAL='F'
    BATALUSR=None
    BATALSTAMP=None
    LVL='1'
    STAMP=None
    USR=decoded_token["id"]
    OWNER=decoded_token["id"]
    # OWNSTAMP="CURRENT_TIMESTAMP"  # datetime
    KETCUS=None
    KET=None
    MOBILE='T'
    FINISHED='F'
    OTOKOSAL='T'
    # OTOKOSALSTAMP="CURRENT_TIMESTAMP"  # datetime
    ####################################################

    #sql query
    query = f"""
        INSERT INTO MSO (
            NOBUK, KODE, NOIDP, TGL, TGLKIRIM, TGLEXPIRE, 
        NOCTRL, NOREF, NOSO, NOPO, KOCUS, NAMCUS, KOWIL, 
        KOSEG, KOSAL, KOEXP, KOASJ, KOMAT, FAKTOR, KURS, 
        JUMLAH, KURSTAX, DISC, PDISC, JDISC, PPN, PPNINCL, PPPN, 
        JPPN, OTAX, OTAXINCL, POTAX, JOTAX, FREIGHT, NET, 
        DP, JDP, NODP, TGLDP, NOFP, TGLFP, KOSER, JTEMPO, 
        STATUS, KONSINYASI, TEMPLATE, OTORISASI, OTOUSR, 
        OTOSTAMP, PRINTED, PRFPAJAK, CLOSED, CLOSEDUSR, 
        CLOSEDSTAMP, BATAL, BATALUSR, BATALSTAMP, LVL, STAMP, 
        USR, OWNER, OWNSTAMP, KETCUS, KET, MOBILE, 
        FINISHED, OTOKOSAL, OTOKOSALSTAMP
        ) VALUES (
        ?, ?, ?, CURRENT_DATE, ?, ?, ?,
        ?, ?, ?, ?, ?, ?, ?, 
        ?, ?, ?, ?, ?, ?, ?, 
        ?, ?, ?, ?, ?, ?, ?, 
        ?, ?, ?, ?, ?, ?, ?, 
        ?, ?, ?, ?, ?, ?, ?, 
        ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP, 
        ?, ?, ?, ?, ?, ?, ?, 
        ?, ?, ?, ?, ?, CURRENT_TIMESTAMP, ?,?,?,?,?,CURRENT_TIMESTAMP
    );"""

    # factorized data
    data = (
        NOBUK, KODE, NOIDP, TGLKIRIM, TGLEXPIRE, 
        NOCTRL, NOREF, NOSO, NOPO, KOCUS, NAMCUS, KOWIL, 
        KOSEG, KOSAL, KOEXP, KOASJ, KOMAT, FAKTOR, KURS, 
        JUMLAH, KURSTAX, DISC, PDISC, JDISC, PPN, PPNINCL, PPPN, 
        JPPN, OTAX, OTAXINCL, POTAX, JOTAX, FREIGHT, NET, 
        DP, JDP, NODP, TGLDP, NOFP, TGLFP, KOSER, JTEMPO, 
        STATUS, KONSINYASI, TEMPLATE, OTORISASI, OTOUSR
        , PRINTED, PRFPAJAK, CLOSED, CLOSEDUSR, 
        CLOSEDSTAMP, BATAL, BATALUSR, BATALSTAMP, LVL, STAMP, 
        USR, OWNER, KETCUS, KET, MOBILE, 
        FINISHED, OTOKOSAL
    )

    #executing query
    cursor.execute(query, data)
    conn.commit()

    #closing connection
    cursor.close()
    conn.close()


    return jsonify({
        "status":200,
        "message":"Success! You have posted a sales order"
    })

def convert_item(items, nobuk, cursor, kosal):
    # Extract kobar values (keys of the items dictionary)
    kobar_values = list(items.keys())  # ['B000171', 'S-0053610']

    # Create placeholders based on the number of kobar values
    placeholders = ', '.join(['?' for _ in range(len(kobar_values))])

    # Build the query
    query = f"""
        SELECT 
            k.kobar, 
            k.nambar, 
            k.hjual,
            COALESCE(t.kosat, k.kobar) AS SATQTY,
            COALESCE(t.kvrsi, 1) AS kvrsiqty,
            k.kosat

        FROM kobar k
        LEFT JOIN tbkvrsi t ON k.kobar = t.kobar
        WHERE k.kobar IN ({placeholders})
        """

    # executing query
    cursor.execute(query, kobar_values)

    # Fetch and build the return_value dictionary
    results = cursor.fetchall()
    return_value = {"items": {}}
    jumlah=0
    for row in results:
        # Calculate the total and add item details to the return dictionary
        kobar, nambar, hjual, satqty, kvrsiqty,sathrg = row
        qty = items.get(kobar, 0)  # Get quantity from items, default to 0 if not found
        total = hjual * qty * kvrsiqty
        
        return_value["items"][kobar] = {
            "KOBAR": kobar,
            "NAMBAR": nambar,
            "HARGA": hjual,
            "QTY": qty,
            "TOTAL": total,
            "SATQTY":satqty,
            "KVRSIQTY":kvrsiqty,
            "SATHRG":sathrg,
            "NOBUK":nobuk
        }
        jumlah+=total
        res = create_mutso_query(return_value["items"][kobar], kosal)
        cursor.execute(res["query"], res["value"])
   
    return_value["JUMLAH"]=jumlah
    return return_value



def create_mutso_query(items, kosal):
    #####################################################
    NOBUK = items["NOBUK"]
    KODE = 'CC'
    NOIDP = 'MKS'
    NOMOR = None  # Will be generated by the trigger
    # TGL = '2025-01-16'
    KOBAR = items["KOBAR"]
    KOALI = None
    QTYKIRIM = None
    QTY = items["QTY"]
    SATQTY = items["SATQTY"]
    KVRSIQTY = items["KVRSIQTY"]
    HARGA = items["HARGA"]
    SATHRG = items["SATHRG"]
    KVRSIHRG = 1
    DISC = 0
    TDISC = 'P'
    JDISC = 0
    JUMLAH = items["TOTAL"]
    KODEP = None
    KOPRO = None
    TEMPLATE = 'F'
    OTORISASI = 'T'
    BATAL = 'F'
    STAMP = None  # Usually handled directly in SQL
    USR = None
    OWNER = kosal ###WARNING UPDATE KE KODE SALES NNTI###
    OWNSTAMP = 'CURRENT_TIMESTAMP'  # Usually handled directly in SQL
    KET = None
    NAMBAR = items["NAMBAR"]
    #####################################################


    # SQL query with placeholders
    sql_query = """
    INSERT INTO MUTSO (
    NOBUK, KODE, NOIDP, NOMOR, TGL, KOBAR, KOALI, QTYKIRIM, QTY, SATQTY, KVRSIQTY, HARGA, SATHRG, KVRSIHRG, 
    DISC, TDISC, JDISC, JUMLAH, KODEP, KOPRO, TEMPLATE, OTORISASI, BATAL, STAMP, USR, OWNER, OWNSTAMP, KET, NAMBAR
    )
    VALUES (
    ?, ?, ?, ?, CURRENT_DATE, ?, ?, ?, ?, ?, ?, ?, ?, ?, 
    ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP, ?, ?
    );
    """

    # Values for placeholders
    values = (
        NOBUK, KODE, NOIDP, NOMOR, KOBAR, KOALI, QTYKIRIM, QTY, SATQTY, KVRSIQTY, HARGA, SATHRG, KVRSIHRG,
        DISC, TDISC, JDISC, JUMLAH, KODEP, KOPRO, TEMPLATE, OTORISASI, BATAL,STAMP, USR, OWNER, KET, NAMBAR
    )

    return {
        "query":sql_query,
        "value":values
    }


def generate_mso(kosal, cursor):
    # Get the current year (last 2 digits)
    current_year = datetime.now().year % 100  # e.g., 2025 → 25

    # Query the table for the highest existing MSO starting with the given Kosal and year
    cursor.execute(f"""
        SELECT MAX(NOBUK)
        FROM MSO
        WHERE NOBUK LIKE '{kosal}0{current_year}%'
    """)
    result = cursor.fetchone()[0]

    # Extract the sequential number from the highest MSO
    if result:
        last_sequence = int(result[-5:])  # Get the last 5 digits
    else:
        last_sequence = 0  # Start from 0 if no MSO exists

    # Increment the sequence
    new_sequence = last_sequence + 1

    # Pad the sequence to 5 digits
    sequence_str = str(new_sequence).zfill(5)

    # Construct the new MSO
    new_mso = f"{kosal}0{current_year}{sequence_str}"
    return new_mso

def get_customer_details(customer_id, cursor):
    cursor.execute(f"""
        SELECT 
            KOCUS.KOCUS, 
            KOCUS.NAMCUS, 
            KOCUS.KOWIL, 
            KOCUS.KOTAX, 
            KOCUS.JTEMPO, 
            COALESCE(K.PERSEN, 0) AS PPPN
        FROM KOCUS
        LEFT JOIN KOTAX AS K ON KOCUS.KOTAX = K.KOTAX
        WHERE KOCUS.KOCUS = '{customer_id}'
    """)
    kocus, namcus, kowil, kotax, jtempo, pppn=cursor.fetchall()[0]
    return {
        'KOCUS':kocus,
        'NAMCUS':namcus,
        'KOWIL':kowil,
        'KOTAX':kotax,
        'JTEMPO':jtempo,
        "PPPN":pppn
    }