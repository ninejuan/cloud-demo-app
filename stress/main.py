from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import time
import threading
import os
from typing import Optional

app = FastAPI(title="Stress App", version="1.0.0")

class StressData(BaseModel):
    requestid: str
    uuid: str
    length: int

class StressResponse(BaseModel):
    status: str
    length: int
    duration: float

def cpu_stress(length: int):
    for i in range(length):
        for j in range(1000):
            math_result = j * j + j * 2 + 1
            if math_result % 2 == 0:
                math_result = math_result * 3
            else:
                math_result = math_result + 1

@app.get("/healthcheck")
async def healthcheck():
    return {"status": "ok"}

@app.post("/v1/stress", response_model=StressResponse)
async def create_stress(data: StressData):
    try:
        if data.length <= 0 or data.length > 300:
            raise HTTPException(status_code=400, detail="Length must be between 1 and 300 seconds")
        
        start_time = time.time()
        
        stress_thread = threading.Thread(target=cpu_stress, args=(data.length,))
        stress_thread.start()
        stress_thread.join()
        
        end_time = time.time()
        actual_duration = end_time - start_time
        
        return StressResponse(
            status="completed",
            length=data.length,
            duration=round(actual_duration, 2)
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Stress test failed: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
