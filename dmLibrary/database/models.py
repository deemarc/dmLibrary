from . import db

class DatabaseTable(db.Model):
    __tablename__ = 'database_table'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), unique=True,nullable=False)
