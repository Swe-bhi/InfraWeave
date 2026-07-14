from fastapi import FastAPI
from pydantic import BaseModel
import psycopg2
import os

app = FastAPI()

def get_connection():
    return psycopg2.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST")
    )

# ---------------------------
# READ: Health Check
# ---------------------------
@app.get("/health")
def health_check():
    try:
        conn = get_connection()
        conn.close()
        return {"status": "ok", "message": "Database connected"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

# ---------------------------
# READ: Get All Users
# ---------------------------
@app.get("/users")
def get_users():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users;")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return {"users": rows}

# ---------------------------
# READ: Get User by ID
# ---------------------------
@app.get("/user/{user_id}")
def get_user_by_id(user_id: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE id = %s;", (user_id,))
    row = cur.fetchone()
    cur.close()
    conn.close()

    if row:
        return {"user": row}
    else:
        return {"message": "User not found"}

# ---------------------------
# CREATE: Add a New User
# ---------------------------
class User(BaseModel):
    name: str
    email: str

@app.post("/add-user")
def add_user(user: User):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO users (name, email) VALUES (%s, %s)",
        (user.name, user.email)
    )
    conn.commit()
    cur.close()
    conn.close()
    return {"message": "User added successfully", "user": user}

# ---------------------------
# UPDATE: Update User by ID
# ---------------------------
class UserUpdate(BaseModel):
    name: str | None = None
    email: str | None = None

@app.put("/update-user/{user_id}")
def update_user(user_id: int, user: UserUpdate):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT id, name, email FROM users WHERE id = %s;", (user_id,))
    existing = cur.fetchone()

    if not existing:
        cur.close()
        conn.close()
        return {"message": "User not found"}

    new_name = user.name if user.name is not None else existing[1]
    new_email = user.email if user.email is not None else existing[2]

    cur.execute(
        "UPDATE users SET name = %s, email = %s WHERE id = %s;",
        (new_name, new_email, user_id)
    )
    conn.commit()

    cur.close()
    conn.close()

    return {
        "message": "User updated successfully",
        "updated_user": {"id": user_id, "name": new_name, "email": new_email}
    }

# ---------------------------
# DELETE: Delete User by ID
# ---------------------------
@app.delete("/delete-user/{user_id}")
def delete_user(user_id: int):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT id FROM users WHERE id = %s;", (user_id,))
    existing = cur.fetchone()

    if not existing:
        cur.close()
        conn.close()
        return {"message": "User not found"}

    cur.execute("DELETE FROM users WHERE id = %s;", (user_id,))
    conn.commit()

    cur.close()
    conn.close()

    return {"message": "User deleted successfully", "deleted_id": user_id}

