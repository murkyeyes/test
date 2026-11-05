# Backend HKchat local

Chạy `docker compose -f hkchat/compose.yaml up -d` tại gốc repo. Container dùng Node 22 và SQLite tích hợp, không cần cài npm package cho backend. Database nằm ở `/data/hkchat.sqlite` trong volume `hkchat-local_hkchat_data`. Nếu volume mới chưa có database và có `hkchat/backup/hkchat.sqlite`, Compose sẽ chép bản mẫu vào volume một lần. File backup chứa tài khoản và hội thoại test để dùng khi triển khai bản demo trên máy khác. Xóa hoặc đổi tên file backup trước lần chạy đầu nếu muốn database trống.

## Schema phiên bản đầu

`server/migrations/001_core.sql` tạo các bảng chat; `002_features.sql` thêm cấu trúc cho các tính năng mở rộng; `003_groups.sql` thêm nhóm chat riêng. Server lưu phiên bản đã áp dụng trong `schema_migrations` và chỉ chạy migration mới khi khởi động. Không sửa migration đã được triển khai; thay đổi tiếp theo cần file `004_*.sql`.

| Bảng | Vai trò |
| --- | --- |
| `users` | Tài khoản, email duy nhất, mật khẩu đã hash bằng scrypt và salt riêng. |
| `sessions` | Chỉ lưu SHA-256 của token phiên; phiên hết hạn sau 30 ngày. |
| `channels` | Kênh công khai và DM. `dm_key` bảo đảm một cặp người dùng chỉ có một DM. |
| `channel_members` | Quyền truy cập kênh và DM. |
| `group_chats` | Đánh dấu nhóm chat riêng; chỉ thành viên được xem và gửi tin. |
| `messages` | Tin nhắn, tác giả, liên kết trả lời, mốc sửa/xóa. |
| `reactions`, `attachments` | Reaction đang hoạt động; attachments mới có schema, chưa có API upload. |
| `workspaces`, `workspace_members`, `workspace_channels` | Cấu trúc nhóm và phân quyền cho giai đoạn nhiều workspace. |
| `user_preferences` | Cấu hình riêng của từng tài khoản. |
| `playbooks`, `playbook_tasks`, `playbook_runs`, `playbook_run_tasks` | Mẫu checklist và lần thực hiện. |
| `ai_conversations`, `ai_messages` | Lịch sử tác vụ AI local. |
| `calls`, `call_participants` | Phiên gọi và người tham gia. |
| `device_registrations`, `notifications` | Thiết bị nhận push và hộp thông báo. |

SQLite bật foreign keys và WAL; có index cho phiên, thành viên và danh sách tin theo kênh. API kiểm tra quyền thành viên trước khi đọc/gửi tin hoặc tìm kiếm. Các bảng cho workspace, playbook, AI, call và push mới là thiết kế dữ liệu; chưa có API hay chức năng ứng dụng tương ứng.

## API hiện có

| Method | Đường dẫn | Mô tả |
| --- | --- | --- |
| GET | `/api/health` | Kiểm tra server. |
| POST | `/api/register`, `/api/login`, `/api/logout` | Tài khoản và phiên. |
| GET | `/api/me`, `/api/users` | Thông tin bản thân và tìm người dùng. |
| GET/POST | `/api/channels` | Danh sách và tạo kênh. |
| GET | `/api/channels/public` | Kênh công khai có thể tham gia. |
| POST | `/api/channels/:id/join`, `/api/dm` | Tham gia kênh, mở DM. |
| POST | `/api/groups` | Tạo nhóm chat riêng với `name` và `userIds` của thành viên khác. |
| GET/POST | `/api/channels/:id/messages` | Đọc/gửi tin, nhận `replyTo` khi trả lời. `after=0` trả 100 tin mới nhất; `after>0` đồng bộ tăng dần. |
| PATCH/DELETE | `/api/messages/:id` | Tác giả sửa/xóa tin của mình. |
| POST/DELETE | `/api/messages/:id/reactions` | Thêm reaction hoặc bỏ reaction qua `/api/messages/:id/reactions/:emoji`. |
| GET | `/api/messages/:id/thread` | Đọc chuỗi trả lời trong kênh mình tham gia. |
| GET | `/api/search?q=...` | Tìm trong các kênh mà người dùng là thành viên. |

Các API trừ health/register/login cần `Authorization: Bearer <token>`. Client hiện tải lại 100 tin mới nhất mỗi 2 giây để thấy cả sửa/xóa và reaction. Backend chưa có WebSocket, call signaling, push gateway, AI service, playbook engine hoặc API upload file.
