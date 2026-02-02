# =====================================================
# 🔥 FORCE MODEL REGISTRATION (CRITICAL)
# =====================================================

from app.models.user import User, PasswordReset
from app.models.address import UserAddress, OrderAddress
from app.models.product import Product, Tag
from app.models.cart import CartItem
from app.models.order import Order
from app.models.order_item import OrderItem

# =====================================================
# SAFE TO IMPORT SQLALCHEMY AFTER MODELS
# =====================================================

from sqlalchemy.orm import Session
import random

from app.database import SessionLocal, Base, engine
from app.schemas.order_status import OrderStatus
from app.utils.security import hash_password
from app.utils.order_id import generate_order_id

# =====================================================
# RESET DATABASE
# =====================================================

Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

db: Session = SessionLocal()

# =====================================================
# USERS
# =====================================================

users = [
    User(
        email="admin@test.com",
        first_name="Admin",
        last_name="User",
        phone="+31600000000",
        hashed_password=hash_password("admin123"),
        is_admin=True,
    ),
    User(
        email="customer1@test.com",
        first_name="Jan",
        last_name="de Vries",
        phone="+31612345678",
        hashed_password=hash_password("customer123"),
    ),
    User(
        email="customer2@test.com",
        first_name="Sanne",
        last_name="Jansen",
        phone="+31687654321",
        hashed_password=hash_password("customer123"),
    ),
]

db.add_all(users)
db.commit()

# =====================================================
# USER ADDRESSES — Netherlands 🇳🇱
# =====================================================

addresses = [
    UserAddress(
        user_id=users[1].id,
        label="Home",
        name="Jan de Vries",
        phone="+31612345678",
        house_number="12",
        line1="Prinsengracht",
        line2="3rd Floor",
        city="Amsterdam",
        state="Noord-Holland",
        postal_code="1015 AB",
        country="Netherlands",
        is_default=True,
    ),
    UserAddress(
        user_id=users[1].id,
        label="Office",
        name="Jan de Vries",
        phone="+31612345678",
        house_number="221",
        line1="Herengracht",
        line2=None,
        city="Amsterdam",
        state="Noord-Holland",
        postal_code="1016 BN",
        country="Netherlands",
        is_default=False,
    ),
    UserAddress(
        user_id=users[2].id,
        label="Home",
        name="Sanne Jansen",
        phone="+31687654321",
        house_number="45",
        line1="Coolsingel",
        line2="Apartment 5B",
        city="Rotterdam",
        state="Zuid-Holland",
        postal_code="3012 AD",
        country="Netherlands",
        is_default=True,
    ),
    UserAddress(
        user_id=users[2].id,
        label="Other",
        name="Sanne Jansen",
        phone="+31687654321",
        house_number="88",
        line1="Oudegracht",
        line2=None,
        city="Utrecht",
        state="Utrecht",
        postal_code="3511 AR",
        country="Netherlands",
        is_default=False,
    ),
]

db.add_all(addresses)
db.commit()

# =====================================================
# CATEGORY TAGS
# =====================================================

category_tags = {
    "Chocolate": Tag(name="Chocolate", slug="chocolate", type="CATEGORY"),
    "Candy": Tag(name="Candy", slug="candy", type="CATEGORY"),
    "Gummies": Tag(name="Gummies", slug="gummies", type="CATEGORY"),
    "Biscuits": Tag(name="Biscuits", slug="biscuits", type="CATEGORY"),
    "Snacks": Tag(name="Snacks", slug="snacks", type="CATEGORY"),
    "Bakery": Tag(name="Bakery", slug="bakery", type="CATEGORY"),
    "Beverages": Tag(name="Beverages", slug="beverages", type="CATEGORY"),
}

db.add_all(category_tags.values())
db.commit()

# =====================================================
# SUBCATEGORY TAGS
# =====================================================

subcategory_tags = {
    "Dark Chocolate": Tag(
        name="Dark Chocolate",
        slug="dark-chocolate",
        type="SUBCATEGORY",
        parent=category_tags["Chocolate"],
    ),
    "Milk Chocolate": Tag(
        name="Milk Chocolate",
        slug="milk-chocolate",
        type="SUBCATEGORY",
        parent=category_tags["Chocolate"],
    ),
    "Hard Candy": Tag(
        name="Hard Candy",
        slug="hard-candy",
        type="SUBCATEGORY",
        parent=category_tags["Candy"],
    ),
    "Soft Candy": Tag(
        name="Soft Candy",
        slug="soft-candy",
        type="SUBCATEGORY",
        parent=category_tags["Candy"],
    ),
}

db.add_all(subcategory_tags.values())
db.commit()

# =====================================================
# PROMOTION / LABEL TAGS
# =====================================================

promo_tags = [
    Tag(name="Limited Offer", slug="limited-offer", type="PROMOTION"),
    Tag(name="Discounted", slug="discounted", type="PROMOTION"),
    Tag(name="New Arrival", slug="new-arrival", type="LABEL"),
    Tag(name="Best Seller", slug="best-seller", type="LABEL"),
]

db.add_all(promo_tags)
db.commit()

# =====================================================
# PRODUCTS
# =====================================================

product_images = [
    "/images/product1.png",
    "/images/product2.png",
    "/images/product3.png",
]

products = []

for subcat_name, subcat_tag in subcategory_tags.items():
    category_tag = subcat_tag.parent

    for i in range(10):
        product = Product(
            name=f"{subcat_name} Item {i + 1}",
            description=f"Tasty {subcat_name.lower()} product",
            image=random.choice(product_images),
            price=round(random.uniform(2.0, 25.0), 2),
            stock=random.randint(0, 200),
            is_active=True,
        )

        product.tags.extend([category_tag, subcat_tag])
        product.tags.extend(random.sample(promo_tags, random.randint(0, 2)))

        products.append(product)

db.add_all(products)
db.commit()

# =====================================================
# ORDERS + ORDER ITEMS
# =====================================================

customers = [u for u in users if not u.is_admin]
all_products = db.query(Product).all()

for customer in customers:
    for _ in range(3):
        selected_products = random.sample(all_products, random.randint(2, 5))

        order = Order(
            user_id=customer.id,
            status=random.choice([
                OrderStatus.PROCESSING.value,
                OrderStatus.COMPLETED.value,
                OrderStatus.PAYMENT_PENDING.value,
            ]),
            total_amount=0,
        )

        db.add(order)
        db.flush()

        order.order_id = generate_order_id(order.id)

        total = 0
        for product in selected_products:
            qty = random.randint(1, 3)
            total += product.price * qty

            order.items.append(
                OrderItem(
                    product=product,
                    price=product.price,
                    quantity=qty,
                )
            )

        order.total_amount = round(total, 2)

db.commit()
db.close()

print("✅ Seed completed successfully (NL users, addresses, products, orders)")
