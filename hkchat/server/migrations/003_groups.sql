CREATE TABLE IF NOT EXISTS group_chats (
    channel_id TEXT PRIMARY KEY REFERENCES channels(id) ON DELETE CASCADE,
    creator_id TEXT NOT NULL REFERENCES users(id),
    created_at INTEGER NOT NULL
);
