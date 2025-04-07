from api.index import app, db, request, jsonify
from datetime import datetime
from api.database_model import Target, TargetAssignment, TargetDetail
from api.index import token_required

@app.route('/api/v1/admin/create-target', methods=['POST'])
@token_required
def create_target():
    data = request.get_json()

    # Extract values from input
    target_name = data.get("target-name")
    description = data.get("target-desc")
    prize = data.get("prize")
    start_date = datetime.strptime(data.get("start-date"), "%Y-%m-%d")
    end_date = datetime.strptime(data.get("end-date"), "%Y-%m-%d")
    assigned_to = data.get("assigned-to", [])  # List of user IDs
    target_items = data.get("target-items", {})  # Dictionary of items

    try:
        # Insert into Target table
        new_target = Target(
            author=1,  # Change dynamically if needed
            target_name=target_name,
            description=description,
            prize=str(prize),
            created_at=datetime.now(),
            start_date=start_date,
            end_date=end_date
        )
        db.session.add(new_target)
        db.session.flush()  # Get target_id before commit

        # Insert into TargetAssignment table
        for user_id in assigned_to:
            db.session.add(TargetAssignment(target_id=new_target.target_id, user_id=user_id))

        # Insert into TargetDetail table
        for item_id, qty in target_items.items():
            db.session.add(TargetDetail(target_id=new_target.target_id, items_id=item_id, qty=qty))

        db.session.commit()  # Commit transaction

        return jsonify({
            "status": 200,
            "message": "Target created successfully",
            "target_id": new_target.target_id
        })

    except Exception as e:
        db.session.rollback()
        return jsonify({
            "status": 500,
            "message": "Database error",
            "error": str(e)
        }), 500

    finally:
        db.session.close()  # Always close the session
