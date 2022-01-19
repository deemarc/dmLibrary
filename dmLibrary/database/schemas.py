from . import ma
from .models import DatabaseTable

class DatabaseSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = DatabaseTable
