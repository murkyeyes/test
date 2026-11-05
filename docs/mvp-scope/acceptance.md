# HKchat — tiêu chí nghiệm thu MVP

Các bước dưới đây dùng server local. Android Emulator nhập URL `http://10.0.2.2:8070`; iPhone cùng Wi-Fi nhập `http://<IP-LAN-của-máy-Windows>:8070`. Trước khi thử, `GET http://localhost:8070/api/health` cần trả `{"status":"ok","product":"HKchat"}`.

## AC-01 — Tài khoản và phiên

1. Đăng ký tài khoản mới với username, email, mật khẩu hợp lệ. Tài khoản xuất hiện trong SQLite và đăng nhập được.
2. Đăng nhập bằng tên hoặc email và mật khẩu đúng. Ứng dụng mở danh sách kênh; mở lại ứng dụng vẫn khôi phục phiên.
3. Thử sai mật khẩu hoặc URL server không hợp lệ. Ứng dụng hiển thị lỗi và không mở hội thoại.
4. Đăng xuất, mở lại ứng dụng. Client không dùng lại phiên cũ; API từ chối token đã thu hồi.

## AC-02 — Kênh, nhóm và DM

1. Tạo kênh công khai, mở kênh và gửi một tin. Tài khoản khác có thể tham gia kênh công khai rồi đọc tin.
2. Vào tab Mọi người, chọn một tài khoản và mở DM. Hai thành viên đọc được tin; tài khoản thứ ba gọi API đọc DM phải nhận `403`.
3. Mở nhóm mẫu bốn người nếu database demo đã được nạp. Mỗi người thuộc nhóm có thể đọc và gửi tin. **Tạo nhóm mới hiện có ở API, chưa có nút tạo nhóm trong app.**

## AC-03 — Tin nhắn và ngữ cảnh

1. Người A gửi tin trong kênh/DM. Người B mở cùng hội thoại và thấy tin sau khi client làm mới.
2. Người B chọn **Trả lời** một tin của A. Phản hồi mang `replyTo` trỏ đúng ID tin gốc và hiển thị liên hệ với tin đó.
3. Người A sửa tin của mình; nội dung mới xuất hiện trong hội thoại và kết quả tìm kiếm. Người B sửa/xóa tin của A qua API phải nhận `403`.
4. Thành viên thả và bỏ một cảm xúc. Số lượt và trạng thái `me` cập nhật đúng; người ngoài hội thoại không được phản ứng.
5. Xóa tin của mình. Tin không còn trong hội thoại và tìm kiếm.

## AC-04 — Tìm kiếm

1. Gửi một tin chứa từ khóa dễ nhận biết trong kênh đã tham gia; tìm từ khóa đó và thấy người gửi cùng nội dung khớp.
2. Chạm kết quả. App mở **kênh chứa tin**. Chưa yêu cầu tự cuộn tới đúng vị trí tin trong MVP hiện tại.
3. Tạo tin trùng từ khóa trong DM mà người kiểm thử không tham gia. Kết quả tìm kiếm của người đó không được chứa tin riêng này.

## AC-05 — Lưu trữ và chạy lại

1. Dừng rồi khởi động lại API với cùng file SQLite hoặc Docker volume. Tài khoản, kênh, tin nhắn và cảm xúc còn tồn tại.
2. Chạy `npm.cmd run typecheck`, `npm.cmd run test:server` và Android debug build theo `AGENTS.md` trước bản nộp cuối. Bộ test server hiện kiểm tra xác thực, phân quyền, tin nhắn, reply, sửa/xóa, cảm xúc, tìm kiếm và lưu dữ liệu sau restart.

## Kịch bản thuyết trình 3 phút

1. Nêu nỗi đau: chủ đề bị trộn, phản hồi mất ngữ cảnh, khó tìm lại quyết định.
2. Mở app bằng tài khoản demo; chỉ URL server local và danh sách kênh/nhóm.
3. Vào hội thoại, gửi tin rồi trả lời một tin gốc; chỉ rõ mối liên hệ giữa hai tin.
4. Tìm một từ khóa, chạm kết quả và mở lại kênh chứa tin.
5. Nêu giới hạn trung thực: chưa có push khi đóng app, chưa tự cuộn tới tin từ kết quả tìm kiếm và chưa có UI tạo nhóm mới.
