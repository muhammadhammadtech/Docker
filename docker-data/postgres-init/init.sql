CREATE DATABASE app_production;
CREATE USER app_user WITH ENCRYPTED PASSWORD 'AppUserSecurePass123!';
GRANT ALL PRIVILEGES ON DATABASE app_production TO app_user;
\c app_production;
CREATE SCHEMA IF NOT EXISTS app_schema;
GRANT ALL ON SCHEMA app_schema TO app_user;

CREATE TABLE app_schema.products (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    price DECIMAL(10,2) NOT NULL,
    category VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE app_schema.inventory (
    id SERIAL PRIMARY KEY,
    product_id INTEGER REFERENCES app_schema.products(id),
    quantity INTEGER NOT NULL DEFAULT 0,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO app_schema.products (name, description, price, category) VALUES
('Gaming Laptop', 'High-performance laptop', 1299.99, 'Electronics'),
('Office Chair', 'Ergonomic chair', 299.99, 'Furniture'),
('Coffee Maker', 'Drip coffee maker', 89.99, 'Appliances'),
('Bluetooth Headphones', 'Wireless headphones', 199.99, 'Electronics'),
('Standing Desk', 'Adjustable desk', 449.99, 'Furniture');

INSERT INTO app_schema.inventory (product_id, quantity) VALUES
(1, 15), (2, 8), (3, 25), (4, 12), (5, 6);
