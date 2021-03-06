DROP TABLE IF EXISTS transactions;
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS merchants;
DROP TABLE IF EXISTS categorys;

CREATE TABLE merchants(
    id SERIAL PRIMARY KEY,
    name VARCHAR(255),
    location VARCHAR(255),
    activated BOOLEAN
);

CREATE TABLE users(
    id SERIAL PRIMARY KEY,
    name VARCHAR(255),
    spending_limit DECIMAL(10,2)
);

CREATE TABLE categorys (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255),
    activated BOOLEAN
);

CREATE TABLE transactions(
    id SERIAL PRIMARY KEY,
    amount DECIMAL(10,2),
    category_id INT REFERENCES categorys(id) ON DELETE CASCADE,
    date DATE,
    merchant_id INT REFERENCES merchants(id) ON DELETE CASCADE,
    user_id INT REFERENCES users(id) ON DELETE CASCADE
);

