from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

todoslist = []


class Todos(BaseModel):
    id: int
    task: str
    iscompleted: bool


@app.post("/todos")
def create_todo(todo: Todos):

    todoslist.append(todo)

    return {
        "message": "Created",
        "todos": todo
    }


@app.get("/todos")
def get_all_todos():

    return {
        "list": todoslist
    }


@app.get("/todos/{id}")
def get_todo(id: int):

    for todo in todoslist:

        if todo.id == id:
            return todo

    return {"error": "Todo not found"}


@app.put("/todos/{todo_id}")
def update_todo(todo_id: int, updated_todo: Todos):

    for index, todo in enumerate(todoslist):

        if todo.id == todo_id:

            todoslist[index] = updated_todo

            return {
                "message": "Data Updated",
                "data": updated_todo
            }

    return {"error": "Todo not found"}


@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int):

    for index, todo in enumerate(todoslist):

        if todo.id == todo_id:

            todoslist.pop(index)

            return {
                "message": "Data Deleted"
            }

    return {
        "error": "Todo not found"
    }