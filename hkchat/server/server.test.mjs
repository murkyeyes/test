import assert from 'node:assert/strict';
import {spawn} from 'node:child_process';
import {mkdtempSync, rmSync} from 'node:fs';
import {createServer} from 'node:net';
import {tmpdir} from 'node:os';
import {join} from 'node:path';
import {setTimeout as delay} from 'node:timers/promises';
import test from 'node:test';
import {fileURLToPath} from 'node:url';

const serverFile = fileURLToPath(new URL('./server.mjs', import.meta.url));

async function freePort() {
    const server = createServer();
    await new Promise((resolve) => server.listen(0, '127.0.0.1', resolve));
    const port = server.address().port;
    await new Promise((resolve) => server.close(resolve));
    return port;
}

async function start(dbPath, port) {
    const child = spawn(process.execPath, [serverFile], {
        env: {...process.env, HKCHAT_DB: dbPath, HKCHAT_PORT: String(port)},
        stdio: 'ignore',
    });
    for (let attempt = 0; attempt < 60; attempt++) {
        if (child.exitCode !== null || child.signalCode !== null) throw new Error(`HKchat server exited: ${child.exitCode || child.signalCode}`);
        try {
            const response = await fetch(`http://127.0.0.1:${port}/api/health`);
            if (response.ok) return child;
        } catch { /* Wait for server start. */ }
        await delay(100);
    }
    child.kill();
    throw new Error('HKchat server did not start');
}

async function stop(child) {
    if (child.exitCode !== null || child.signalCode !== null) return;
    const exited = new Promise((resolve) => child.once('exit', resolve));
    child.kill();
    await exited;
}

