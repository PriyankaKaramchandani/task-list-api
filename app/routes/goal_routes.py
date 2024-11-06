from flask import Blueprint, make_response, abort, request, Response
from app.models.goal import Goal
from app.models.task import Task
from ..db import db
from .route_utilities import create_model, validate_model

bp = Blueprint("goals", __name__, url_prefix="/goals")

@bp.post("")
def creat_goal():
    request_body = request.get_json()
    return create_model(Goal, request_body)

@bp.get("")
def get_all_goals():
    query = db.select(Goal).order_by(Goal.id)
    goals = db.session.scalars(query)

    goals_response = [goal.to_dict()["goal"] for goal in goals]

    return goals_response

@bp.get("/<goal_id>")
def get_one_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    return goal.to_dict(), 200

@bp.put("/<goal_id>")
def update_one_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    request_body = request.get_json()

    goal.title = request_body["title"]

    db.session.commit()

    return goal.to_dict()

@bp.delete("/<goal_id>")
def delete_one_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    db.session.delete(goal)
    db.session.commit()

    response = {"details": f"Goal {goal_id} \"{goal.title}\" successfully deleted"}
    
    return make_response(response)

@bp.get("/<goal_id>/tasks")
def get_all_tasks_associated_with_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    tasks_response = [task.to_dict()["task"] for task in goal.tasks]
    
    response = {
        "id": goal.id,
        "title": goal.title,
        "tasks": tasks_response
    }

    return make_response(response)

@bp.post("/<goal_id>/tasks")
def create_task_specific_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    request_body = request.get_json()

    task_ids = request_body.get("task_ids", [])

    for task in task_ids:
        Task.query.get(task).goal_id = goal.id

    db.session.commit()

    return {
        "id": int(goal_id),
        "task_ids": task_ids
    }

    
        