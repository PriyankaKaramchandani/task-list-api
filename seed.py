from datetime import datetime
from app.db import db
from app.models.task import Task
from app.models.goal import Goal  


def seed_data():
    
    goal1 = Goal(title="Complete Python Project")
    goal2 = Goal(title="Learn SQLAlchemy")

    
    task1 = Task(
        title="Write Python code",
        description="Complete the coding part of the project.",
        completed_at=datetime(2024, 11, 7, 14, 30),
        goal=goal1  
    )

    task2 = Task(
        title="Test the code",
        description="Run tests to ensure functionality.",
        completed_at=None,  
        goal=goal1  
    )

    task3 = Task(
        title="Read SQLAlchemy documentation",
        description="Understand SQLAlchemy ORM basics.",
        completed_at=datetime(2024, 11, 6, 10, 0),
        goal=goal2  
    )

    db.session.add_all([goal1, goal2, task1, task2, task3])
    db.session.commit()


