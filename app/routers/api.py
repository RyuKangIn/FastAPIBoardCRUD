from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Task
from app.schemas import TaskCreate, TaskUpdate, TaskResponse

router = APIRouter()

# 할 일 추가
@router.post("/tasks", response_model=TaskResponse)
def create_task(task_data: TaskCreate, db: Session = Depends(get_db)):
    new_task = Task(title=task_data.title)
    db.add(new_task)
    db.commit()
    db.refresh(new_task)#?
    return new_task

@router.get("/tasks", response_model=list[TaskResponse])
def get_tasks(db: Session = Depends(get_db)):
    tasks = db.query(Task).all()
    return tasks

# 완료된 일 조회
@router.get("/tasks/done", response_model=list[TaskResponse])
def get_done_tasks(db: Session = Depends(get_db)):
    tasks = db.query(Task).filter(Task.is_done == True).all()
    return tasks

# 미완료 일만 조회
@router.get("/tasks/undone", response_model=list[TaskResponse])
def get_undone_tasks(db: Session = Depends(get_db)):
    tasks = db.query(Task).filter(Task.is_done == False).all()
    return tasks

# 할 일 수정
@router.patch("/tasks/{id}", response_model=TaskResponse)
def update_task(id: int, updates:TaskUpdate,db: Session = Depends(get_db)):
    task = db.get(Task, id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    if updates.title is not None:
        task.title = updates.title
    if updates.is_done is not None:
        task.is_done = updates.is_done

    db.commit()
    db.refresh(task)
    return task

# 할 일 삭제
@router.delete("/tasks/{id}")
def delete_task(id: int, db: Session = Depends(get_db)):
    task = db.get(Task, id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    db.delete(task)
    db.commit()
    return {"message": f"Task({id}) deleted."}