import pytest
from fastapi.testclient import TestClient
from shop_backend import app, CartItem, OrderItem, Order

client = TestClient(app)

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_get_products():
    response = client.get("/products")
    assert response.status_code == 200
    assert len(response.json()) == 4

def test_get_products_with_category_filter():
    response = client.get("/products?category=Movies")
    assert response.status_code == 200
    products = response.json()
    assert len(products) == 2
    assert all(product['category'] == "Movies" for product in products)

def test_add_to_cart():
    response = client.post("/cart", json={"product_id": 1, "quantity": 1})
    assert response.status_code == 200
    assert response.json() == {"message": "Item added to cart"}

def test_add_non_existing_product_to_cart():
    response = client.post("/cart", json={"product_id": 99, "quantity": 1})
    assert response.status_code == 404
    assert response.json() == {"detail": "Product not found"}

def test_view_cart():
    client.post("/cart", json={"product_id": 1, "quantity": 1})
    client.post("/cart", json={"product_id": 2, "quantity": 2})
    
    response = client.get("/cart")
    assert response.status_code == 200
    cart_items = response.json()
    assert len(cart_items) == 2

def test_checkout():
    client.post("/cart", json={"product_id": 1, "quantity": 1})
    client.post("/cart", json={"product_id": 2, "quantity": 2})
    
    order = {"items": [{"product_id": 1, "quantity": 1}, {"product_id": 2, "quantity": 2}]}
    response = client.post("/checkout", json=order)
    assert response.status_code == 200
    assert response.json() == {"message": "Order successfully placed"}

def test_checkout_insufficient_quantity():
    client.post("/cart", json={"product_id": 1, "quantity": 1})
    
    order = {"items": [{"product_id": 1, "quantity": 2}]}
    response = client.post("/checkout", json=order)
    assert response.status_code == 400
    assert response.json() == {"detail": "Insufficient quantity for product 1"}

def test_checkout_product_not_in_cart():
    order = {"items": [{"product_id": 1, "quantity": 1}]}
    response = client.post("/checkout", json=order)
    assert response.status_code == 400
    assert response.json() == {"detail": "Product 1 not in cart"}