from fastapi import FastAPI
from datetime import datetime
import uvicorn
import pytz

app = FastAPI(title="HelloWorld App", version="1.0.0")

@app.get("/")
async def root():
    return "Hello World!"

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.get("/time")
async def get_time():
    kst = pytz.timezone('Asia/Seoul')
    return {"timestamp": datetime.now(kst).isoformat()}

@app.get("/ver")
async def get_version():
    return {"version": "1.0.0"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
