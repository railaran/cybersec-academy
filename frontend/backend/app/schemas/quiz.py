from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from datetime import datetime

class AnswerBase(BaseModel):
    text: str
    is_correct: bool = False

class AnswerOut(AnswerBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

class QuestionBase(BaseModel):
    text: str
    type: str = "single"
    points: int = 1
    order: int = 0

class QuestionCreate(QuestionBase):
    answers: List[AnswerBase] = []

class QuestionOut(QuestionBase):
    id: int
    answers: List[AnswerOut] = []
    model_config = ConfigDict(from_attributes=True)

class QuizBase(BaseModel):
    title: str
    description: Optional[str] = None
    category: str = "general"
    difficulty: str = "easy"
    time_limit_min: int = 15
    pass_score: int = 70
    is_active: bool = True

class QuizCreate(QuizBase):
    questions: List[QuestionCreate] = []

class QuizUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    difficulty: Optional[str] = None
    time_limit_min: Optional[int] = None
    pass_score: Optional[int] = None
    is_active: Optional[bool] = None

class QuizOut(QuizBase):
    id: int
    created_at: Optional[datetime] = None
    questions: List[QuestionOut] = []
    model_config = ConfigDict(from_attributes=True)

class QuizSubmit(BaseModel):
    answers: dict  # {question_id: answer_id atau [answer_ids]}
