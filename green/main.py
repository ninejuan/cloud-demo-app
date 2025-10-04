from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import asyncpg
import os
import uuid
from typing import Optional

app = FastAPI(title="Green App", version="1.0.0")

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost:5432/green_db")

class GreenData(BaseModel):
    x: str
    y: int

class GreenResponse(BaseModel):
    x: str
    y: int
    version: str

class InsertResponse(BaseModel):
    status: str
    id: str

pool = None

async def get_db_pool():
    global pool
    if pool is None:
        pool = await asyncpg.create_pool(DATABASE_URL)
    return pool

@app.on_event("startup")
async def startup():
    await get_db_pool()

@app.on_event("shutdown")
async def shutdown():
    global pool
    if pool:
        await pool.close()

@app.get("/health")
async def health():
    return "200 OK"

@app.post("/green", response_model=InsertResponse)
async def create_green_data(data: GreenData):
    pool = await get_db_pool()
    data_id = f"xx11{str(uuid.uuid4())[:8]}"
    
    async with pool.acquire() as conn:
        await conn.execute(
            "INSERT INTO green (id, x, y) VALUES ($1, $2, $3)",
            data_id, data.x, data.y
        )
    
    return InsertResponse(status="inserted", id=data_id)

@app.get("/green", response_model=GreenResponse)
async def get_green_data(id: str):
    pool = await get_db_pool()
    
    async with pool.acquire() as conn:
        row = await conn.fetchrow(
            "SELECT x, y FROM green WHERE id = $1", id
        )
    
    if not row:
        raise HTTPException(status_code=404, detail="Data not found")
    
    return GreenResponse(x=row['x'], y=row['y'], version="1.0.0")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
