"""Use case diagram and specifications tied to the implemented HKchat client/API."""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


HERE = Path(__file__).resolve().parent


def diagram():
    path = HERE / "report-images" / "use-cases-hkchat.png"
    canvas = Image.new("RGB", (2200, 1580), "white")
    draw = ImageDraw.Draw(canvas)
    font = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 34)
    bold = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 43)
    small = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 29)
    ink, accent, pale = "#301542", "#A81C7F", "#F9F5F9"
    draw.rounded_rectangle((335, 70, 1860, 1500), radius=22, outline=ink, width=5)
    draw.text((865, 92), "HỆ THỐNG HKCHAT", font=bold, fill=ink)

    def actor(x, y, label):
        draw.ellipse((x - 32, y, x + 32, y + 64), outline=ink, width=5)
        draw.line((x, y + 64, x, y + 180), fill=ink, width=5)
        draw.line((x - 65, y + 108, x + 65, y + 108), fill=ink, width=5)
        draw.line((x, y + 180, x - 60, y + 260), fill=ink, width=5)
        draw.line((x, y + 180, x + 60, y + 260), fill=ink, width=5)
        box = draw.textbbox((0, 0), label, font=font)
        draw.text((x - (box[2] - box[0]) / 2, y + 290), label, font=font, fill=ink)

    actor(160, 610, "Khách")
    actor(2050, 610, "Thành viên")

    def use_case(cx, cy, label, side):
        w, h = 595, 116
        draw.ellipse((cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2), fill=pale, outline=accent, width=4)
        box = draw.textbbox((0, 0), label, font=font)
        draw.text((cx - (box[2] - box[0]) / 2, cy - (box[3] - box[1]) / 2 - 5), label, font=font, fill=ink)
        if side == "left":
            draw.line((210, 745, cx - w / 2, cy), fill=ink, width=3)
        else:
            draw.line((cx + w / 2, cy, 1995, 745), fill=ink, width=3)

    for y, label in [(380, "UC01  Đăng ký"), (585, "UC02  Đăng nhập"), (790, "Nhập URL máy chủ")]:
        use_case(755, y, label, "left")
    for y, label in [
        (300, "UC03  Quản lý kênh"),
        (480, "UC04  Mở DM"),
        (660, "UC05  Gửi và trả lời tin"),
        (840, "UC06  Sửa / xóa tin"),
        (1020, "UC07  Thả cảm xúc"),
        (1200, "UC08  Tìm kiếm tin"),
        (1380, "UC09  Đăng xuất"),
    ]:
        use_case(1420, y, label, "right")
    draw.text((385, 1530), "Đường nối thể hiện vai trò có thể khởi tạo thao tác; điều kiện chi tiết ở các đặc tả UC.", font=small, fill=ink)
    canvas.save(path)
    return path


def _field(doc, title, value):
    p = doc.add_paragraph()
    p.add_run(title + ": ").bold = True
    p.add_run(value)


def _spec(doc, code, title, actor, goal, pre, main, alternatives, post, evidence):
    doc.add_heading(f"{code} — {title}", 3)
    _field(doc, "Tác nhân và mục tiêu", f"{actor}. {goal}")
    _field(doc, "Tiền điều kiện", pre)
    p = doc.add_paragraph()
    p.add_run("Luồng chính: ").bold = True
    for index, step in enumerate(main, 1):
        doc.add_paragraph(f"{index}. {step}")
    for label, detail in alternatives:
        _field(doc, f"Luồng thay thế — {label}", detail)
    _field(doc, "Hậu điều kiện", post)
    _field(doc, "Minh chứng/điểm kiểm tra", evidence)


