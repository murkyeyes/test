import React, { useCallback, useEffect, useState } from "react";
import {
    ActivityIndicator,
    Alert,
    FlatList,
    Image,
    KeyboardAvoidingView,
    Platform,
    Pressable,
    SafeAreaView,
    ScrollView,
    StatusBar,
    StyleSheet,
    Text,
    TextInput,
    View,
} from "react-native";
import * as Keychain from "react-native-keychain";

type User = { id: string; username: string; email?: string };
type Channel = { id: string; name: string; kind: "public" | "dm" | "group" };
type Message = {
    id: number;
    channelId: string;
    userId: string;
    username: string;
    body: string;
    replyTo?: number | null;
    reactions?: Array<{ emoji: string; count: number; me: boolean }>;
};
type Page = "channels" | "people" | "search";
let serverUrl =
    Platform.OS === "android"
        ? "http://10.0.2.2:8070"
        : "http://localhost:8070";
const colors = {
    dark: "#301542",
    text: "#37213F",
    accent: "#A81C7F",
    pink: "#F553AB",
    pale: "#FFD1E9",
    muted: "#796B82",
    border: "#EADCEB",
};

async function api<T>(
    path: string,
    method: string,
    token?: string,
    payload?: object,
): Promise<T> {
    const response = await fetch(`${serverUrl}/api${path}`, {
        method,
        headers: {
            "content-type": "application/json",
            ...(token ? { authorization: `Bearer ${token}` } : {}),
        },
        body: payload ? JSON.stringify(payload) : undefined,
    });
    const data = await response.json();
    if (!response.ok) {
        throw new Error(data.error || `HTTP ${response.status}`);
    }
    return data as T;
}

function Action({
    label,
    onPress,
    disabled,
}: {
    label: string;
    onPress: () => void;
    disabled?: boolean;
}) {
    return (
        <Pressable
            accessibilityRole="button"
            disabled={disabled}
            onPress={onPress}
            style={[styles.action, disabled && { opacity: 0.5 }]}
        >
            <Text style={styles.actionText}>{label}</Text>
        </Pressable>
    );
}

