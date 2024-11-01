from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.core.database import get_db
from app.schemas.question import Question, QuestionCreate, Answer, AnswerCreate
from app.services.question_service import QuestionService
from app.api.deps import get_current_user
from app.models.user import User

router = APIRouter()

@router.post("/questions/", response_model=Question)
async def create_question(
    question: QuestionCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return await QuestionService.create_question(db, question, current_user.id)

@router.get("/questions/", response_model=List[Question])
async def read_questions(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db)
):
    questions = await QuestionService.get_questions(db, skip=skip, limit=limit)
    return questions

@router.get("/questions/{question_id}", response_model=Question)
async def read_question(
    question_id: int,
    db: AsyncSession = Depends(get_db)
):
    return await QuestionService.get_question(db, question_id)

@router.post("/questions/{question_id}/answers/", response_model=Answer)
async def create_answer(
    question_id: int,
    answer: AnswerCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return await QuestionService.create_answer(db, question_id, answer, current_user.id) 