def add_usecases(doc, image, para):
    doc.add_heading("Sơ đồ và đặc tả use case", 2)
    para(doc, "Sơ đồ dưới đây chỉ mô tả những thao tác mà người dùng có thể bắt đầu từ giao diện HKchat hiện tại. Nhóm hội thoại đã có được đọc và gửi tin theo cùng luồng kênh; API tạo nhóm chưa có màn hình tạo nhóm nên không đặt thành use case của người dùng di động. Mỗi đặc tả ghi tác nhân, tiền điều kiện, luồng chính, nhánh lỗi và kết quả để nối với user stories và ca kiểm thử ở các phần sau.")
    diagram()
    image(doc, "use-cases-hkchat.png", "Hình UC-01. Sơ đồ use case của bản HKchat đang chạy", 16.0)

    _spec(doc, "UC01", "Đăng ký tài khoản", "Khách", "Tạo tài khoản trên server HKchat để tham gia trò chuyện.",
          "Server hoạt động; người dùng nhập URL hợp lệ và chưa có phiên đăng nhập.",
          ["Chọn Đăng ký rồi nhập tên đăng nhập, email và mật khẩu.",
           "Client gửi POST /api/register tới URL đã chọn.",
           "Server kiểm tra tên 3–32 ký tự, email hợp lệ, mật khẩu ít nhất 8 ký tự và tính duy nhất của tên/email; tạo user, gắn General/Random và cấp phiên.",
           "Client lưu token và URL, tải danh sách kênh và mở màn chính."],
          [("Dữ liệu sai", "Server trả 400; form hiển thị lỗi để sửa và gửi lại."),
           ("Tên/email trùng", "Server trả 409; không tạo tài khoản thứ hai."),
           ("Không kết nối được", "Form giữ người dùng ở màn xác thực và báo lỗi kết nối.")],
          "Tài khoản tồn tại trong users, phiên trong sessions và người dùng là thành viên General/Random.",
          "FR01, US01; màn Figma 02–03; App.tsx authenticate(); POST /api/register; test đăng ký hợp lệ.")

    _spec(doc, "UC02", "Đăng nhập và khôi phục phiên", "Khách hoặc thành viên quay lại", "Vào đúng dữ liệu của tài khoản.",
          "Server có tài khoản; URL server hợp lệ.",
          ["Nhập tên đăng nhập hoặc email cùng mật khẩu và bấm Đăng nhập.",
           "Client gửi POST /api/login; server đối chiếu mật khẩu và cấp Bearer token có hạn.",
           "Client lưu token trong Keychain, gọi API lấy kênh rồi hiển thị ba tab chính.",
           "Khi mở lại ứng dụng, client đọc token đã lưu, gọi GET /api/me và tải lại kênh nếu phiên còn hợp lệ."],
          [("Sai thông tin", "Server trả 401; form giữ nguyên để nhập lại."),
           ("Phiên cũ hết hạn", "GET /api/me không hợp lệ; client trở về form xác thực."),
           ("URL không đúng", "Client báo định dạng URL sai hoặc lỗi kết nối trước khi vào ứng dụng.")],
          "Ứng dụng gắn với đúng user và chỉ dùng token còn hiệu lực.",
          "FR02, US02–US03; màn Figma 01/03; App.tsx authenticate()/khôi phục phiên; /api/login, /api/me.")

    _spec(doc, "UC03", "Xem, tạo và tham gia kênh", "Thành viên đã đăng nhập", "Trao đổi chung theo chủ đề.",
          "Token còn hạn; API truy cập được.",
          ["Mở tab Kênh; client lấy kênh đã tham gia và kênh công khai còn có thể tham gia.",
           "Chọn kênh đã có để đọc tin, hoặc nhập tên 2–80 ký tự và bấm Tạo kênh.",
           "Khi tạo kênh, server thêm người tạo vào channel_members; khi chọn Tham gia, server thêm membership vào kênh public.",
           "Client tải lại danh sách và mở hội thoại của kênh vừa chọn."],
          [("Tên sai", "POST /api/channels trả 400, kênh không được tạo."),
           ("Kênh không công khai hoặc không tồn tại", "Thao tác tham gia trả 404; client báo lỗi."),
           ("Đọc trước khi tham gia", "API tin nhắn trả 403; không lộ nội dung.")],
          "Kênh mới hoặc đã tham gia hiện trong danh sách của user; membership được lưu.",
          "FR03–FR04, US04–US05; màn Figma 04–06; GET/POST /api/channels, /api/channels/public, /join; server.test.mjs.")

    _spec(doc, "UC04", "Mở trò chuyện trực tiếp", "Thành viên đã đăng nhập", "Trao đổi riêng với một người khác.",
          "Tài khoản người nhận tồn tại và khác tài khoản hiện tại.",
          ["Mở tab Mọi người và chọn người muốn nhắn.",
           "Client gửi POST /api/dm với userId người nhận.",
           "Server tính dm_key từ hai id; dùng lại DM đã có hoặc tạo channel mới và thêm đúng hai thành viên.",
           "Client mở hội thoại DM để đọc và gửi tin."],
          [("Người nhận sai", "Server trả 400; không tạo DM."),
           ("Người thứ ba truy cập", "API đọc tin hoặc tìm kiếm không trả nội dung DM cho người ngoài.")],
          "Hai thành viên nhìn thấy cùng một DM, người ngoài không có quyền đọc.",
          "FR05, US06; màn Figma 07–08; POST /api/dm, channel_members; bài test DM và 403.")

    _spec(doc, "UC05", "Gửi và trả lời tin", "Thành viên của cuộc trò chuyện", "Gửi nội dung và giữ ngữ cảnh phản hồi.",
          "Đã mở kênh, DM hoặc nhóm có membership; token còn hạn.",
          ["Nhập nội dung 1–4000 ký tự rồi bấm Gửi; nếu cần trả lời, chọn Trả lời trên tin gốc trước khi nhập.",
           "Client gửi POST /api/channels/:id/messages với body và replyTo khi có tin gốc.",
           "Server kiểm tra membership, nội dung và tin replyTo chưa bị xóa trong cùng kênh; lưu messages.",
           "Client tải lại hội thoại; tin mới và trích dẫn phản hồi xuất hiện."],
          [("Tin rỗng hoặc quá dài", "Server trả 400; không ghi nội dung sai."),
           ("replyTo sai kênh/không tồn tại", "Server trả 400; không ghi phản hồi."),
           ("Người ngoài kênh", "Server trả 403 trước khi ghi tin.")],
          "Tin có tác giả, thời điểm và liên kết reply_to nếu là phản hồi.",
          "FR07–FR08, US07–US08; màn Figma 09–10; messages, reply_to; test gửi, reply và thread.")

    _spec(doc, "UC06", "Sửa hoặc xóa tin của mình", "Tác giả tin", "Điều chỉnh hoặc gỡ nội dung đã gửi.",
          "Tin chưa bị xóa; người dùng còn là thành viên kênh và là tác giả.",
          ["Nhấn giữ tin của mình và chọn Sửa hoặc Xóa.",
           "Với Sửa, client gửi PATCH /api/messages/:id cùng nội dung mới; server ghi body và edited_at.",
           "Với Xóa, client hỏi xác nhận rồi gửi DELETE /api/messages/:id; server ghi deleted_at.",
           "Client tải lại hội thoại để phản ánh nội dung mới hoặc bỏ tin đã xóa."],
          [("Không phải tác giả", "Server trả 403, tin không thay đổi."),
           ("Tin đã xóa/không tồn tại", "Server trả 404."),
           ("Nội dung sửa rỗng", "Server trả 400 và giữ nội dung cũ.")],
          "Tin sửa có edited_at; tin xóa mềm không còn ở danh sách và kết quả tìm kiếm.",
          "FR09, US09–US10; màn Figma 11–12/14; PATCH, DELETE /api/messages/:id; test quyền tác giả.")

    _spec(doc, "UC07", "Thêm hoặc bỏ cảm xúc", "Thành viên kênh", "Phản hồi nhanh đối với một tin.",
          "Tin còn tồn tại và người dùng có quyền đọc kênh.",
          ["Chạm bộ chọn cảm xúc dưới tin và chọn một emoji.",
           "Client gửi POST /api/messages/:id/reactions; server ghi bộ ba message_id, user_id, emoji nếu chưa có.",
           "API trả tin với tổng count và cờ me; client hiển thị trạng thái mới.",
           "Nếu bỏ cảm xúc, client gọi DELETE /api/messages/:id/reactions/:emoji và cập nhật count."],
          [("Emoji không hợp lệ", "Server trả 400."),
           ("Người ngoài kênh", "Server trả 403."),
           ("Chọn lại cùng emoji", "Khóa duy nhất giữ một reaction cho mỗi người/emoji/tin; count không tăng trùng.")],
          "Tổng cảm xúc của tin phản ánh các bản ghi hợp lệ trong reactions.",
          "FR10, US11; màn Figma 13; reactions; server.test.mjs kiểm tra count/me.")

    _spec(doc, "UC08", "Tìm và mở lại tin", "Thành viên đã đăng nhập", "Tìm lại nội dung có quyền xem.",
          "Token còn hạn; người dùng đang ở tab Tìm kiếm.",
          ["Nhập từ khóa và bấm Tìm kiếm.",
           "Client gọi GET /api/search?q=...; server tìm trong tin chưa xóa thuộc kênh người dùng tham gia.",
           "API trả tối đa 50 kết quả mới nhất; client hiện tác giả và nội dung.",
           "Chọn một kết quả để mở cuộc hội thoại chứa tin."],
          [("Từ khóa rỗng", "API trả danh sách rỗng, không tìm toàn bộ database."),
           ("Không có kết quả", "Danh sách kết quả trống; người dùng có thể nhập từ khóa khác."),
           ("Tin của DM/kênh ngoài quyền", "Không xuất hiện trong kết quả.")],
          "Đúng hội thoại được mở; bản hiện tại chưa tự cuộn tới vị trí của tin được chọn.",
          "FR11, US12; màn Figma 15–17; GET /api/search; test tìm kiếm theo membership.")

    _spec(doc, "UC09", "Đăng xuất", "Thành viên đã đăng nhập", "Kết thúc phiên trên thiết bị.",
          "Client có token phiên đang dùng.",
          ["Bấm Đăng xuất và xác nhận trong hộp thoại.",
           "Client gọi POST /api/logout; server xóa hash token của phiên hiện tại.",
           "Client xóa token local, dữ liệu hội thoại đang mở và trở về màn xác thực."],
          [("Hủy xác nhận", "Không gọi API, giữ nguyên phiên."),
           ("API logout lỗi mạng", "Client vẫn xóa token trên thiết bị; phiên phía server hết hạn theo thời hạn đã cấp nếu request không tới được.")],
          "Thiết bị không tự vào lại app bằng token vừa xóa.",
          "US13; màn Figma 18; App.tsx logout(); POST /api/logout, Keychain.")
