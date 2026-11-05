# HKchat — phạm vi MVP

## Bài toán và người dùng

Một nhóm nhỏ trao đổi nhiều chủ đề trong cùng một luồng chat sẽ dễ bỏ sót tin, mất ngữ cảnh khi trả lời và mất thời gian tìm lại quyết định cũ. HKchat tập trung vào nhân viên và trưởng nhóm cần trao đổi trên điện thoại qua kênh chung hoặc tin nhắn riêng. Bản demo dùng server do nhóm tự chạy trên máy local.

Giá trị cốt lõi của MVP là **vào đúng hội thoại, trao đổi có ngữ cảnh và tìm lại thông tin**. Tình huống này là giả định thiết kế của đồ án; nhóm chưa có số liệu khảo sát người dùng để chứng minh mức độ phổ biến hay thời gian tiết kiệm được.

## Ranh giới MVP hiện tại

| Mức ưu tiên | Chức năng | Trạng thái | Căn cứ |
| --- | --- | --- | --- |
| Must | Đăng ký, đăng nhập bằng URL server, khôi phục phiên, đăng xuất | Có | `hkchat/mobile/App.tsx`; `/api/register`, `/api/login`, `/api/logout` |
| Must | Xem, tạo, tham gia kênh công khai; mở nhóm mẫu | Có | Tab Kênh; `/api/channels`, `/api/groups` |
| Must | Tìm người và mở DM | Có | Tab Mọi người; `/api/users`, `/api/dm` |
| Must | Đọc, gửi tin và trả lời gắn tin gốc | Có | Màn hội thoại; `/api/channels/:id/messages`, `/api/messages/:id/thread` |
| Must | Tìm tin theo từ khóa trong hội thoại có quyền | Có giới hạn | Tab Tìm kiếm; `/api/search` |
| Should | Sửa/xóa tin của mình; thêm/bỏ cảm xúc | Có | Màn hội thoại; `/api/messages/:id` và reactions |
| Could | Tạo nhóm nhiều người bằng giao diện | Chưa có | API `/api/groups` có nhưng client chưa có luồng tạo nhóm |
| Later | Push khi ứng dụng đóng, chia sẻ tệp, gọi thoại, quản trị tổ chức | Chưa có | Chưa có luồng hoạt động và kiểm thử đầu cuối |

**Giới hạn quan trọng:** Chạm kết quả tìm kiếm mở kênh chứa tin, chưa tự cuộn tới đúng tin. Tin mới được client làm mới bằng polling 2 giây khi đang xem hội thoại; đây không phải push notification. Bản iPhone chạy qua Expo Go SDK 58; chưa có bản iOS native được build và ký trên macOS.

## Điều kiện hoàn thành MVP

Một người dùng có thể đăng nhập vào server local, mở kênh hoặc DM có quyền, gửi tin, trả lời một tin gốc và tìm lại nội dung qua từ khóa. API phải từ chối người ngoài hội thoại và từ chối sửa/xóa tin của người khác. Dữ liệu vẫn tồn tại sau khi khởi động lại server với cùng file SQLite/volume. Các phép kiểm tra chi tiết nằm ở [tiêu chí nghiệm thu](acceptance.md).

## Tài liệu liên quan

- [Ma trận phạm vi và truy vết](traceability.md)
- [Tiêu chí nghiệm thu và kịch bản demo](acceptance.md)
- [Ảnh Android dùng trong báo cáo](../report-images/README.md)
- [Hướng dẫn chạy dự án](../../README.md)
