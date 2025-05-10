from api.index import app, db, jsonify, connect
from api.database_model import Target, TargetAssignment, TargetDetail
from api.index import token_required, decode_token
from datetime import date

@app.route('/api/v1/sales/get_target', methods=['GET'])
@token_required
def get_target():
    payload = decode_token()
    user_id = payload["id"]
    current_date = date.today()

    # Fetch all active targets for the user
    targets = db.session.query(Target).join(TargetAssignment).filter(
        TargetAssignment.user_id == user_id,
        db.cast(current_date, db.Date).between(Target.start_date, Target.end_date)
    ).all()

    if not targets:
        return jsonify({"targets": []})

    # Map to collect all item_ids to query at once later
    all_item_ids = set()
    target_map = {}

    for target in targets:
        target_details = db.session.query(TargetDetail).filter_by(target_id=target.target_id).all()
        item_ids = [detail.items_id for detail in target_details]
        all_item_ids.update(item_ids)

        target_map[target.target_id] = {
            "meta": target,
            "details_raw": target_details,
            "item_ids": item_ids
        }

    # Convert set to tuple for SQL IN clause
    item_ids_tuple = tuple(all_item_ids)
    
    # Use Firebird connection
    conn = connect()
    cursor = conn.cursor()

    # Fetch all item names (nambar) in one query
    item_names = {}
    if item_ids_tuple:
        placeholders = ', '.join(['?'] * len(item_ids_tuple))  # Firebird uses '?' as parameter placeholder
        cursor.execute(f"""
            SELECT kobar, nambar FROM kobar
            WHERE kobar IN ({placeholders})
        """, item_ids_tuple)
        item_names = {row[0]: row[1] for row in cursor.fetchall()}

    target_data = []

    for target_id, data in target_map.items():
        target = data["meta"]
        item_ids = data["item_ids"]
        details_raw = data["details_raw"]

        # Fetch sold items in one query
        if item_ids:
            placeholders = ', '.join(['?'] * len(item_ids))  # Firebird uses '?' for parameter placeholders
            cursor.execute(f"""
                SELECT mutso.kobar, mutso.nambar, SUM(mutso.qty)
                FROM mso
                LEFT JOIN mutso ON mutso.nobuk = mso.nobuk
                WHERE mso.kosal = ?
                AND mso.tgl BETWEEN ? AND ?
                AND mutso.kobar IN ({placeholders})
                GROUP BY mutso.kobar, mutso.nambar
            """, (user_id, target.start_date, target.end_date, *item_ids))
            sold_rows = cursor.fetchall()
        else:
            sold_rows = []

        sold_data = [{
            "items_id": kobar,
            "item_name": nambar,
            "qty_sold": total_qty
        } for kobar, nambar, total_qty in sold_rows]

        details_data = [{
            "items_id": detail.items_id,
            "item_name": item_names.get(detail.items_id, ""),
            "qty": detail.qty
        } for detail in details_raw]

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
