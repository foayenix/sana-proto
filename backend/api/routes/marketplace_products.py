"""
SANA Marketplace Products Routes
E-commerce & practitioner prescriptions
"""

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field
from typing import Optional, List, Dict
from datetime import datetime
import uuid

router = APIRouter()


# ============================================================================
# SCHEMAS
# ============================================================================

class Product(BaseModel):
    id: str
    name: str
    brand: str
    category: str
    description: str
    price: float
    currency: str = "GBP"
    image_url: Optional[str] = None
    shi_score: Optional[float] = None
    in_stock: bool = True
    supplier_id: str


class Supplier(BaseModel):
    id: str
    name: str
    type: str  # manufacturer, distributor, practitioner
    verified: bool
    product_count: int
    rating: float


class CartItem(BaseModel):
    product_id: str
    product_name: str
    quantity: int
    price: float
    subtotal: float


class Cart(BaseModel):
    user_id: str
    items: List[CartItem]
    subtotal: float
    shipping: float
    total: float


class Order(BaseModel):
    id: str
    user_id: str
    items: List[CartItem]
    total: float
    status: str
    created_at: datetime
    tracking_number: Optional[str] = None


class Prescription(BaseModel):
    id: str
    practitioner_id: str
    practitioner_name: str
    client_id: str
    items: List[Dict]
    notes: Optional[str] = None
    valid_until: datetime
    status: str  # pending, purchased, expired


class Commission(BaseModel):
    practitioner_id: str
    total_earned: float
    pending: float
    paid_out: float
    orders_count: int


# ============================================================================
# MOCK DATA
# ============================================================================

PRODUCTS = [
    {
        "id": "mp_001",
        "name": "Ashwagandha KSM-66 500mg (60 caps)",
        "brand": "Pure Encapsulations",
        "category": "Adaptogens",
        "description": "Clinically studied ashwagandha root extract for stress support",
        "price": 32.99,
        "currency": "GBP",
        "image_url": "https://example.com/ashwagandha.jpg",
        "shi_score": 82,
        "in_stock": True,
        "supplier_id": "sup_001"
    },
    {
        "id": "mp_002",
        "name": "Magnesium Glycinate 400mg (120 caps)",
        "brand": "Thorne",
        "category": "Minerals",
        "description": "Highly absorbable magnesium for relaxation and sleep",
        "price": 28.50,
        "currency": "GBP",
        "image_url": "https://example.com/magnesium.jpg",
        "shi_score": 88,
        "in_stock": True,
        "supplier_id": "sup_001"
    },
    {
        "id": "mp_003",
        "name": "Omega-3 Fish Oil 1000mg (90 softgels)",
        "brand": "Nordic Naturals",
        "category": "Essential Fatty Acids",
        "description": "High-potency EPA/DHA for brain and heart health",
        "price": 34.99,
        "currency": "GBP",
        "image_url": "https://example.com/omega3.jpg",
        "shi_score": 85,
        "in_stock": True,
        "supplier_id": "sup_002"
    },
    {
        "id": "mp_004",
        "name": "Liver Support Formula",
        "brand": "Mediherb",
        "category": "Herbal Formulas",
        "description": "Professional-grade milk thistle and liver herbs",
        "price": 45.00,
        "currency": "GBP",
        "image_url": "https://example.com/liver.jpg",
        "shi_score": 79,
        "in_stock": True,
        "supplier_id": "sup_003"
    }
]

SUPPLIERS = [
    {"id": "sup_001", "name": "Practitioner Supplements UK", "type": "distributor", "verified": True, "product_count": 450, "rating": 4.8},
    {"id": "sup_002", "name": "Nordic Naturals Direct", "type": "manufacturer", "verified": True, "product_count": 85, "rating": 4.9},
    {"id": "sup_003", "name": "Professional Herb Supply", "type": "distributor", "verified": True, "product_count": 320, "rating": 4.7}
]

CARTS: Dict[str, Cart] = {}
PRESCRIPTIONS: Dict[str, Prescription] = {}


# ============================================================================
# ROUTES - PRODUCTS
# ============================================================================

