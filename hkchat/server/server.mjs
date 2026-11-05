import {createServer} from 'node:http';
import {readFileSync, mkdirSync, readdirSync} from 'node:fs';
import {dirname, join} from 'node:path';
import {randomBytes, randomUUID, scryptSync, createHash, timingSafeEqual} from 'node:crypto';
import {fileURLToPath} from 'node:url';
import {DatabaseSync} from 'node:sqlite';

const dir = dirname(fileURLToPath(import.meta.url));
const dbPath = process.env.HKCHAT_DB || join(dir, 'hkchat.sqlite');
mkdirSync(dirname(dbPath), {recursive: true});
const db = new DatabaseSync(dbPath);
db.exec('PRAGMA foreign_keys = ON; PRAGMA journal_mode = WAL; CREATE TABLE IF NOT EXISTS schema_migrations (version INTEGER PRIMARY KEY, applied_at INTEGER NOT NULL)');
for (const file of readdirSync(join(dir, 'migrations')).filter((name) => /^\d+_.*\.sql$/.test(name)).sort()) {
    const version = Number(file.split('_')[0]);
    if (db.prepare('SELECT 1 FROM schema_migrations WHERE version=?').get(version)) continue;
    db.exec('BEGIN');
    try {
        db.exec(readFileSync(join(dir, 'migrations', file), 'utf8'));
        db.prepare('INSERT INTO schema_migrations (version,applied_at) VALUES (?,?)').run(version, Date.now());
        db.exec('COMMIT');
    } catch (error) {
        db.exec('ROLLBACK');
        throw error;
    }
}
const port = Number(process.env.HKCHAT_PORT || 8070);
const now = () => Date.now();
const hash = (value) => createHash('sha256').update(value).digest('hex');

function passwordHash(password) {
    const salt = randomBytes(16).toString('hex');
    return `${salt}:${scryptSync(password, salt, 64).toString('hex')}`;
}

function checkPassword(password, stored) {
    const [salt, digest] = stored.split(':');
    if (!salt || !digest) return false;
    const actual = scryptSync(password, salt, 64);
    const expected = Buffer.from(digest, 'hex');
    return actual.length === expected.length && timingSafeEqual(actual, expected);
}

function send(res, status, data) {
    res.writeHead(status, {'content-type': 'application/json; charset=utf-8', 'cache-control': 'no-store'});
    res.end(JSON.stringify(data));
}

async function body(req) {
    let data = '';
    for await (const chunk of req) {
        data += chunk;
        if (data.length > 64 * 1024) throw Object.assign(new Error('Request too large'), {status: 413});
    }
    try { return JSON.parse(data || '{}'); } catch { throw Object.assign(new Error('Invalid JSON'), {status: 400}); }
}

function issueSession(userId) {
    const token = randomBytes(32).toString('hex');
    db.prepare('INSERT INTO sessions (token_hash,user_id,expires_at) VALUES (?,?,?)').run(hash(token), userId, now() + 30 * 86400000);
    return token;
}

function auth(req) {
    const token = /^Bearer ([a-f0-9]{64})$/.exec(req.headers.authorization || '')?.[1];
    if (!token) return null;
    return db.prepare('SELECT u.id,u.username,u.email,u.created_at FROM sessions s JOIN users u ON u.id=s.user_id WHERE s.token_hash=? AND s.expires_at>?').get(hash(token), now()) || null;
}

function member(channelId, userId) {
    return db.prepare('SELECT 1 FROM channel_members WHERE channel_id=? AND user_id=?').get(channelId, userId);
}

function channelDto(row, userId) {
    let name = row.name;
    const isGroup = Boolean(db.prepare('SELECT 1 FROM group_chats WHERE channel_id=?').get(row.id));
    if (row.kind === 'dm' && userId && !isGroup) {
        const otherId = row.dm_key.split(':').find((id) => id !== userId);
        name = db.prepare('SELECT username FROM users WHERE id=?').get(otherId)?.username || name;
    }
    return {id: row.id, name, kind: isGroup ? 'group' : row.kind, createdAt: row.created_at};
}

