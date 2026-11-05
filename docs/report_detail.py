"""Detailed HKchat report chapters grounded in current source and test cases."""

from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent


def paragraphs(doc, para, items):
    for item in items:
        para(doc, item)


def section(doc, para, title, items):
    doc.add_heading(title, 2)
    paragraphs(doc, para, items)


def market(doc, table, para):
    section(doc, para, "2.2 Cách đối chiếu và bài học từ thị trường", [
        "Năm sản phẩm được chọn vì đều giải quyết ít nhất một trong ba việc HKchat cần làm: tổ chức hội thoại nhóm, nhắn trực tiếp và giữ ngữ cảnh trao đổi. Nhóm xem tài liệu công khai của từng sản phẩm và ghi nhận cách tổ chức chức năng, thay vì đánh giá tốc độ hoặc mức độ hài lòng mà chưa có phép đo. Phạm vi đối chiếu này giúp giải thích vì sao giao diện HKchat dùng ba tab Kênh, Mọi người và Tìm kiếm.",
        "Slack đặt kênh ở trung tâm trải nghiệm. Người dùng có thể tách thảo luận theo chủ đề, dự án hoặc đơn vị. HKchat chọn cách tương tự ở mức gọn hơn: kênh đã tham gia được liệt kê ngay sau đăng nhập, phần tạo kênh ở dưới danh sách, và các kênh công khai chưa tham gia được đặt riêng. Sự phân tách này giúp người dùng biết nơi nào có thể đọc và nơi nào cần bấm tham gia.",
        "Microsoft Teams tổ chức các cuộc trao đổi theo phạm vi nhóm và kênh. Bài học áp dụng là người dùng cần nhận ra sự khác biệt giữa cuộc trò chuyện chung và cuộc trò chuyện riêng. Trong HKchat, API lưu cả kênh công khai và DM trong bảng channels nhưng trường kind và bảng channel_members quyết định cách hiển thị và quyền đọc. Danh sách trong giao diện dùng ký hiệu # cho kênh công khai và dấu chấm cho cuộc trò chuyện khác.",
        "Google Chat sử dụng space cho nhóm và cung cấp trả lời theo luồng. HKchat giữ một liên kết reply_to trên mỗi tin nhắn. Khi người dùng chọn Trả lời, thanh ngữ cảnh cho biết đang trả lời ai; tin gửi đi mang id tin gốc. Trong hội thoại, phần trích dẫn giúp người đọc nhận ra mối liên hệ giữa phản hồi và nội dung trước đó.",
        "Zulip phân tách nội dung theo channel và topic. HKchat chưa dùng topic như một thực thể riêng; thay vào đó, tên kênh và reply theo tin đáp ứng phạm vi đồ án. Rocket.Chat cho thấy việc tự vận hành máy chủ đã có trên thị trường; vì thế báo cáo không xem chạy local là tính năng độc quyền, mà là lựa chọn triển khai phù hợp với môi trường thử nghiệm của nhóm.",
    ])
    table(doc, ["Tiêu chí", "Cách HKchat thể hiện", "Căn cứ trong dự án"], [
        ("Phân loại hội thoại", "Kênh công khai, DM và nhóm mẫu", "channels.kind, group_chats, giao diện Kênh"),
        ("Theo dõi ngữ cảnh", "reply_to và thanh trả lời", "messages.reply_to, App.tsx"),
        ("Tìm nội dung", "Tìm từ khóa trong kênh được phép đọc", "GET /api/search"),
        ("Tự vận hành", "Node.js API, SQLite, Docker volume", "compose.yaml, server.mjs"),
        ("Thiết kế di động", "Ba tab và danh sách hội thoại", "App.tsx, Figma 18 trạng thái"),
    ], [3.2, 6.1, 7.4])
    section(doc, para, "2.3 Giá trị thiết kế rút ra", [
        "So sánh cho thấy chức năng không nên tách khỏi luồng sử dụng. Một người mới cần biết địa chỉ server, đăng nhập và thấy ngay các kênh có thể mở. Một thành viên cũ cần ít thao tác để vào hội thoại đã có. Khi tìm tin, kết quả cần giữ tên tác giả và nội dung đủ nhận diện; chọn kết quả đưa người dùng trở lại đúng cuộc trò chuyện. Những quyết định này được phản ánh trong bộ màn hình Figma và client React Native.",
        "Điểm khác biệt phù hợp với bản HKchat hiện tại là tính dễ thử trên máy riêng: server và dữ liệu chạy local, ứng dụng Android trỏ tới 10.0.2.2 khi dùng emulator, còn iPhone qua Expo Go trỏ tới IP LAN. Cách trình bày trong báo cáo chỉ mô tả bản đồ án có thật; không suy ra ưu thế hiệu năng, bảo mật tuyệt đối hay quy mô doanh nghiệp khi chưa có đo kiểm tương ứng.",
    ])


def overview(doc, table, para):
    section(doc, para, "1.4 Phạm vi sử dụng của bản hiện tại", [
        "HKchat giải quyết bài toán liên lạc bằng văn bản cho một nhóm có máy chủ do chính nhóm vận hành. Người dùng không phải chọn một dịch vụ chat công cộng bên ngoài: họ nhập URL của server HKchat, tạo tài khoản trên database local và làm việc với kênh hoặc DM của cùng server. Cách triển khai này phù hợp khi nhóm cần trình diễn chức năng trên một máy Windows và một số thiết bị trong cùng mạng thử nghiệm.",
        "Một cuộc trao đổi thông thường bắt đầu từ danh sách kênh. Thành viên chọn General, Random hoặc kênh đã tham gia; tin được hiển thị theo thứ tự và làm mới định kỳ. Nếu cần trao đổi riêng, tab Mọi người mở DM hai người. Nếu cần tìm lại thông tin, tab Tìm kiếm trả nội dung theo từ khóa trong phạm vi quyền xem. Sửa, xóa, trả lời và cảm xúc là các thao tác sau khi cuộc trò chuyện đã được mở.",
        "Bản dữ liệu mẫu có tài khoản và hội thoại bốn thành viên để báo cáo chức năng nhóm. Nội dung nói chuyện về đồ án chỉ là dữ liệu kiểm thử; đối tượng sản phẩm là nhóm làm việc nội bộ. Tên người dùng trong ảnh vì vậy không đại diện cho vai trò cố định trong doanh nghiệp. Dữ liệu thật có thể khác khi người dùng tự đăng ký và tạo kênh mới.",
        "Phạm vi báo cáo dựa trên mã chạy, test server, ảnh Android và file Figma. Schema có thêm một số bảng dành cho các hướng mở rộng nhưng khi chưa có route hoặc màn hình tương ứng, báo cáo không liệt kê chúng là tính năng hiện hữu. Sự phân biệt này giúp hội đồng đối chiếu từng mô tả với nguồn minh chứng rõ ràng.",
    ])
    table(doc, ["Nhu cầu", "Bước trên ứng dụng", "Dữ liệu liên quan"], [
        ("Gia nhập nhóm", "Nhập URL, đăng ký/đăng nhập", "users, sessions"),
        ("Trao đổi chung", "Chọn hoặc tạo kênh", "channels, channel_members"),
        ("Trao đổi riêng", "Chọn người từ tab Mọi người", "channels kind dm, dm_key"),
        ("Giữ ngữ cảnh", "Chọn Trả lời trên một tin", "messages.reply_to"),
        ("Tìm lại thông tin", "Nhập từ khóa và mở kết quả", "messages kết hợp membership"),
    ], [3.3, 6.7, 6.7])
    section(doc, para, "1.5 Các bên tham gia vào một cuộc trò chuyện", [
        "Người gửi chịu trách nhiệm nội dung mình viết. Trong API, user_id của tin được lấy từ phiên xác thực, không lấy từ dữ liệu JSON do client tự khai. Người đọc phải là thành viên kênh ở thời điểm gọi API. Người tạo kênh công khai được thêm vào membership ngay khi tạo; người khác có thể tham gia qua endpoint join. Trong DM, hai thành viên được thêm cùng lúc trong transaction.",
        "Server là nơi quyết định quyền; giao diện giúp thao tác thuận tiện nhưng không phải lớp bảo vệ duy nhất. Ví dụ một nút Sửa có thể chỉ xuất hiện cho tin của mình, nhưng nếu người dùng gửi PATCH thủ công vào tin của người khác thì server vẫn trả 403. Tương tự, biết id một tin trong kênh khác không cho phép đọc thread hoặc gắn reaction.",
        "Quá trình dùng app vì vậy có hai loại trạng thái cần theo dõi: trạng thái giao diện như tab đang chọn, kênh đang mở và bản nháp; trạng thái bền vững trên server như phiên, membership và các hàng tin nhắn. Khi khởi động lại app hoặc server, phần giao diện được dựng lại từ API và database thay vì giả định state cũ trong bộ nhớ còn tồn tại.",
    ])


