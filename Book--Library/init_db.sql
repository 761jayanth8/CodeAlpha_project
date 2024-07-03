-- Create Categories Table
CREATE TABLE IF NOT EXISTS category (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(50) NOT NULL
);

-- Create Books Table
CREATE TABLE IF NOT EXISTS book (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title VARCHAR(100) NOT NULL,
    author VARCHAR(100) NOT NULL,
    category_id INTEGER NOT NULL,
    is_borrowed BOOLEAN DEFAULT 0,
    FOREIGN KEY (category_id) REFERENCES category (id)
);

-- Create Borrow History Table
CREATE TABLE IF NOT EXISTS borrow_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    book_id INTEGER NOT NULL,
    borrow_date DATE NOT NULL,
    return_date DATE,
    FOREIGN KEY (book_id) REFERENCES book (id)
);

-- Insert default categories if not exists
INSERT OR IGNORE INTO category (name) VALUES ('Fiction');
INSERT OR IGNORE INTO category (name) VALUES ('Non-Fiction');
INSERT OR IGNORE INTO category (name) VALUES ('Science');
INSERT OR IGNORE INTO category (name) VALUES ('History');
INSERT OR IGNORE INTO category (name) VALUES ('Fantasy');
