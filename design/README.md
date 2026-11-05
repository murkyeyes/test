# HKchat – thiết kế màn hình Figma

## Bản bàn giao

- [Mở file Figma trên cloud](https://www.figma.com/design/95mjvVcx7H8xI4mxwJG2OH/HKchat-%E2%80%93-M%C3%A0n-h%C3%ACnh-%E1%BB%A9ng-d%E1%BB%A5ng--b%C3%A1o-c%C3%A1o-) và chọn trang **HKchat – Thiết kế đầy đủ (editable)**.
- `HKchat-editable-screens.fig` là bản dự phòng có thể mở trong Figma Desktop bằng **File → Open local file…** hoặc kéo thả vào Figma.
- `figma-plugin/manifest.json` cùng `code.js` là mã tạo lại các màn hình. Trong Figma Desktop chọn **Plugins → Development → Import plugin from manifest…**, mở manifest, rồi chạy plugin **HKchat Editable Screens**. Mỗi lần chạy sẽ tạo một trang thiết kế mới.
- `figma-enhance-plugin/manifest.json` là plugin bổ sung **HKchat Design System and Prototype**. Chạy plugin này trong cùng file Figma sau khi đã có trang 18 màn hình. Nó tạo trang **HKchat – Design System** gồm Color Styles, Text Styles, component sets và các variants; đồng thời nối các nút của 18 frame thành prototype. Chạy xong chọn frame **01 / Đăng nhập và URL server** và bấm **Present** để thử luồng.

**Cách xem trong Figma:** Ở cột **Pages** chọn **HKchat – Design System** để xem bảng màu, kiểu chữ, spacing và components. Quay về trang **HKchat – Thiết kế đầy đủ (editable)** đầu tiên, chọn frame **01**, mở tab **Prototype** ở bên phải để xem dây nối; bấm **Present** (▶) để thử luồng. Nếu màn hình nhỏ, tăng Zoom từ mức 17%. Chạy nhầm plugin **HKchat Editable Screens** sẽ tạo thêm một trang 18 màn hình trùng lặp; không dùng trang trùng lặp để kiểm tra prototype.

**Kiểm tra prototype:** Chạy lại plugin **HKchat Design System and Prototype** bằng **Plugins → Development**. Thông báo cuối cùng ghi số liên kết đã tạo và số màn hình có thể đi từ **Flow 1**; mục tiêu là đủ **18/18 màn hình** và số liên kết tạo được bằng số dự kiến. Nếu thiếu, chụp lại toàn bộ thông báo (nhất là dòng lỗi đầu) để sửa đúng nút. Trong Present, thử theo thứ tự: **Đăng ký → Đăng nhập → Kênh → Hội thoại nhóm → Tùy chọn tin → Trả lời**; sau đó thử **Tìm kiếm → Kết quả → Mở hội thoại**, **Mọi người → DM**, và **Đăng xuất**. Đây là prototype mô phỏng: nút Đăng nhập đi tiếp mà không xác thực dữ liệu thật.

Ngày 05/11/2026, người dùng đã chạy lại plugin và xác nhận thông báo **18/18 màn hình có thể đi từ Flow 1**. Đây là kết quả kiểm tra đường đi; trước khi nộp vẫn cần bấm thử các luồng trong Present, lưu bản `.fig` mới và xác nhận link Figma mở được bằng tài khoản khác.

Màn hình được ghép từ các layer Figma riêng cho chữ, ô nhập, nút, tab, avatar, bong bóng tin nhắn và hộp thoại. Logo được nhúng từ `expo-preview/assets/hkchat-logo.png`. Trang **Page 1** là ảnh chụp tham chiếu cũ, không phải bản thiết kế để nộp.

## Danh mục 18 trạng thái

| Số | Màn hình/trạng thái | Chức năng minh họa |
| --- | --- | --- |
| 01 | Đăng nhập và URL server | Kết nối server, đăng nhập |
| 02 | Đăng ký tài khoản | Tạo tài khoản |
| 03 | Lỗi địa chỉ server | Xử lý lỗi kết nối |
| 04 | Danh sách kênh | Kênh đang tham gia |
| 05 | Tạo kênh mới | Tạo kênh công khai |
| 06 | Tham gia kênh | Xem và tham gia kênh |
| 07 | Mọi người và bắt đầu DM | Danh sách thành viên |
| 08 | Tin nhắn trực tiếp | Trò chuyện hai người |
| 09 | Hội thoại nhóm | Trò chuyện bốn người |
| 10 | Trả lời tin nhắn | Reply theo tin |
| 11 | Sửa tin nhắn | Sửa tin của mình |
| 12 | Thả cảm xúc | Reaction |
| 13 | Tùy chọn tin nhắn | Menu thao tác tin |
| 14 | Xác nhận xóa tin | Xóa tin của mình |
| 15 | Tìm kiếm | Nhập từ khóa |
| 16 | Kết quả tìm kiếm | Xem kết quả |
| 17 | Mở hội thoại từ kết quả | Điều hướng tới tin |
| 18 | Đăng xuất | Xác nhận thoát |

Đây là 18 trạng thái giao diện của các chức năng có trong `hkchat/mobile/App.tsx`, không phải 18 tuyến điều hướng độc lập. File không mô tả các chức năng chưa được cài trong app.

**Lưu ý đồng bộ:** Figma Desktop đã báo có thay đổi chưa đồng bộ với cloud khi xuất bản. Nếu trang cloud chưa hiện đủ 18 màn hình, mở file `.fig` tại đây; đó là bản đã lưu trên máy. Sau khi chạy plugin bổ sung, dùng **File → Save local copy…** để lưu lại `.fig` mới và kiểm tra link cloud bằng cửa sổ ẩn danh.