function messageDtos(rows, userId) {
    if (!rows.length) return [];
    const reactions = new Map();
    const placeholders = rows.map(() => '?').join(',');
    const reactionRows = db.prepare(`SELECT message_id,emoji,COUNT(*) AS count,MAX(CASE WHEN user_id=? THEN 1 ELSE 0 END) AS me FROM reactions WHERE message_id IN (${placeholders}) GROUP BY message_id,emoji ORDER BY emoji`).all(userId, ...rows.map((row) => row.id));
    for (const reaction of reactionRows) {
        if (!reactions.has(reaction.message_id)) reactions.set(reaction.message_id, []);
        reactions.get(reaction.message_id).push({emoji: reaction.emoji, count: reaction.count, me: Boolean(reaction.me)});
    }
    return rows.map((row) => ({
        id: row.id,
        channelId: row.channel_id,
        userId: row.user_id,
        username: row.username,
        body: row.body,
        replyTo: row.reply_to,
        createdAt: row.created_at,
        editedAt: row.edited_at,
        reactions: reactions.get(row.id) || [],
    }));
}

const messageSelect = 'SELECT m.*,u.username FROM messages m JOIN users u ON u.id=m.user_id';

function fail(message, status = 400) {
    throw Object.assign(new Error(message), {status});
}