@router.get("/products", response_model=List[Product])
async def browse_products(
    category: Optional[str] = None,
    brand: Optional[str] = None,
    min_shi_score: Optional[float] = None,
    search: Optional[str] = None,
    limit: int = Query(default=20, le=100)
):
    """
    Browse product catalog

    **Filters:**
    - Category (Adaptogens, Minerals, Herbs, etc.)
    - Brand
    - Minimum SHI score
    - Search by name
    """
    results = PRODUCTS.copy()

    if category:
        results = [p for p in results if p["category"].lower() == category.lower()]
    if brand:
        results = [p for p in results if brand.lower() in p["brand"].lower()]
    if min_shi_score:
        results = [p for p in results if p.get("shi_score", 0) >= min_shi_score]
    if search:
        results = [p for p in results if search.lower() in p["name"].lower()]

    return [Product(**p) for p in results[:limit]]


@router.get("/products/{product_id}", response_model=Product)
async def get_product(product_id: str):
    """
    Get product details
    """
    product = next((p for p in PRODUCTS if p["id"] == product_id), None)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return Product(**product)


@router.get("/suppliers", response_model=List[Supplier])
async def list_suppliers(type: Optional[str] = None):
    """
    List product suppliers

    **Types:**
    - manufacturer: Direct from brand
    - distributor: Authorized distributor
    - practitioner: Practitioner dispensary
    """
    results = SUPPLIERS
    if type:
        results = [s for s in results if s["type"] == type]
    return [Supplier(**s) for s in results]


@router.get("/suppliers/{supplier_id}/catalog")
async def get_supplier_catalog(supplier_id: str, limit: int = 50):
    """
    Get supplier's product catalog
    """
    products = [p for p in PRODUCTS if p["supplier_id"] == supplier_id]
    return {
        "supplier_id": supplier_id,
        "products": [Product(**p) for p in products[:limit]],
        "total": len(products)
    }


# ============================================================================
# ROUTES - CART
# ============================================================================

@router.get("/cart/{user_id}", response_model=Cart)
async def get_cart(user_id: str):
    """
    Get user's shopping cart
    """
    cart = CARTS.get(user_id)
    if not cart:
        return Cart(
            user_id=user_id,
            items=[],
            subtotal=0,
            shipping=0,
            total=0
        )
    return cart


@router.post("/cart/{user_id}/add")
async def add_to_cart(user_id: str, product_id: str, quantity: int = 1):
    """
    Add product to cart
    """
    product = next((p for p in PRODUCTS if p["id"] == product_id), None)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    cart = CARTS.get(user_id)
    if not cart:
        cart = Cart(user_id=user_id, items=[], subtotal=0, shipping=5.99, total=5.99)

    # Add or update item
    existing = next((i for i in cart.items if i.product_id == product_id), None)
    if existing:
        existing.quantity += quantity
        existing.subtotal = existing.quantity * existing.price
    else:
        cart.items.append(CartItem(
            product_id=product_id,
            product_name=product["name"],
            quantity=quantity,
            price=product["price"],
            subtotal=product["price"] * quantity
        ))

    cart.subtotal = sum(i.subtotal for i in cart.items)
    cart.total = cart.subtotal + cart.shipping

    CARTS[user_id] = cart
    return cart


@router.delete("/cart/{user_id}/item/{product_id}")
async def remove_from_cart(user_id: str, product_id: str):
    """
    Remove product from cart
    """
    cart = CARTS.get(user_id)
    if cart:
        cart.items = [i for i in cart.items if i.product_id != product_id]
        cart.subtotal = sum(i.subtotal for i in cart.items)
        cart.total = cart.subtotal + cart.shipping
        CARTS[user_id] = cart
    return {"removed": True}


# ============================================================================
# ROUTES - ORDERS
# ============================================================================

@router.post("/orders/{user_id}", response_model=Order)
async def create_order(
    user_id: str,
    shipping_address: Dict,
    payment_method_id: str
):
    """
    Create order from cart

    **Flow:**
    1. Validate cart
    2. Process payment
    3. Create order
    4. Clear cart
    5. Notify supplier
    """
    cart = CARTS.get(user_id)
    if not cart or not cart.items:
        raise HTTPException(status_code=400, detail="Cart is empty")

    order_id = f"ord_{uuid.uuid4().hex[:8]}"

    order = Order(
        id=order_id,
        user_id=user_id,
        items=cart.items,
        total=cart.total,
        status="confirmed",
        created_at=datetime.utcnow()
    )

    # Clear cart
    CARTS[user_id] = Cart(user_id=user_id, items=[], subtotal=0, shipping=0, total=0)

    return order