export default function HKchatApp() {
    const [token, setToken] = useState<string>();
    const [user, setUser] = useState<User>();
    const [loading, setLoading] = useState(true);
    const [busy, setBusy] = useState(false);
    const [error, setError] = useState("");
    const [register, setRegister] = useState(false);
    const [username, setUsername] = useState("");
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [serverAddress, setServerAddress] = useState(serverUrl);
    const [page, setPage] = useState<Page>("channels");
    const [channels, setChannels] = useState<Channel[]>([]);
    const [available, setAvailable] = useState<Channel[]>([]);
    const [people, setPeople] = useState<User[]>([]);
    const [current, setCurrent] = useState<Channel>();
    const [messages, setMessages] = useState<Message[]>([]);
    const [draft, setDraft] = useState("");
    const [replyTo, setReplyTo] = useState<Message>();
    const [editing, setEditing] = useState<Message>();
    const [emojiPicker, setEmojiPicker] = useState<number>();
    const [newChannel, setNewChannel] = useState("");
    const [query, setQuery] = useState("");
    const [results, setResults] = useState<Message[]>([]);
    const showError = (reason: unknown) =>
        setError(reason instanceof Error ? reason.message : "Có lỗi xảy ra");

    const refreshChannels = useCallback(async (session: string) => {
        const [mine, publicChannels] = await Promise.all([
            api<{ channels: Channel[] }>("/channels", "GET", session),
            api<{ channels: Channel[] }>("/channels/public", "GET", session),
        ]);
        setChannels(mine.channels);
        setAvailable(publicChannels.channels);
    }, []);

    useEffect(() => {
        let active = true;
        (async () => {
            try {
                const savedServer = await Keychain.getGenericPassword({
                    service: "hkchat.server",
                });
                if (savedServer && active) {
                    serverUrl = savedServer.password;
                    setServerAddress(serverUrl);
                }
                const saved = await Keychain.getGenericPassword({
                    service: "hkchat.local",
                });
                if (saved && active) {
                    const data = await api<{ user: User }>(
                        "/me",
                        "GET",
                        saved.password,
                    );
                    setUser(data.user);
                    setToken(saved.password);
                    await refreshChannels(saved.password);
                }
            } catch {
                await Keychain.resetGenericPassword({
                    service: "hkchat.local",
                });
            } finally {
                if (active) {
                    setLoading(false);
                }
            }
        })();
        return () => {
            active = false;
        };
    }, [refreshChannels]);

    useEffect(() => {
        if (!token || !current) {
            return;
        }
        let active = true;
        setMessages([]);
        setDraft("");
        setReplyTo(undefined);
        setEditing(undefined);
        setEmojiPicker(undefined);
        const poll = async () => {
            try {
                const data = await api<{ messages: Message[] }>(
                    `/channels/${current.id}/messages?after=0`,
                    "GET",
                    token,
                );
                if (!active) {
                    return;
                }
                setMessages(data.messages);
            } catch (reason) {
                if (active) {
                    showError(reason);
                }
            }
        };
        poll();
        const timer = setInterval(poll, 2000);
        return () => {
            active = false;
            clearInterval(timer);
        };
    }, [token, current]);

    const authenticate = async () => {
        setBusy(true);
        setError("");
        try {
            const address = serverAddress.trim().replace(/\/$/, "");
            if (!/^https?:\/\/[^/\s]+$/i.test(address)) {
                throw new Error("Địa chỉ server phải có dạng http://IP:8070");
            }
            serverUrl = address;
            const data = register
                ? await api<{ user: User; token: string }>(
                      "/register",
                      "POST",
                      undefined,
                      {
                          username,
                          email,
                          password,
                      },
                  )
                : await api<{ user: User; token: string }>(
                      "/login",
                      "POST",
                      undefined,
                      {
                          identifier: username,
                          password,
                      },
                  );
            await Keychain.setGenericPassword("session", data.token, {
                service: "hkchat.local",
            });
            await Keychain.setGenericPassword("server", address, {
                service: "hkchat.server",
            });
            setUser(data.user);
            setToken(data.token);
            setPassword("");
            await refreshChannels(data.token);
        } catch (reason) {
            showError(reason);
        } finally {
            setBusy(false);
        }
    };

    const logout = () =>
        Alert.alert("Đăng xuất", "Bạn muốn đăng xuất khỏi HKchat?", [
            { text: "Hủy", style: "cancel" },
            {
                text: "Đăng xuất",
                onPress: async () => {
                    try {
                        if (token) {
                            await api("/logout", "POST", token);
                        }
                    } catch {
                        /* Clear the local session anyway. */
                    }
                    await Keychain.resetGenericPassword({
                        service: "hkchat.local",
                    });
                    setToken(undefined);
                    setUser(undefined);
                    setCurrent(undefined);
                    setMessages([]);
                },
            },
        ]);

    const openPage = async (next: Page) => {
        setPage(next);
        setError("");
        if (!token) {
            return;
        }
        try {
            if (next === "channels") {
                await refreshChannels(token);
            }
            if (next === "people") {
                setPeople(
                    (await api<{ users: User[] }>("/users", "GET", token))
                        .users,
                );
            }
        } catch (reason) {
            showError(reason);
        }
    };

    const createChannel = async () => {
        if (!token || !newChannel.trim()) {
            return;
        }
        try {
            const data = await api<{ channel: Channel }>(
                "/channels",
                "POST",
                token,
                {
                    name: newChannel.trim(),
                },
            );
            setNewChannel("");
            await refreshChannels(token);
            setCurrent(data.channel);
        } catch (reason) {
            showError(reason);
        }
    };
    const joinChannel = async (channel: Channel) => {
        if (!token) {
            return;
        }
        try {
            await api(`/channels/${channel.id}/join`, "POST", token);
            await refreshChannels(token);
            setAvailable((previous) =>
                previous.filter((item) => item.id !== channel.id),
            );
            setCurrent(channel);
        } catch (reason) {
            showError(reason);
        }
    };
    const openDm = async (person: User) => {
        if (!token) {
            return;
        }
        try {
            const data = await api<{ channel: Channel }>("/dm", "POST", token, {
                userId: person.id,
            });
            await refreshChannels(token);
            setCurrent(data.channel);
        } catch (reason) {
            showError(reason);
        }
    };
    const send = async () => {
        const body = draft.trim();
        if (!token || !current || !body) {
            return;
        }
        setDraft("");
        try {
            if (editing) {
                await api(`/messages/${editing.id}`, "PATCH", token, { body });
                setEditing(undefined);
            } else {
                await api(`/channels/${current.id}/messages`, "POST", token, {
                    body,
                    ...(replyTo ? { replyTo: replyTo.id } : {}),
                });
                setReplyTo(undefined);
            }
            setMessages(
                (
                    await api<{ messages: Message[] }>(
                        `/channels/${current.id}/messages?after=0`,
                        "GET",
                        token,
                    )
                ).messages,
            );
        } catch (reason) {
            setDraft(body);
            showError(reason);
        }
    };

    const refreshMessages = async () => {
        if (!token || !current) {
            return;
        }
        setMessages(
            (
                await api<{ messages: Message[] }>(
                    `/channels/${current.id}/messages?after=0`,
                    "GET",
                    token,
                )
            ).messages,
        );
    };

    const reactTo = async (message: Message, emoji: string) => {
        if (!token) {
            return;
        }
        try {
            const mine = message.reactions?.find(
                (reaction) => reaction.emoji === emoji,
            )?.me;
            await api(
                `/messages/${message.id}/reactions${mine ? `/${encodeURIComponent(emoji)}` : ""}`,
                mine ? "DELETE" : "POST",
                token,
                mine ? undefined : { emoji },
            );
            await refreshMessages();
        } catch (reason) {
            showError(reason);
        }
    };

    const messageActions = (message: Message) => {
        const reply = () => {
            setEditing(undefined);
            setReplyTo(message);
            setDraft("");
        };
        if (message.userId !== user?.id) {
            Alert.alert("Tin nhắn", message.body, [
                { text: "Hủy", style: "cancel" },
                { text: "Trả lời", onPress: reply },
            ]);
            return;
        }
        Alert.alert("Tin nhắn", message.body, [
            { text: "Trả lời", onPress: reply },
            {
                text: "Sửa",
                onPress: () => {
                    setReplyTo(undefined);
                    setEditing(message);
                    setDraft(message.body);
                },
            },
            {
                text: "Thêm",
                onPress: () =>
                    Alert.alert("Tin nhắn", "", [
                        { text: "Hủy", style: "cancel" },
                        {
                            text: "Xóa",
                            style: "destructive",
                            onPress: () =>
                                Alert.alert(
                                    "Xóa tin nhắn?",
                                    "Không thể hoàn tác",
                                    [
                                        { text: "Hủy", style: "cancel" },
                                        {
                                            text: "Xóa",
                                            style: "destructive",
                                            onPress: async () => {
                                                if (!token) {
                                                    return;
                                                }
                                                try {
                                                    await api(
                                                        `/messages/${message.id}`,
                                                        "DELETE",
                                                        token,
                                                    );
                                                    await refreshMessages();
                                                } catch (reason) {
                                                    showError(reason);
                                                }
                                            },
                                        },
                                    ],
                                ),
                        },
                    ]),
            },
        ]);
    };
    const search = async () => {
        if (!token) {
            return;
        }
        try {
            setResults(
                (
                    await api<{ messages: Message[] }>(
                        `/search?q=${encodeURIComponent(query)}`,
                        "GET",
                        token,
                    )
                ).messages,
            );
        } catch (reason) {
            showError(reason);
        }
    };

    if (loading) {
        return (
            <View style={styles.loading}>
                <ActivityIndicator color={colors.pink} size="large" />
            </View>
        );
    }
    if (!token || !user) {
        return (
            <SafeAreaView style={styles.authScreen}>
                <StatusBar
                    backgroundColor={colors.dark}
                    barStyle="light-content"
                />
                <ScrollView
                    contentContainerStyle={styles.authContent}
                    keyboardShouldPersistTaps="handled"
                >
                    <Image
                        source={require("../../appicon.webp")}
                        style={styles.logo}
                    />
                    <Text style={styles.brand}>HKchat</Text>
                    <Text style={styles.subtitle}>
                        Không gian trò chuyện của riêng bạn
                    </Text>
                    <View style={styles.card}>
                        <Text style={styles.heading}>
                            {register ? "Tạo tài khoản" : "Đăng nhập"}
                        </Text>
                        <TextInput
                            accessibilityLabel="Địa chỉ server HKchat"
                            autoCapitalize="none"
                            autoCorrect={false}
                            keyboardType="url"
                            placeholder="http://10.0.2.2:8070"
                            placeholderTextColor={colors.muted}
                            style={styles.input}
                            value={serverAddress}
                            onChangeText={setServerAddress}
                        />
                        <TextInput
                            accessibilityLabel="Tên đăng nhập hoặc email"
                            autoCapitalize="none"
                            placeholder={
                                register
                                    ? "Tên đăng nhập"
                                    : "Tên đăng nhập hoặc email"
                            }
                            placeholderTextColor={colors.muted}
                            style={styles.input}
                            value={username}
                            onChangeText={setUsername}
                        />
                        {register && (
                            <TextInput
                                accessibilityLabel="Email"
                                autoCapitalize="none"
                                keyboardType="email-address"
                                placeholder="Email"
                                placeholderTextColor={colors.muted}
                                style={styles.input}
                                value={email}
                                onChangeText={setEmail}
                            />
                        )}
                        <TextInput
                            accessibilityLabel="Mật khẩu"
                            placeholder="Mật khẩu"
                            placeholderTextColor={colors.muted}
                            secureTextEntry={true}
                            style={styles.input}
                            value={password}
                            onChangeText={setPassword}
                        />
                        {Boolean(error) && (
                            <Text style={styles.error}>{error}</Text>
                        )}
                        <Action
                            label={
                                busy
                                    ? "Đang xử lý..."
                                    : register
                                      ? "Đăng ký"
                                      : "Đăng nhập"
                            }
                            onPress={authenticate}
                            disabled={busy}
                        />
                        <Pressable
                            onPress={() => {
                                setError("");
                                setRegister(!register);
                            }}
                        >
                            <Text style={styles.link}>
                                {register
                                    ? "Đã có tài khoản? Đăng nhập"
                                    : "Chưa có tài khoản? Đăng ký"}
                            </Text>
                        </Pressable>
                    </View>
                    <Text style={styles.hint}>Server: {serverAddress}</Text>
                </ScrollView>
            </SafeAreaView>
        );
    }

    return (
        <SafeAreaView style={styles.screen}>
            <StatusBar backgroundColor={colors.dark} barStyle="light-content" />
            <View style={styles.header}>
                <View>
                    <Text style={styles.headerTitle}>
                        {current ? current.name : "HKchat"}
                    </Text>
                    <Text style={styles.headerSub}>
                        Xin chào, {user.username}
                    </Text>
                </View>
                <Pressable
                    accessibilityRole="button"
                    onPress={current ? () => setCurrent(undefined) : logout}
                >
                    <Text style={styles.headerAction}>
                        {current ? "Trở lại" : "Đăng xuất"}
                    </Text>
                </Pressable>
            </View>
            {Boolean(error) && (
                <Pressable onPress={() => setError("")}>
                    <Text style={styles.banner}>{error} ×</Text>
                </Pressable>
            )}
            {current ? (
                <KeyboardAvoidingView
                    behavior={Platform.OS === "ios" ? "padding" : undefined}
                    style={styles.fill}
                >
                    <FlatList
                        data={messages}
                        keyExtractor={(item) => String(item.id)}
                        contentContainerStyle={styles.messages}
                        renderItem={({ item }) => (
                            <Pressable
                                accessibilityLabel={`Tin nhắn của ${item.username}: ${item.body}. Nhấn giữ để xem tùy chọn`}
                                onLongPress={() => messageActions(item)}
                                style={[
                                    styles.bubble,
                                    item.userId === user.id && styles.ownBubble,
                                ]}
                            >
                                <Text style={styles.author}>
                                    {item.username}
                                </Text>
                                {item.replyTo ? (
                                    <Text style={styles.replySnippet}>
                                        ↳{" "}
                                        {messages.find(
                                            (message) =>
                                                message.id === item.replyTo,
                                        )?.body || "Tin nhắn trước"}
                                    </Text>
                                ) : null}
                                <Text style={styles.body}>{item.body}</Text>
                                <View style={styles.reactionRow}>
                                    {item.reactions?.map((reaction) => (
                                        <Pressable
                                            key={reaction.emoji}
                                            accessibilityLabel={`${reaction.emoji} ${reaction.count}`}
                                            onPress={() =>
                                                reactTo(item, reaction.emoji)
                                            }
                                            style={[
                                                styles.reaction,
                                                reaction.me &&
                                                    styles.ownReaction,
                                            ]}
                                        >
                                            <Text>
                                                {reaction.emoji}{" "}
                                                {reaction.count}
                                            </Text>
                                        </Pressable>
                                    ))}
                                    <Pressable
                                        accessibilityLabel="Thả cảm xúc"
                                        onPress={() =>
                                            setEmojiPicker(
                                                emojiPicker === item.id
                                                    ? undefined
                                                    : item.id,
                                            )
                                        }
                                        style={styles.reaction}
                                    >
                                        <Text>＋</Text>
                                    </Pressable>
                                </View>
                                {emojiPicker === item.id && (
                                    <View style={styles.reactionRow}>
                                        {["👍", "❤️", "😂", "🎉"].map(
                                            (emoji) => (
                                                <Pressable
                                                    key={emoji}
                                                    onPress={() => {
                                                        setEmojiPicker(
                                                            undefined,
                                                        );
                                                        reactTo(item, emoji);
                                                    }}
                                                    style={styles.reaction}
                                                >
                                                    <Text>{emoji}</Text>
                                                </Pressable>
                                            ),
                                        )}
                                    </View>
                                )}
                            </Pressable>
                        )}
                    />
                    {(replyTo || editing) && (
                        <View style={styles.contextBar}>
                            <Text numberOfLines={1} style={styles.contextText}>
                                {editing
                                    ? `Sửa: ${editing.body}`
                                    : `Trả lời ${replyTo?.username}: ${replyTo?.body}`}
                            </Text>
                            <Pressable
                                accessibilityLabel="Hủy trả lời hoặc sửa"
                                onPress={() => {
                                    setReplyTo(undefined);
                                    setEditing(undefined);
                                    setDraft("");
                                }}
                            >
                                <Text style={styles.contextClose}>×</Text>
                            </Pressable>
                        </View>
                    )}
                    <View style={styles.composer}>
                        <TextInput
                            accessibilityLabel="Nội dung tin nhắn"
                            multiline={true}
                            placeholder={
                                editing ? "Sửa tin nhắn..." : "Viết tin nhắn..."
                            }
                            placeholderTextColor={colors.muted}
                            style={styles.composerInput}
                            value={draft}
                            onChangeText={setDraft}
                        />
                        <Pressable
                            accessibilityRole="button"
                            onPress={send}
                            style={styles.send}
                        >
                            <Text style={styles.sendText}>
                                {editing ? "Lưu" : "Gửi"}
                            </Text>
                        </Pressable>
                    </View>
                </KeyboardAvoidingView>
            ) : (
                <>
                    <View style={styles.tabs}>
                        {(["channels", "people", "search"] as const).map(
                            (item) => (
                                <Pressable
                                    key={item}
                                    onPress={() => openPage(item)}
                                    style={[
                                        styles.tab,
                                        page === item && styles.activeTab,
                                    ]}
                                >
                                    <Text
                                        style={[
                                            styles.tabText,
                                            page === item &&
                                                styles.activeTabText,
                                        ]}
                                    >
                                        {item === "channels"
                                            ? "Kênh"
                                            : item === "people"
                                              ? "Mọi người"
                                              : "Tìm kiếm"}
                                    </Text>
                                </Pressable>
                            ),
                        )}
                    </View>
                    <ScrollView
                        style={styles.fill}
                        contentContainerStyle={styles.list}
                        keyboardShouldPersistTaps="handled"
                    >
                        {page === "channels" && (
                            <>
                                <Text style={styles.section}>Kênh của tôi</Text>
                                {channels.map((channel) => (
                                    <Pressable
                                        key={channel.id}
                                        onPress={() => setCurrent(channel)}
                                        style={styles.row}
                                    >
                                        <Text style={styles.rowIcon}>
                                            {channel.kind === "public" ? "#" : "●"}
                                        </Text>
                                        <Text style={styles.rowText}>
                                            {channel.name}
                                        </Text>
                                        <Text style={styles.chevron}>›</Text>
                                    </Pressable>
                                ))}
                                <Text style={styles.section}>Tạo kênh</Text>
                                <TextInput
                                    accessibilityLabel="Tên kênh mới"
                                    placeholder="Tên kênh mới"
                                    placeholderTextColor={colors.muted}
                                    style={styles.input}
                                    value={newChannel}
                                    onChangeText={setNewChannel}
                                />
                                <Action
                                    label="Tạo kênh"
                                    onPress={createChannel}
                                />
                                {available.length > 0 && (
                                    <Text style={styles.section}>
                                        Kênh có thể tham gia
                                    </Text>
                                )}
                                {available.map((channel) => (
                                    <Pressable
                                        key={channel.id}
                                        onPress={() => joinChannel(channel)}
                                        style={styles.row}
                                    >
                                        <Text style={styles.rowIcon}>#</Text>
                                        <Text style={styles.rowText}>
                                            {channel.name}
                                        </Text>
                                        <Text style={styles.chevron}>
                                            Tham gia
                                        </Text>
                                    </Pressable>
                                ))}
                            </>
                        )}
                        {page === "people" && (
                            <>
                                <Text style={styles.section}>
                                    Bắt đầu tin nhắn trực tiếp
                                </Text>
                                {people.map((person) => (
                                    <Pressable
                                        key={person.id}
                                        onPress={() => openDm(person)}
                                        style={styles.row}
                                    >
                                        <Text style={styles.avatar}>
                                            {person.username
                                                .slice(0, 1)
                                                .toUpperCase()}
                                        </Text>
                                        <Text style={styles.rowText}>
                                            {person.username}
                                        </Text>
                                        <Text style={styles.chevron}>›</Text>
                                    </Pressable>
                                ))}
                            </>
                        )}
                        {page === "search" && (
                            <>
                                <Text style={styles.section}>Tìm tin nhắn</Text>
                                <TextInput
                                    accessibilityLabel="Từ khóa tìm kiếm"
                                    placeholder="Nhập từ khóa"
                                    placeholderTextColor={colors.muted}
                                    style={styles.input}
                                    value={query}
                                    onChangeText={setQuery}
                                    onSubmitEditing={search}
                                />
                                <Action label="Tìm kiếm" onPress={search} />
                                {results.map((message) => (
                                    <Pressable
                                        key={message.id}
                                        style={styles.result}
                                        onPress={() => {
                                            const channel = channels.find(
                                                (item) =>
                                                    item.id ===
                                                    message.channelId,
                                            );
                                            if (channel) {
                                                setCurrent(channel);
                                            }
                                        }}
                                    >
                                        <Text style={styles.author}>
                                            {message.username}
                                        </Text>
                                        <Text style={styles.body}>
                                            {message.body}
                                        </Text>
                                    </Pressable>
                                ))}
                            </>
                        )}
                    </ScrollView>
                </>
            )}
        </SafeAreaView>
    );
}

