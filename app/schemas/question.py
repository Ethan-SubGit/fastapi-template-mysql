from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List
from app.schemas.user import User

class AnswerBase(BaseModel):
    content: str

class AnswerCreate(AnswerBase):
    pass

class Answer(AnswerBase):
    id: int
    question_id: int
    user_id: int
    created_at: datetime
    user: Optional[User] = None

    class Config:
        from_attributes = True

class QuestionBase(BaseModel):
    title: str
    content: str

class QuestionCreate(QuestionBase):
    pass

class QuestionUpdate(QuestionBase):
    pass

class Question(QuestionBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    user: Optional[User] = None
    answers: List[Answer] = []

    class Config:
        from_attributes = True 