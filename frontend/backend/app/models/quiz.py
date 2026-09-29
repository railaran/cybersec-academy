from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class Quiz(Base):
    __tablename__ = "quizzes"
    id             = Column(Integer, primary_key=True)
    title          = Column(String(200), nullable=False, index=True)
    description    = Column(Text)
    category       = Column(String(50), default="general")
    difficulty     = Column(String(20), default="easy")
    time_limit_min = Column(Integer, default=15)
    pass_score     = Column(Integer, default=70)
    is_active      = Column(Boolean, default=True)
    created_at     = Column(DateTime(timezone=True), server_default=func.now())

    questions = relationship("Question", back_populates="quiz",
                             cascade="all, delete-orphan", order_by="Question.order")

class Question(Base):
    __tablename__ = "questions"
    id       = Column(Integer, primary_key=True)
    quiz_id  = Column(Integer, ForeignKey("quizzes.id", ondelete="CASCADE"))
    text     = Column(Text, nullable=False)
    type     = Column(String(20), default="single")  # single, multiple, truefalse
    points   = Column(Integer, default=1)
    order    = Column(Integer, default=0)

    quiz    = relationship("Quiz", back_populates="questions")
    answers = relationship("Answer", back_populates="question",
                           cascade="all, delete-orphan")

class Answer(Base):
    __tablename__ = "answers"
    id          = Column(Integer, primary_key=True)
    question_id = Column(Integer, ForeignKey("questions.id", ondelete="CASCADE"))
    text        = Column(String(500), nullable=False)
    is_correct  = Column(Boolean, default=False)

    question = relationship("Question", back_populates="answers")
