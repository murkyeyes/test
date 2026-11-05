const fs = require('node:fs');
const path = require('node:path');
const source = path.join(__dirname, '..', 'hkchat', 'mobile', 'App.tsx');
const destination = path.join(__dirname, 'App.tsx');
let app = fs.readFileSync(source, 'utf8');
const keychainImport = 'import * as Keychain from "react-native-keychain";';
const iconImport = 'require("../../appicon.webp")';
if (!app.includes(keychainImport) || !app.includes(iconImport)) {
  throw new Error('HKchat App.tsx changed: update Expo preview adapter before starting.');
}
app = app.replace(keychainImport, 'import * as Keychain from "./secure-keychain";\nimport Constants from "expo-constants";');
app = app.replace(iconImport, 'require("./assets/hkchat-logo.png")');
const nativeServerDefault = 'let serverUrl =\n    Platform.OS === "android"\n        ? "http://10.0.2.2:8070"\n        : "http://localhost:8070";';
const expoServerDefault = 'const expoHost = Constants.expoConfig?.hostUri?.split(":")[0];\nlet serverUrl = expoHost ? `http://${expoHost}:8070` : "http://localhost:8070";';
if (!app.includes(nativeServerDefault)) {
  throw new Error('HKchat server default changed: update Expo preview adapter.');
}
app = app.replace(nativeServerDefault, expoServerDefault);
app = app.replace('placeholder="http://10.0.2.2:8070"', 'placeholder={serverUrl}');
// SDK 58 no longer accepts the Android-only StatusBar backgroundColor prop.
app = app.replace(/\s+backgroundColor=\{colors\.dark\}(?=\s+barStyle=)/g, '');
fs.writeFileSync(destination, app);
console.log('Expo preview synchronized with hkchat/mobile/App.tsx');
