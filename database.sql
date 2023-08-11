CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    password_hash VARCHAR(100) NOT NULL,
    discord_id_hash VARCHAR(100) NOT NULL
);

CREATE TYPE pr_stats AS (
    name VARCHAR(100),
    bench DECIMAL(5,1),
    squat DECIMAL(5,1),
    deadlift DECIMAL(10,2),
)

CREATE TABLE historical (
    entry_id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(user_id),
    record_date DATE NOT NULL,
    pr pr_stats 
);