async function handler(req, res) {
    try {
        const url = new URL(req.url, `http://${req.headers.host || 'localhost'}`);
        const path = url.pathname;
        if (req.method === 'GET' && path === '/api/health') return send(res, 200, {status: 'ok', product: 'HKchat'});

        if (req.method === 'POST' && path === '/api/register') {
            const input = await body(req);
            const username = String(input.username || '').trim();
            const email = String(input.email || '').trim().toLowerCase();
            const password = String(input.password || '');
            if (!/^[\p{L}\p{N}_]{3,32}$/u.test(username) || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email) || password.length < 8) fail('Use a 3-32 character username, valid email and password of at least 8 characters');
            if (db.prepare('SELECT 1 FROM users WHERE username=? OR email=?').get(username, email)) fail('Username or email already exists', 409);
            const user = {id: randomUUID(), username, email, created_at: now()};
            db.exec('BEGIN');
            try {
                db.prepare('INSERT INTO users (id,username,email,password_hash,created_at) VALUES (?,?,?,?,?)').run(user.id, user.username, user.email, passwordHash(password), user.created_at);
                for (const name of ['General', 'Random']) {
                    let channel = db.prepare('SELECT id FROM channels WHERE kind=? AND name=?').get('public', name);
                    if (!channel) {
                        channel = {id: randomUUID()};
                        db.prepare('INSERT INTO channels (id,name,kind,created_at) VALUES (?,?,?,?)').run(channel.id, name, 'public', now());
                    }
                    db.prepare('INSERT INTO channel_members (channel_id,user_id,joined_at) VALUES (?,?,?)').run(channel.id, user.id, now());
                }
                db.exec('COMMIT');
            } catch (error) { db.exec('ROLLBACK'); throw error; }
            return send(res, 201, {user, token: issueSession(user.id)});
        }

        if (req.method === 'POST' && path === '/api/login') {
            const input = await body(req);
            const identifier = String(input.identifier || '').trim();
            const password = String(input.password || '');
            const row = db.prepare('SELECT * FROM users WHERE username=? OR email=?').get(identifier, identifier);
            if (!row || !checkPassword(password, row.password_hash)) fail('Invalid username or password', 401);
            return send(res, 200, {user: {id: row.id, username: row.username, email: row.email, createdAt: row.created_at}, token: issueSession(row.id)});
        }

        const user = auth(req);
        if (!user) return send(res, 401, {error: 'Sign in required'});
        if (req.method === 'GET' && path === '/api/me') return send(res, 200, {user});
        if (req.method === 'POST' && path === '/api/logout') {
            const token = req.headers.authorization.slice(7);
            db.prepare('DELETE FROM sessions WHERE token_hash=?').run(hash(token));
            return send(res, 200, {ok: true});
        }
        if (req.method === 'GET' && path === '/api/users') {
            const q = `%${String(url.searchParams.get('q') || '').slice(0, 80)}%`;
            const users = db.prepare('SELECT id,username FROM users WHERE id<>? AND username LIKE ? ORDER BY username LIMIT 50').all(user.id, q);
            return send(res, 200, {users});
        }
        if (req.method === 'GET' && path === '/api/channels') {
            const rows = db.prepare('SELECT c.* FROM channels c JOIN channel_members cm ON cm.channel_id=c.id WHERE cm.user_id=? ORDER BY c.kind,c.name').all(user.id);
            return send(res, 200, {channels: rows.map((row) => channelDto(row, user.id))});
        }
        if (req.method === 'GET' && path === '/api/channels/public') {
            const rows = db.prepare('SELECT c.* FROM channels c WHERE c.kind=? AND NOT EXISTS (SELECT 1 FROM group_chats g WHERE g.channel_id=c.id) AND NOT EXISTS (SELECT 1 FROM channel_members cm WHERE cm.channel_id=c.id AND cm.user_id=?) ORDER BY c.name').all('public', user.id);
            return send(res, 200, {channels: rows.map((row) => channelDto(row, user.id))});
        }
        const joinRoute = /^\/api\/channels\/([^/]+)\/join$/.exec(path);
        if (req.method === 'POST' && joinRoute) {
            const channel = db.prepare('SELECT * FROM channels WHERE id=? AND kind=? AND NOT EXISTS (SELECT 1 FROM group_chats g WHERE g.channel_id=channels.id)').get(joinRoute[1], 'public');
            if (!channel) return send(res, 404, {error: 'Channel not found'});
            db.prepare('INSERT OR IGNORE INTO channel_members (channel_id,user_id,joined_at) VALUES (?,?,?)').run(channel.id,user.id,now());
            return send(res, 200, {channel: channelDto(channel, user.id)});
        }
        if (req.method === 'POST' && path === '/api/channels') {
            const input = await body(req);
            const name = String(input.name || '').trim();
            if (name.length < 2 || name.length > 80) fail('Channel name must be 2-80 characters');
            const channel = {id: randomUUID(), name, kind: 'public', created_at: now()};
            db.exec('BEGIN');
            try {
                db.prepare('INSERT INTO channels (id,name,kind,created_at) VALUES (?,?,?,?)').run(channel.id, channel.name, channel.kind, channel.created_at);
                db.prepare('INSERT INTO channel_members (channel_id,user_id,joined_at) VALUES (?,?,?)').run(channel.id, user.id, now());
                db.exec('COMMIT');
            } catch (error) { db.exec('ROLLBACK'); throw error; }
            return send(res, 201, {channel: channelDto(channel, user.id)});
        }
        if (req.method === 'POST' && path === '/api/groups') {
            const input = await body(req);
            const name = String(input.name || '').trim();
            if (name.length < 2 || name.length > 80) fail('Group name must be 2-80 characters');
            if (!Array.isArray(input.userIds) || input.userIds.length < 2 || input.userIds.length > 19) fail('Group needs 3-20 people including you');
            const ids = [...new Set(input.userIds)];
            if (ids.length !== input.userIds.length || ids.includes(user.id) || ids.some((id) => typeof id !== 'string')) fail('Invalid group members');
            const found = db.prepare(`SELECT id FROM users WHERE id IN (${ids.map(() => '?').join(',')})`).all(...ids);
            if (found.length !== ids.length) fail('Group member not found');
            const channel = {id: randomUUID(), name, kind: 'public', created_at: now()};
            db.exec('BEGIN');
            try {
                db.prepare('INSERT INTO channels (id,name,kind,created_at) VALUES (?,?,?,?)').run(channel.id, channel.name, channel.kind, channel.created_at);
                db.prepare('INSERT INTO group_chats (channel_id,creator_id,created_at) VALUES (?,?,?)').run(channel.id, user.id, channel.created_at);
                const addMember = db.prepare('INSERT INTO channel_members (channel_id,user_id,joined_at) VALUES (?,?,?)');
                for (const id of [user.id, ...ids]) addMember.run(channel.id, id, now());
                db.exec('COMMIT');
            } catch (error) { db.exec('ROLLBACK'); throw error; }
            return send(res, 201, {channel: channelDto(channel, user.id)});
        }
        if (req.method === 'POST' && path === '/api/dm') {
            const input = await body(req);
            const otherId = String(input.userId || '');
            const other = db.prepare('SELECT id,username FROM users WHERE id=?').get(otherId);
            if (!other || otherId === user.id) fail('Invalid recipient');
            const dmKey = [user.id, other.id].sort().join(':');
            let row = db.prepare('SELECT * FROM channels WHERE dm_key=?').get(dmKey);
            if (!row) {
                db.exec('BEGIN');
                try {
                    row = {id: randomUUID(), name: other.username, kind: 'dm', dm_key: dmKey, created_at: now()};
                    db.prepare('INSERT INTO channels (id,name,kind,dm_key,created_at) VALUES (?,?,?,?,?)').run(row.id,row.name,row.kind,row.dm_key,row.created_at);
                    const addMember = db.prepare('INSERT INTO channel_members (channel_id,user_id,joined_at) VALUES (?,?,?)');
                    addMember.run(row.id, user.id, now());
                    addMember.run(row.id, other.id, now());
                    db.exec('COMMIT');
                } catch (error) { db.exec('ROLLBACK'); throw error; }
            }
            return send(res, 200, {channel: channelDto(row, user.id)});
        }
        const messagesRoute = /^\/api\/channels\/([^/]+)\/messages$/.exec(path);
        if (messagesRoute) {
            const channelId = messagesRoute[1];
            if (!member(channelId, user.id)) return send(res, 403, {error: 'Not a channel member'});
            if (req.method === 'GET') {
                const after = Math.max(0, Number(url.searchParams.get('after') || 0) || 0);
                const rows = after === 0
                    ? db.prepare(`${messageSelect} WHERE m.channel_id=? AND m.deleted_at IS NULL ORDER BY m.id DESC LIMIT 100`).all(channelId).reverse()
                    : db.prepare(`${messageSelect} WHERE m.channel_id=? AND m.id>? AND m.deleted_at IS NULL ORDER BY m.id LIMIT 100`).all(channelId, after);
                return send(res, 200, {messages: messageDtos(rows, user.id)});
            }
            if (req.method === 'POST') {
                const input = await body(req);
                const text = String(input.body || '').trim();
                if (!text || text.length > 4000) fail('Message must be 1-4000 characters');
                const replyTo = input.replyTo == null ? null : Number(input.replyTo);
                if (replyTo !== null && (!Number.isSafeInteger(replyTo) || replyTo < 1 || !db.prepare('SELECT 1 FROM messages WHERE id=? AND channel_id=? AND deleted_at IS NULL').get(replyTo, channelId))) fail('Reply target not found');
                const result = db.prepare('INSERT INTO messages (channel_id,user_id,body,reply_to,created_at) VALUES (?,?,?,?,?)').run(channelId,user.id,text,replyTo,now());
                const row = db.prepare(`${messageSelect} WHERE m.id=?`).get(Number(result.lastInsertRowid));
                return send(res, 201, {message: messageDtos([row], user.id)[0]});
            }
        }
        const reactionRoute = /^\/api\/messages\/(\d+)\/reactions(?:\/([^/]+))?$/.exec(path);
        const threadRoute = /^\/api\/messages\/(\d+)\/thread$/.exec(path);
        const messageRoute = /^\/api\/messages\/(\d+)$/.exec(path);
        if (reactionRoute || threadRoute || messageRoute) {
            const messageId = Number((reactionRoute || threadRoute || messageRoute)[1]);
            const row = db.prepare(`${messageSelect} WHERE m.id=? AND m.deleted_at IS NULL`).get(messageId);
            if (!row) return send(res, 404, {error: 'Message not found'});
            if (!member(row.channel_id, user.id)) return send(res, 403, {error: 'Not a channel member'});

            if (threadRoute && req.method === 'GET') {
                const root = db.prepare('WITH RECURSIVE ancestors(id,reply_to) AS (SELECT id,reply_to FROM messages WHERE id=? UNION ALL SELECT m.id,m.reply_to FROM messages m JOIN ancestors a ON m.id=a.reply_to) SELECT id FROM ancestors WHERE reply_to IS NULL').get(messageId);
                const rows = db.prepare('WITH RECURSIVE descendants(id) AS (SELECT id FROM messages WHERE id=? UNION ALL SELECT m.id FROM messages m JOIN descendants d ON m.reply_to=d.id) SELECT m.*,u.username FROM descendants d JOIN messages m ON m.id=d.id JOIN users u ON u.id=m.user_id WHERE m.deleted_at IS NULL ORDER BY m.id LIMIT 100').all(root.id);
                return send(res, 200, {messages: messageDtos(rows, user.id)});
            }

            if (messageRoute && req.method === 'PATCH') {
                if (row.user_id !== user.id) return send(res, 403, {error: 'Only the author can edit this message'});
                const input = await body(req);
                const text = String(input.body || '').trim();
                if (!text || text.length > 4000) fail('Message must be 1-4000 characters');
                const editedAt = now();
                db.prepare('UPDATE messages SET body=?,edited_at=? WHERE id=?').run(text, editedAt, messageId);
                return send(res, 200, {message: messageDtos([{...row, body: text, edited_at: editedAt}], user.id)[0]});
            }
            if (messageRoute && req.method === 'DELETE') {
                if (row.user_id !== user.id) return send(res, 403, {error: 'Only the author can delete this message'});
                db.prepare('UPDATE messages SET deleted_at=? WHERE id=?').run(now(), messageId);
                return send(res, 200, {ok: true});
            }

            if (reactionRoute && (req.method === 'POST' || req.method === 'DELETE')) {
                if ((req.method === 'POST' && reactionRoute[2]) || (req.method === 'DELETE' && !reactionRoute[2])) return send(res, 404, {error: 'Not found'});
                let emoji;
                if (req.method === 'POST') emoji = (await body(req)).emoji;
                else {
                    try { emoji = decodeURIComponent(reactionRoute[2]); } catch { fail('Invalid emoji'); }
                }
                if (typeof emoji !== 'string' || !emoji.trim() || emoji.length > 64 || /[\x00-\x1f\x7f]/.test(emoji)) fail('Invalid emoji');
                if (req.method === 'POST') db.prepare('INSERT OR IGNORE INTO reactions (message_id,user_id,emoji) VALUES (?,?,?)').run(messageId, user.id, emoji);
                else db.prepare('DELETE FROM reactions WHERE message_id=? AND user_id=? AND emoji=?').run(messageId, user.id, emoji);
                return send(res, 200, {message: messageDtos([row], user.id)[0]});
            }
        }
        if (req.method === 'GET' && path === '/api/search') {
            const q = String(url.searchParams.get('q') || '').trim().slice(0, 100);
            if (!q) return send(res, 200, {messages: []});
            const rows = db.prepare(`${messageSelect} JOIN channel_members cm ON cm.channel_id=m.channel_id WHERE cm.user_id=? AND m.deleted_at IS NULL AND instr(lower(m.body),lower(?))>0 ORDER BY m.id DESC LIMIT 50`).all(user.id, q);
            return send(res, 200, {messages: messageDtos(rows, user.id)});
        }
        return send(res, 404, {error: 'Not found'});
    } catch (error) {
        const status = error.status || (error.code?.startsWith('SQLITE_CONSTRAINT') ? 409 : 500);
        if (status === 500) console.error(error);
        return send(res, status, {error: status === 500 ? 'Internal server error' : error.message});
    }
}

createServer(handler).listen(port, '0.0.0.0', () => console.log(`HKchat API ready on ${port}`));
