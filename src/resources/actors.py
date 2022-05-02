from flask import request
from flask_restful import Resource
from marshmallow import ValidationError

from src import db
from src.database.models import Actor

from src.schemas.actors import ActorSchema


class ActorListApi(Resource):
    actor_schema = ActorSchema()

    def get(self, id=None):
        if not id:
            films = db.session.query(Actor).all()
            return self.actor_schema.dump(films, many=True), 200
        actor = db.session.query(Actor).filter_by(id=id).first()
        if not actor:
            return '', 404
        return self.actor_schema.dump(actor), 200

    def post(self):
        try:
            actor = self.actor_schema.load(request.json, session=db.session)
        except ValidationError as e:
            return {'message': str(e)}, 400
        db.session.add(actor)
        db.session.commit()
        return self.actor_schema.dump(actor), 201

    def put(self, id):
        try:
            actor = db.session.query(Actor).filter_by(id=id).first()
        except ValidationError as e:
            return {'message': str(e)}, 400
        if not actor:
            return '', 404
        actor = self.actor_schema.load(request.json, instance=actor, session=db.session)
        db.session.add(actor)
        db.session.commit()

    def delete(self, id):
        actor = db.session.query(Actor).filter_by(id=id).first()
        if not actor:
            return '', 404
        db.session.delete(actor)
        db.session.commit()
        return '', 204
