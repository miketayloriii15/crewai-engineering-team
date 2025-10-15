from typing import List, Dict, Optional
from pathlib import Path

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel

# ---------- MODELS ----------
class Product(BaseModel):
    id: int
    name: str
    category: str
    price: float
    in_stock: bool

class CartItem(BaseModel):
    product_id: int
    quantity: int

class ResponseMessage(BaseModel):
    message: str

class OrderItem(BaseModel):
    product_id: int
    quantity: int

class Order(BaseModel):
    items: List[OrderItem]

# ---------- SERVICE ----------
class ShopService:
    def __init__(self):
        self.catalog: List[Product] = self._load_catalog()
        self.cart: Dict[int, int] = {}

    def _load_catalog(self) -> List[Product]:
        return [
            Product(id=1, name="Inception", category="Movies", price=10.0, in_stock=True),
            Product(id=2, name="The Matrix", category="Movies", price=12.0, in_stock=True),
            Product(id=3, name="1984", category="Books", price=8.0, in_stock=True),
            Product(id=4, name="The Hobbit", category="Books", price=15.0, in_stock=True),
        ]

    def get_health(self) -> Dict[str, str]:
        return {"status": "healthy"}

    def get_products(self, category=None, q=None, ids=None) -> List[Product]:
        items = [p for p in self.catalog if p.in_stock]
        if category:
            items = [p for p in items if p.category.lower() == category.lower()]
        if q:
            q_lower = q.lower()
            items = [p for p in items if q_lower in p.name.lower()]
        if ids:
            id_set = set(ids)
            items = [p for p in items if p.id in id_set]
        return items

    def add_to_cart(self, item: CartItem) -> ResponseMessage:
        if item.product_id not in [p.id for p in self.catalog]:
            raise HTTPException(status_code=404, detail="Product not found")
        self.cart[item.product_id] = self.cart.get(item.product_id, 0) + item.quantity
        return ResponseMessage(message="Item added to cart")

    def view_cart(self) -> List[CartItem]:
        return [CartItem(product_id=i, quantity=q) for i, q in self.cart.items()]

    def checkout(self, order: Order) -> ResponseMessage:
        for item in order.items:
            if item.product_id not in self.cart:
                raise HTTPException(status_code=400, detail=f"Product {item.product_id} not in cart")
            if self.cart[item.product_id] < item.quantity:
                raise HTTPException(status_code=400, detail=f"Insufficient quantity for product {item.product_id}")
        for item in order.items:
            self.cart[item.product_id] -= item.quantity
            if self.cart[item.product_id] <= 0:
                del self.cart[item.product_id]
        return ResponseMessage(message="Order successfully placed")

# ---------- APP ----------
app = FastAPI(title="ShopBackend")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

service = ShopService()

FRONTEND_DIR = Path(__file__).resolve().parent / "frontend"

# Static assets (css/js) served at /assets
if FRONTEND_DIR.exists():
    app.mount("/assets", StaticFiles(directory=str(FRONTEND_DIR)), name="assets")

# Serve index.html at /
@app.get("/", include_in_schema=False)
def root():
    index_path = FRONTEND_DIR / "index.html"
    if not index_path.exists():
        raise HTTPException(status_code=500, detail=f"index.html not found at {index_path}")
    return FileResponse(index_path)

# ---------- API ROUTES ----------
@app.get("/health", response_model=Dict[str, str])
def health():
    return service.get_health()

@app.get("/products", response_model=List[Product])
def products(category: Optional[str] = None, q: Optional[str] = None,
             id: Optional[int] = None,
             ids: Optional[str] = Query(None, description="Comma-separated IDs")):
    ids_list = None
    if ids:
        ids_list = [int(x) for x in ids.split(",") if x.strip()]
    elif id is not None:
        ids_list = [id]
    return service.get_products(category, q, ids_list)

@app.post("/cart", response_model=ResponseMessage)
def add_cart(item: CartItem):
    return service.add_to_cart(item)

@app.get("/cart", response_model=List[CartItem])
def view_cart():
    return service.view_cart()

@app.post("/checkout", response_model=ResponseMessage)
def checkout(order: Order):
    return service.checkout(order)
