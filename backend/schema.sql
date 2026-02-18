-- =====================================================
-- USERS
-- =====================================================

CREATE TABLE users (
                       id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
                       email VARCHAR NOT NULL,
                       hashed_password VARCHAR NOT NULL,
                       first_name VARCHAR,
                       last_name VARCHAR,
                       phone VARCHAR,
                       is_admin BOOLEAN
);

CREATE UNIQUE INDEX ix_users_email ON users (email);


-- =====================================================
-- TAGS
-- =====================================================

CREATE TABLE tags (
                      id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
                      name VARCHAR NOT NULL,
                      slug VARCHAR NOT NULL,
                      type VARCHAR NOT NULL,
                      parent_id INTEGER,
                      is_active BOOLEAN NOT NULL,
                      CONSTRAINT fk_tags_parent
                          FOREIGN KEY (parent_id) REFERENCES tags (id)
);

CREATE UNIQUE INDEX ix_tags_slug ON tags (slug);


-- =====================================================
-- PRODUCTS
-- =====================================================

CREATE TABLE products (
                          id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
                          name VARCHAR NOT NULL,
                          description VARCHAR,
                          image VARCHAR,
                          price FLOAT NOT NULL,
                          stock INTEGER,
                          is_active BOOLEAN NOT NULL
);

CREATE INDEX ix_products_name ON products (name);


-- =====================================================
-- PASSWORD RESETS
-- =====================================================

CREATE TABLE password_resets (
                                 id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
                                 user_id INTEGER NOT NULL,
                                 otp VARCHAR NOT NULL,
                                 channel VARCHAR NOT NULL,
                                 expires_at TIMESTAMPTZ NOT NULL,
                                 is_used BOOLEAN,
                                 created_at TIMESTAMPTZ DEFAULT NOW(),
                                 CONSTRAINT fk_password_resets_user
                                     FOREIGN KEY (user_id) REFERENCES users (id)
);


-- =====================================================
-- USER ADDRESSES
-- =====================================================

CREATE TABLE user_addresses (
                                id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
                                user_id INTEGER NOT NULL,
                                label VARCHAR,
                                name VARCHAR NOT NULL,
                                phone VARCHAR NOT NULL,
                                house_number VARCHAR NOT NULL,
                                line1 VARCHAR NOT NULL,
                                line2 VARCHAR,
                                city VARCHAR NOT NULL,
                                state VARCHAR NOT NULL,
                                postal_code VARCHAR NOT NULL,
                                country VARCHAR NOT NULL,
                                is_default BOOLEAN,
                                created_at TIMESTAMPTZ DEFAULT NOW(),
                                CONSTRAINT fk_user_addresses_user
                                    FOREIGN KEY (user_id) REFERENCES users (id)
);

CREATE INDEX ix_user_addresses_user_id ON user_addresses (user_id);


-- =====================================================
-- PRODUCT TAGS (M2M)
-- =====================================================

CREATE TABLE product_tags (
                              product_id INTEGER NOT NULL,
                              tag_id INTEGER NOT NULL,
                              PRIMARY KEY (product_id, tag_id),
                              CONSTRAINT fk_product_tags_product
                                  FOREIGN KEY (product_id) REFERENCES products (id),
                              CONSTRAINT fk_product_tags_tag
                                  FOREIGN KEY (tag_id) REFERENCES tags (id)
);


-- =====================================================
-- CART ITEMS
-- =====================================================

CREATE TABLE cart_items (
                            id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
                            user_id INTEGER NOT NULL,
                            product_id INTEGER NOT NULL,
                            quantity INTEGER,
                            CONSTRAINT fk_cart_items_user
                                FOREIGN KEY (user_id) REFERENCES users (id),
                            CONSTRAINT fk_cart_items_product
                                FOREIGN KEY (product_id) REFERENCES products (id)
);


-- =====================================================
-- ORDERS
-- =====================================================

CREATE TABLE orders (
                        id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
                        order_id VARCHAR(30),
                        user_id INTEGER,
                        total_amount FLOAT NOT NULL,
                        status VARCHAR(15),
                        payment_method VARCHAR,
                        created_at TIMESTAMPTZ,
                        CONSTRAINT fk_orders_user
                            FOREIGN KEY (user_id) REFERENCES users (id)
);

CREATE UNIQUE INDEX ix_orders_order_id ON orders (order_id);
CREATE INDEX ix_orders_status ON orders (status);
CREATE INDEX ix_orders_user_id ON orders (user_id);


-- =====================================================
-- ORDER ADDRESSES
-- =====================================================

CREATE TABLE order_addresses (
                                 id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
                                 order_id INTEGER NOT NULL UNIQUE,
                                 user_id INTEGER NOT NULL,
                                 name VARCHAR NOT NULL,
                                 phone VARCHAR NOT NULL,
                                 house_number VARCHAR NOT NULL,
                                 line1 VARCHAR NOT NULL,
                                 line2 VARCHAR,
                                 city VARCHAR NOT NULL,
                                 state VARCHAR NOT NULL,
                                 postal_code VARCHAR NOT NULL,
                                 country VARCHAR NOT NULL,
                                 created_at TIMESTAMPTZ DEFAULT NOW(),
                                 CONSTRAINT fk_order_addresses_order
                                     FOREIGN KEY (order_id) REFERENCES orders (id),
                                 CONSTRAINT fk_order_addresses_user
                                     FOREIGN KEY (user_id) REFERENCES users (id)
);


-- =====================================================
-- ORDER ITEMS
-- =====================================================

CREATE TABLE order_items (
                             id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
                             order_id INTEGER,
                             product_id INTEGER,
                             price FLOAT NOT NULL,
                             quantity INTEGER NOT NULL,
                             CONSTRAINT fk_order_items_order
                                 FOREIGN KEY (order_id) REFERENCES orders (id) ON DELETE CASCADE,
                             CONSTRAINT fk_order_items_product
                                 FOREIGN KEY (product_id) REFERENCES products (id)
);
