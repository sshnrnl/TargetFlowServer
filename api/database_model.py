from api.index import app, db

# USERS TABLE
class User(db.Model):
    __tablename__ = "users"
    
    id = db.Column(db.String(3), primary_key=True)
    username = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(10), nullable=False)

# TARGET TABLE
class Target(db.Model):
    __tablename__ = "target"
    
    target_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # author = db.Column(db.Integer, nullable=False)
    author = db.Column(db.String(3), db.ForeignKey("users.id"), primary_key=True)
    target_name = db.Column(db.String(64), nullable=False)
    description = db.Column(db.String(256))
    prize = db.Column(db.String(64))
    created_at = db.Column(db.DateTime, nullable=False)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)

    details = db.relationship("TargetDetail", back_populates="target")
    assignments = db.relationship("TargetAssignment", back_populates="target")

# TARGET DETAILS TABLE
class TargetDetail(db.Model):
    __tablename__ = "target_details"
    
    target_id = db.Column(db.Integer, db.ForeignKey("target.target_id"), primary_key=True)
    items_id = db.Column(db.String(64), primary_key=True)
    qty = db.Column(db.Integer, nullable=False)

    target = db.relationship("Target", back_populates="details")

# TARGET ASSIGNMENT TABLE
class TargetAssignment(db.Model):
    __tablename__ = "target_assignment"
    
    target_id = db.Column(db.Integer, db.ForeignKey("target.target_id"), primary_key=True)
    user_id = db.Column(db.String(3), db.ForeignKey("users.id"), primary_key=True)

    target = db.relationship("Target", back_populates="assignments")
    user = db.relationship("User")

# Initialize the database
with app.app_context():
    db.create_all()
