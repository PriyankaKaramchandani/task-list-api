from flask import Blueprint, abort, make_response, Response
from flask import request
from app.db import db
from app.models.task import Task
from datetime import datetime
from app.routes.route_utilities import validate_model, create_model, get_models_with_filters
import requests
import os
from dotenv import load_dotenv

load_dotenv()

bp = Blueprint("bp", __name__, url_prefix="/tasks")

@bp.post("")
def create_a_task():
    request_body = request.get_json()
    return create_model(Task, request_body)

# @bp.get("")
# def get_all_tasks():
#     sort_param = request.args.get("sort")

#     query = db.select(Task)

#     if sort_param == "desc":
#         query = query.order_by(Task.title.desc())
#     if sort_param == "asc":
#         query = query.order_by(Task.title.asc())
    
#     tasks = db.session.scalars(query)

#     tasks_response = [task.to_dict()["task"] for task in tasks]
#     return tasks_response

@bp.get("")
def get_all_tasks():
    return get_models_with_filters(Task, request.args)

@bp.get("/<task_id>")
def get_one_task(task_id):
    task = validate_model(Task, task_id)

    return task.to_dict()
    
@bp.put("/<task_id>")
def update_one_task(task_id):
    task = validate_model(Task, task_id)
    request_body = request.get_json()

    task.title = request_body["title"]
    task.description = request_body["description"]

    db.session.commit()

    return task.to_dict()

@bp.delete("/<task_id>")
def delete_task(task_id):
    task = validate_model(Task, task_id)

    db.session.delete(task)
    db.session.commit()

    response = {"details": f"Task {task.id} \"{task.title}\" successfully deleted"}

    return response

@bp.patch("/<task_id>/mark_complete")
def task_mark_complete(task_id):
    task = validate_model(Task, task_id)
    task.completed_at = datetime.now()

    db.session.commit()

    url = "https://slack.com/api/chat.postMessage"
    token = os.environ.get('SLACKBOT_TOKEN')
    header = {"Authorization": f"Bearer {token}"}
    request_body = {
        "channel": "C07TDEQ17RQ",
        "text": f"Someone just completed the task {task.title}"
    }

    notification = requests.post(url, json=request_body, headers=header)
    if notification:
        return task.to_dict()

@bp.patch("/<task_id>/mark_incomplete")
def task_mark_incomplete(task_id):
    task = validate_model(Task, task_id)
    
    task.completed_at = None

    db.session.commit()
    
    return task.to_dict()

