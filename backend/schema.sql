CREATE TABLE users (
	id INTEGER NOT NULL, 
	email VARCHAR NOT NULL, 
	hashed_password VARCHAR NOT NULL, 
	first_name VARCHAR, 
	last_name VARCHAR, 
	phone VARCHAR, 
	is_admin BOOLEAN, 
	PRIMARY KEY (id)
);
CREATE INDEX ix_users_id ON users (id);
CREATE UNIQUE INDEX ix_users_email ON users (email);
CREATE TABLE tags (
	id INTEGER NOT NULL, 
	name VARCHAR NOT NULL, 
	slug VARCHAR NOT NULL, 
	type VARCHAR NOT NULL, 
	parent_id INTEGER, 
	is_active BOOLEAN NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(parent_id) REFERENCES tags (id)
);
CREATE INDEX ix_tags_id ON tags (id);
CREATE UNIQUE INDEX ix_tags_slug ON tags (slug);
CREATE TABLE products (
	id INTEGER NOT NULL, 
	name VARCHAR NOT NULL, 
	description VARCHAR, 
	image VARCHAR, 
	price FLOAT NOT NULL, 
	stock INTEGER, 
	is_active BOOLEAN NOT NULL, 
	PRIMARY KEY (id)
);
CREATE INDEX ix_products_id ON products (id);
CREATE INDEX ix_products_name ON products (name);
CREATE TABLE password_resets (
	id INTEGER NOT NULL, 
	user_id INTEGER NOT NULL, 
	otp VARCHAR NOT NULL, 
	channel VARCHAR NOT NULL, 
	expires_at DATETIME NOT NULL, 
	is_used BOOLEAN, 
	created_at DATETIME DEFAULT CURRENT_TIMESTAMP, 
	PRIMARY KEY (id), 
	FOREIGN KEY(user_id) REFERENCES users (id)
);
CREATE TABLE user_addresses (
	id INTEGER NOT NULL, 
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
	created_at DATETIME DEFAULT CURRENT_TIMESTAMP, 
	PRIMARY KEY (id), 
	FOREIGN KEY(user_id) REFERENCES users (id)
);
CREATE INDEX ix_user_addresses_id ON user_addresses (id);
CREATE TABLE product_tags (
	product_id INTEGER NOT NULL, 
	tag_id INTEGER NOT NULL, 
	PRIMARY KEY (product_id, tag_id), 
	FOREIGN KEY(product_id) REFERENCES products (id), 
	FOREIGN KEY(tag_id) REFERENCES tags (id)
);
CREATE TABLE cart_items (
	id INTEGER NOT NULL, 
	user_id INTEGER NOT NULL, 
	product_id INTEGER NOT NULL, 
	quantity INTEGER, 
	PRIMARY KEY (id), 
	FOREIGN KEY(user_id) REFERENCES users (id), 
	FOREIGN KEY(product_id) REFERENCES products (id)
);
CREATE TABLE orders (
	id INTEGER NOT NULL, 
	order_id VARCHAR(30), 
	user_id INTEGER, 
	total_amount FLOAT NOT NULL, 
	status VARCHAR(15), 
	payment_method VARCHAR, 
	created_at DATETIME, 
	PRIMARY KEY (id), 
	FOREIGN KEY(user_id) REFERENCES users (id)
);
CREATE INDEX ix_orders_status ON orders (status);
CREATE INDEX ix_orders_user_id ON orders (user_id);
CREATE INDEX ix_orders_id ON orders (id);
CREATE UNIQUE INDEX ix_orders_order_id ON orders (order_id);
CREATE TABLE order_addresses (
	id INTEGER NOT NULL, 
	order_id INTEGER NOT NULL, 
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
	created_at DATETIME DEFAULT CURRENT_TIMESTAMP, 
	PRIMARY KEY (id), 
	UNIQUE (order_id), 
	FOREIGN KEY(order_id) REFERENCES orders (id), 
	FOREIGN KEY(user_id) REFERENCES users (id)
);
CREATE INDEX ix_order_addresses_id ON order_addresses (id);
CREATE TABLE order_items (
	id INTEGER NOT NULL, 
	order_id INTEGER, 
	product_id INTEGER, 
	price FLOAT NOT NULL, 
	quantity INTEGER NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(order_id) REFERENCES orders (id) ON DELETE CASCADE, 
	FOREIGN KEY(product_id) REFERENCES products (id)
);
CREATE INDEX ix_order_items_id ON order_items (id);
