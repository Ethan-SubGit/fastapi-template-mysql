from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from app.models.question import Question, Answer
from app.schemas.question import QuestionCreate, QuestionUpdate, AnswerCreate
from fastapi import HTTPException, status

class QuestionService:
    @staticmethod
    async def create_question(db: AsyncSession, question: QuestionCreate, user_id: int):
        db_question = Question(
            title=question.title,
            content=question.content,
            user_id=user_id
        )
        db.add(db_question)
        await db.commit()
        await db.refresh(db_question)
        
        # 관계 데이터를 명시적으로 로드
        query = select(Question).options(
            selectinload(Question.user),
            selectinload(Question.answers)
        ).where(Question.id == db_question.id)
        result = await db.execute(query)
        return result.scalar_one()

    @staticmethod
    async def get_questions(db: AsyncSession, skip: int = 0, limit: int = 100):
        query = select(Question).options(
            selectinload(Question.user),
            selectinload(Question.answers).selectinload(Answer.user)
        ).offset(skip).limit(limit)
        result = await db.execute(query)
        return result.scalars().all()

    @staticmethod
    async def get_question(db: AsyncSession, question_id: int):
        query = select(Question).options(
            selectinload(Question.user),
            selectinload(Question.answers).selectinload(Answer.user)
        ).where(Question.id == question_id)
        result = await db.execute(query)
        question = result.scalar_one_or_none()
        if question is None:
            raise HTTPException(status_code=404, detail="Question not found")
        return question

    @staticmethod
    async def create_answer(
        db: AsyncSession, 
        question_id: int, 
        answer: AnswerCreate, 
        user_id: int
    ):
        db_answer = Answer(
            content=answer.content,
            question_id=question_id,
            user_id=user_id
        )
        db.add(db_answer)
        await db.commit()
        await db.refresh(db_answer)
        
        # 관계 데이터를 명시적으로 로드
        query = select(Answer).options(
            selectinload(Answer.user),
            selectinload(Answer.question)
        ).where(Answer.id == db_answer.id)
        result = await db.execute(query)
        return result.scalar_one()