import datetime
from fastapi import FastAPI
from utils import map_fields_to_array, map_fields
from db import cur, con
from pydantic import BaseModel

app = FastAPI()


# pydantic uses to define the schemas of the data that it receives (requests) and returns (responses)
# helps to validate and document inside the "/docs endpoint" aka predictable and safe
class TodoOut(BaseModel):
    description: str | None = None
    completed: bool | None = None
    id: int
    created_date: datetime.date | None = None
    updated_date: datetime.date | None = None


class TodoIn(BaseModel):
    description: str
    completed: bool


@app.post('/api/todo')
async def create_todo(todo_item: TodoIn) -> TodoOut:
    return {
        "description": "Blah",
        "completed": False,
        "id": 1,
        "created_date": datetime.date.today(),
        "updated_date": datetime.date.today()
    }


@app.get('/api/todos')
async def fetch_todos():
    cur.execute("SELECT * FROM todo")
    colnames = [desc[0] for desc in cur.description]
    todos = cur.fetchall()

    response_data = map_fields_to_array(todos, colnames)

    return {"todos": response_data}


@app.put('/api/todo/')
async def update_todo(todo: TodoOut):
    set_columns = []
    for key, value in todo:
        if value is not None:
            if type(value) == str:
                set_columns.append(f"{key}='{value}'")
            else:
                set_columns.append(f'{key}={value}')
    set_string = ", ".join(set_columns)

    cur.execute(
        f"""
        UPDATE todo
        SET {set_string}
        WHERE id = {todo.id}
        """
    )

    updated_rows = cur.rowcount
    con.commit()

    cur.execute(
        f"""
        SELECT * FROM todo
        WHERE id = {todo.id}
        """
    )
    updated_todo = cur.fetchall()
    colnames = [desc[0] for desc in cur.description]

    response_data = map_fields(updated_todo, colnames)

    return {"updated_todo": response_data, "updated_count": updated_rows}


@app.get('/api/favorites')
async def fetch_favorites():
    cur.execute(
        """
        SELECT favorites.id AS favorite_id, todo.id, description, completed, updated_date
        FROM todo
        INNER JOIN favorites ON todo.id = favorites.todo_id
        """
    )
    favorites = cur.fetchall()
    colnames = [desc[0] for desc in cur.description]

    response_data = map_fields_to_array(favorites, colnames)

    return {"favorites": response_data}


@app.get('/')
async def root():
    return {"message": "Hello World"}
