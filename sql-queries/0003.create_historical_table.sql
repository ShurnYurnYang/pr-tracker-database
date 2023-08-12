CREATE TABLE historical (
    entry_id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    record_date DATE NOT NULL,
    pr pr_stats 
);