def stories(doc, table, para):
    section(doc, para, "3.7 Danh mục câu chuyện người dùng chi tiết", [
        "Câu chuyện người dùng được viết theo mục tiêu thao tác, điều kiện nghiệm thu và chứng cứ có thể kiểm tra. Một luồng được xem là hoàn thành khi API trả dữ liệu đúng và giao diện có đường đi để người dùng thực hiện, hoặc khi báo cáo ghi rõ trường hợp chỉ có API. Phần này không gán những yêu cầu chưa có trong app vào phạm vi đã triển khai.",
        "Với tài khoản, điều kiện quan trọng là tên/email không trùng, mật khẩu đủ dài, phiên còn hiệu lực và token bị hủy khi đăng xuất. Với hội thoại, điều kiện quan trọng là membership chặn người ngoài, tác giả mới được sửa/xóa và reply không trỏ sang kênh khác. Với tìm kiếm, quyền xem phải được áp dụng trong truy vấn trước khi trả kết quả.",
    ])
    table(doc, ["User story", "Mục tiêu", "Tiêu chí nghiệm thu và bằng chứng"], [
        ("US01", "Tôi muốn đăng ký tài khoản.", "Dữ liệu hợp lệ tạo user; trùng tên/email trả 409; test API."),
        ("US02", "Tôi muốn đăng nhập bằng tên hoặc email.", "Đúng thông tin cấp token; sai mật khẩu trả 401; test API và form."),
        ("US03", "Tôi muốn mở lại app mà vẫn giữ phiên.", "Client đọc Keychain, GET /me và tải kênh; App.tsx."),
        ("US04", "Tôi muốn tạo kênh công khai.", "Tên 2–80 ký tự; người tạo thành viên; API và tab Kênh."),
        ("US05", "Tôi muốn tham gia kênh khác.", "Join tạo membership; đọc tin chuyển từ 403 sang 200; test API."),
        ("US06", "Tôi muốn nhắn riêng cho đồng nghiệp.", "Cặp người dùng có một DM; người ngoài không đọc được; test API."),
        ("US07", "Tôi muốn gửi tin trong cuộc trò chuyện.", "Tin 1–4000 ký tự, người gửi là thành viên; test API và Android."),
        ("US08", "Tôi muốn trả lời một tin cụ thể.", "replyTo đúng tin cùng kênh; tin hiển thị trích dẫn; test và ảnh."),
        ("US09", "Tôi muốn sửa tin của mình.", "PATCH đổi body/edited_at; người khác nhận 403; test API."),
        ("US10", "Tôi muốn xóa tin của mình.", "DELETE ghi deleted_at; tin không còn trong danh sách; test API."),
        ("US11", "Tôi muốn thả cảm xúc.", "Count và me cập nhật; một người không bị tính trùng; test API."),
        ("US12", "Tôi muốn tìm lại một tin.", "Từ khóa chỉ tìm trong kênh có quyền; chọn kết quả mở kênh; test/ảnh."),
        ("US13", "Tôi muốn đăng xuất.", "Token bị xóa ở server và client quay về form; route và App.tsx."),
    ], [2.1, 6.3, 8.3])
    section(doc, para, "3.8 Liên kết yêu cầu với màn hình và API", [
        "Ma trận truy vết cho thấy mỗi yêu cầu chính có nơi thực hiện trên client và endpoint tương ứng. Nó đặc biệt hữu ích với đồ án có prototype Figma: số màn hình được nối không tự chứng minh server xử lý đúng. Ngược lại, một endpoint có test thành công cũng không tự chứng minh người dùng thao tác được trên giao diện.",
        "Ví dụ, API /api/groups có test và dữ liệu nhóm mẫu, nhưng giao diện hiện không có form tạo nhóm. Vì vậy chức năng nhóm trong báo cáo được mô tả là đọc/nhắn trong nhóm đã có, không ghi thành luồng người dùng tự tạo nhóm. Việc chỉ ra ranh giới này giúp demo trùng với báo cáo khi giảng viên hỏi trực tiếp.",
    ])
    table(doc, ["Yêu cầu", "Use case", "Màn hình", "Thành phần/API"], [
        ("US01–US03", "UC01–UC02", "Figma 01–03", "App.tsx xác thực; register/login/me; users, sessions"),
        ("US04–US05", "UC03", "Figma 04–06", "App.tsx tab Kênh; channels/public/join; channel_members"),
        ("US06", "UC04", "Figma 07–08", "App.tsx tab Mọi người; users/dm; dm_key"),
        ("US07–US08", "UC05", "Figma 09–10", "App.tsx hội thoại; messages/thread; reply_to"),
        ("US09–US11", "UC06–UC07", "Figma 11–14", "App.tsx thao tác tin; PATCH/DELETE; reactions"),
        ("US12", "UC08", "Figma 15–17", "App.tsx Tìm kiếm; GET /api/search; membership"),
        ("US13", "UC09", "Figma 18", "App.tsx logout; POST /api/logout; sessions"),
    ], [2.4, 2.3, 3.4, 8.6])


def requirements(doc, table, para):
    section(doc, para, "3.4 Đặc tả yêu cầu chức năng", [
        "Nhóm yêu cầu tài khoản bao gồm đăng ký, đăng nhập, khôi phục phiên khi mở lại app và đăng xuất. Tên đăng nhập được server chấp nhận khi có 3–32 ký tự chữ, số hoặc dấu gạch dưới; email phải có định dạng hợp lệ; mật khẩu tối thiểu 8 ký tự. API trả HTTP 409 nếu tên hoặc email đã tồn tại. Người dùng nhập địa chỉ server trước khi xác thực; client kiểm tra URL có dạng http(s)://host và lưu địa chỉ dùng gần nhất.",
        "Sau khi đăng ký, server tạo hoặc tìm hai kênh công khai General và Random rồi thêm tài khoản mới vào bảng thành viên. Điều này giúp tài khoản mới có nội dung điều hướng ngay khi vào ứng dụng. Khi đăng nhập, tên hoặc email đều được chấp nhận làm định danh. Phiên được cấp token ngẫu nhiên và lưu dạng hash kèm thời điểm hết hạn sau 30 ngày; thao tác Đăng xuất xóa token trên server và thông tin phiên trong app.",
        "Nhóm yêu cầu kênh bao gồm xem kênh đã tham gia, xem kênh công khai khác, tạo kênh và tham gia kênh. Tên kênh mới phải dài 2–80 ký tự. API chỉ cho phép tham gia kênh công khai không phải group chat. Giao diện hiển thị tên, biểu tượng và hành động Tham gia. Nếu kênh đã mở, màn hội thoại đọc tin theo quyền thành viên.",
        "Tin nhắn trực tiếp được mở từ tab Mọi người. Client gửi userId của người nhận; server xác nhận tài khoản tồn tại và không phải chính người gửi. Khóa dm_key ghép hai userId theo thứ tự ổn định để cùng một cặp người chỉ có một cuộc DM. Bảng channel_members chứa đúng hai thành viên khi tạo DM. Người thứ ba không thể đọc hoặc tìm nội dung cuộc trò chuyện này.",
        "Nhóm hội thoại được API tạo với một người tạo và 2–19 thành viên khác, tổng 3–20 người. Server xác nhận mọi userId, loại bỏ khả năng trùng hoặc tự thêm chính mình. Bản dữ liệu mẫu có cuộc trò chuyện bốn người để kiểm thử giao diện; client hiện hiển thị nhóm này như một cuộc hội thoại trong danh sách kênh. Báo cáo không mô tả màn hình tự tạo nhóm vì client chưa có thao tác đó.",
    ])
    table(doc, ["Mã", "Đầu vào và điều kiện", "Kết quả hệ thống"], [
        ("FR01", "Tên 3–32 ký tự, email hợp lệ, mật khẩu ≥8", "Tạo users, phiên và gắn General/Random"),
        ("FR02", "Tên hoặc email và mật khẩu đúng", "Cấp phiên, mở danh sách kênh"),
        ("FR03", "Tên kênh 2–80 ký tự", "Tạo kênh công khai và thêm người tạo"),
        ("FR04", "Kênh công khai có thật", "Thêm người dùng vào channel_members"),
        ("FR05", "Người nhận DM hợp lệ", "Tạo hoặc dùng lại DM của cùng cặp"),
        ("FR06", "Nhóm 3–20 người, danh sách duy nhất", "Tạo group_chats và thành viên"),
    ], [1.3, 7.1, 8.3])
    section(doc, para, "3.5 Đặc tả thao tác với tin nhắn", [
        "Người dùng chỉ gửi tin khi thuộc kênh. Server cắt khoảng trắng đầu/cuối và từ chối nội dung trống hoặc dài hơn 4000 ký tự. Nếu tin là phản hồi, replyTo phải trỏ đến một tin chưa xóa trong cùng kênh. Tin được gán id tăng tự động, user_id tác giả và thời điểm tạo. Client làm mới hội thoại mỗi hai giây khi đang mở để lấy nội dung mới từ server.",
        "Danh sách tin ban đầu lấy tối đa 100 tin mới nhất, sau đó trả về theo thứ tự cũ đến mới. API cũng hỗ trợ tham số after để lấy tối đa 100 tin có id lớn hơn mốc đã biết. Cách này giúp client có khả năng truy vấn bổ sung mà không đọc toàn bộ lịch sử. Tin có deleted_at không được trả trong danh sách thông thường.",
        "Tác giả có thể sửa nội dung bằng PATCH và xóa bằng DELETE. Khi sửa, server kiểm tra nội dung theo cùng giới hạn 1–4000 ký tự và ghi edited_at. Xóa là xóa mềm: server ghi deleted_at, giữ bản ghi để liên kết reply không bị hỏng. Người khác trong kênh vẫn đọc được tin trước khi xóa nhưng không thể sửa hoặc xóa thay tác giả.",
        "Cảm xúc là bản ghi riêng theo bộ ba message_id, user_id và emoji. Trùng một cảm xúc của cùng người trên cùng tin không tạo thêm hàng; thao tác xóa bỏ đúng hàng của người đó. API tổng hợp số lượt và cờ me cho từng emoji khi trả tin. Giao diện cung cấp bốn biểu tượng 👍, ❤️, 😂 và 🎉, cùng nút mở bộ chọn cảm xúc bên dưới mỗi tin.",
        "Tìm kiếm nhận một từ khóa tối đa 100 ký tự; chuỗi rỗng trả danh sách trống. Truy vấn dùng bảng thành viên để giới hạn kết quả trong các kênh người dùng được phép xem, bỏ tin đã xóa và trả tối đa 50 kết quả mới nhất. Giao diện hiển thị tác giả và nội dung; chạm vào kết quả mở cuộc hội thoại tương ứng.",
    ])
    table(doc, ["Mã", "Ràng buộc", "Phản hồi lỗi hoặc trạng thái"], [
        ("FR07", "Tin 1–4000 ký tự, người gửi là thành viên", "400 nếu nội dung sai; 403 nếu ngoài kênh"),
        ("FR08", "replyTo là tin còn tồn tại trong cùng kênh", "400 nếu tin đích sai"),
        ("FR09", "Sửa/xóa chỉ dành cho tác giả", "403 nếu người khác thao tác"),
        ("FR10", "Emoji không rỗng, tối đa 64 ký tự", "400 nếu emoji không hợp lệ"),
        ("FR11", "Từ khóa tối đa 100 ký tự", "Trả tối đa 50 tin trong kênh có quyền"),
    ], [1.3, 7.1, 8.3])
    section(doc, para, "3.6 Yêu cầu phi chức năng được kiểm tra", [
        "Bảo vệ dữ liệu bắt đầu ở xác thực: mật khẩu được xử lý bằng scrypt với salt ngẫu nhiên riêng trước khi ghi vào users; token phiên được băm SHA-256 trước khi lưu vào sessions. Server so sánh hash mật khẩu bằng timingSafeEqual. Các endpoint ngoài đăng ký, đăng nhập và health đều kiểm tra Bearer token còn hạn. Kiểm tra quyền thành viên được đặt trước thao tác đọc và gửi tin, mở thread hoặc thả cảm xúc.",
        "Tính toàn vẹn dữ liệu dựa trên khóa ngoại SQLite, CHECK cho kind và độ dài body, UNIQUE cho username/email/dm_key và các khóa chính ghép trong bảng thành viên, cảm xúc. Các thao tác tạo tài khoản, kênh, nhóm và DM dùng transaction để tránh trạng thái chỉ tạo một phần khi có lỗi. Chế độ WAL được bật khi mở database để hỗ trợ ghi và đọc ổn định trong phạm vi server local.",
        "Khả năng cài đặt lặp lại được thể hiện qua Docker Compose, volume giữ database và README từng bước cho Windows. Người dùng Android Emulator dùng 10.0.2.2 để vào máy host; iPhone chạy Expo Go dùng IP LAN. Đây là hai đường kiểm thử đã mô tả trong dự án. Báo cáo không đặt chỉ tiêu thời gian phản hồi, FPS hoặc tải đồng thời vì nhóm chưa có phép đo tương ứng.",
        "Khả năng sử dụng được hỗ trợ bởi nhãn rõ ràng cho ô nhập và nút, lỗi xác thực hiển thị trong màn đăng nhập, thanh ngữ cảnh khi reply/sửa, phản hồi khi thao tác đang bận và ba tab cố định sau đăng nhập. Những quyết định này có thể quan sát trong mã React Native và ảnh Android; đánh giá khả dụng định lượng cần nghiên cứu người dùng riêng.",
    ])


