
CREATE TABLE IF NOT EXISTS books (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    price REAL NOT NULL CHECK (price > 0),
    currency TEXT NOT NULL,
    availability TEXT NOT NULL,
    rating TEXT NOT NULL,
    page INTEGER NOT NULL CHECK (page > 0),
    product_url TEXT NOT NULL UNIQUE
);
