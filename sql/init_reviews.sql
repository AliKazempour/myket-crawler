CREATE TABLE IF NOT EXISTS myket_reviews (
    comment_id VARCHAR(64) PRIMARY KEY,
    package_name VARCHAR(150) NOT NULL,
    author_name VARCHAR(255),
    rating SMALLINT CHECK (rating >= 0 AND rating <= 5),
    comment_text TEXT,
    comment_date VARCHAR(100),
    likes_count INTEGER DEFAULT 0,
    dislikes_count INTEGER DEFAULT 0,
    reply_text TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_myket_reviews_pkg ON myket_reviews(package_name);