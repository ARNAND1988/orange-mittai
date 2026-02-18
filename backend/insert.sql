BEGIN;

-- =====================================================
-- USERS
-- =====================================================

INSERT INTO users (email, first_name, last_name, phone, hashed_password, is_admin)
VALUES
    ('admin@test.com', 'Admin', 'User', '+31600000000', '$5$rounds=535000$EweMJEiZa3JJvnMo$ViGwrbO82JPLVyEf6q7jyRfXJrTmK1wShSNQhRYfSg0', true),
    ('customer1@test.com', 'Jan', 'de Vries', '+31612345678', '$5$rounds=535000$ewpTRPqkX8bt6QCP$oHjyjmSapUxSGsnKaln9Gt7XVbglaKpEb/aRiNNs1NB', false),
    ('customer2@test.com', 'Sanne', 'Jansen', '+31687654321', '$5$rounds=535000$TsxFyVXPkWRU10a7$Wayg4TcmN3kZt.8mkwHtQJpVnr72VSE2DtRy5f4vgd1', false)
    ON CONFLICT (email) DO NOTHING;

-- =====================================================
-- USER ADDRESSES (NL 🇳🇱)
-- =====================================================

INSERT INTO user_addresses
(user_id, label, name, phone, house_number, line1, line2, city, state, postal_code, country, is_default)
VALUES
    (
        (SELECT id FROM users WHERE email='customer1@test.com'),
        'Home', 'Jan de Vries', '+31612345678',
        '12', 'Prinsengracht', '3rd Floor',
        'Amsterdam', 'Noord-Holland', '1015 AB', 'Netherlands', true
    ),
    (
        (SELECT id FROM users WHERE email='customer1@test.com'),
        'Office', 'Jan de Vries', '+31612345678',
        '221', 'Herengracht', NULL,
        'Amsterdam', 'Noord-Holland', '1016 BN', 'Netherlands', false
    ),
    (
        (SELECT id FROM users WHERE email='customer2@test.com'),
        'Home', 'Sanne Jansen', '+31687654321',
        '45', 'Coolsingel', 'Apartment 5B',
        'Rotterdam', 'Zuid-Holland', '3012 AD', 'Netherlands', true
    ),
    (
        (SELECT id FROM users WHERE email='customer2@test.com'),
        'Other', 'Sanne Jansen', '+31687654321',
        '88', 'Oudegracht', NULL,
        'Utrecht', 'Utrecht', '3511 AR', 'Netherlands', false
    );

-- =====================================================
-- CATEGORY TAGS
-- =====================================================

INSERT INTO tags (name, slug, type, is_active)
VALUES
    ('Chocolate', 'chocolate', 'CATEGORY', true),
    ('Candy', 'candy', 'CATEGORY', true),
    ('Gummies', 'gummies', 'CATEGORY', true),
    ('Biscuits', 'biscuits', 'CATEGORY', true),
    ('Snacks', 'snacks', 'CATEGORY', true),
    ('Bakery', 'bakery', 'CATEGORY', true),
    ('Beverages', 'beverages', 'CATEGORY', true)
    ON CONFLICT (slug) DO NOTHING;

-- =====================================================
-- SUBCATEGORY TAGS
-- =====================================================

INSERT INTO tags (name, slug, type, parent_id, is_active)
VALUES
    (
        'Dark Chocolate', 'dark-chocolate', 'SUBCATEGORY',
        (SELECT id FROM tags WHERE slug='chocolate'), true
    ),
    (
        'Milk Chocolate', 'milk-chocolate', 'SUBCATEGORY',
        (SELECT id FROM tags WHERE slug='chocolate'), true
    ),
    (
        'Hard Candy', 'hard-candy', 'SUBCATEGORY',
        (SELECT id FROM tags WHERE slug='candy'), true
    ),
    (
        'Soft Candy', 'soft-candy', 'SUBCATEGORY',
        (SELECT id FROM tags WHERE slug='candy'), true
    )
    ON CONFLICT (slug) DO NOTHING;

-- =====================================================
-- PROMOTION / LABEL TAGS
-- =====================================================

INSERT INTO tags (name, slug, type, is_active)
VALUES
    ('Limited Offer', 'limited-offer', 'PROMOTION', true),
    ('Discounted', 'discounted', 'PROMOTION', true),
    ('New Arrival', 'new-arrival', 'LABEL', true),
    ('Best Seller', 'best-seller', 'LABEL', true)
    ON CONFLICT (slug) DO NOTHING;

-- =====================================================
-- PRODUCTS
-- =====================================================

INSERT INTO products (name, description, image, price, stock, is_active)
VALUES
    ('Dark Chocolate Item 1', 'Tasty dark chocolate product', '/images/product1.png', 5.99, 120, true),
    ('Dark Chocolate Item 2', 'Tasty dark chocolate product', '/images/product2.png', 6.49, 80, true),
    ('Milk Chocolate Item 1', 'Creamy milk chocolate', '/images/product3.png', 4.99, 150, true),
    ('Hard Candy Item 1', 'Classic hard candy', '/images/product1.png', 2.99, 300, true),
    ('Soft Candy Item 1', 'Chewy soft candy', '/images/product2.png', 3.49, 200, true);

-- =====================================================
-- PRODUCT ↔ TAG MAPPING
-- =====================================================

INSERT INTO product_tags (product_id, tag_id)
VALUES
    (
        (SELECT id FROM products WHERE name='Dark Chocolate Item 1'),
        (SELECT id FROM tags WHERE slug='dark-chocolate')
    ),
    (
        (SELECT id FROM products WHERE name='Milk Chocolate Item 1'),
        (SELECT id FROM tags WHERE slug='milk-chocolate')
    ),
    (
        (SELECT id FROM products WHERE name='Hard Candy Item 1'),
        (SELECT id FROM tags WHERE slug='hard-candy')
    ),
    (
        (SELECT id FROM products WHERE name='Soft Candy Item 1'),
        (SELECT id FROM tags WHERE slug='soft-candy')
    );

-- =====================================================
-- SAMPLE ORDERS
-- =====================================================

INSERT INTO orders (order_id, user_id, total_amount, status, payment_method, created_at)
VALUES
    (
        'ORD-000001',
        (SELECT id FROM users WHERE email='customer1@test.com'),
        18.47,
        'PROCESSING',
        'CARD',
        NOW()
    ),
    (
        'ORD-000002',
        (SELECT id FROM users WHERE email='customer2@test.com'),
        9.98,
        'COMPLETED',
        'CARD',
        NOW()
    )
    ON CONFLICT (order_id) DO NOTHING;

-- =====================================================
-- ORDER ITEMS
-- =====================================================

INSERT INTO order_items (order_id, product_id, price, quantity)
VALUES
    (
        (SELECT id FROM orders WHERE order_id='ORD-000001'),
        (SELECT id FROM products WHERE name='Dark Chocolate Item 1'),
        5.99,
        2
    ),
    (
        (SELECT id FROM orders WHERE order_id='ORD-000001'),
        (SELECT id FROM products WHERE name='Milk Chocolate Item 1'),
        4.99,
        1
    ),
    (
        (SELECT id FROM orders WHERE order_id='ORD-000002'),
        (SELECT id FROM products WHERE name='Soft Candy Item 1'),
        3.49,
        2
    );

COMMIT;
