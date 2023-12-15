
CREATE TABLE stores (
    store_id SERIAL PRIMARY KEY,
    store_name VARCHAR(255) NOT NULL,
    address VARCHAR(255) NOT NULL,
    city VARCHAR(100) NOT NULL,
    state VARCHAR(50),
    zip VARCHAR(10),
    UNIQUE (store_name)
);

CREATE TABLE products (
    product_id SERIAL PRIMARY KEY,
    product_name VARCHAR(255) NOT NULL,
    description TEXT,
    price DECIMAL(10, 2) NOT NULL,
    UNIQUE (product_name)
);

CREATE TABLE sales (
    sale_id SERIAL PRIMARY KEY,
    store_id INT,
    product_id INT,
    quantity INT NOT NULL,
    sale_date DATE NOT NULL,
    FOREIGN KEY (store_id) REFERENCES stores(store_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);



INSERT INTO stores (store_name, address, city, state, zip) VALUES
    ('SuperMart', '123 Main St', 'Anytown', 'CA', '12345'),
    ('MegaMart', '456 Oak St', 'Othercity', 'NY', '54321'),
    ('CityGrocery', '789 Pine St', 'Bigcity', 'TX', '67890');

INSERT INTO products (product_name, description, price) VALUES
    ('Monitor', 'High-resolution monitor', 299.99),
    ('Mouse', 'Wireless mouse with ergonomic design', 39.99),
    ('Keyboard', 'Mechanical gaming keyboard', 89.99),
    ('Printer', 'Color inkjet printer', 149.99),
    ('Tablet', '10-inch Android tablet', 199.99),
    ('Smart TV', '4K UHD Smart TV', 799.99),
    ('Digital Camera', 'Mirrorless digital camera', 649.99),
    ('External SSD', '500GB External Solid State Drive', 129.99),
    ('Wireless Earbuds', 'Bluetooth wireless earbuds', 79.99),
    ('Gaming Console', 'Next-gen gaming console', 499.99);

INSERT INTO sales (store_id, product_id, quantity, sale_date) VALUES
    (1, 1, 3, '2023-02-01'),
    (2, 3, 5, '2023-02-02'),
    (3, 2, 2, '2023-02-03'),
    (1, 4, 1, '2023-02-04'),
    (2, 5, 4, '2023-02-05'),
    (3, 6, 2, '2023-02-06'),
    (1, 7, 3, '2023-02-07'),
    (2, 8, 1, '2023-02-08'),
    (3, 9, 4, '2023-02-09'),
    (1, 10, 2, '2023-02-10');
