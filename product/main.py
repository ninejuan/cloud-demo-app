from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import boto3
import os
import json
from typing import Optional
from botocore.exceptions import ClientError

app = FastAPI(title="Product App", version="1.0.0")

AWS_REGION = "ap-northeast-2"
TABLE_NAME = os.getenv("TABLE_NAME", "product")

dynamodb = boto3.resource('dynamodb', region_name=AWS_REGION)
table = dynamodb.Table(TABLE_NAME)

class ProductData(BaseModel):
    requestid: str
    uuid: str
    id: str
    name: str
    price: int

class ProductResponse(BaseModel):
    id: str
    name: str
    price: int

class InsertResponse(BaseModel):
    status: str
    id: str

@app.get("/healthcheck")
async def healthcheck():
    return {"status": "ok"}

@app.post("/v1/product", response_model=InsertResponse)
async def create_product(data: ProductData):
    try:
        table.put_item(
            Item={
                'id': data.id,
                'requestid': data.requestid,
                'uuid': data.uuid,
                'name': data.name,
                'price': data.price
            }
        )
        
        return InsertResponse(status="created", id=data.id)
    
    except ClientError as e:
        raise HTTPException(status_code=500, detail=f"DynamoDB error: {str(e)}")

@app.get("/v1/product", response_model=ProductResponse)
async def get_product(id: str, requestid: str, uuid: str):
    try:
        response = table.get_item(
            Key={'id': id}
        )
        
        if 'Item' not in response:
            raise HTTPException(status_code=404, detail="Product not found")
        
        item = response['Item']
        
        if item.get('requestid') != requestid or item.get('uuid') != uuid:
            raise HTTPException(status_code=404, detail="Product not found")
        
        return ProductResponse(
            id=item['id'],
            name=item['name'],
            price=item['price']
        )
    
    except ClientError as e:
        raise HTTPException(status_code=500, detail=f"DynamoDB error: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
