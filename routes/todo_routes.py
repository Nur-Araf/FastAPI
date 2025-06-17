from fastapi import APIRouter, HTTPException
from configrations import db
from database.schemas import list_data
from database.models import TodoItem
from bson.objectid import ObjectId
from datetime import datetime

todo_router = APIRouter(prefix="/api/v1/todos", tags=["Todos"])

collection = db['learning_collection']

@todo_router.get("/")
async def get_todos():
    todos = collection.find({"is_deleted": False})
    return list_data(todos)

@todo_router.post("/")
async def create_todo(new_task: TodoItem):
    try:
        response = collection.insert_one(dict(new_task))
        return {"status": 200, "id": str(response.inserted_id)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@todo_router.put("/{todo_id}")
async def update_todo(todo_id: str, updated_task: TodoItem):
    try:
        id = ObjectId(todo_id)
        existing_doc = collection.find_one({"_id": id, "is_deleted": False})
        if not existing_doc:
            raise HTTPException(status_code=404, detail="Todo not found")
        updated_task.updated_at = datetime.now()
        response = collection.update_one({"_id": id}, {"$set": dict(updated_task)})
        if response.modified_count == 0:
            raise HTTPException(status_code=304, detail="Todo not modified")
        return {"status": 200, "message": "Todo updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@todo_router.delete("/{todo_id}")
async def delete_todo(todo_id: str):
    try:
        id = ObjectId(todo_id)
        existing_doc = collection.find_one({"_id": id, "is_deleted": False})
        if not existing_doc:
            raise HTTPException(status_code=404, detail="Todo not found")
        response = collection.update_one({"_id": id}, {"$set": {"is_deleted": True}})
        if response.modified_count == 0:
            raise HTTPException(status_code=304, detail="Todo not modified")
        return {"status": 200, "message": "Todo deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
