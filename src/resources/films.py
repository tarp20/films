from datetime import datetime

from flask import request
from flask_restful import Resource
from marshmallow import ValidationError

from src import db
from src.database.models import Film
from src.schemas.actors import ActorSchema
from src.schemas.films import FilmSchema


class FilmListApi(Resource):
    film_schema = FilmSchema()

    def get(self, uuid=None):
        if not uuid:
            films = db.session.query(Film).all()
            return self.film_schema.dump(films, many=True), 200
        film = db.session.query(Film).filter_by(uuid=uuid).first()
        if not film:
            return '', 404
        return self.film_schema.dump(film), 200

    def post(self):
        try:
            film = self.film_schema.load(request.json, session=db.session)
        except ValidationError as e:
            return {'message': str(e)}, 400
        db.session.add(film)
        db.session.commit()
        return self.film_schema.dump(film), 201

    def put(self, uuid):
        try:
            film = db.session.query(Film).filter_by(uuid=uuid).first()
        except ValidationError as e:
            return {'message': str(e)}, 400
        if not film:
            return '', 404
        film = self.film_schema.load(request.json, instance=film,
                                     session=db.session)
        db.session.add(film)
        db.session.commit()

    def patch(self, uuid):
        try:
            film = db.session.query(Film).filter(Film.uuid == uuid).first()
        except ValidationError as e:
            return {'message': str(e)}, 400
        film = self.film_schema.load(request.json, instance=film,
                                     session=db.session)
        db.session.add(film)
        db.session.commit()

        # film = db.session.query(Film).filter_by(uuid=uuid).first()
        # if not film:
        #     return '', 404
        # film_json = request.json
        # title = film_json['title'],
        # release_date = datetime.strptime(film_json['release_date'], '%B %d, %Y'),
        # distributed_by = film_json['distributed_by'],
        # description = film_json['description'],
        # length = film_json['length'],
        # rating = film_json['rating']
        #
        # if title:
        #     film.title = title
        # elif release_date:
        #     film.release_date = release_date
        # elif description:
        #     film.description = description
        # elif description:
        #     film.distributed_by = distributed_by
        # elif length:
        #     film.length = length
        # elif rating:
        #     film.rating = rating
        # db.session.add(film)
        # db.session.commit()
        # return {'message': 'Updated successfully'}, 200

    def delete(self, uuid):
        film = db.session.query(Film).filter_by(uuid=uuid).first()
        if not film:
            return '', 404
        db.session.delete(film)
        db.session.commit()
        return '', 204
