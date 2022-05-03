from flask_restful import Resource
from sqlalchemy import func

from src import db
from src.database.models import Film


class AggregationApi(Resource):
    def get(self):
        films_count = db.session.query(func.count(Film.id)).scalar()
