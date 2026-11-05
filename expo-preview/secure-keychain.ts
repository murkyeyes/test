import * as SecureStore from "expo-secure-store";

type Options = { service: string };

export async function getGenericPassword({ service }: Options) {
    const value = await SecureStore.getItemAsync(service);
    return value === null ? false : { username: service, password: value };
}

export async function setGenericPassword(
    _username: string,
    password: string,
    { service }: Options,
) {
    await SecureStore.setItemAsync(service, password);
    return true;
}

export async function resetGenericPassword({ service }: Options) {
    await SecureStore.deleteItemAsync(service);
    return true;
}
