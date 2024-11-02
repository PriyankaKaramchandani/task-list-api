from flask import Blueprint, abort, make_response, Response
from flask import request
from app.db import db
from app.models.task import Task
from datetime import datetime

tasks_bp = Blueprint("tasks_bp", __name__, url_prefix="/tasks")

@tasks_bp.post("")
def create_a_task():
    request_body = request.get_json()

    validate_missing_attributes(request_body)

    title = request_body["title"]
    description = request_body["description"]
    completed_at = request_body.get("completed_at", None)
    new_task = Task(title=title, description=description, completed_at=completed_at)

    db.session.add(new_task)
    db.session.commit()

    return new_task.to_dict(), 201

@tasks_bp.get("")
def get_all_tasks():
    sort_param = request.args.get("sort")

    query = db.select(Task)

    if sort_param == "desc":
        query = query.order_by(Task.title.desc())
    if sort_param == "asc":
        query = query.order_by(Task.title.asc())
    
    tasks = db.session.scalars(query)

    tasks_response = [task.to_dict()["task"] for task in tasks]
    return tasks_response

@tasks_bp.get("/<task_id>")
def get_one_task(task_id):
    task = validate_task(task_id)

    return task.to_dict()
    

@tasks_bp.put("/<task_id>")
def update_one_task(task_id):
    task = validate_task(task_id)
    request_body = request.get_json()

    task.title = request_body["title"]
    task.description = request_body["description"]

    db.session.commit()

    return task.to_dict()

@tasks_bp.delete("/<task_id>")
def delete_task(task_id):
    task = validate_task(task_id)

    db.session.delete(task)
    db.session.commit()

    response = {"details": f"Task {task.id} \"{task.title}\" successfully deleted"}

    return response

@tasks_bp.patch("/<task_id>/mark_complete")
def task_mark_complete(task_id):
    task = validate_task(task_id)
    
    task.completed_at = datetime.now()

    db.session.commit()

    return task.to_dict()

@tasks_bp.patch("/<task_id>/mark_incomplete")
def task_mark_incomplete(task_id):
    task = validate_task(task_id)

    task.completed_at = None

    db.session.commit()

    return task.to_dict()

def validate_task(task_id):
    try:
        task_id = int(task_id)
    except:
        abort(make_response({"message": f"task {task_id} should be an int data type"}, 400))

    query = db.select(Task).where(Task.id == task_id)
    task = db.session.scalar(query)

    if not task:
        abort(make_response({"message": f"There is no existing task with an id of {task_id}"}, 404))
    
    return task

def validate_missing_attributes(request_body):
    if "title" not in request_body or "description" not in request_body:
        abort(make_response({"details": "Invalid data"}, 400))