def diagram(name, columns, subtitle):
    path = ROOT / "report-images" / name
    im = Image.new("RGB", (1600, 520), "white")
    d = ImageDraw.Draw(im)
    regular = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 28)
    bold = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 37)
    title = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 29)
    d.text((55, 40), subtitle, font=title, fill="#301542")
    for i, (heading, lines) in enumerate(columns):
        x = 55 + i * (1490 // len(columns))
        width = 1490 // len(columns) - 34
        d.rounded_rectangle((x, 120, x + width, 415), radius=22, fill="#F9F5F9", outline="#A81C7F", width=3)
        d.text((x + 23, 150), heading, font=bold, fill="#301542")
        d.multiline_text((x + 23, 230), lines, font=regular, fill="#37213F", spacing=15)
        if i < len(columns) - 1:
            d.line((x + width + 5, 265, x + width + 26, 265), fill="#A81C7F", width=4)
            d.polygon([(x + width + 20, 255), (x + width + 20, 275), (x + width + 33, 265)], fill="#A81C7F")
    im.save(path)
    return path


def architecture(doc, table, para, image):
    section(doc, para, "4.4 Cấu trúc mã nguồn và trách nhiệm từng thành phần", [
        "Tệp hkchat/mobile/App.tsx chứa client React Native. Phần đầu định nghĩa kiểu User, Channel, Message và hàm api() chung. Các state của component quản lý phiên đăng nhập, tab hiện tại, kênh đang mở, tin đã tải, bản nháp, tin đang trả lời hoặc sửa và danh sách kết quả tìm kiếm. Tách các trạng thái này giúp màn hình đổi giữa xác thực, danh sách và hội thoại mà vẫn giữ dữ liệu cần thiết cho mỗi thao tác.",
        "Tệp hkchat/server/server.mjs khởi tạo database, áp dụng migration, định nghĩa helper cho mật khẩu và phiên, sau đó điều phối các route trong một HTTP handler. Các route công khai là health, register và login. Phần còn lại đi qua kiểm tra Bearer token trước khi xử lý. Việc đọc hoặc sửa tin còn có một lớp kiểm tra thành viên kênh và, với sửa/xóa, kiểm tra tác giả.",
        "Ba migration SQL trong hkchat/server/migrations được áp dụng theo số phiên bản. 001_core.sql định nghĩa dữ liệu cốt lõi, 002_features.sql tạo thêm các bảng nền cho những phân hệ khác, còn 003_groups.sql bổ sung group_chats. Phần báo cáo chức năng chỉ căn cứ vào route và giao diện đã có; sự tồn tại của một bảng trong migration không đồng nghĩa tính năng tương ứng đã được triển khai ở client.",
        "Tệp hkchat/compose.yaml mô tả service api dùng Node.js 22 Alpine, mount thư mục server ở chế độ chỉ đọc, gắn volume hkchat_data vào /data và công bố cổng 8070. Healthcheck gọi /api/health bên trong container. Khi volume còn trống, command có thể chép database mẫu từ thư mục backup; dữ liệu tạo sau đó nằm trong volume và tồn tại qua các lần khởi động lại container.",
    ])
    diagram("architecture-hkchat.png", [
        ("Ứng dụng", "React Native\nAndroid / Expo Go\nGiao diện và phiên"),
        ("HTTP API", "Node.js server.mjs\nXác thực và quyền\nRoute nghiệp vụ"),
        ("Dữ liệu", "SQLite migrations\nBảng người dùng, kênh, tin\nDocker volume"),
    ], "Luồng dữ liệu của HKchat")
    image(doc, "architecture-hkchat.png", "Hình. Sơ đồ các tầng client, API và SQLite", 16.1)
    table(doc, ["Thư mục hoặc tệp", "Nội dung", "Liên hệ khi chạy"], [
        ("hkchat/mobile/App.tsx", "Giao diện và hàm gọi API", "Được build thành ứng dụng React Native"),
        ("hkchat/server/server.mjs", "HTTP handler và truy vấn SQLite", "Chạy trong container api"),
        ("hkchat/server/migrations", "Schema phiên bản 001–003", "Áp dụng khi server khởi động"),
        ("hkchat/compose.yaml", "Service, cổng, volume, healthcheck", "docker compose up -d"),
        ("expo-preview", "Bản thử trên iPhone từ Windows", "Expo Go SDK 58"),
        ("android, ios", "Dự án native", "Gradle Android; Xcode trên macOS"),
    ], [5.1, 5.7, 5.9])
    section(doc, para, "4.5 Đường đi của một request", [
        "Ví dụ khi gửi tin, client gọi POST /api/channels/:id/messages cùng Bearer token và nội dung. Handler đọc token, tìm sessions còn hạn và người dùng tương ứng. Tiếp đó API kiểm tra người dùng có hàng trong channel_members của kênh đích. Nếu không có, response 403 được trả trước khi nội dung được ghi. Nếu có quyền, body được chuẩn hóa, kiểm tra độ dài và replyTo, sau đó INSERT vào messages.",
        "Sau khi ghi, server đọc lại hàng vừa tạo, bổ sung username và danh sách cảm xúc để tạo message DTO trả về. Client cập nhật danh sách tin và lần poll sau tiếp tục đồng bộ với server. Cấu trúc response thống nhất giúp cùng một thành phần hiển thị tin mới, tin đã sửa và tin tải từ lịch sử. Trường deleted_at được lọc khi đọc danh sách nên tin xóa mềm không xuất hiện trở lại.",
        "Đối với tìm kiếm, chuỗi truy vấn được cắt về tối đa 100 ký tự. SQL kết hợp messages với channel_members theo userId của phiên, bỏ tin có deleted_at và so khớp nội dung bằng instr(lower(body), lower(q)). Kết quả được sắp theo id giảm dần, giới hạn 50 hàng. Điều kiện quyền nằm trong truy vấn, giúp tránh đưa tin của DM hoặc nhóm khác vào kết quả rồi mới lọc ở client.",
    ])
    section(doc, para, "4.6 Vận hành và truy cập từ thiết bị", [
        "Docker Compose mặc định công bố 127.0.0.1:8070 trên máy Windows. Cách bind này phù hợp khi chỉ dùng Android Emulator hoặc máy host. Android Emulator truy cập localhost của host qua địa chỉ 10.0.2.2, nên màn hình xác thực dùng URL http://10.0.2.2:8070. Trên iPhone thật, 10.0.2.2 không có ý nghĩa; người dùng nhập IP Wi-Fi của máy Windows và đặt HKCHAT_BIND=0.0.0.0 trước khi tạo lại container.",
        "README hướng dẫn kiểm tra /api/health trước khi mở app. Response có status ok và product HKchat cho thấy API đã lắng nghe; nó không thay cho việc kiểm tra tài khoản và quyền. Docker volume giữ database sau khi dừng hoặc tạo lại container bình thường. Lệnh down -v xóa volume và vì vậy xóa dữ liệu đang lưu; báo cáo chỉ ghi thao tác này như một ranh giới vận hành, không xem đó là bước chạy thông thường.",
        "Bản Expo Go nằm trong expo-preview và đồng bộ giao diện từ App.tsx trước khi chạy. Cách này cho phép kiểm thử giao diện và API trên iPhone từ Windows, trong khi project iOS native ở thư mục ios vẫn cần Xcode trên macOS để build và ký cài trực tiếp. Hai hình thức kiểm thử được phân biệt để không coi Expo Go là bản IPA native đã phát hành.",
    ])


def data_model(doc, table, para, image):
    section(doc, para, "4.7 Quan hệ dữ liệu và khóa ngoại", [
        "Tập dữ liệu cốt lõi gồm users, sessions, channels, channel_members, messages, reactions và group_chats. users là gốc của phiên và quyền tác giả. channels là gốc của hội thoại; channel_members nối người dùng với hội thoại. messages thuộc một kênh và một tác giả, còn reply_to tự tham chiếu tới một tin khác. reactions nối người dùng với tin, cho phép tổng hợp số lượt theo emoji.",
        "SQLite bật PRAGMA foreign_keys = ON để các tham chiếu được kiểm tra. Một số quan hệ có ON DELETE CASCADE, ví dụ xóa kênh sẽ kéo theo membership và messages; báo cáo không mô tả xóa kênh như một thao tác UI vì client hiện chưa cung cấp thao tác đó. Các khóa chính ghép ngăn thành viên bị thêm hai lần vào cùng kênh và ngăn một người gắn cùng emoji hai lần vào một tin.",
    ])
    diagram("data-model-hkchat.png", [
        ("users", "id khóa chính\nusername, email duy nhất\npassword_hash"),
        ("channel_members", "user_id + channel_id\nKhóa chính ghép\nQuyền đọc kênh"),
        ("channels", "id khóa chính\nkind public / dm\ndm_key duy nhất"),
    ], "Quan hệ người dùng và cuộc trò chuyện")
    image(doc, "data-model-hkchat.png", "Hình. Quan hệ users, channel_members và channels", 16.1)
    section(doc, para, "4.8 Từ điển dữ liệu bảng users và sessions", [
        "Bảng users lưu định danh UUID, tên đăng nhập, email, hash mật khẩu và thời điểm tạo. COLLATE NOCASE cùng UNIQUE được đặt cho username và email, giúp kiểm tra trùng không phụ thuộc chữ hoa/chữ thường. Server vẫn kiểm tra dữ liệu đầu vào trước khi INSERT để trả thông báo nghiệp vụ dễ hiểu hơn lỗi ràng buộc thô của SQLite.",
        "Bảng sessions không lưu token thuần. Client nhận token 32 byte ngẫu nhiên ở dạng hex; server băm SHA-256 và lưu token_hash làm khóa chính, cùng user_id và expires_at. Mỗi request có Authorization: Bearer sẽ băm token nhận được rồi tìm phiên chưa hết hạn. Đăng xuất xóa hàng ứng với token hiện tại.",
    ])
    table(doc, ["Bảng.trường", "Kiểu và ràng buộc", "Mục đích"], [
        ("users.id", "TEXT, PRIMARY KEY", "UUID của tài khoản"),
        ("users.username", "TEXT, NOT NULL, UNIQUE, NOCASE", "Tên hiển thị và định danh đăng nhập"),
        ("users.email", "TEXT, NOT NULL, UNIQUE, NOCASE", "Email đăng nhập"),
        ("users.password_hash", "TEXT, NOT NULL", "Chuỗi salt:hash scrypt"),
        ("users.created_at", "INTEGER, NOT NULL", "Mốc tạo tài khoản tính bằng ms"),
        ("sessions.token_hash", "TEXT, PRIMARY KEY", "Hash SHA-256 của token phiên"),
        ("sessions.user_id", "TEXT, FOREIGN KEY", "Người sở hữu phiên"),
        ("sessions.expires_at", "INTEGER, NOT NULL", "Thời điểm hết hạn phiên"),
    ], [4.3, 5.7, 6.7])
    section(doc, para, "4.9 Từ điển dữ liệu bảng channels và channel_members", [
        "channels chứa cả kênh công khai và DM. kind chỉ nhận public hoặc dm theo CHECK trong schema. DM có dm_key duy nhất là hai userId đã được sắp xếp và ghép; với kênh công khai, dm_key để trống. group_chats đánh dấu một channel là nhóm, còn DTO của API trả kind group cho client để hiển thị đúng. Cách mô hình hóa này tận dụng chung messages và membership cho nhiều loại hội thoại.",
        "channel_members dùng khóa chính (channel_id, user_id). Khi đăng ký, hai hàng được thêm cho General và Random. Khi tạo kênh, người tạo được thêm ngay. Khi tham gia kênh công khai hoặc tạo DM/nhóm, bảng này cập nhật quyền đọc tin. Truy vấn danh sách kênh chỉ lấy channel có membership của người đăng nhập.",
    ])
    table(doc, ["Bảng.trường", "Kiểu và ràng buộc", "Mục đích"], [
        ("channels.id", "TEXT, PRIMARY KEY", "UUID cuộc trò chuyện"),
        ("channels.name", "TEXT, NOT NULL", "Tên kênh hoặc DM"),
        ("channels.kind", "TEXT, CHECK public/dm", "Loại lưu ở schema"),
        ("channels.dm_key", "TEXT, UNIQUE", "Cặp người dùng DM"),
        ("channels.created_at", "INTEGER, NOT NULL", "Mốc tạo kênh"),
        ("channel_members.channel_id", "TEXT, PK ghép, FK", "Cuộc trò chuyện"),
        ("channel_members.user_id", "TEXT, PK ghép, FK", "Thành viên"),
        ("channel_members.joined_at", "INTEGER, NOT NULL", "Mốc tham gia"),
        ("group_chats.channel_id", "TEXT, PRIMARY KEY, FK", "Kênh được đánh dấu là nhóm"),
        ("group_chats.creator_id", "TEXT, FOREIGN KEY", "Người tạo nhóm"),
    ], [5.1, 5.7, 5.9])
    section(doc, para, "4.10 Từ điển dữ liệu bảng messages và reactions", [
        "messages dùng id INTEGER PRIMARY KEY AUTOINCREMENT để tăng theo thứ tự ghi. channel_id gắn tin với hội thoại; user_id gắn tác giả. body có ràng buộc CHECK độ dài 1–4000 ký tự. reply_to là khóa ngoại tự tham chiếu; nó cho phép một tin trả lời tin khác và hỗ trợ truy vấn thread bằng CTE đệ quy. created_at, edited_at và deleted_at phân biệt tin gốc, tin sửa và tin đã xóa mềm.",
        "reactions có khóa chính ghép (message_id, user_id, emoji). Khi server tạo DTO, truy vấn GROUP BY message_id và emoji để tính count; biểu thức CASE đánh dấu me nếu người đang xem đã chọn cảm xúc đó. Nhờ vậy client không phải tự tổng hợp từng người thả emoji hoặc tải toàn bộ bản ghi reaction.",
    ])
    table(doc, ["Bảng.trường", "Kiểu và ràng buộc", "Mục đích"], [
        ("messages.id", "INTEGER, AUTOINCREMENT PK", "Thứ tự và định danh tin"),
        ("messages.channel_id", "TEXT, NOT NULL, FK", "Hội thoại chứa tin"),
        ("messages.user_id", "TEXT, NOT NULL, FK", "Tác giả"),
        ("messages.body", "TEXT, CHECK 1–4000 ký tự", "Nội dung"),
        ("messages.reply_to", "INTEGER, FK tự tham chiếu", "Tin được trả lời"),
        ("messages.created_at", "INTEGER, NOT NULL", "Mốc tạo"),
        ("messages.edited_at", "INTEGER, NULL", "Mốc sửa"),
        ("messages.deleted_at", "INTEGER, NULL", "Mốc xóa mềm"),
        ("reactions.message_id", "INTEGER, PK ghép, FK", "Tin được thả cảm xúc"),
        ("reactions.user_id", "TEXT, PK ghép, FK", "Người thả cảm xúc"),
        ("reactions.emoji", "TEXT, PK ghép", "Biểu tượng cảm xúc"),
    ], [5.0, 5.6, 6.1])
    section(doc, para, "4.11 Chỉ mục và ràng buộc toàn vẹn", [
        "Chỉ mục sessions_user_idx phục vụ các thao tác liên quan tới phiên của một người. channel_members_user_idx hỗ trợ truy vấn danh sách kênh của người dùng. messages_channel_idx và messages_user_idx giúp truy vấn tin theo kênh hoặc tác giả; reactions và group_chats đã có khóa chính phù hợp với các phép tra cứu thường dùng. Đây là chỉ mục có trong migration, không phải kết quả benchmark hiệu năng.",
        "Giao dịch BEGIN/COMMIT bao quanh việc tạo người dùng và kênh mặc định, tạo kênh với membership, tạo nhóm với toàn bộ thành viên và tạo DM. Nếu một INSERT lỗi, ROLLBACK tránh để lại kênh không có thành viên hoặc tài khoản chỉ được tạo một phần. Error handler đổi lỗi SQLITE_CONSTRAINT thành HTTP 409 và lỗi nội bộ thành thông báo chung để response không làm lộ chi tiết truy vấn.",
        "Migration được theo dõi trong schema_migrations(version, applied_at). Khi khởi động, server đọc các file có tên dạng số_thứ-tự.sql, bỏ qua phiên bản đã ghi nhận và áp dụng file mới trong transaction. Cơ chế này giữ database hiện có khi nâng cấp; thay đổi schema mới nên thêm migration thay vì sửa file migration đã được chạy.",
    ])


def protocol_detail(doc, table, para):
    section(doc, para, "4.12 Danh mục endpoint của API", [
        "API trả JSON theo cùng cách cho client React Native và bộ test tích hợp. Health, register và login không cần phiên; các route còn lại phải có Bearer token. Endpoint theo kênh luôn kiểm tra membership trước khi đọc hoặc ghi. Endpoint theo tin tra channel_id của tin rồi kiểm tra thành viên kênh, sau đó mới xét tác giả nếu thao tác là sửa hoặc xóa.",
        "Các endpoint được mô tả tiếp theo là giao diện thực tế trong server.mjs. Tham số :id đại diện UUID kênh hoặc id số của tin tùy đường dẫn. Status thành công phản ánh thao tác: 201 cho tài nguyên mới, 200 cho đọc hoặc cập nhật. Error handler dùng 400 cho đầu vào sai, 401 cho chưa đăng nhập, 403 cho không có quyền, 404 cho tài nguyên không tìm thấy và 409 cho trùng dữ liệu.",
    ])
    table(doc, ["Method", "Endpoint", "Quyền", "Mục đích"], [
        ("GET", "/api/health", "Công khai", "Kiểm tra server hoạt động"),
        ("POST", "/api/register", "Công khai", "Tạo tài khoản và phiên"),
        ("POST", "/api/login", "Công khai", "Xác thực và cấp phiên"),
        ("GET", "/api/me", "Có token", "Khôi phục người dùng"),
        ("POST", "/api/logout", "Có token", "Hủy phiên hiện tại"),
        ("GET", "/api/users", "Có token", "Danh sách người dùng khác"),
        ("GET", "/api/channels", "Có token", "Kênh đã tham gia"),
        ("GET", "/api/channels/public", "Có token", "Kênh công khai chưa tham gia"),
        ("POST", "/api/channels", "Có token", "Tạo kênh công khai"),
        ("POST", "/api/channels/:id/join", "Có token", "Tham gia kênh công khai"),
        ("POST", "/api/dm", "Có token", "Tạo hoặc mở DM"),
        ("POST", "/api/groups", "Có token", "Tạo nhóm qua API"),
        ("GET/POST", "/api/channels/:id/messages", "Thành viên", "Đọc hoặc gửi tin"),
        ("GET", "/api/messages/:id/thread", "Thành viên", "Đọc chuỗi trả lời"),
        ("PATCH/DELETE", "/api/messages/:id", "Tác giả", "Sửa hoặc xóa tin"),
        ("POST/DELETE", "/api/messages/:id/reactions", "Thành viên", "Thêm hoặc bỏ cảm xúc"),
        ("GET", "/api/search", "Có token", "Tìm trong kênh có quyền"),
    ], [2.4, 6.6, 2.6, 5.1])
    section(doc, para, "4.13 Cấu trúc request và response", [
        "Request đăng ký gửi JSON với username, email và password. Server không trả password_hash trong response; chỉ trả user và token dùng cho phiên. Request đăng nhập gửi identifier và password, trong đó identifier có thể là tên đăng nhập hoặc email. Client lưu token bằng Keychain thay vì đưa token vào URL. Các request đã đăng nhập gắn Authorization: Bearer <token> trong header.",
        "Request gửi tin gửi body và, nếu đang trả lời, replyTo là số id của tin gốc. Response thành công chứa message DTO: id, channelId, userId, username, body, replyTo, createdAt, editedAt và reactions. Trường reactions là danh sách các mục emoji, count và me; me cho biết người đang xem đã thả cảm xúc đó. Cùng DTO được dùng khi đọc lịch sử và sau khi sửa hoặc thay đổi reaction.",
        "Lỗi được đóng gói dưới khóa error để client hiển thị trong form hoặc banner. Error handler không trả stack trace cho lỗi nội bộ; thay vào đó trả 'Internal server error'. Điều này giữ response nhất quán và tránh đưa câu lệnh SQL hoặc đường dẫn tệp ra phía ứng dụng. Khi một token sai hoặc hết hạn, API trả 401 trước khi xử lý route nghiệp vụ.",
    ])
    table(doc, ["Tình huống", "JSON đầu vào ví dụ", "Phản hồi cốt lõi"], [
        ("Đăng ký", '{"username":"Lan","email":"lan@example.test","password":"********"}', "201; user và token"),
        ("Đăng nhập", '{"identifier":"Lan","password":"********"}', "200; user và token"),
        ("Tạo kênh", '{"name":"du-an-noi-bo"}', "201; channel"),
        ("Mở DM", '{"userId":"<UUID người nhận>"}', "200; channel"),
        ("Gửi reply", '{"body":"Đã nhận","replyTo":42}', "201; message"),
        ("Sửa tin", '{"body":"Nội dung cập nhật"}', "200; message"),
        ("Thả cảm xúc", '{"emoji":"👍"}', "200; message với count mới"),
    ], [3.1, 8.2, 5.4])
    section(doc, para, "4.14 Ma trận quyền truy cập", [
        "Token hợp lệ xác định người dùng nhưng không tự cho phép đọc mọi dữ liệu. Membership là điều kiện thứ hai cho kênh, tin, thread và reaction. Quyền tác giả là điều kiện thứ ba với PATCH/DELETE tin. Tách ba điều kiện này ngăn trường hợp người đã đăng nhập đoán id của một tin hoặc kênh khác rồi truy cập trực tiếp bằng API.",
        "Với kênh công khai chưa tham gia, người dùng có thể thấy tên trong danh sách public nhưng chưa đọc tin. Họ phải gọi join để tạo membership. Với DM, endpoint join không chấp nhận và danh sách public không trả DM. Với nhóm, API public và join cũng không đưa nhóm riêng vào luồng tham gia mở. Những quy tắc này đã được test với tài khoản outsider.",
    ])
    table(doc, ["Hành động", "Người chưa đăng nhập", "Ngoài kênh", "Thành viên", "Tác giả tin"], [
        ("Xem danh sách public", "Không", "Có", "Có", "Có"),
        ("Đọc tin kênh", "Không", "Không", "Có", "Có"),
        ("Gửi tin", "Không", "Không", "Có", "Có"),
        ("Xem thread", "Không", "Không", "Có", "Có"),
        ("Thả cảm xúc", "Không", "Không", "Có", "Có"),
        ("Sửa/xóa một tin", "Không", "Không", "Không", "Có"),
        ("Tìm thấy tin trong kênh", "Không", "Không", "Có", "Có"),
    ], [4.5, 4.0, 2.5, 2.6, 3.1])
    section(doc, para, "4.15 Chu trình migration và khởi động server", [
        "Khi process Node.js bắt đầu, server xác định đường dẫn database từ HKCHAT_DB hoặc dùng tệp mặc định cạnh server.mjs. Nó tạo thư mục cha nếu cần, mở DatabaseSync, bật foreign_keys và journal_mode WAL, rồi bảo đảm schema_migrations tồn tại. Danh sách tệp trong migrations được lọc theo mẫu tên số_*.sql và sắp xếp để áp dụng 001, 002, 003 theo thứ tự.",
        "Với mỗi tệp, server đọc số phiên bản từ tên. Nếu schema_migrations đã có số đó, nó bỏ qua; nếu chưa, nó mở transaction, chạy SQL và ghi applied_at. Lỗi trong SQL làm rollback và dừng khởi động. Cách xử lý này tránh một bản migration được xem là hoàn tất khi chỉ một phần câu lệnh đã chạy. Đây là cơ chế đang có trong mã, không phải công cụ migration bên ngoài.",
        "Sau migration, HTTP server lắng nghe trên 0.0.0.0:8070 bên trong container. Docker quyết định địa chỉ trên máy host qua HKCHAT_BIND. Healthcheck nội bộ gọi GET /api/health; Docker đánh dấu service healthy khi response thành công. Lần chạy gần nhất, API đã trả JSON status ok và product HKchat ở localhost:8070 sau khi container khởi động.",
    ])
    section(doc, para, "4.16 Kịch bản cài đặt lại trên Windows", [
        "Một máy mới cần Node.js đúng phiên bản, Docker Desktop, Android Studio, Android SDK và JDK theo README. Sau npm ci, người dùng mở Docker Desktop, đặt JAVA_HOME và ANDROID_HOME, rồi chạy docker compose -f hkchat/compose.yaml up -d. Lệnh curl tới /api/health xác nhận backend trước khi chạy npm run android. Cách kiểm tra theo thứ tự này tách lỗi dependency, Docker và client để dễ tìm nguyên nhân.",
        "Nếu Docker CLI báo không tìm thấy pipe dockerDesktopLinuxEngine, engine chưa chạy; cần mở Docker Desktop và đợi trạng thái ready. Nếu Compose báo cổng 8070 đã được dùng, kiểm tra process hoặc thử lại khi Docker vừa khởi động. Trong lần kiểm tra ở máy thử, lệnh Compose thứ hai khởi động được container và healthcheck chuyển healthy, nên báo cáo không xem đó là lỗi mã nguồn HKchat.",
        "Nếu health API trả ok nhưng app không đăng nhập được, kiểm tra URL trên thiết bị. Android Emulator cần 10.0.2.2; iPhone cần IP LAN của Windows và Docker bind ra mạng phù hợp. Việc thử Safari trên iPhone tới /api/health giúp phân biệt lỗi mạng với lỗi tài khoản. Đây là quy trình hỗ trợ kiểm thử thực tế đã ghi trong README, không đòi hỏi dịch vụ chat bên ngoài.",
    ])


def workflows(doc, table, para, image):
    section(doc, para, "5.3 Luồng đăng ký và khởi tạo tài khoản", [
        "Người dùng mở HKchat và thấy màn hình nhập địa chỉ server, tên đăng nhập hoặc email, mật khẩu. Khi chọn Đăng ký, form có thêm email và tên đăng nhập. Client loại dấu / cuối địa chỉ và kiểm tra URL trước khi gọi API. Nếu địa chỉ sai, lỗi được hiển thị ngay trong form; nếu kết nối thất bại, người dùng có thể sửa IP hoặc cổng rồi thử lại.",
        "Server chuẩn hóa username bằng trim và email bằng trim/lowercase, kiểm tra định dạng rồi tra users để phát hiện trùng. Khi dữ liệu hợp lệ, transaction tạo user và thêm người đó vào General và Random. Nếu một trong các thao tác thất bại, transaction rollback. Sau commit, server cấp token phiên và trả về user. Client lưu token bằng Keychain và chuyển sang danh sách kênh.",
        "Một tài khoản mới vì vậy có hai kênh mặc định. Điều này là một quyết định trong mã nguồn, không phụ thuộc dữ liệu mẫu. Nếu username/email đã tồn tại, API trả 409; nếu định dạng không đạt, trả 400. Hai nhánh lỗi đều giữ người dùng ở form để sửa đầu vào, không tạo phiên dở dang.",
    ])
    diagram("sequence-auth-hkchat.png", [
        ("Người dùng", "Nhập URL, tên, email\nMật khẩu\nBấm Đăng ký"),
        ("Client", "Kiểm tra URL\nPOST /api/register\nLưu token"),
        ("Server + SQLite", "Validate và transaction\nusers + channel_members\nTrả phiên"),
    ], "Trình tự đăng ký trong HKchat")
    image(doc, "sequence-auth-hkchat.png", "Hình. Trình tự từ form đăng ký tới database", 16.1)
    table(doc, ["Bước", "Tác nhân", "Điều kiện và kết quả"], [
        ("1", "Người dùng", "Nhập URL server, tên, email và mật khẩu"),
        ("2", "Client", "Kiểm tra URL; gửi POST /api/register"),
        ("3", "Server", "Kiểm tra độ dài tên, email, mật khẩu và trùng lặp"),
        ("4", "SQLite", "Ghi users và membership General/Random trong transaction"),
        ("5", "Client", "Nhận token, lưu phiên, tải danh sách kênh"),
    ], [1.2, 3.6, 11.9])
    section(doc, para, "5.4 Luồng đăng nhập, khôi phục phiên và đăng xuất", [
        "Khi đăng nhập, client gửi identifier và password tới /api/login. Server tìm tài khoản theo username hoặc email rồi đối chiếu mật khẩu đã băm. Sai thông tin được phản hồi bằng HTTP 401. Đúng thông tin thì server tạo token mới, gửi về user và thời điểm tạo; client lưu token với service hkchat.local trong Keychain, đồng thời lưu URL server dưới service hkchat.server.",
        "Khi app mở lại, effect khởi tạo đọc URL đã lưu trước rồi đọc token. Client gọi GET /api/me bằng token đó; nếu phiên hợp lệ, user và danh sách kênh được khôi phục, người dùng không phải nhập lại mật khẩu. Nếu token hết hạn hoặc API lỗi, client xóa token đã lưu và trả về màn xác thực. Cơ chế này dựa vào việc server là nguồn xác nhận phiên, không chỉ dựa vào thông tin trên điện thoại.",
        "Khi đăng xuất, client gọi POST /api/logout, server xóa token_hash của phiên hiện tại. Client xóa thông tin phiên và trở về màn xác thực. Địa chỉ server được lưu riêng để lần vào sau không phải nhập lại IP nếu môi trường mạng không thay đổi. Trong Figma, hộp thoại xác nhận đăng xuất là một trạng thái riêng trước khi trở về màn đăng nhập.",
    ])
    section(doc, para, "5.5 Luồng tạo kênh và tham gia kênh", [
        "Trang Kênh phân biệt các kênh người dùng đã tham gia và kênh công khai khác. Khi tạo, client gửi tên kênh mới. Server kiểm tra độ dài 2–80 ký tự, tạo UUID, ghi kênh với kind public và thêm người tạo vào channel_members trong cùng transaction. Sau khi API thành công, client làm mới danh sách và mở kênh để người dùng có thể bắt đầu gửi tin.",
        "Khi tham gia, client gửi POST tới /api/channels/:id/join. Server tìm đúng một kênh public không thuộc group_chats; kênh không hợp lệ trả 404. Lệnh INSERT OR IGNORE trong membership giúp bấm lại không tạo bản ghi trùng. Danh sách kênh có thể tham gia sau đó được làm mới, vì kênh vừa tham gia chuyển sang nhóm Kênh của tôi.",
        "Với hội thoại nhóm, server có API /api/groups để tạo kênh cùng danh sách thành viên và bản ghi group_chats. Tuy nhiên giao diện hiện tại chưa có biểu mẫu tự tạo nhóm; bản chụp dùng nhóm bốn người được chuẩn bị trong database mẫu. Việc phân biệt API và giao diện giúp báo cáo phản ánh đúng chức năng mà người dùng thao tác được.",
    ])
    section(doc, para, "5.6 Luồng DM và kiểm soát người tham gia", [
        "Tab Mọi người tải danh sách user khác tài khoản hiện tại, sắp theo tên. Chạm vào một người gửi userId lên /api/dm. Server kiểm tra người nhận tồn tại, không phải chính người gửi; sau đó ghép hai id theo thứ tự sắp xếp thành dm_key. Nếu đã có DM cho cặp này, API trả lại kênh cũ; nếu chưa, transaction tạo channel kind dm và hai hàng channel_members.",
        "Sau khi mở DM, màn hội thoại dùng cùng thành phần tin nhắn như kênh công khai. Quyền đọc được xác định theo channel_members. Một người thứ ba có token hợp lệ nhưng không thuộc DM vẫn nhận HTTP 403 khi gọi API đọc tin. Tìm kiếm cũng JOIN qua channel_members, do đó nội dung DM không xuất hiện trong kết quả của người thứ ba.",
    ])
    section(doc, para, "5.7 Luồng gửi tin, trả lời và thread", [
        "Khi người dùng viết tin và bấm Gửi, client gửi body tới endpoint messages của kênh đang mở. Nếu đang trả lời, request có thêm replyTo là id của tin được chọn. Server kiểm tra membership và tính hợp lệ của tin đích trong cùng kênh. Sau khi ghi, response trả bản tin đầy đủ để client có thể hiển thị ngay, trong khi cơ chế poll định kỳ đồng bộ các tin mới từ người khác.",
        "Trên giao diện, nhấn giữ một tin mở menu với Trả lời và các hành động tương ứng. Chọn Trả lời đưa nội dung trích dẫn lên thanh ngữ cảnh phía trên ô soạn; người dùng có thể hủy để trở về chế độ gửi tin thường. Trong danh sách, một tin có replyTo hiển thị đoạn trích của tin gốc nếu tin đó còn ở dữ liệu đã tải. Màn hình thread dùng API đệ quy tìm gốc và các tin con khi cần xem chuỗi liên quan.",
        "API thread dùng hai CTE đệ quy: ancestors đi ngược reply_to đến tin gốc, descendants đi từ gốc xuống các phản hồi. Kết quả bỏ tin đã xóa và giới hạn 100 tin. Việc kiểm tra membership diễn ra trước truy vấn, nên biết id tin của kênh khác không đủ để đọc nội dung thread.",
    ])
    diagram("sequence-message-hkchat.png", [
        ("Người gửi", "Chọn kênh\nViết tin / chọn reply\nBấm Gửi"),
        ("API", "Kiểm tra phiên\nKiểm tra membership\nValidate body và replyTo"),
        ("SQLite + client", "INSERT messages\nTrả DTO\nHiển thị và poll"),
    ], "Trình tự gửi và đồng bộ tin")
    image(doc, "sequence-message-hkchat.png", "Hình. Luồng gửi tin và phản hồi từ API", 16.1)
    section(doc, para, "5.8 Luồng sửa, xóa, cảm xúc và tìm kiếm", [
        "Chọn Sửa trên tin của mình chuyển ô soạn sang chế độ chỉnh sửa, giữ bản gốc ở thanh ngữ cảnh. Bấm Lưu gửi PATCH với nội dung mới. Server kiểm tra tác giả và độ dài trước khi cập nhật body, edited_at. Chọn Xóa hiển thị xác nhận; nếu người dùng chấp nhận, client gọi DELETE và server ghi deleted_at. Tin biến mất khỏi danh sách đọc mà không xóa vật lý hàng dữ liệu.",
        "Bộ chọn cảm xúc nằm dưới tin. Chạm một emoji gửi POST; chạm lại cảm xúc của chính mình gửi DELETE theo emoji. Server trả lại DTO với count và me mới, nên giao diện có thể đổi trạng thái được chọn. Người dùng không thuộc kênh không thể thả cảm xúc dù biết id tin.",
        "Ở tab Tìm kiếm, người dùng nhập từ khóa và bấm Tìm kiếm. Client gửi q đã mã hóa URL; API trả tối đa 50 tin phù hợp trong các kênh thành viên. Chạm một kết quả lấy channelId từ response, tìm kênh tương ứng trong danh sách đã tải rồi mở hội thoại. Đây là luồng đang có trong app; bản hiện tại mở hội thoại chứ chưa tự cuộn đến đúng vị trí tin tìm thấy.",
    ])


def design(doc, table, para):
    section(doc, para, "6.3 Nguyên tắc bố cục và phản hồi", [
        "Bộ màn hình lấy vùng tiêu đề tím làm mốc nhận diện và vùng nội dung sáng làm nơi đọc tin. Màn xác thực dùng nền tím toàn trang, thẻ biểu mẫu trắng và nút tím hồng nổi bật để chỉ rõ hành động chính. Sau đăng nhập, thanh tab ba mục nằm ngay dưới tiêu đề; tab được chọn có màu nhấn và chỉ báo dưới chân. Cấu trúc lặp lại giữa các trang giúp người dùng không phải học lại vị trí điều hướng.",
        "Trong hội thoại, bong bóng của người đang dùng có nền hồng nhạt, tin của người khác có nền sáng khác. Tên tác giả được đặt ở đầu bong bóng. Khi trả lời, trích dẫn nằm trước nội dung mới; khi sửa, thanh ngữ cảnh cho biết đang sửa tin nào. Nút cảm xúc đặt sát tin để người dùng thấy hành động gắn với nội dung cụ thể, không phải toàn kênh.",
        "Ứng dụng dùng TextInput với nhãn accessibility cho địa chỉ server, tên, email, mật khẩu, nội dung tin và từ khóa tìm kiếm. Các nút chính dùng accessibilityRole button. Thông báo lỗi có chữ hiển thị trong form hoặc banner, không chỉ đổi màu. Đây là các quyết định triển khai có thể kiểm tra trong App.tsx; báo cáo không gán điểm accessibility định lượng khi chưa chạy công cụ đo chuyên dụng.",
        "Figma dùng khung 390 × 844 px và ghi quy tắc khoảng cách theo bội số 8 px. Các thành phần được tách layer để sửa nội dung, màu và hình khối. Trang Design System bổ sung Button, Input, Tab, Message và Avatar cùng các biến thể trạng thái. File thiết kế đóng vai trò mô phỏng hướng đi; ảnh Android trong báo cáo chứng minh một số màn hình của ứng dụng đang chạy.",
    ])
    table(doc, ["Thành phần", "Trạng thái trong Figma", "Cách dùng"], [
        ("Button", "Primary, Secondary, Disabled, Destructive", "Hành động gửi, xác nhận, hủy hoặc xóa"),
        ("Input", "Default, Focused, Error", "Đăng nhập, tạo kênh, tìm kiếm"),
        ("Tab", "Selected, Default", "Kênh, Mọi người, Tìm kiếm"),
        ("Message", "Mine, Other", "Phân biệt người gửi trong hội thoại"),
        ("Avatar", "Member", "Danh sách người dùng"),
    ], [2.8, 6.2, 7.7])
    section(doc, para, "6.4 Các trạng thái xác thực và kênh", [
        "Màn 01 là điểm bắt đầu Flow 1: form nhập URL server, tên hoặc email và mật khẩu. Màn 02 thêm trường tên đăng nhập và email để tạo tài khoản. Màn 03 minh họa lỗi kết nối hoặc URL không dùng được. Ba trạng thái chung khung nhận diện và thẻ form nên người dùng hiểu đây là một bước xác thực với các trường hợp khác nhau, không phải ba ứng dụng độc lập.",
        "Màn 04 liệt kê kênh đã tham gia và ba tab chính. Màn 05 minh họa nhập tên kênh mới, bấm Tạo kênh và chuyển sang hội thoại. Màn 06 cho thấy kênh công khai chưa tham gia với hành động Tham gia. Khi đánh giá prototype, luồng từ màn danh sách tới các trạng thái tạo, tham gia và trở lại kênh đã được nối bằng tương tác của plugin Figma.",
        "Trong ứng dụng thật, tài khoản mới có General và Random nhờ server tạo membership trong transaction đăng ký. Kênh có thể tham gia được tải từ endpoint riêng, chỉ trả kênh public mà người dùng chưa là thành viên và không phải group chat. Vì vậy phần hiển thị trên màn 04–06 có quy tắc dữ liệu đi kèm, không chỉ là bố cục minh họa.",
    ])
    table(doc, ["Màn", "Nội dung", "Hành động chính"], [
        ("01", "Đăng nhập và URL server", "Đăng nhập; chuyển sang Đăng ký"),
        ("02", "Đăng ký", "Tạo tài khoản; quay lại Đăng nhập"),
        ("03", "Lỗi địa chỉ server", "Sửa URL hoặc thông tin và thử lại"),
        ("04", "Danh sách kênh", "Mở kênh, đổi tab, tạo/tham gia"),
        ("05", "Tạo kênh mới", "Nhập tên rồi tạo"),
        ("06", "Tham gia kênh", "Bấm Tham gia để mở hội thoại"),
    ], [1.5, 6.1, 9.1])
    section(doc, para, "6.5 Mọi người, DM và hội thoại nhóm", [
        "Màn 07 là danh sách thành viên để bắt đầu DM. Dòng người dùng có avatar chữ đầu và ký hiệu mở ở bên phải. Màn 08 là hội thoại riêng giữa Huy và Khải, dùng cùng định dạng tin với màn nhóm. Tên cuộc trò chuyện thay cho tên ứng dụng ở thanh tiêu đề; nút Trở lại đưa người dùng về danh sách.",
        "Màn 09 trình bày hội thoại nhóm bốn người. Dữ liệu mẫu dùng các tên Huy, Khải, Tân và Đạt với nội dung trò chuyện về đồ án để dễ nhận ra nhiều tác giả; đó là nội dung kiểm thử, không giới hạn HKchat cho chủ đề học tập. Mục đích sử dụng sản phẩm vẫn là nhắn tin nội bộ cho nhóm làm việc. Tin của Huy dùng nền hồng nhạt, các tin còn lại dùng nền sáng trung tính.",
        "Khi mở một kênh hoặc DM, client đặt current, tải tối đa 100 tin ban đầu và lặp yêu cầu lấy tin mỗi hai giây. Đổi hội thoại sẽ hủy timer cũ, xóa bản nháp, trạng thái reply/sửa và bộ chọn emoji để tránh thao tác nhầm trên cuộc trò chuyện trước. Những chi tiết này liên quan trực tiếp tới tính nhất quán của màn 08–09.",
    ])
    section(doc, para, "6.6 Các thao tác trên tin", [
        "Màn 10 hiển thị thanh trả lời với trích dẫn ngắn; ô soạn chứa nội dung mới và nút Gửi. Màn 11 dùng cùng vị trí thanh ngữ cảnh nhưng nhãn chuyển thành Sửa và nút thành Lưu. Người dùng có thể bấm × để hủy thao tác. Việc chia hai trạng thái cho phép reviewer thấy sự khác biệt giữa tạo reply mới và cập nhật tin đã có.",
        "Màn 12 hiển thị bộ emoji và số lượt phản ứng. Màn 13 là menu tùy chọn sau nhấn giữ tin, gồm Trả lời, Sửa, Thêm và Hủy trong prototype; thao tác app thật tùy quyền của người dùng đối với tin. Màn 14 là hộp xác nhận Xóa, tạo một bước kiểm tra trước khi gửi DELETE. Trong server, xóa chỉ ghi deleted_at và tác giả mới được phép thực hiện.",
        "Các trạng thái 10–14 dùng cùng một nền hội thoại để người xem hiểu thao tác bắt đầu từ tin đã chọn. Figma nối những nút này tới trạng thái tiếp theo, còn Android screenshot cho thấy trực tiếp thanh reply trong ứng dụng đang chạy. Nhờ đó case study có cả quyết định thiết kế lẫn bằng chứng triển khai.",
    ])
    table(doc, ["Màn", "Trạng thái", "Quy tắc nghiệp vụ liên quan"], [
        ("10", "Trả lời", "replyTo trỏ tin còn tồn tại trong cùng kênh"),
        ("11", "Sửa", "Chỉ tác giả PATCH được tin"),
        ("12", "Thả cảm xúc", "Một emoji/người/tin là duy nhất"),
        ("13", "Tùy chọn tin", "Hành động phụ thuộc tin và quyền"),
        ("14", "Xác nhận xóa", "Chỉ tác giả DELETE được; server xóa mềm"),
    ], [1.5, 5.7, 9.5])
    section(doc, para, "6.7 Tìm kiếm và kết thúc phiên", [
        "Màn 15 là form từ khóa với hướng dẫn khi chưa tìm. Màn 16 hiển thị kết quả gồm tên tác giả và đoạn nội dung, đủ để người dùng chọn đúng tin. Màn 17 là hội thoại sau khi mở kết quả; app thật mở kênh tương ứng. Vì client chưa tự cuộn đến id tin được chọn, báo cáo chỉ khẳng định hành vi mở hội thoại chứ không khẳng định định vị chính xác tin trong lịch sử.",
        "Màn 18 là hộp thoại xác nhận Đăng xuất trên nền danh sách kênh. Chọn Hủy giữ nguyên phiên; chọn Đăng xuất trở về form xác thực. Đây là điểm kết thúc tự nhiên của Flow 1. Plugin Figma đã kiểm đếm và người dùng xác nhận có thể đi tới 18/18 màn hình từ điểm bắt đầu.",
        "Bộ ảnh case study dùng các màn ứng dụng thật cho đăng nhập, kênh, hội thoại, reply, tìm kiếm và mở kết quả; ảnh Figma dùng để trình bày độ bao phủ thiết kế. Phân biệt hai loại ảnh này giúp người xem biết phần nào là app chạy thật và phần nào là prototype tương tác.",
    ])
    table(doc, ["Màn", "Nội dung", "Liên hệ chức năng"], [
        ("15", "Nhập từ khóa", "GET /api/search?q=..."),
        ("16", "Danh sách kết quả", "Tối đa 50 tin trong kênh có quyền"),
        ("17", "Mở hội thoại", "Dùng channelId của kết quả"),
        ("18", "Xác nhận đăng xuất", "POST /api/logout và xóa phiên client"),
    ], [1.5, 6.3, 8.9])


def testing(doc, table, para):
    section(doc, para, "8.3 Phương pháp kiểm thử API", [
        "Tệp server.test.mjs sử dụng node:test và assert. Trước mỗi lần chạy, test tạo thư mục tạm và file SQLite mới, tìm cổng localhost trống rồi spawn server.mjs với HKCHAT_DB và HKCHAT_PORT riêng. Hàm call gửi HTTP request thật tới server và đọc JSON response. Cách này kiểm tra cả route, xác thực, truy vấn và persistence thay vì chỉ gọi hàm nội bộ.",
        "Một bài test tích hợp bao phủ nhiều assertion liên tiếp. Test tạo năm tài khoản thử, sau đó đi qua tạo nhóm, DM, gửi và reply, sửa, cảm xúc, tìm kiếm, xóa, kênh công khai, phân trang và khởi động lại server. Mỗi assertion đối chiếu status hoặc payload với kết quả mong đợi. Kết thúc bài test, process server bị dừng và thư mục tạm được xóa. Vì vậy số '1/1 bài test' biểu thị một kịch bản tích hợp dài, không phải chỉ một request.",
        "Khi đánh giá kết quả, cần phân biệt API test tự động với kiểm thử giao diện trên thiết bị. API test xác nhận dữ liệu và quyền; ảnh Android chứng minh một số thao tác nhìn thấy được trong emulator; người dùng đã xác nhận prototype Figma có 18/18 màn hình đi tới được. Báo cáo không gộp ba loại bằng chứng thành một phép đo UX hay hiệu năng.",
    ])
    table(doc, ["ID", "Dữ liệu hoặc thao tác", "Kết quả được assert trong test"], [
        ("TC01", "Đăng ký 5 user", "Mỗi request trả HTTP 201"),
        ("TC02", "Đăng nhập bằng tên có dấu Đạt", "HTTP 200"),
        ("TC03", "Đăng nhập sai mật khẩu", "HTTP 401"),
        ("TC04", "Gọi /api/channels không token", "HTTP 401"),
        ("TC05", "Tạo nhóm bốn người", "HTTP 201, kind group"),
        ("TC06", "Tạo nhóm với userId không tồn tại", "HTTP 400"),
        ("TC07", "Người ngoài đọc nhóm", "HTTP 403"),
        ("TC08", "Người ngoài join nhóm riêng", "HTTP 404"),
        ("TC09", "Tạo DM của Alice và Bob", "HTTP 200, có channel id"),
        ("TC10", "Charlie đọc hoặc tìm DM", "HTTP 403 khi đọc, 0 kết quả tìm"),
    ], [1.2, 6.4, 9.1])
    section(doc, para, "8.4 Ca kiểm thử tin và thread", [
        "Test gửi tin 'private hello' trong DM, sau đó so sánh nội dung đọc từ phía thành viên còn lại. Tin mới có replyTo null và mảng reactions rỗng. Bob gửi một tin trả lời; test xác nhận replyTo đúng id tin gốc. Reply tới id không tồn tại bị từ chối 400, còn người ngoài DM cố gửi reply bị từ chối 403.",
        "Test tạo thêm một phản hồi lồng nhau rồi gọi /api/messages/:id/thread. Kết quả trả chuỗi id từ tin gốc qua tin trả lời đến tin lồng. Khi Charlie gọi endpoint thread của DM, API trả 403. Các assertion này kiểm tra cả quan hệ đệ quy và lớp quyền truy cập trước khi dữ liệu thread được trả.",
        "Bob sửa tin trả lời của mình; test xác nhận body đã trim và nội dung cũ không còn xuất hiện trong tìm kiếm. Alice và Charlie không thể sửa tin của Bob, dù Alice là thành viên DM. Nội dung chỉ có khoảng trắng bị từ chối 400. Sau khi Bob xóa tin, sửa lại hoặc gắn cảm xúc vào tin đã xóa đều trả 404; thread và tìm kiếm không chứa tin đó.",
    ])
    table(doc, ["ID", "Dữ liệu hoặc thao tác", "Kết quả được assert trong test"], [
        ("TC11", "Gửi và đọc tin DM", "HTTP 201; thành viên đọc đúng body"),
        ("TC12", "Reply tới tin hợp lệ", "replyTo bằng id tin gốc"),
        ("TC13", "Reply tới id không tồn tại", "HTTP 400"),
        ("TC14", "Người ngoài gửi reply", "HTTP 403"),
        ("TC15", "Đọc thread lồng nhau", "Đúng thứ tự id gốc, con, cháu"),
        ("TC16", "Người ngoài đọc thread", "HTTP 403"),
        ("TC17", "Người khác sửa tin", "HTTP 403"),
        ("TC18", "Sửa tin của mình", "Body mới được trim và trả trong response"),
        ("TC19", "Sửa thành nội dung trống", "HTTP 400"),
        ("TC20", "Xóa tin của mình", "HTTP 200, tin không còn trong thread"),
    ], [1.2, 6.4, 9.1])
    section(doc, para, "8.5 Ca kiểm thử cảm xúc, tìm kiếm và lưu trữ", [
        "Với cảm xúc, test thử người ngoài DM và emoji rỗng trước; hai thao tác lần lượt trả 403 và 400. Alice và Bob cùng gắn 👍 lên một tin; số lượt trở thành 2, cờ me trong response của từng người là true. Gắn lại cùng emoji của cùng người không làm tăng count vì khóa chính ghép và INSERT OR IGNORE. Khi Bob bỏ cảm xúc, Alice vẫn thấy count 1 và me true.",
        "Test tạo một kênh công khai mới. Bob chưa tham gia nên chưa đọc được tin; sau POST /join, request đọc trả 200. Kịch bản gửi 105 tin vào kênh này để xác nhận lần đọc đầu chỉ trả 100 tin mới nhất. Với tham số after trỏ id gần cuối, API chỉ trả tin mới hơn. Đây là kiểm thử phân trang theo id, không phải benchmark số lượng người dùng đồng thời.",
        "Cuối cùng test dừng server và khởi động lại với cùng file SQLite tạm. Tài khoản vẫn đăng nhập được, tin DM và cảm xúc còn tồn tại. Điều này xác nhận dữ liệu được ghi xuống file database, không chỉ giữ trong bộ nhớ process. Trên môi trường Docker, volume đóng vai trò giữ file tương ứng qua vòng đời container.",
    ])
    table(doc, ["ID", "Dữ liệu hoặc thao tác", "Kết quả được assert trong test"], [
        ("TC21", "Người ngoài thả cảm xúc", "HTTP 403"),
        ("TC22", "Emoji rỗng", "HTTP 400"),
        ("TC23", "Hai thành viên thả 👍", "Count = 2, me đúng theo người xem"),
        ("TC24", "Một người thả lại 👍", "Count không tăng thêm"),
        ("TC25", "Bỏ cảm xúc", "Count giảm còn 1"),
        ("TC26", "Tìm nội dung DM", "Thành viên thấy; người ngoài không thấy"),
        ("TC27", "Tạo kênh, đọc trước/sau join", "403 trước, 200 sau khi tham gia"),
        ("TC28", "Đọc sau khi gửi 105 tin", "Chỉ 100 tin mới nhất"),
        ("TC29", "Đọc với tham số after", "Chỉ tin id lớn hơn mốc"),
        ("TC30", "Khởi động lại server", "Tin và cảm xúc được giữ trong SQLite"),
    ], [1.2, 6.4, 9.1])
    section(doc, para, "8.6 Kiểm tra build và giao diện", [
        "Lệnh npm.cmd run typecheck chạy TypeScript ở chế độ noEmit để phát hiện lỗi kiểu trong client. Lệnh npm.cmd run test:server chạy bộ test tích hợp nói trên. Android debug build dùng Gradle assembleDebug với JDK 23 trên máy thử; kết quả BUILD SUCCESSFUL đã được ghi nhận. Các phép kiểm tra này cần chạy lại khi mã nguồn thay đổi trước khi nộp bản cuối.",
        "Kiểm thử Android Emulator được minh họa bằng ảnh nhập server/đăng nhập, danh sách kênh, hội thoại nhóm, reply, tìm kiếm và mở lại hội thoại. Ảnh giúp xác nhận bố cục và một số trạng thái chính trên thiết bị ảo. Bản iPhone từ Windows được thử qua Expo Go SDK 58 trên cùng Wi-Fi với server local; người dùng đã đăng nhập thành công khi URL trỏ tới IP LAN đúng. Báo cáo không gọi đó là bản iOS native đã build bằng Xcode.",
        "Trong Figma, hai plugin của dự án tạo màn hình dạng layer và bổ sung Design System cùng liên kết prototype. Người dùng đã xác nhận plugin báo 18/18 màn hình đi tới được từ Flow 1. Kết quả đó kiểm tra đồ thị điều hướng của thiết kế; nó khác với việc xác thực dữ liệu nhập thật trên ứng dụng chạy. Vì vậy phần trình bày giữ tách biệt giữa prototype và ảnh chụp Android.",
    ])
    section(doc, para, "8.7 Ranh giới kết quả", [
        "Những mục có bảng trong migration 002_features.sql như gọi thoại, AI, playbook hoặc push không được báo cáo như tính năng đang sử dụng, vì server hiện không có route nghiệp vụ và client không có màn hình tương ứng cho chúng. Tương tự, bảng attachments trong 001_core.sql không chứng minh tải tệp đã hoạt động. Phạm vi kiểm thử và ảnh minh họa của tài liệu tập trung vào xác thực, kênh, DM, tin nhắn và tìm kiếm.",
        "Ứng dụng local dùng HTTP cho thử nghiệm mạng nội bộ. Khi đưa ra mạng ngoài, cần một cấu hình TLS và chính sách vận hành riêng; báo cáo này không tuyên bố đã có triển khai công khai. Không có số đo tải, thời gian phản hồi hoặc tỷ lệ lỗi trên nhiều thiết bị, nên các chỉ tiêu hiệu năng không được gán giá trị. Cách ghi giới hạn này giúp phân biệt sản phẩm hiện có với những khả năng chỉ mới có cấu trúc dữ liệu hoặc ý tưởng.",
    ])


def manual_walkthrough(doc, table, para):
    section(doc, para, "8.8 Kịch bản trình diễn trên Android Emulator", [
        "Kịch bản trình diễn bắt đầu bằng việc kiểm tra Docker Desktop đang chạy và GET http://localhost:8070/api/health trả status ok. Trong Android Studio, nhóm mở emulator rồi chạy ứng dụng bằng npm.cmd run android. Tại form đầu, URL phải là http://10.0.2.2:8070. Nếu URL sai, phản hồi lỗi kết nối trước khi thử tài khoản giúp phân biệt mạng và xác thực.",
        "Người trình diễn có thể đăng ký tài khoản mới hoặc dùng tài khoản mẫu trong database của nhóm. Sau đăng nhập, kiểm tra tab Kênh có General, Random và các kênh đã tham gia. Chọn một kênh để xem tin; trở lại danh sách, nhập tên kênh mới và bấm Tạo kênh. Từ tài khoản thứ hai, tìm kênh đó trong Kênh có thể tham gia, bấm Tham gia và gửi một tin. Bước này chứng minh membership được cập nhật qua API.",
        "Sang tab Mọi người, chọn một thành viên để mở DM. Gửi một tin riêng và đăng nhập tài khoản khác trên thiết bị hoặc qua bộ test để xác nhận người ngoài không đọc được. Trong hội thoại nhóm mẫu, nhấn giữ một tin, chọn Trả lời, nhập nội dung và gửi; sau đó thử thả cảm xúc bằng dấu cộng. Với tin của mình, mở tùy chọn để sửa hoặc xóa. Với tin của người khác, API vẫn bảo vệ quyền tác giả dù giao diện có hay không hiển thị nút.",
        "Cuối cùng sang tab Tìm kiếm, nhập một từ có trong hội thoại, xem kết quả và chạm vào tin để mở lại kênh. Màn hiện tại mở hội thoại nhưng không tự cuộn đến đúng tin, nên khi demo cần mô tả đúng giới hạn này. Chọn Đăng xuất để kết thúc phiên; mở lại app nhằm kiểm tra token không còn khôi phục phiên vừa hủy.",
    ])
    table(doc, ["Bước", "Thao tác trên app", "Dấu hiệu cần quan sát"], [
        ("01", "Mở /api/health", "JSON status ok, product HKchat"),
        ("02", "Mở app, nhập URL", "Form đăng nhập hiển thị đúng server"),
        ("03", "Đăng ký hoặc đăng nhập", "Chuyển sang danh sách kênh"),
        ("04", "Tạo và tham gia kênh", "Kênh chuyển vào danh sách của người dùng"),
        ("05", "Gửi tin và mở DM", "Tin hiển thị trong hội thoại đúng"),
        ("06", "Trả lời, sửa, xóa, cảm xúc", "Ngữ cảnh, body và count cập nhật"),
        ("07", "Tìm kiếm và mở kết quả", "Mở đúng cuộc trò chuyện"),
        ("08", "Đăng xuất", "Trở về màn xác thực"),
    ], [1.3, 7.0, 8.4])
    section(doc, para, "8.9 Kịch bản thử trên iPhone cùng mạng", [
        "Vì máy phát triển dùng Windows, bản thử iPhone chạy trong Expo Go SDK 58. Trước tiên, Compose cần bind API ra mạng nội bộ bằng HKCHAT_BIND=0.0.0.0 và container được tạo lại. Từ iPhone cùng Wi-Fi, Safari mở http://<IP-LAN-Windows>:8070/api/health. Nếu trang này không trả JSON, lỗi thuộc mạng, firewall hoặc địa chỉ; không nên thử đăng nhập trước khi kết nối cơ bản hoạt động.",
        "Bản Expo Go được chạy từ expo-preview với Metro trên cổng 8082. Người dùng đăng nhập cùng Expo Account trên máy tính và iPhone, quét QR rồi mở bản xem thử. Form của HKchat cần trỏ tới IP LAN của Windows, không phải localhost hay 10.0.2.2. Khi server reachable và URL đúng, các thao tác đăng nhập, mở kênh, DM và gửi tin dùng cùng API Node.js với bản Android.",
        "Kịch bản này đã từng được kiểm tra đến mức màn đăng nhập và đăng nhập thành công trên iPhone trong mạng nội bộ. Báo cáo không suy ra bản iOS native đã ký và cài độc lập. Để tạo IPA hoặc chạy từ Xcode, project ios/HKchat.xcodeproj cần máy Mac và cấu hình signing của Apple.",
    ])
    section(doc, para, "8.10 Nhật ký lỗi khởi động Docker và cách xác nhận", [
        "Một lần chạy mới trên Windows cho thấy npm.cmd ci cài 596 package thành công, nhưng Docker CLI ban đầu báo không tìm thấy pipe dockerDesktopLinuxEngine. Đây là dấu hiệu Docker Desktop/engine chưa chạy, không phải lỗi TypeScript hoặc package của HKchat. Sau khi Docker Desktop khởi động, Compose lần đầu báo cổng 8070 tạm thời không bind được. Kiểm tra netstat không thấy listener bền vững trên 8070 và cổng này không thuộc dải cổng Windows loại trừ.",
        "Chạy lại docker compose -f hkchat/compose.yaml up -d đã khởi động container. docker compose ps hiển thị trạng thái healthy và mapping 127.0.0.1:8070->8070/tcp. Lệnh curl trả {status:ok, product:HKchat}. Chuỗi bằng chứng này phân biệt một lỗi khởi động môi trường tạm thời với lỗi API. Khi tài liệu hướng dẫn máy mới, nhóm đặt kiểm tra Docker Desktop và healthcheck trước lệnh mở app.",
    ])


def glossary(doc, table, para):
    doc.add_heading("Phụ lục thuật ngữ và đối chiếu mã nguồn", 1)
    para(doc, "Các thuật ngữ dưới đây được dùng nhất quán trong báo cáo để người đọc đối chiếu thiết kế, API và database. Chúng phản ánh cách HKchat đặt tên ở bản hiện tại.")
    table(doc, ["Thuật ngữ", "Nghĩa trong HKchat", "Vị trí kiểm tra"], [
        ("Kênh công khai", "Cuộc trò chuyện có thể tìm và tham gia", "channels.kind = public; /api/channels/public"),
        ("DM", "Cuộc trò chuyện hai người với dm_key duy nhất", "POST /api/dm; channel_members"),
        ("Nhóm", "Channel được đánh dấu trong group_chats", "POST /api/groups; nhóm mẫu trong DB"),
        ("Phiên", "Bearer token có hạn, lưu hash trên server", "sessions; /api/me, /api/logout"),
        ("Reply", "Tin chứa id tin được trả lời", "messages.reply_to; thread API"),
        ("Reaction", "Cảm xúc của một người trên một tin", "reactions; message DTO"),
        ("Xóa mềm", "Ghi deleted_at và lọc khỏi kết quả", "messages.deleted_at"),
        ("Flow 1", "Điểm bắt đầu prototype Figma", "Màn 01, 18/18 trạng thái đi tới được"),
        ("Healthcheck", "Truy vấn kiểm tra API còn đáp ứng", "GET /api/health; compose.yaml"),
    ], [3.2, 6.8, 6.7])
    para(doc, "Các đường dẫn nêu trong phần này là điểm bắt đầu để kiểm tra lại từng khẳng định. Test API nằm trong hkchat/server/server.test.mjs; giao diện di động trong hkchat/mobile/App.tsx; schema trong hkchat/server/migrations; cấu hình container trong hkchat/compose.yaml; ảnh kiểm thử ở docs/report-images; file Figma được liên kết tại phần thiết kế.")
