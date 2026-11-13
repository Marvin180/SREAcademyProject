from fastapi import FastAPI

import time
import random

app = FastAPI()


@app.get("/")
async def root():
    random_seconds = random.randrange(0, 2)
    time.sleep(random_seconds)
    return {"message": "Hello World"}

@app.get("/get-orders")
def get_orders():
    random_seconds = random.randrange(0, 5)
    time.sleep(random_seconds)

    list_of_orders = {
        "ORD-100234": {
            "customer": "Emily Carter",
            "email": "emily.carter@example.com",
            "status": "Shipped",
            "order_date": "2026-11-01T09:15:42Z",
            "items": [
                {"sku": "SKU-1001", "name": "Wireless Mouse", "quantity": 1, "unit_price": 24.99},
                {"sku": "SKU-2040", "name": "USB-C Cable 2m", "quantity": 2, "unit_price": 9.50},
            ],
            "total": 43.99,
            "currency": "USD",
            "shipping_address": "123 Maple St, Austin, TX 78701, US",
            "payment_method": "Credit Card",
        },
        "ORD-100235": {
            "customer": "Michael Johnson",
            "email": "m.johnson@example.com",
            "status": "Processing",
            "order_date": "2026-11-02T14:03:10Z",
            "items": [
                {"sku": "SKU-3302", "name": "Mechanical Keyboard", "quantity": 1, "unit_price": 89.00},
                {"sku": "SKU-1001", "name": "Wireless Mouse", "quantity": 1, "unit_price": 24.99},
                {"sku": "SKU-4410", "name": "Monitor Stand", "quantity": 1, "unit_price": 34.50},
            ],
            "total": 148.49,
            "currency": "USD",
            "shipping_address": "45 Oak Ave, Denver, CO 80203, US",
            "payment_method": "PayPal",
        },
        "ORD-100236": {
            "customer": "Sofia Martinez",
            "email": "sofia.martinez@example.com",
            "status": "Delivered",
            "order_date": "2026-10-28T18:47:29Z",
            "items": [
                {"sku": "SKU-5120", "name": "Laptop Backpack", "quantity": 1, "unit_price": 59.90},
            ],
            "total": 59.90,
            "currency": "USD",
            "shipping_address": "78 Pine Rd, Miami, FL 33101, US",
            "payment_method": "Credit Card",
        },
    }

    return list_of_orders

@app.get("/get-customers")
def get_customers():
    random_seconds = random.randrange(0, 5)
    time.sleep(random_seconds)

    list_of_customers = {
        "CUST-5001": {
            "name": "Emily Carter",
            "email": "emily.carter@example.com",
            "phone": "+1-512-555-0142",
            "address": "123 Maple St, Austin, TX 78701, US",
        },
        "CUST-5002": {
            "name": "Michael Johnson",
            "email": "m.johnson@example.com",
            "phone": "+1-303-555-0178",
            "address": "45 Oak Ave, Denver, CO 80203, US",
        },
        "CUST-5003": {
            "name": "Sofia Martinez",
            "email": "sofia.martinez@example.com",
            "phone": "+1-305-555-0119",
            "address": "78 Pine Rd, Miami, FL 33101, US",
        },
    }

    return list_of_customers

@app.get("/get-customers/{customer}")
def get_customer(customer):
    list_of_customers = {
        "CUST-5001": {
            "name": "Emily Carter",
            "email": "emily.carter@example.com",
            "phone": "+1-512-555-0142",
            "address": "123 Maple St, Austin, TX 78701, US",
        },
        "CUST-5002": {
            "name": "Michael Johnson",
            "email": "m.johnson@example.com",
            "phone": "+1-303-555-0178",
            "address": "45 Oak Ave, Denver, CO 80203, US",
        },
        "CUST-5003": {
            "name": "Sofia Martinez",
            "email": "sofia.martinez@example.com",
            "phone": "+1-305-555-0119",
            "address": "78 Pine Rd, Miami, FL 33101, US",
        },
    }

    return list_of_customers[customer]


@app.post("/add-id/{id}")
def add_id(id):
    # Need to do a curl post: curl -X POST http://127.0.0.1:8000/add-id/300
    customer = {
        "CUST-5001": {
            "name": "Emily Carter",
            "email": "emily.carter@example.com",
            "phone": "+1-512-555-0142",
            "address": "123 Maple St, Austin, TX 78701, US",
            "id": ""
        }
    }

    customer["CUST-5001"]["id"] = id
    return customer



