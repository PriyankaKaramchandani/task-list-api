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

    if isinstance(new_model, Goal):
        return make_response(new_model.to_dict(), 201)
    elif isinstance(new_model, Task):
        return make_response(new_model.to_dict_without_goal_id(), 201)

def get_models_with_filters(cls, filters=None):
    query = db.select(cls)
    
    sort_param = filters.get("sort") if filters else None

    if sort_param == "desc":
        query = query.order_by(getattr(cls, "title").desc())
    else:
        query = query.order_by(getattr(cls, "title").asc())

    if filters:
        for attribute, value in filters.items():
            if hasattr(cls, attribute):
                query = query.where(getattr(cls, attribute).ilike(f"%{value}%"))

    models = db.session.scalars(query.order_by(cls.id))

    models_response = [model.to_dict_without_goal_id()["task"] for model in models]

    return models_response