test('accounts, channel permissions, DM, search and persistence', async () => {
    const directory = mkdtempSync(join(tmpdir(), 'hkchat-test-'));
    const dbPath = join(directory, 'chat.sqlite');
    const port = await freePort();
    const base = `http://127.0.0.1:${port}/api`;
    let child;
    const call = async (path, method = 'GET', token, payload) => {
        const response = await fetch(base + path, {
            method,
            headers: {'content-type': 'application/json', ...(token ? {authorization: `Bearer ${token}`} : {})},
            body: payload ? JSON.stringify(payload) : undefined,
        });
        return {status: response.status, data: await response.json()};
    };

    try {
        child = await start(dbPath, port);
        const alice = await call('/register', 'POST', undefined, {username: 'alice', email: 'alice@example.test', password: 'password123'});
        const bob = await call('/register', 'POST', undefined, {username: 'bob', email: 'bob@example.test', password: 'password123'});
        const charlie = await call('/register', 'POST', undefined, {username: 'charlie', email: 'charlie@example.test', password: 'password123'});
        const dave = await call('/register', 'POST', undefined, {username: 'Đạt', email: 'dat@example.test', password: 'password123'});
        const outsider = await call('/register', 'POST', undefined, {username: 'outsider', email: 'outsider@example.test', password: 'password123'});
        assert.equal(alice.status, 201);
        assert.equal(bob.status, 201);
        assert.equal(charlie.status, 201);
        assert.equal(dave.status, 201);
        assert.equal(outsider.status, 201);
        assert.equal((await call('/login', 'POST', undefined, {identifier: 'Đạt', password: 'password123'})).status, 200);
        const group = await call('/groups', 'POST', alice.data.token, {name: 'Đồ án chuyên ngành', userIds: [bob.data.user.id, charlie.data.user.id, dave.data.user.id]});
        assert.equal(group.status, 201);
        assert.equal(group.data.channel.kind, 'group');
        assert.equal((await call('/groups', 'POST', alice.data.token, {name: 'Invalid', userIds: [bob.data.user.id, outsider.data.user.id, 'missing']})).status, 400);
        assert.equal((await call('/channels', 'GET', dave.data.token)).data.channels.find((channel) => channel.id === group.data.channel.id)?.kind, 'group');
        assert.equal((await call('/channels/public', 'GET', outsider.data.token)).data.channels.some((channel) => channel.id === group.data.channel.id), false);
        assert.equal((await call(`/channels/${group.data.channel.id}/join`, 'POST', outsider.data.token)).status, 404);
        assert.equal((await call(`/channels/${group.data.channel.id}/messages`, 'GET', outsider.data.token)).status, 403);
        assert.equal((await call(`/channels/${group.data.channel.id}/messages`, 'POST', bob.data.token, {body: 'Group hello'})).status, 201);
        assert.equal((await call(`/channels/${group.data.channel.id}/messages`, 'GET', dave.data.token)).data.messages[0].body, 'Group hello');
        assert.equal((await call('/channels')).status, 401);
        assert.equal((await call('/login', 'POST', undefined, {identifier: 'alice', password: 'wrong'})).status, 401);

        const dm = await call('/dm', 'POST', alice.data.token, {userId: bob.data.user.id});
        assert.equal(dm.status, 200);
        const channelId = dm.data.channel.id;
        assert.equal((await call(`/channels/${channelId}/messages`, 'GET', charlie.data.token)).status, 403);
        assert.equal((await call('/search?q=private', 'GET', charlie.data.token)).data.messages.length, 0);

        const post = await call(`/channels/${channelId}/messages`, 'POST', alice.data.token, {body: 'private hello'});
        assert.equal(post.status, 201);
        assert.equal(post.data.message.replyTo, null);
        assert.deepEqual(post.data.message.reactions, []);
        assert.equal((await call(`/channels/${channelId}/messages`, 'GET', bob.data.token)).data.messages[0].body, 'private hello');
        assert.equal((await call('/search?q=private', 'GET', bob.data.token)).data.messages.length, 1);
        assert.equal((await call('/search?q=private', 'GET', charlie.data.token)).data.messages.length, 0);

        const postId = post.data.message.id;
        const reply = await call(`/channels/${channelId}/messages`, 'POST', bob.data.token, {body: 'reply before edit', replyTo: postId});
        assert.equal(reply.status, 201);
        assert.equal(reply.data.message.replyTo, postId);
        const replyId = reply.data.message.id;
        assert.equal((await call(`/channels/${channelId}/messages`, 'POST', bob.data.token, {body: 'bad reply', replyTo: 999999})).status, 400);
        assert.equal((await call(`/channels/${channelId}/messages`, 'POST', charlie.data.token, {body: 'intrusion', replyTo: postId})).status, 403);
        const nested = await call(`/channels/${channelId}/messages`, 'POST', alice.data.token, {body: 'nested reply', replyTo: replyId});
        assert.equal(nested.status, 201);
        assert.deepEqual((await call(`/messages/${nested.data.message.id}/thread`, 'GET', alice.data.token)).data.messages.map((message) => message.id), [postId, replyId, nested.data.message.id]);
        assert.equal((await call(`/messages/${postId}/thread`, 'GET', charlie.data.token)).status, 403);

        assert.equal((await call(`/messages/${replyId}`, 'PATCH', alice.data.token, {body: 'takeover'})).status, 403);
        assert.equal((await call(`/messages/${replyId}`, 'PATCH', charlie.data.token, {body: 'takeover'})).status, 403);
        assert.equal((await call(`/messages/${replyId}`, 'PATCH', bob.data.token, {body: '  reply after edit  '})).data.message.body, 'reply after edit');
        assert.equal((await call(`/messages/${replyId}`, 'PATCH', bob.data.token, {body: ' '})).status, 400);
        assert.equal((await call('/search?q=before%20edit', 'GET', alice.data.token)).data.messages.length, 0);
        assert.equal((await call('/search?q=after%20edit', 'GET', alice.data.token)).data.messages.length, 1);

        assert.equal((await call(`/messages/${postId}/reactions`, 'POST', charlie.data.token, {emoji: '👍'})).status, 403);
        assert.equal((await call(`/messages/${postId}/reactions`, 'POST', bob.data.token, {emoji: ''})).status, 400);
        assert.equal((await call(`/messages/${postId}/reactions`, 'POST', alice.data.token, {emoji: '👍'})).status, 200);
        assert.equal((await call(`/messages/${postId}/reactions`, 'POST', bob.data.token, {emoji: '👍'})).status, 200);
        assert.equal((await call(`/messages/${postId}/reactions`, 'POST', bob.data.token, {emoji: '👍'})).data.message.reactions[0].count, 2);
        assert.deepEqual((await call(`/channels/${channelId}/messages`, 'GET', alice.data.token)).data.messages[0].reactions, [{emoji: '👍', count: 2, me: true}]);
        assert.deepEqual((await call(`/channels/${channelId}/messages`, 'GET', bob.data.token)).data.messages[0].reactions, [{emoji: '👍', count: 2, me: true}]);
        assert.equal((await call(`/messages/${postId}/reactions/${encodeURIComponent('👍')}`, 'DELETE', charlie.data.token)).status, 403);
        assert.deepEqual((await call(`/messages/${postId}/reactions/${encodeURIComponent('👍')}`, 'DELETE', bob.data.token)).data.message.reactions, [{emoji: '👍', count: 1, me: false}]);

        assert.equal((await call(`/messages/${replyId}`, 'DELETE', alice.data.token)).status, 403);
        assert.equal((await call(`/messages/${replyId}`, 'DELETE', charlie.data.token)).status, 403);
        assert.equal((await call(`/messages/${replyId}`, 'DELETE', bob.data.token)).status, 200);
        assert.equal((await call(`/messages/${replyId}`, 'PATCH', bob.data.token, {body: 'restore'})).status, 404);
        assert.equal((await call(`/messages/${replyId}/reactions`, 'POST', bob.data.token, {emoji: '👍'})).status, 404);
        assert.deepEqual((await call(`/messages/${postId}/thread`, 'GET', alice.data.token)).data.messages.map((message) => message.id), [postId, nested.data.message.id]);
        assert.equal((await call(`/messages/${nested.data.message.id}`, 'DELETE', alice.data.token)).status, 200);
        assert.deepEqual((await call(`/messages/${postId}/thread`, 'GET', alice.data.token)).data.messages.map((message) => message.id), [postId]);
        assert.equal((await call('/search?q=after%20edit', 'GET', alice.data.token)).data.messages.length, 0);

        const created = await call('/channels', 'POST', alice.data.token, {name: 'Project'});
        assert.equal(created.status, 201);
        assert.equal((await call(`/channels/${created.data.channel.id}/messages`, 'GET', bob.data.token)).status, 403);
        assert.equal((await call(`/channels/${created.data.channel.id}/join`, 'POST', bob.data.token)).status, 200);
        assert.equal((await call(`/channels/${created.data.channel.id}/messages`, 'GET', bob.data.token)).status, 200);

        const publicId = created.data.channel.id;
        const sentIds = [];
        for (let index = 0; index < 105; index++) {
            const sent = await call(`/channels/${publicId}/messages`, 'POST', alice.data.token, {body: `message ${index}`});
            assert.equal(sent.status, 201);
            sentIds.push(sent.data.message.id);
        }
        const latest = await call(`/channels/${publicId}/messages?after=0`, 'GET', bob.data.token);
        assert.equal(latest.status, 200);
        assert.deepEqual(latest.data.messages.map((message) => message.id), sentIds.slice(-100));
        const incremental = await call(`/channels/${publicId}/messages?after=${sentIds[103]}`, 'GET', bob.data.token);
        assert.deepEqual(incremental.data.messages.map((message) => message.id), [sentIds[104]]);

        await stop(child);
        child = await start(dbPath, port);
        const login = await call('/login', 'POST', undefined, {identifier: 'alice', password: 'password123'});
        assert.equal(login.status, 200);
        assert.equal((await call(`/channels/${channelId}/messages`, 'GET', login.data.token)).data.messages[0].body, 'private hello');
        assert.deepEqual((await call(`/channels/${channelId}/messages`, 'GET', login.data.token)).data.messages[0].reactions, [{emoji: '👍', count: 1, me: true}]);
    } finally {
        if (child) await stop(child);
        rmSync(directory, {recursive: true, force: true});
    }
});