const styles = StyleSheet.create({
    fill: { flex: 1 },
    loading: {
        flex: 1,
        backgroundColor: colors.dark,
        justifyContent: "center",
    },
    authScreen: { flex: 1, backgroundColor: colors.dark },
    authContent: {
        flexGrow: 1,
        alignItems: "center",
        justifyContent: "center",
        padding: 22,
    },
    logo: { width: 150, height: 150, borderRadius: 32 },
    brand: { color: "white", fontSize: 38, fontWeight: "800", marginTop: 8 },
    subtitle: { color: colors.pale, marginBottom: 24 },
    card: {
        backgroundColor: "white",
        borderRadius: 24,
        padding: 22,
        width: "100%",
    },
    heading: {
        color: colors.text,
        fontSize: 25,
        fontWeight: "700",
        marginBottom: 18,
    },
    input: {
        backgroundColor: "#F9F5F9",
        borderWidth: 1,
        borderColor: colors.border,
        borderRadius: 13,
        color: colors.text,
        paddingHorizontal: 14,
        paddingVertical: 12,
        fontSize: 16,
        marginBottom: 12,
    },
    action: {
        backgroundColor: colors.accent,
        borderRadius: 13,
        paddingVertical: 14,
        alignItems: "center",
        marginVertical: 5,
    },
    actionText: { color: "white", fontSize: 16, fontWeight: "700" },
    link: {
        color: colors.accent,
        textAlign: "center",
        marginTop: 15,
        fontWeight: "600",
    },
    hint: { color: colors.pale, fontSize: 12, marginTop: 20 },
    error: { color: "#B42318", marginBottom: 10 },
    screen: { flex: 1, backgroundColor: "white" },
    header: {
        backgroundColor: colors.dark,
        paddingHorizontal: 18,
        paddingVertical: 14,
        flexDirection: "row",
        justifyContent: "space-between",
        alignItems: "center",
    },
    headerTitle: { color: "white", fontSize: 23, fontWeight: "700" },
    headerSub: { color: colors.pale, fontSize: 12 },
    headerAction: { color: colors.pale, fontWeight: "700" },
    banner: { backgroundColor: "#FEE4E2", color: "#B42318", padding: 10 },
    tabs: {
        flexDirection: "row",
        borderBottomWidth: 1,
        borderBottomColor: colors.border,
    },
    tab: { flex: 1, alignItems: "center", paddingVertical: 15 },
    activeTab: { borderBottomWidth: 3, borderBottomColor: colors.pink },
    tabText: { color: colors.muted, fontWeight: "600" },
    activeTabText: { color: colors.accent },
    list: { padding: 18 },
    section: {
        color: colors.text,
        fontSize: 18,
        fontWeight: "700",
        marginTop: 18,
        marginBottom: 12,
    },
    row: {
        minHeight: 62,
        flexDirection: "row",
        alignItems: "center",
        borderBottomWidth: 1,
        borderBottomColor: colors.border,
    },
    rowIcon: { color: colors.accent, fontSize: 24, width: 36 },
    rowText: { flex: 1, color: colors.text, fontSize: 17 },
    chevron: { color: colors.muted, fontSize: 18 },
    avatar: {
        backgroundColor: colors.pale,
        color: colors.accent,
        borderRadius: 18,
        width: 36,
        height: 36,
        textAlign: "center",
        textAlignVertical: "center",
        marginRight: 10,
        fontWeight: "700",
    },
    messages: { padding: 16 },
    bubble: {
        alignSelf: "flex-start",
        backgroundColor: "#F7F2F7",
        borderRadius: 16,
        padding: 12,
        marginBottom: 10,
        maxWidth: "85%",
    },
    ownBubble: { alignSelf: "flex-end", backgroundColor: colors.pale },
    author: {
        color: colors.accent,
        fontSize: 12,
        fontWeight: "700",
        marginBottom: 4,
    },
    body: { color: colors.text, fontSize: 16 },
    replySnippet: {
        color: colors.muted,
        borderLeftWidth: 2,
        borderLeftColor: colors.accent,
        paddingLeft: 6,
        marginBottom: 4,
    },
    reactionRow: { flexDirection: "row", flexWrap: "wrap", marginTop: 5 },
    reaction: {
        borderWidth: 1,
        borderColor: colors.border,
        borderRadius: 12,
        paddingHorizontal: 7,
        paddingVertical: 3,
        marginRight: 4,
    },
    ownReaction: { borderColor: colors.accent, backgroundColor: "#FFF0F8" },
    contextBar: {
        flexDirection: "row",
        alignItems: "center",
        paddingHorizontal: 14,
        paddingVertical: 7,
        backgroundColor: "#F7F2F7",
    },
    contextText: { color: colors.text, flex: 1 },
    contextClose: { color: colors.accent, fontSize: 22, paddingHorizontal: 8 },
    composer: {
        borderTopWidth: 1,
        borderTopColor: colors.border,
        flexDirection: "row",
        padding: 10,
        alignItems: "flex-end",
    },
    composerInput: {
        flex: 1,
        color: colors.text,
        fontSize: 16,
        minHeight: 42,
        maxHeight: 110,
        paddingHorizontal: 10,
    },
    send: {
        backgroundColor: colors.accent,
        borderRadius: 12,
        paddingHorizontal: 18,
        paddingVertical: 11,
    },
    sendText: { color: "white", fontWeight: "700" },
    result: {
        padding: 14,
        borderBottomWidth: 1,
        borderBottomColor: colors.border,
    },
});
