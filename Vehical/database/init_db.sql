CREATE TABLE IF NOT EXISTS users_new (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password TEXT NOT NULL,
    first_name VARCHAR(255),
    last_name VARCHAR(255),
    contact_number VARCHAR(100),
    address VARCHAR(255)
);
