from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import os
from motor.motor_asyncio import AsyncIOMotorClient
from uuid import UUID, uuid4

# Load environment variables from .env file
MONOGODB_CONNECTION_STRING = os.environ['MONGODB_CONNECTION_STRING'] 


client = AsyncIOMotorClient(MONOGODB_CONNECTION_STRING, uuidRepresentation="standard")

db = client.todolist
todos = db.todos

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# @app.get("/")
# def read_root():
#     return {"message": "API is running"}

class todoTask(BaseModel):
    id: UUID = Field(default_factory=uuid4, alias="_id")  # MongoDB uses _id as the default primary key field
    content: str

class todoTaskCreate(BaseModel):
    content: str

#todos: list[todoTask] = []
#id_counter = 1

@app.post("/todos", response_model=todoTask)
async def create_todo(task: todoTaskCreate):
    #global id_counter
    new_task = todoTask(content=task.content)
    await todos.insert_one(new_task.model_dump(by_alias=True))  # Insert the task into MongoDB
    return new_task

@app.get("/todos", response_model=list[todoTask])
async def read_todos():
    return await todos.find().to_list(length=None)  # Retrieve all tasks from MongoDB and return as a list

@app.delete("/todos/{task_id}")
async def delete_todo(task_id: UUID):
    result = await todos.delete_one({"_id": task_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"message": "Task deleted successfully"} 