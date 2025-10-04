from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import aiomysql
import os
import uuid
from typing import Optional

app = FastAPI(title="Red App", version="1.0.0")

DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": int(os.getenv("DB_PORT", "3306")),
    "user": os.getenv("DB_USER", "user"),
    "password": os.getenv("DB_PASSWORD", "password"),
    "db": os.getenv("DB_NAME", "red_db"),
    "charset": "utf8mb4"
}

class RedData(BaseModel):
    name: str

class RedResponse(BaseModel):
    name: str
    version: str

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

@app.get("/health")
async def health():
    return "200 OK"

@app.post("/red", response_model=InsertResponse)
async def create_red_data(data: RedData):
    pool = await get_db_pool()
    data_id = f"yy11{str(uuid.uuid4())[:8]}"
    
    async with pool.acquire() as conn:
        async with conn.cursor() as cursor:
            await cursor.execute(
                "INSERT INTO red (id, name) VALUES (%s, %s)",
                (data_id, data.name)
            )
            await conn.commit()
    
    return InsertResponse(status="inserted", id=data_id)

@app.get("/red", response_model=RedResponse)
async def get_red_data(id: str):
    pool = await get_db_pool()
    
    async with pool.acquire() as conn:
        async with conn.cursor() as cursor:
            await cursor.execute(
                "SELECT name FROM red WHERE id = %s", (id,)
            )
            row = await cursor.fetchone()
    
    if not row:
        raise HTTPException(status_code=404, detail="Data not found")
    
    return RedResponse(name=row[0], version="1.0.0")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
