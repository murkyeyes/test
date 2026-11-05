# HKchat

HKchat là ứng dụng nhắn tin nội bộ cho doanh nghiệp và nhóm làm việc. Nhân viên trao đổi trong kênh chung, nhóm riêng hoặc tin nhắn trực tiếp; có thể trả lời theo luồng, thả cảm xúc, sửa/xóa tin của mình và tìm kiếm nội dung. Android và iOS client dùng chung mã React Native. API và database SQLite chạy local trong Docker.

## Chạy trên Windows lần đầu

1. Cài Node.js 22.22+ hoặc 24.15+, Docker Desktop, Android Studio và JDK 23. Trong SDK Manager cài Android SDK Platform 36, Build-Tools 36.0.0, Platform-Tools, Emulator và NDK 27.1.12297006. Tạo Android Virtual Device API 30 trở lên. Bản Android đã được build với JDK 23; JDK 25 của Android Studio trên máy thử gây lỗi CMake.
2. Mở Docker Desktop. Mở PowerShell tại thư mục HK-Chat rồi chạy:

```powershell
npm.cmd ci
$env:JAVA_HOME = 'C:\Program Files\Java\jdk-23'
$env:ANDROID_HOME = "$env:USERPROFILE\AppData\Local\Android\Sdk"
docker compose -f hkchat\compose.yaml up -d
curl.exe http://localhost:8070/api/health
```

3. Mở máy ảo Android trong Android Studio và chạy:

```powershell
npm.cmd run android
```

Trong Android Emulator, địa chỉ server mặc định là `http://10.0.2.2:8070`. Nếu dùng điện thoại thật, nhập `http://<IPv4-máy-chạy-Docker>:8070` trên màn hình đăng nhập, mở cổng 8070 trong mạng nội bộ và đặt `HKCHAT_BIND=0.0.0.0` trước khi chạy Compose.

Database mẫu trong `hkchat/backup/hkchat.sqlite` được nạp một lần khi tạo Docker volume mới. Nếu muốn database trống, xóa file backup trước lần đầu chạy. Không chạy `docker compose down -v` nếu muốn giữ tài khoản và tin nhắn.

## Test trên iPhone từ Windows bằng Expo Go

Bản xem thử ở `expo-preview/` dùng cùng mã giao diện và API HKchat. Cách này **không cần Mac hoặc Apple Developer**. App chạy bên trong Expo Go, không tạo file IPA và không cài biểu tượng HKchat riêng trên màn hình chính. Bản Expo Go trên iPhone đã kiểm tra dùng SDK 58, nên bản xem thử có dependency riêng tương thích SDK 58; app Android/iOS native ở thư mục gốc vẫn dùng React Native 0.83.

1. Trên iPhone, cài **Expo Go** từ App Store. Đăng ký/đăng nhập Expo Account trong Expo Go. Kết nối iPhone và Windows vào cùng Wi-Fi riêng.
2. Trên Windows, mở Docker Desktop. Mở PowerShell tại `D:\deploy_web\HK-Chat` và chạy:

```powershell
$env:HKCHAT_BIND = '0.0.0.0'
docker compose -f hkchat\compose.yaml up -d --force-recreate
curl.exe http://localhost:8070/api/health
ipconfig
```

Ghi IPv4 của Wi-Fi, ví dụ `192.168.1.10`. Trên iPhone, mở Safari và thử `http://192.168.1.10:8070/api/health` (thay bằng IP của bạn). Nếu không mở được, cho phép TCP 8070 qua Windows Firewall cho mạng Private. Có thể chạy PowerShell bằng quyền Administrator:

```powershell
New-NetFirewallRule -DisplayName "HKchat API" -Direction Inbound -Action Allow -Protocol TCP -LocalPort 8070 -Profile Private
```

3. Trong một PowerShell khác, chạy bản xem thử. `npm ci` chỉ cần lần đầu hoặc sau khi dependency thay đổi:

```powershell
cd D:\deploy_web\HK-Chat\expo-preview
npm.cmd ci
npx.cmd expo login
npm.cmd run start -- --lan --port 8082
```

Đăng nhập **cùng Expo Account** trên máy tính và Expo Go iPhone. Nếu firewall hỏi, cho phép Node/Expo trên mạng Private; nếu vẫn không quét được QR, cho phép TCP 8082 trên mạng Private. Mở Camera iPhone quét QR trong terminal và chọn mở bằng Expo Go.

4. Khi HKchat hiện màn hình đăng nhập, bản Expo tự điền URL server từ IP đang chạy Metro (ví dụ `http://192.168.1.21:8070`). Kiểm tra ô này trước khi bấm Đăng nhập; nếu IP Windows thay đổi, sửa lại theo `ipconfig`. Không dùng `localhost` hoặc `10.0.2.2` trên iPhone. Đăng nhập hoặc đăng ký, rồi kiểm tra kênh, DM, nhóm, gửi tin, trả lời, reaction, sửa/xóa tin và tìm kiếm.

