CREATE DATABASE product_sales;
USE product_sales;

CREATE TABLE Stores (
    Store_ID INT PRIMARY KEY AUTO_INCREMENT,
    Store_Name VARCHAR(255) NOT NULL,
    Address VARCHAR(255) NOT NULL,
    City VARCHAR(100) NOT NULL,
    State VARCHAR(50),
    ZIP VARCHAR(10),
    UNIQUE (Store_Name)
);

CREATE TABLE Products (
    Product_ID INT PRIMARY KEY AUTO_INCREMENT,
    Product_Name VARCHAR(255) NOT NULL,
    Description TEXT,
    Price DECIMAL(10, 2) NOT NULL,
    UNIQUE (Product_Name)
);

CREATE TABLE Sales (
    Sale_ID INT PRIMARY KEY AUTO_INCREMENT,
    Store_ID INT,
    Product_ID INT,
    Quantity INT NOT NULL,
    Sale_Date DATE NOT NULL,
    FOREIGN KEY (Store_ID) REFERENCES Stores(Store_ID),
    FOREIGN KEY (Product_ID) REFERENCES Products(Product_ID)
);



INSERT INTO Stores (Store_Name, Address, City, State, ZIP) VALUES
    ('SuperMart', '123 Main St', 'Anytown', 'CA', '12345'),
    ('MegaMart', '456 Oak St', 'Othercity', 'NY', '54321'),
    ('CityGrocery', '789 Pine St', 'Bigcity', 'TX', '67890');


INSERT INTO Products (Product_Name, Description, Price) VALUES
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


INSERT INTO Sales (Store_ID, Product_ID, Quantity, Sale_Date) VALUES
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

