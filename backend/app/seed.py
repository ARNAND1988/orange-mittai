# ✅ MUST BE FIRST
import app.models

from sqlalchemy.orm import Session
import random

from app.database import SessionLocal, Base, engine
from app.models.user import User
from app.models.product import Product, Tag
from app.models.order import Order
from app.models.order_item import OrderItem
from app.schemas.order_status import OrderStatus
from app.utils.security import hash_password
from app.utils.order_id import generate_order_id

# ========================
# Setup
# ========================
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)
db: Session = SessionLocal()

# ========================
# Users (GDPR-safe)
# ========================
users = [
    User(
        email="admin@test.com",
        first_name="Admin",
        last_name="User",
        phone="9999999999",
        hashed_password=hash_password("admin123"),
        is_admin=True,
    ),
    User(
        email="customer1@test.com",
        first_name="Customer",
        last_name="One",
        phone="9000000001",
        hashed_password=hash_password("customer123"),
    ),
    User(
        email="customer2@test.com",
        first_name="Customer",
        last_name="Two",
        phone="9000000002",
        hashed_password=hash_password("customer123"),
    ),
]


db.add_all(users)
db.commit()

# ========================
# Category Tags
# ========================
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

# ========================
# Subcategory Tags
# ========================
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
    "Fruit Gummies": Tag(
        name="Fruit Gummies",
        slug="fruit-gummies",
        type="SUBCATEGORY",
        parent=category_tags["Gummies"],
    ),
    "Sour Gummies": Tag(
        name="Sour Gummies",
        slug="sour-gummies",
        type="SUBCATEGORY",
        parent=category_tags["Gummies"],
    ),
    "Cream Biscuits": Tag(
        name="Cream Biscuits",
        slug="cream-biscuits",
        type="SUBCATEGORY",
        parent=category_tags["Biscuits"],
    ),
    "Digestive Biscuits": Tag(
        name="Digestive Biscuits",
        slug="digestive-biscuits",
        type="SUBCATEGORY",
        parent=category_tags["Biscuits"],
    ),
    "Chips": Tag(
        name="Chips",
        slug="chips",
        type="SUBCATEGORY",
        parent=category_tags["Snacks"],
    ),
    "Namkeen": Tag(
        name="Namkeen",
        slug="namkeen",
        type="SUBCATEGORY",
        parent=category_tags["Snacks"],
    ),
    "Cakes": Tag(
        name="Cakes",
        slug="cakes",
        type="SUBCATEGORY",
        parent=category_tags["Bakery"],
    ),
    "Cookies": Tag(
        name="Cookies",
        slug="cookies",
        type="SUBCATEGORY",
        parent=category_tags["Bakery"],
    ),
    "Soft Drinks": Tag(
        name="Soft Drinks",
        slug="soft-drinks",
        type="SUBCATEGORY",
        parent=category_tags["Beverages"],
    ),
    "Juices": Tag(
        name="Juices",
        slug="juices",
        type="SUBCATEGORY",
        parent=category_tags["Beverages"],
    ),
}


db.add_all(subcategory_tags.values())
db.commit()

# ========================
# Promotion / Label Tags (⬅️ EXPANDED)
# ========================
promo_tags = [
    Tag(name="Limited Offer", slug="limited-offer", type="PROMOTION"),
    Tag(name="Discounted", slug="discounted", type="PROMOTION"),
    Tag(name="New Arrival", slug="new-arrival", type="LABEL"),
    Tag(name="Best Seller", slug="best-seller", type="LABEL"),
    Tag(name="Trending", slug="trending", type="LABEL"),
    Tag(name="Seasonal Special", slug="seasonal-special", type="LABEL"),
]


db.add_all(promo_tags)
db.commit()

# ========================
# Products (⬅️ MORE VARIETY)
# ========================
product_names = {
    "Dark Chocolate": [
        "70% Dark Bar", "85% Dark Bar", "Dark Cocoa Bite",
        "Midnight Truffle", "Intense Cocoa Square"
    ],
    "Milk Chocolate": [
        "Milk Choco Bar", "Creamy Cocoa", "Caramel Milk",
        "Hazelnut Milk Bar", "Almond Milk Chocolate"
    ],
    "Hard Candy": [
        "Lemon Drops", "Mint Rocks", "Cola Candy",
        "Orange Lozenges", "Ginger Candy"
    ],
    "Soft Candy": [
        "Fruit Chews", "Soft Toffee", "Berry Bites",
        "Caramel Cubes", "Mango Chews"
    ],
    "Fruit Gummies": [
        "Gummy Bears", "Fruit Rings", "Gummy Worms",
        "Peach Gummies", "Strawberry Gummies"
    ],
    "Sour Gummies": [
        "Sour Bears", "Tangy Worms", "Sour Mix",
        "Sour Cola Bottles", "Sour Apple Rings"
    ],
    "Cream Biscuits": [
        "Vanilla Cream Biscuit", "Chocolate Cream Biscuit",
        "Strawberry Cream Biscuit"
    ],
    "Digestive Biscuits": [
        "Oat Digestive", "Wheat Digestive", "Multigrain Digestive"
    ],
    "Chips": [
        "Classic Chips", "Masala Chips", "Salted Chips",
        "Chili Chips", "Sour Cream Chips"
    ],
    "Namkeen": [
        "Mixture", "Spicy Sev", "Salted Peanuts",
        "Bhujia", "Chana Dal"
    ],
    "Cakes": [
        "Chocolate Cake Slice", "Vanilla Cake Slice",
        "Red Velvet Slice", "Butterscotch Slice"
    ],
    "Cookies": [
        "Butter Cookies", "Choco Chip Cookies",
        "Oat Cookies", "Almond Cookies"
    ],
    "Soft Drinks": [
        "Cola Drink", "Orange Soda",
        "Lemon Soda", "Ginger Ale"
    ],
    "Juices": [
        "Apple Juice", "Mango Juice",
        "Orange Juice", "Mixed Fruit Juice"
    ],
}

product_images = [
    "/images/product1.png",
    "/images/product2.png",
    "/images/product3.png",
    "/images/product4.png",
    "/images/product5.png",
]

products = []

# ⬅️ Increase volume: 20 products per subcategory
for subcat_name, subcat_tag in subcategory_tags.items():
    category_tag = subcat_tag.parent

    for i in range(20):
        base = random.choice(product_names[subcat_name])

        product = Product(
            name=f"{base} {i + 1}",
            description=f"Tasty {base.lower()} made with quality ingredients.",
            image=random.choice(product_images),
            price=round(random.uniform(1.5, 25.0), 2),
            stock=random.randint(0, 300),
            is_active=random.random() > 0.1,
        )

        # Core classification tags
        product.tags.extend([category_tag, subcat_tag])

        # ⬅️ Attach 1–3 random promo/label tags
        for tag in random.sample(promo_tags, random.randint(0, 3)):
            product.tags.append(tag)

        products.append(product)

db.add_all(products)
db.commit()

# ========================
# Orders + Order Items
# ========================
customers = [u for u in users if not u.is_admin]
all_products = db.query(Product).all()

for customer in customers:
    for _ in range(5):  # ⬅️ More orders
        selected_products = random.sample(all_products, random.randint(2, 6))

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
            qty = random.randint(1, 4)
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

print("✅ Seeded rich dataset with more products, labels, and orders!")