Mỗi lần chạy `npm.cmd run start`, script tự đồng bộ `hkchat/mobile/App.tsx` vào bản xem thử. Phiên đăng nhập của Expo Go được lưu bằng Expo SecureStore. Chỉ chạy server HTTP trên mạng Wi-Fi riêng khi kiểm thử.

## Build bản iOS native trên Mac

Project iOS nằm trong `ios/HKchat.xcodeproj`. Windows không chạy Xcode và không thể build/cài ứng dụng React Native native trực tiếp lên iPhone. Bạn cần mượn một máy Mac, hoặc dùng dịch vụ build iOS có tài khoản Apple Developer và cấu hình ký app. Tài khoản Apple cá nhân miễn phí có thể ký để chạy trên iPhone của chính bạn bằng Xcode; bản cài thử này có thời hạn và phải ký lại định kỳ.

1. Trên Windows, mở Docker Desktop và PowerShell tại thư mục dự án:

```powershell
$env:HKCHAT_BIND = '0.0.0.0'
docker compose -f hkchat\compose.yaml up -d --force-recreate
curl.exe http://localhost:8070/api/health
ipconfig
```

Ghi địa chỉ IPv4 của máy Windows trên Wi-Fi (ví dụ `192.168.1.10`). Cho phép TCP 8070 qua Windows Firewall trên mạng Private. Chỉ dùng mạng Wi-Fi riêng để thử vì API local dùng HTTP.

2. Chép **toàn bộ** thư mục `HK-Chat` sang Mac, bỏ qua `node_modules`, `android/build` và `ios/Pods`. Cài Xcode bản hỗ trợ iOS của điện thoại, Xcode Command Line Tools, Node.js phù hợp `package.json`, Ruby/Bundler và CocoaPods. Trên Mac, tại thư mục gốc:

```bash
npm ci
bundle install
cd ios
bundle exec pod install
cd ..
npx react-native start --host 0.0.0.0
```

3. Kết nối iPhone với Mac bằng cáp, xác nhận **Trust This Computer** và bật **Developer Mode** trên iPhone nếu máy yêu cầu. Mở `ios/HKchat.xcworkspace` bằng Xcode. Chọn target **HKchat** → **Signing & Capabilities** → bật **Automatically manage signing** → chọn **Personal Team** của Apple Account đã đăng nhập trong Xcode. Nếu bundle ID `com.hkchat.app` không khả dụng với Team của bạn, đổi nó thành ID riêng trong Xcode.

4. Chọn iPhone trong danh sách thiết bị của Xcode rồi bấm **Run** (▶). Giữ Metro ở bước 2 đang chạy trên Mac và cho phép cổng 8081 qua firewall của Mac nếu được hỏi. Khi mở app, tại màn hình đăng nhập, điền URL server là `http://<IPv4-Windows>:8070` (ví dụ `http://192.168.1.10:8070`). iPhone và Windows phải ở cùng Wi-Fi; mở URL `http://<IPv4-Windows>:8070/api/health` trong Safari để kiểm tra mạng trước khi đăng nhập. Nếu iPhone hỏi quyền **Local Network**, chọn **Allow**.

5. Đăng nhập bằng tài khoản mẫu đã có trong database hoặc đăng ký tài khoản mới. Thử mở kênh, gửi tin, tạo DM/nhóm, trả lời, thả cảm xúc và tìm kiếm. Các bước kiểm thử chi tiết nằm trong `hkchat/README.md`.

Project iOS đã được chuẩn bị trên Windows và kiểm tra cấu hình tĩnh. Bản build Xcode và chạy trên iPhone cần được xác nhận trên Mac.

## Kiểm tra và build APK

```powershell
npm.cmd run typecheck
npm.cmd run test:server
cd android
.\gradlew.bat :app:assembleDebug
```

APK debug nằm ở `android/app/build/outputs/apk/debug/app-debug.apk`. Bản debug dùng Metro khi mở app. APK demo có sẵn bundle ở `artifacts/HKchat-demo.apk`; nó được ký bằng khóa debug của bộ khung và chỉ dùng thử nội bộ. Có thể build lại bằng `cd android; .\gradlew.bat :app:assembleRelease` khi đã đặt `JAVA_HOME` như trên. Để chạy backend những lần sau: `docker compose -f hkchat\compose.yaml up -d` từ gốc dự án, mở emulator rồi `npm.cmd run android`.

## Chức năng hiện có

Đăng ký, đăng nhập, kênh công khai, nhóm riêng, DM, nhắn tin, reply, reaction, sửa/xóa tin, tìm kiếm và lưu phiên. Các thành phần gọi thoại, push khi app đóng, tệp đính kèm, quản trị, AI và playbook chưa được triển khai trong bản HKchat độc lập. Xem [hkchat/README.md](hkchat/README.md) để biết API và schema.

## Tài liệu báo cáo

Ảnh minh họa ở `docs/report-images/`; báo cáo dùng để nộp ở `docs/bao-cao-bai-tap-lon-HK-chat.docx` (có bản sao `docs/bao-cao-HKchat-ban-nop.docx`). Bộ ảnh case study để đăng Behance ở `design/behance-case-study/panels/`.
