# HKchat — ma trận phạm vi MVP

Tài liệu này nối từng nhu cầu với chức năng, mã nguồn và bằng chứng. “Có” nghĩa là luồng đang có trong code; nó không thay thế kiểm thử sử dụng trên nhiều thiết bị hoặc khảo sát người dùng.

| Nỗi đau / nhu cầu | Phản hồi của MVP | Client | API / dữ liệu | Bằng chứng hiện có |
| --- | --- | --- | --- | --- |
| Chủ đề trao đổi bị trộn | Kênh công khai và DM/nhóm tách hội thoại | Tab Kênh, Mọi người | `channels`, `channel_members`, `group_chats`; routes channels/DM | `02-danh-sach-kenh-nhom.png`, test server |
| Phản hồi mất ngữ cảnh | Trả lời gắn tin gốc bằng `replyTo` | Màn hội thoại, thao tác Trả lời | `messages.reply_to`; routes messages/thread | `04-tra-loi-trong-hoi-thoai.png`, test server |
| Khó tìm lại nội dung cũ | Tìm từ khóa trong những hội thoại có quyền | Tab Tìm kiếm | `/api/search`, kiểm tra `channel_members` | `05-tim-kiem-tin-nhan.png`, `06-mo-lai-hoi-thoai.png`, test server |
| Người ngoài xem tin riêng | Chỉ thành viên được đọc/gửi/tìm trong hội thoại | Kênh/DM | Kiểm tra membership; trả `403` | Test server về quyền DM |
| Cần chỉnh tin hoặc phản ứng | Sửa/xóa tin tác giả; thêm/bỏ cảm xúc | Màn hội thoại | Routes messages/reactions | Test server |
| Cần dữ liệu khi chạy lại demo | SQLite trong Docker volume | Client gọi API local | `hkchat/compose.yaml`, migrations SQL | Test restart server |

## Trạng thái tính năng ngoài phạm vi

- **Push notification:** chưa cấu hình Firebase/Apple và chưa có luồng push hoạt động. Polling 2 giây chỉ làm mới khi app đang xem hội thoại.
- **Tìm kiếm mở đúng tin:** API trả kết quả đúng quyền; client hiện chỉ mở kênh chứa tin và chưa tự cuộn tới tin.
- **Tạo nhóm bằng app:** API tạo nhóm đã có; giao diện hiện chỉ mở nhóm mẫu hoặc các nhóm người dùng đã tham gia.
- **Tệp, cuộc gọi, AI, playbook:** sự hiện diện của bảng schema không chứng minh tính năng chạy được. Các mục này không được tính là MVP đã nghiệm thu.
- **iOS native:** bản xem thử trên iPhone dùng Expo Go; build native cần macOS/Xcode.

## Điểm kiểm tra khi cập nhật phạm vi

Khi thêm tính năng, cập nhật đồng thời [phạm vi](README.md), [tiêu chí nghiệm thu](acceptance.md), mã client, route API, test tích hợp và ảnh minh họa. Nếu thay đổi schema, tạo migration SQL mới; không sửa migration đã triển khai.
