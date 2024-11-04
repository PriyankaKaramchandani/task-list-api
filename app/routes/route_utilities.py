from flask import abort, make_response
from app.db import db

def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except:
        abort(make_response({"message": f"{cls.__name__} {model_id} is invalid, should be an int data type"}, 400))

    query = db.select(cls).where(cls.id == model_id)
    task = db.session.scalar(query)

    if not task:
        abort(make_response({"message": f"{cls.__name__} {model_id} is not found"}, 404))
    
    return task