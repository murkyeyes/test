CREATE TABLE IF NOT EXISTS workspaces (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    owner_id TEXT NOT NULL REFERENCES users(id),
    created_at INTEGER NOT NULL
);
CREATE TABLE IF NOT EXISTS workspace_members (
    workspace_id TEXT NOT NULL REFERENCES workspaces(id) ON DELETE CASCADE,
    user_id TEXT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    role TEXT NOT NULL CHECK (role IN ('owner', 'admin', 'member')),
    PRIMARY KEY (workspace_id, user_id)
);
CREATE INDEX IF NOT EXISTS workspace_members_user_idx ON workspace_members(user_id);
CREATE TABLE IF NOT EXISTS workspace_channels (
    workspace_id TEXT NOT NULL REFERENCES workspaces(id) ON DELETE CASCADE,
    channel_id TEXT NOT NULL REFERENCES channels(id) ON DELETE CASCADE,
    PRIMARY KEY (workspace_id, channel_id)
);

CREATE TABLE IF NOT EXISTS user_preferences (
    user_id TEXT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    key TEXT NOT NULL,
    value TEXT NOT NULL,
    PRIMARY KEY (user_id, key)
);

CREATE TABLE IF NOT EXISTS playbooks (
    id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT NOT NULL DEFAULT '',
    created_by TEXT NOT NULL REFERENCES users(id),
    created_at INTEGER NOT NULL
);
CREATE TABLE IF NOT EXISTS playbook_tasks (
    id TEXT PRIMARY KEY,
    playbook_id TEXT NOT NULL REFERENCES playbooks(id) ON DELETE CASCADE,
    position INTEGER NOT NULL,
    title TEXT NOT NULL,
    UNIQUE (playbook_id, position)
);
CREATE TABLE IF NOT EXISTS playbook_runs (
    id TEXT PRIMARY KEY,
    playbook_id TEXT NOT NULL REFERENCES playbooks(id),
    channel_id TEXT REFERENCES channels(id),
    owner_id TEXT NOT NULL REFERENCES users(id),
    status TEXT NOT NULL CHECK (status IN ('open', 'closed')),
    started_at INTEGER NOT NULL,
    closed_at INTEGER
);
CREATE INDEX IF NOT EXISTS playbook_runs_owner_idx ON playbook_runs(owner_id, status);
CREATE TABLE IF NOT EXISTS playbook_run_tasks (
    run_id TEXT NOT NULL REFERENCES playbook_runs(id) ON DELETE CASCADE,
    task_id TEXT NOT NULL REFERENCES playbook_tasks(id),
    completed_by TEXT REFERENCES users(id),
    completed_at INTEGER,
    PRIMARY KEY (run_id, task_id)
);

CREATE TABLE IF NOT EXISTS ai_conversations (
    id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL REFERENCES users(id),
    channel_id TEXT REFERENCES channels(id),
    model TEXT NOT NULL,
    created_at INTEGER NOT NULL
);
CREATE INDEX IF NOT EXISTS ai_conversations_user_idx ON ai_conversations(user_id, created_at);
CREATE TABLE IF NOT EXISTS ai_messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    conversation_id TEXT NOT NULL REFERENCES ai_conversations(id) ON DELETE CASCADE,
    role TEXT NOT NULL CHECK (role IN ('user', 'assistant', 'tool')),
    content TEXT NOT NULL,
    created_at INTEGER NOT NULL
);
CREATE INDEX IF NOT EXISTS ai_messages_conversation_idx ON ai_messages(conversation_id, id);

CREATE TABLE IF NOT EXISTS calls (
    id TEXT PRIMARY KEY,
    channel_id TEXT NOT NULL REFERENCES channels(id),
    started_by TEXT NOT NULL REFERENCES users(id),
    status TEXT NOT NULL CHECK (status IN ('active', 'ended')),
    started_at INTEGER NOT NULL,
    ended_at INTEGER
);
CREATE INDEX IF NOT EXISTS calls_channel_status_idx ON calls(channel_id, status);
CREATE TABLE IF NOT EXISTS call_participants (
    call_id TEXT NOT NULL REFERENCES calls(id) ON DELETE CASCADE,
    user_id TEXT NOT NULL REFERENCES users(id),
    joined_at INTEGER NOT NULL,
    left_at INTEGER,
    PRIMARY KEY (call_id, user_id, joined_at)
);

CREATE TABLE IF NOT EXISTS device_registrations (
    id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    platform TEXT NOT NULL CHECK (platform IN ('android', 'ios')),
    push_token TEXT NOT NULL UNIQUE,
    created_at INTEGER NOT NULL
);
CREATE INDEX IF NOT EXISTS device_registrations_user_idx ON device_registrations(user_id);
CREATE TABLE IF NOT EXISTS notifications (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id TEXT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    kind TEXT NOT NULL,
    payload TEXT NOT NULL,
    read_at INTEGER,
    created_at INTEGER NOT NULL
);
CREATE INDEX IF NOT EXISTS notifications_user_idx ON notifications(user_id, read_at, id);
