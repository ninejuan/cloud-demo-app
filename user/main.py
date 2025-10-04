from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import aiomysql
import os
import uuid
from typing import Optional

app = FastAPI(title="User App", version="1.0.0")

DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": int(os.getenv("DB_PORT", "3306")),
    "user": os.getenv("DB_USER", "user"),
    "password": os.getenv("DB_PASSWORD", "password"),
    "db": os.getenv("DB_NAME", "userdb"),
    "charset": "utf8mb4"
}

class UserData(BaseModel):
    requestid: str
    uuid: str
    username: str
    email: str
    status_message: str

class UserResponse(BaseModel):
    username: str
    email: str
    status_message: str

class InsertResponse(BaseModel):
    status: str
    id: str

pool = None

async def get_db_pool():
    global pool
    if pool is None:
        pool = await aiomysql.create_pool(**DB_CONFIG)
    return pool

@app.on_event("startup")
async def startup():
    await get_db_pool()

@app.on_event("shutdown")
async def shutdown():
    global pool
    if pool:
        pool.close()
        await pool.wait_closed()

@app.get("/healthcheck")
async def healthcheck():
    return {"status": "ok"}

@app.post("/v1/user", response_model=InsertResponse)
async def create_user(data: UserData):
    pool = await get_db_pool()
    user_id = f"user_{data.uuid}"
    
    async with pool.acquire() as conn:
        async with conn.cursor() as cursor:
            await cursor.execute(
                "INSERT INTO user (id, username, email, status_message) VALUES (%s, %s, %s, %s)",
                (user_id, data.username, data.email, data.status_message)
            )
            await conn.commit()
    
    return InsertResponse(status="created", id=user_id)

@app.get("/v1/user", response_model=UserResponse)
async def get_user(email: str, requestid: str, uuid: str):
    pool = await get_db_pool()
    
    async with pool.acquire() as conn:
        async with conn.cursor() as cursor:
            await cursor.execute(
                "SELECT username, email, status_message FROM user WHERE email = %s",
                (email,)
            )
            row = await cursor.fetchone()
    
    if not row:
        raise HTTPException(status_code=404, detail="User not found")
    
    return UserResponse(username=row[0], email=row[1], status_message=row[2])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