@router.get("/orders/{user_id}")
async def list_orders(user_id: str, limit: int = 20):
    """
    List user's orders
    """
    # Mock orders
    return {
        "user_id": user_id,
        "orders": [
            {
                "id": "ord_001",
                "total": 96.48,
                "status": "delivered",
                "created_at": "2024-06-10T10:30:00Z",
                "items_count": 3
            }
        ],
        "total": 5
    }


# ============================================================================
# ROUTES - PRESCRIPTIONS
# ============================================================================

@router.post("/prescriptions", response_model=Prescription)
async def create_prescription(
    practitioner_id: str,
    client_id: str,
    items: List[Dict],  # [{"product_id": "...", "quantity": 1, "instructions": "..."}]
    notes: Optional[str] = None,
    valid_days: int = 30
):
    """
    Practitioner creates prescription/recommendation

    **Features:**
    - Product recommendations with instructions
    - Optional notes
    - Expiration date
    - Client receives notification
    - Practitioner earns commission on purchase
    """
    rx_id = f"rx_{uuid.uuid4().hex[:8]}"

    prescription = Prescription(
        id=rx_id,
        practitioner_id=practitioner_id,
        practitioner_name="Dr. Emily Chen",
        client_id=client_id,
        items=items,
        notes=notes,
        valid_until=datetime(2024, 7, 30),
        status="pending"
    )

    PRESCRIPTIONS[rx_id] = prescription
    return prescription


@router.get("/prescriptions/{prescription_id}", response_model=Prescription)
async def get_prescription(prescription_id: str):
    """
    Get prescription details
    """
    rx = PRESCRIPTIONS.get(prescription_id)
    if not rx:
        raise HTTPException(status_code=404, detail="Prescription not found")
    return rx


@router.post("/prescriptions/{prescription_id}/purchase")
async def purchase_prescription(prescription_id: str, user_id: str):
    """
    Purchase prescribed items

    **Flow:**
    1. Validate prescription not expired
    2. Add items to cart
    3. Apply any discounts
    4. Process order
    5. Record commission for practitioner
    """
    rx = PRESCRIPTIONS.get(prescription_id)
    if not rx:
        raise HTTPException(status_code=404, detail="Prescription not found")

    if rx.status == "expired":
        raise HTTPException(status_code=400, detail="Prescription has expired")

    # Add items to cart
    for item in rx.items:
        await add_to_cart(user_id, item["product_id"], item.get("quantity", 1))

    rx.status = "purchased"
    PRESCRIPTIONS[prescription_id] = rx

    return {
        "prescription_id": prescription_id,
        "status": "added_to_cart",
        "message": "Items added to cart. Proceed to checkout."
    }


@router.get("/prescriptions/client/{client_id}")
async def list_client_prescriptions(client_id: str):
    """
    List prescriptions for a client
    """
    client_rx = [rx for rx in PRESCRIPTIONS.values() if rx.client_id == client_id]
    return {
        "client_id": client_id,
        "prescriptions": client_rx,
        "total": len(client_rx)
    }


# ============================================================================
# ROUTES - COMMISSIONS
# ============================================================================

@router.get("/commissions/{practitioner_id}", response_model=Commission)
async def get_commissions(practitioner_id: str):
    """
    Get practitioner's commission earnings

    **Commission Structure:**
    - 10-15% on recommended products
    - Higher rates for preferred suppliers
    - Monthly payouts via Stripe Connect
    """
    return Commission(
        practitioner_id=practitioner_id,
        total_earned=1245.50,
        pending=234.00,
        paid_out=1011.50,
        orders_count=78
    )


@router.post("/commissions/{practitioner_id}/payout")
async def request_commission_payout(practitioner_id: str, amount: Optional[float] = None):
    """
    Request commission payout
    """
    return {
        "practitioner_id": practitioner_id,
        "payout_id": f"po_{uuid.uuid4().hex[:8]}",
        "amount": amount or 234.00,
        "status": "processing",
        "estimated_arrival": "2024-07-05"
    }


@router.get("/commissions/{practitioner_id}/history")
async def get_commission_history(practitioner_id: str, limit: int = 20):
    """
    Get commission payment history
    """
    return {
        "practitioner_id": practitioner_id,
        "history": [
            {"date": "2024-06-01", "amount": 312.50, "orders": 24, "status": "paid"},
            {"date": "2024-05-01", "amount": 287.00, "orders": 21, "status": "paid"},
            {"date": "2024-04-01", "amount": 412.00, "orders": 33, "status": "paid"}
        ]
    }
