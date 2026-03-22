from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    predictions = db.relationship("Prediction", backref="user", lazy="dynamic")

    def score(self, categories):
        correct = 0
        for pred in self.predictions:
            winner_ids = {n.id for n in pred.category.nominees if n.is_winner}
            if pred.nominee_id in winner_ids:
                correct += 1
        return correct


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    display_order = db.Column(db.Integer, default=0)
    nominees = db.relationship("Nominee", backref="category", lazy="select",
                               order_by="Nominee.name")

    @property
    def winner(self):
        """Returns first winner, or None — used for 'has any winner been set?' checks."""
        return next((n for n in self.nominees if n.is_winner), None)

    @property
    def winners(self):
        """Returns all winners (supports co-winners / ties)."""
        return [n for n in self.nominees if n.is_winner]


class Nominee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey("category.id"), nullable=False)
    name = db.Column(db.String(200), nullable=False)
    detail = db.Column(db.String(200), default="")  # film title for person categories
    is_winner = db.Column(db.Boolean, default=False)


class Prediction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey("category.id"), nullable=False)
    nominee_id = db.Column(db.Integer, db.ForeignKey("nominee.id"), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    category = db.relationship("Category")
    nominee = db.relationship("Nominee")

    __table_args__ = (
        db.UniqueConstraint("user_id", "category_id", name="uq_user_category"),
    )


class Setting(db.Model):
    key = db.Column(db.String(50), primary_key=True)
    value = db.Column(db.String(200), nullable=False)
