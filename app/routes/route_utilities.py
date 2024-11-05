from flask import abort, make_response
from app.db import db
from app.models.goal import Goal
from app.models.task import Task

def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except:
        abort(make_response({"message": f"{cls.__name__} {model_id} is invalid, should be an int data type"}, 400))

    query = db.select(cls).where(cls.id == model_id)
    model = db.session.scalar(query)

    if not model:
        abort(make_response({"message": f"{cls.__name__} {model_id} is not found"}, 404))
    
    return model

def create_model(cls, model_data):
    try:
        new_model = cls.from_dict(model_data)
        
    except KeyError as error:
        response = {'details': 'Invalid data'}
        abort(make_response(response, 400))
    
    db.session.add(new_model)
    db.session.commit()

    return make_response(new_model.to_dict(), 201)
