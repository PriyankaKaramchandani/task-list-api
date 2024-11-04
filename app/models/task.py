from sqlalchemy.orm import Mapped, mapped_column
from ..db import db
from typing import Optional
from datetime import datetime

class Task(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str]
    description: Mapped[str]
    completed_at: Mapped[Optional[datetime]] 

    def to_dict(self):
        return {
            "task": {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "is_complete": self.is_complete() # will use is_complete helper function to return True or False
            }
        }

    def is_complete(self):
        # will return True if completed_at is not None and will return False if its None
        return self.completed_at is not None
            
    @classmethod
    def from_dict(cls, task_data):
        new_task = Task(
            title=task_data["title"], 
            description=task_data["description"], 
            completed_at=task_data.get("completed_at", None)
            )

        return new_task