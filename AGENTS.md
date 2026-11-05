# HKchat repository guide

- `hkchat/mobile/App.tsx` là client React Native cho Android và iOS.
- `expo-preview/` là bản Expo Go SDK 58 để test trên iPhone từ Windows; `sync-app.cjs` đồng bộ giao diện từ `hkchat/mobile/App.tsx`.
- `hkchat/server/` là Node.js API và migration SQLite. Không sửa migration đã triển khai; thêm file migration mới cho thay đổi schema.
- `hkchat/compose.yaml` chạy server Docker và lưu database trong volume.
- `README.md` hướng dẫn cài đặt và chạy trên Windows.
- Chạy `npm.cmd run typecheck`, `npm.cmd run test:server` và Android debug build; iOS build cần macOS/Xcode sau khi sửa mã liên quan.
- Dùng tên HKchat và package `com.hkchat.app`. Không đưa lại mã hoặc kết nối tới dịch vụ chat khác.
