from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import json
try:
	from jose import jwt, JWTError  # python-jose
except Exception:  # fallback to PyJWT
	import jwt  # type: ignore
	class JWTError(Exception):
		pass
import asyncio
from datetime import datetime, timedelta
import sqlite3
from pathlib import Path
import uvicorn

# Import from existing restaurant_billing modules
import sys
sys.path.append(str(Path(__file__).parent.parent))
from restaurant_billing.db import get_conn, list_menu_items, create_order, get_order_by_invoice, list_open_orders, mark_order_paid
from restaurant_billing.auth import get_user, verify_password, user_can
from restaurant_billing.config import CONFIG

app = FastAPI(title="HUNGER Restaurant Mobile API", version="1.0.0")

# CORS for mobile app
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure properly for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# JWT Configuration
SECRET_KEY = "hunger_restaurant_secret_key_2024"  # Use environment variable in production
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 480  # 8 hours

security = HTTPBearer()

# WebSocket connection manager
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []
        self.user_connections: Dict[str, WebSocket] = {}

    async def connect(self, websocket: WebSocket, user_id: str):
        await websocket.accept()
        self.active_connections.append(websocket)
        self.user_connections[user_id] = websocket

    def disconnect(self, websocket: WebSocket, user_id: str):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
        if user_id in self.user_connections:
            del self.user_connections[user_id]

    async def send_personal_message(self, message: str, user_id: str):
        if user_id in self.user_connections:
            await self.user_connections[user_id].send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            try:
                await connection.send_text(message)
            except:
                pass

manager = ConnectionManager()

# Pydantic models
class LoginRequest(BaseModel):
    username: str
    password: str

class OrderItem(BaseModel):
    id: int
    name: str
    rate: float
    gst_slab: float
    hsn_code: str
    quantity: int

class CreateOrderRequest(BaseModel):
    table_number: int
    customer_name: Optional[str] = None
    customer_gstin: Optional[str] = None
    place_of_supply: Optional[str] = None
    items: List[OrderItem]

class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    user: Dict[str, Any]

class MenuUpsert(BaseModel):
	name: str
	price: float
	category: str
	gst_slab: float
	hsn_code: str
	food_type: str

# JWT Functions
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

# API Endpoints
@app.post("/api/auth/login", response_model=TokenResponse)
async def login(request: LoginRequest):
    user = get_user(request.username)
    if not user or not verify_password(request.username, request.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": request.username, "role": user["role"]}, 
        expires_delta=access_token_expires
    )
    
    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        user={
            "username": user["username"],
            "full_name": user["full_name"],
            "role": user["role"]
        }
    )

@app.get("/api/menu")
async def get_menu(token_data: dict = Depends(verify_token)):
	return list_menu_items()

@app.post("/api/menu")
async def create_menu_item(req: MenuUpsert, token_data: dict = Depends(verify_token)):
	if token_data.get("role") not in ("ADMIN", "SUPER_ADMIN"):
		raise HTTPException(status_code=403, detail="Insufficient permissions")
	with get_conn() as conn:
		cur = conn.execute(
			"""
			INSERT INTO MenuItems(name, price, category, gst_slab, hsn_code, food_type)
			VALUES(?,?,?,?,?,?)
			""",
			(req.name, req.price, req.category, req.gst_slab, req.hsn_code, req.food_type)
		)
		item_id = cur.lastrowid
	await manager.broadcast(json.dumps({"type": "menu_updated", "action": "create", "id": item_id}))
	return {"id": item_id}

@app.put("/api/menu/{item_id}")
async def update_menu_item(item_id: int, req: MenuUpsert, token_data: dict = Depends(verify_token)):
	if token_data.get("role") not in ("ADMIN", "SUPER_ADMIN"):
		raise HTTPException(status_code=403, detail="Insufficient permissions")
	with get_conn() as conn:
		cur = conn.execute(
			"""
			UPDATE MenuItems SET name=?, price=?, category=?, gst_slab=?, hsn_code=?, food_type=?
			WHERE id=?
			""",
			(req.name, req.price, req.category, req.gst_slab, req.hsn_code, req.food_type, item_id)
		)
		if cur.rowcount == 0:
			raise HTTPException(status_code=404, detail="Menu item not found")
	await manager.broadcast(json.dumps({"type": "menu_updated", "action": "update", "id": item_id}))
	return {"ok": True}

@app.delete("/api/menu/{item_id}")
async def delete_menu_item(item_id: int, token_data: dict = Depends(verify_token)):
	if token_data.get("role") not in ("ADMIN", "SUPER_ADMIN"):
		raise HTTPException(status_code=403, detail="Insufficient permissions")
	with get_conn() as conn:
		cur = conn.execute("DELETE FROM MenuItems WHERE id=?", (item_id,))
		if cur.rowcount == 0:
			raise HTTPException(status_code=404, detail="Menu item not found")
	await manager.broadcast(json.dumps({"type": "menu_updated", "action": "delete", "id": item_id}))
	return {"ok": True}

@app.get("/api/orders/open")
async def get_open_orders(token_data: dict = Depends(verify_token)):
    return list_open_orders()

@app.post("/api/orders")
async def create_new_order(request: CreateOrderRequest, token_data: dict = Depends(verify_token)):
    # Calculate totals (simplified - would need proper GST calculation)
    subtotal = sum(item.rate * item.quantity for item in request.items)
    totals = {
        "subtotal": subtotal,
        "service_charge": 0.0,
        "cgst": 0.0,
        "sgst": 0.0,
        "igst": 0.0,
        "total": subtotal,
        "hsn_breakdown": {}
    }
    
    # Convert to dict format expected by create_order
    items_dict = []
    for item in request.items:
        items_dict.append({
            "id": item.id,
            "name": item.name,
            "rate": item.rate,
            "gst_slab": item.gst_slab,
            "hsn_code": item.hsn_code,
            "quantity": item.quantity
        })
    
    invoice_number = create_order(
        table_number=request.table_number,
        customer_name=request.customer_name,
        customer_gstin=request.customer_gstin,
        place_of_supply=request.place_of_supply,
        totals=totals,
        items=items_dict
    )
    
    # Broadcast order creation
    await manager.broadcast(json.dumps({
        "type": "order_created",
        "invoice_number": invoice_number,
        "table_number": request.table_number,
        "timestamp": datetime.now().isoformat()
    }))
    
    return {"invoice_number": invoice_number, "message": "Order created successfully"}

@app.post("/api/orders/{invoice_number}/paid")
async def mark_order_as_paid(invoice_number: str, token_data: dict = Depends(verify_token)):
    if not user_can({"role": token_data["role"]}, "checkout_bill"):
        raise HTTPException(status_code=403, detail="Insufficient permissions")
    
    success = mark_order_paid(invoice_number)
    if not success:
        raise HTTPException(status_code=404, detail="Order not found")
    
    # Broadcast payment
    await manager.broadcast(json.dumps({
        "type": "order_paid",
        "invoice_number": invoice_number,
        "timestamp": datetime.now().isoformat()
    }))
    
    return {"message": "Order marked as paid"}

@app.get("/api/orders/{invoice_number}")
async def get_order_details(invoice_number: str, token_data: dict = Depends(verify_token)):
    if not user_can({"role": token_data["role"]}, "lookup_bill"):
        raise HTTPException(status_code=403, detail="Insufficient permissions")
    
    order = get_order_by_invoice(invoice_number)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    return order

# WebSocket endpoint
@app.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: str):
    await manager.connect(websocket, user_id)
    try:
        while True:
            # Keep connection alive
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket, user_id)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
