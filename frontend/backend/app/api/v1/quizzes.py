from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional

from app.database import get_db
from app.dependencies import require_admin
from app.models.quiz import Quiz, Question, Answer
from app.schemas.quiz import QuizCreate, QuizUpdate, QuizOut, QuizSubmit

router = APIRouter(prefix="/quizzes", tags=["Quizzes"])


@router.get("/")
def list_quizzes(page: int = Query(1, ge=1), limit: int = Query(9, ge=1, le=100),
                 search: Optional[str] = None, category: Optional[str] = None,
                 difficulty: Optional[str] = None, db: Session = Depends(get_db)):
    q = db.query(Quiz)
    if search:     q = q.filter(Quiz.title.ilike(f"%{search}%"))
    if category:   q = q.filter(Quiz.category == category)
    if difficulty: q = q.filter(Quiz.difficulty == difficulty)
    total = q.count()
    items = q.order_by(Quiz.id.desc()).offset((page - 1) * limit).limit(limit).all()
    return {"items": [QuizOut.model_validate(i).model_dump() for i in items],
            "total": total, "page": page, "limit": limit}


@router.get("/{quiz_id}", response_model=QuizOut)
def get_quiz(quiz_id: int, db: Session = Depends(get_db)):
    quiz = db.query(Quiz).get(quiz_id)
    if not quiz: raise HTTPException(404, "Quiz tidak ditemukan")
    return quiz


@router.post("/", response_model=QuizOut, status_code=201)
def create_quiz(payload: QuizCreate, db: Session = Depends(get_db), _=Depends(require_admin)):
    quiz = Quiz(**payload.model_dump(exclude={"questions"}))
    db.add(quiz); db.flush()
    for i, q in enumerate(payload.questions):
        question = Question(quiz_id=quiz.id, text=q.text, type=q.type,
                            points=q.points, order=q.order or i)
        db.add(question); db.flush()
        for a in q.answers:
            db.add(Answer(question_id=question.id, text=a.text, is_correct=a.is_correct))
    db.commit(); db.refresh(quiz)
    return quiz


@router.put("/{quiz_id}", response_model=QuizOut)
def update_quiz(quiz_id: int, payload: QuizUpdate, db: Session = Depends(get_db), _=Depends(require_admin)):
    quiz = db.query(Quiz).get(quiz_id)
    if not quiz: raise HTTPException(404, "Quiz tidak ditemukan")
    for k, v in payload.model_dump(exclude_unset=True).items():
        setattr(quiz, k, v)
    db.commit(); db.refresh(quiz)
    return quiz


@router.delete("/{quiz_id}", status_code=204)
def delete_quiz(quiz_id: int, db: Session = Depends(get_db), _=Depends(require_admin)):
    quiz = db.query(Quiz).get(quiz_id)
    if not quiz: raise HTTPException(404, "Quiz tidak ditemukan")
    db.delete(quiz); db.commit()


@router.post("/{quiz_id}/submit")
def submit_quiz(quiz_id: int, payload: QuizSubmit, db: Session = Depends(get_db)):
    quiz = db.query(Quiz).get(quiz_id)
    if not quiz: raise HTTPException(404, "Quiz tidak ditemukan")

    total_points = sum(q.points for q in quiz.questions)
    earned = 0
    detail = []

    for q in quiz.questions:
        submitted = payload.answers.get(str(q.id)) or payload.answers.get(q.id)
        if submitted is None:
            detail.append({"question_id": q.id, "correct": False, "earned": 0})
            continue
        correct_ids = {a.id for a in q.answers if a.is_correct}
        if isinstance(submitted, list):
            submitted_set = set(submitted)
        else:
            submitted_set = {submitted}
        ok = submitted_set == correct_ids
        if ok: earned += q.points
        detail.append({"question_id": q.id, "correct": ok,
                       "earned": q.points if ok else 0})

    score = int((earned / total_points * 100)) if total_points else 0
    return {
        "score": score,
        "earned": earned,
        "total": total_points,
        "passed": score >= quiz.pass_score,
        "detail": detail,
    }
