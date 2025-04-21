from api.index import app, db, jsonify, connect
from api.database_model import Target, TargetAssignment, TargetDetail
from api.index import token_required, decode_token

@app.route('/api/v1/sales/get_target', methods=['GET'])
@token_required
def get_target():
    # Get user data from decoded token
    payload = decode_token()
    user_id = payload["id"]
    
    # Query the targets assigned to the user
    targets = db.session.query(Target).join(TargetAssignment).filter(TargetAssignment.user_id == user_id).all()
    conn = connect()
    
    # Prepare response data
    target_data = []
    for target in targets:
        # Get target item details
        target_details = db.session.query(TargetDetail).filter(TargetDetail.target_id == target.target_id).all()
        
        # Prepare list of items_id from target details
        item_ids = [f"'{detail.items_id}'" for detail in target_details]
        item_ids_str = ", ".join(item_ids)  # Convert list to string like 'B000026', 'B000133'
        
        # Query sold data (mutso) for the items assigned to the user within the target date range
        cursor = conn.cursor()
        cursor.execute(f"""
            SELECT 
                mutso.kobar,
                mutso.nambar,
                SUM(mutso.qty) AS total_qty
            FROM mso
            LEFT JOIN mutso ON mutso.nobuk = mso.nobuk
            WHERE mso.kosal = '{user_id}'
              AND mso.tgl BETWEEN DATE '{target.start_date.strftime('%Y-%m-%d')}'
                              AND DATE '{target.end_date.strftime('%Y-%m-%d')}'
              AND mutso.kobar IN ({item_ids_str})
            GROUP BY mutso.kobar, mutso.nambar
        """)
        so_data = cursor.fetchall()

        # Process sold data into a dictionary format with item name
        sold_data = []
        for row in so_data:
            kobar, nambar, total_qty = row
            sold_data.append({
                "items_id": kobar,
                "item_name": nambar,  # Add item name (nambar)
                "qty_sold": total_qty
            })
        
        # Prepare details data (items assigned in the target)
        details_data = [{"items_id": detail.items_id, "qty": detail.qty} for detail in target_details]
        
        # Append target data with sold data and details
        target_data.append({
            "target_id": target.target_id,
            "target_name": target.target_name,
            "description": target.description,
            "prize": target.prize,
            "created_at": target.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            "start_date": target.start_date.strftime("%Y-%m-%d"),
            "end_date": target.end_date.strftime("%Y-%m-%d"),
            "details": details_data,
            "sold": sold_data
        })
    
    return jsonify({"targets": target_data})
