import uvicorn
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException
from typing import List, Optional

app = FastAPI()

class Task(BaseModel):
    id: int
    title:str
    description:Optional[str] = None
    completed:bool = False
    
tasks = []

@app.get("/tasks", response_model=List[Task])
def list_task():
    return tasks

@app.post("/tasks", response_model=Task)
def create_task(task:Task):
    tasks.append(task)
    return task

@app.put("/tasks/{task_id}",response_model=Task)
def update_task(task_id:int, task:Task):
    for idx, t in enumerate(tasks):
        if t.id == task_id:
            tasks[idx] = task
            return task
    raise HTTPException(status_code=404, detail="Task not found")

@app.delete("/tasks/{task_id}",response_model=Task)
def delete_task(task_id: int):
    for idx, t in enumerate(tasks):
        if t.id == task_id:
            return tasks.pop(idx)
    raise HTTPException(status_code=404, detail="Task not found")


if __name__ == "__main__":
   uvicorn.run(app, host="127.0.0.1", port=8000)