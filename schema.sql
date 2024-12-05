DROP TABLE IF EXISTS likes CASCADE;
DROP TABLE IF EXISTS replies CASCADE;
DROP TABLE IF EXISTS threads CASCADE;
DROP TABLE IF EXISTS topics CASCADE;
DROP TABLE IF EXISTS users CASCADE;

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    created_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP,
    is_admin BOOLEAN DEFAULT FALSE
);

CREATE TABLE topics (
    id SERIAL PRIMARY KEY,
    text_id VARCHAR(20) UNIQUE NOT NULL,
    title VARCHAR(100) UNIQUE NOT NULL,
    description TEXT,
    is_hidden BOOLEAN DEFAULT FALSE
);

CREATE TABLE threads (
    id SERIAL PRIMARY KEY,
    topic_id INTEGER REFERENCES topics(id),
    user_id INTEGER REFERENCES users(id),
    title VARCHAR(100) NOT NULL,
    created_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE replies (
    id SERIAL PRIMARY KEY,
    thread_id INTEGER REFERENCES threads(id),
    user_id INTEGER REFERENCES users(id),
    content TEXT NOT NULL,
    created_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE likes (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    reply_id INTEGER REFERENCES replies(id),
);
