"""Academic analysis chapters for the HKchat report, based on checked project evidence."""

def market_research(doc, table, para):
    doc.add_heading('Khảo sát năm sản phẩm tương đồng', 2)
    para(doc, 'Phương pháp khảo sát là đọc tài liệu chức năng chính thức của năm sản phẩm nhắn tin cho nhóm và đối chiếu với các luồng đã triển khai trong HKchat. Đây là khảo sát tài liệu thứ cấp; nhóm chưa phỏng vấn người dùng hoặc đo hiệu năng của các sản phẩm. Vì vậy, “khoảng trống” dưới đây chỉ nêu khác biệt về phạm vi của bản HKchat, không kết luận sản phẩm khác kém chất lượng.')
    entries = [
        ('Slack', 'Kênh và tin nhắn trực tiếp là hai cách tổ chức hội thoại chính; tìm kiếm hỗ trợ lọc theo cuộc trò chuyện và người gửi.', 'Nhiều tính năng cộng tác ngoài phạm vi đồ án. HKchat chọn luồng ngắn gồm kênh, DM, reply và tìm tin bằng từ khóa; chưa có bộ lọc tìm kiếm nâng cao.', 'Điểm rút ra cho thiết kế là phải làm rõ điểm vào của mỗi loại hội thoại. Danh sách kênh cần hiển thị ngay sau đăng nhập; DM cần mở từ danh sách người dùng; kết quả tìm kiếm phải quay lại hội thoại. Ba luồng này đã được đặt vào ba tab của client. Các bộ lọc theo người gửi hoặc thời gian có thể bổ sung sau khi luồng cơ bản được kiểm thử ổn định.', 'https://slack.com/help/articles/1500000019301-Find-and-start-conversations'),
        ('Microsoft Teams', 'Nhóm và kênh gắn với dự án hoặc đơn vị, có phân loại kênh tiêu chuẩn, riêng tư và chia sẻ.', 'HKchat chưa có mô hình team, vai trò quản trị hay kênh riêng tư. Bản hiện tại dùng kênh công khai và membership để giới hạn quyền đọc hội thoại.', 'Khảo sát này cho thấy tên kênh và phạm vi thành viên là hai thông tin khác nhau. Trong HKchat, kênh công khai có thể xuất hiện ở danh sách tham gia, còn DM và nhóm không xuất hiện ở đó. Server kiểm tra channel_members trước khi đọc tin. Giải pháp này đáp ứng bài toán thử nghiệm nhóm nhỏ, nhưng chưa thay thế được mô hình quản trị tổ chức hoặc nhiều cấp quyền như Teams.', 'https://learn.microsoft.com/en-us/microsoftteams/teams-channels-overview'),
        ('Google Chat', 'Space hỗ trợ trao đổi nhóm; trả lời một tin có thể mở luồng riêng để giữ ngữ cảnh.', 'HKchat lưu reply_to và hiển thị trích dẫn trong hội thoại. Bản hiện tại chưa có trải nghiệm thread tách riêng đầy đủ như sản phẩm tham chiếu.', 'Ý tưởng quan trọng là phản hồi phải gắn với tin gốc thay vì chỉ đứng sau nó theo thời gian. HKchat lưu id tin được trả lời trong messages.reply_to và API có endpoint đọc thread. Ở giao diện hiện tại, người dùng thấy phần trích dẫn khi trả lời; một màn hình thread độc lập và chỉ báo số phản hồi vẫn là hướng hoàn thiện. Vì vậy báo cáo tách khả năng của API khỏi mức độ hoàn thiện trên UI.', 'https://support.google.com/chat/answer/12176589?hl=en'),
        ('Zulip', 'Tổ chức hội thoại bằng channel và topic; tìm kiếm có bộ lọc theo channel, topic, người gửi và DM.', 'HKchat chưa có topic. Tên kênh và liên kết reply_to giúp phân nhóm ở mức đồ án; tìm kiếm chỉ khớp từ khóa trong các kênh được phép đọc.', 'Zulip làm rõ lợi ích của việc gắn ngữ cảnh cho nội dung ngay từ lúc gửi. Với thời gian và phạm vi triển khai của đồ án, HKchat dùng tên kênh để tách chủ đề lớn và reply để nối câu trả lời với một tin cụ thể. Tìm kiếm theo từ khóa phục vụ việc tra lại; chưa có toán tử tìm kiếm hoặc topic. Đây là giới hạn chức năng được nêu rõ để không đánh đồng hai mô hình tổ chức hội thoại.', 'https://zulip.com/help/getting-started-with-zulip'),
        ('Rocket.Chat', 'Có kênh, nhóm, DM, thread, tìm kiếm và lựa chọn tự vận hành máy chủ.', 'HKchat cũng chạy server riêng nhưng chỉ là bản phục vụ nhóm nhỏ; chưa có quản trị tổ chức, chia sẻ tệp hoặc thông báo đẩy như hệ sản phẩm đầy đủ.', 'Sản phẩm tham chiếu này cho thấy tự vận hành máy chủ là một lựa chọn phổ biến, không phải điểm độc quyền của HKchat. Đóng góp của đồ án nằm ở việc tự thiết kế và kiểm chứng một phiên bản nhỏ: Node.js API, SQLite, Docker volume, client React Native và bộ kiểm thử quyền truy cập. Báo cáo chỉ đánh giá những phần nhóm thực sự chạy được trên máy local và thiết bị thử.', 'https://docs.rocket.chat/docs/our-plans'),
    ]
    for i, (name, strength, scope, insight, url) in enumerate(entries, 1):
        p = doc.add_paragraph()
        p.add_run(f'{i}. {name}. ').bold = True
        p.add_run('Đặc điểm và thế mạnh: ').bold = True
        p.add_run(strength)
        p = doc.add_paragraph()
        p.add_run('Giới hạn đối chiếu và lựa chọn cho HKchat: ').bold = True
        p.add_run(scope)
        p = doc.add_paragraph()
        p.add_run('Bài học áp dụng: ').bold = True
        p.add_run(insight)
        para(doc, f'Nguồn tài liệu: {url}')
    doc.add_heading('Bảng đối sánh và khoảng trống giải pháp', 2)
    table(doc, ['Tiêu chí', 'Sản phẩm tham chiếu', 'HKchat hiện tại', 'Căn cứ'], [
        ('Kênh / nhóm', 'Cả năm sản phẩm có cách trao đổi nhóm', 'Kênh công khai; nhóm mẫu 4 người', 'channels, group_chats, ảnh Android'),
        ('DM', 'Slack, Teams, Google Chat, Zulip, Rocket.Chat', 'DM hai người, khóa cặp người dùng', 'POST /api/dm, dm_key'),
        ('Trả lời theo ngữ cảnh', 'Slack/Google Chat/Rocket.Chat có thread', 'reply_to, trích dẫn; chưa có đầy đủ màn thread riêng', 'messages.reply_to, App.tsx'),
        ('Tìm kiếm', 'Có ở các sản phẩm tham chiếu', 'Từ khóa trong kênh có quyền; tối đa 50 kết quả', 'GET /api/search'),
        ('Vận hành server', 'Rocket.Chat có bản tự vận hành', 'Node.js, SQLite, Docker trên máy nhóm', 'compose.yaml'),
    ], [2.7, 4.6, 5.9, 3.5])
    para(doc, 'Cơ hội sản phẩm của HKchat trong phạm vi đồ án là cung cấp một bộ chức năng giao tiếp văn bản dễ trình diễn, có cơ sở dữ liệu riêng và đường chạy local rõ ràng. Đây là lựa chọn triển khai có chủ đích; báo cáo không khẳng định HKchat có ưu thế tính năng hoặc hiệu năng so với các nền tảng trưởng thành.')


def idea_chapter(doc, table, para):
    doc.add_heading('Hình thành ý tưởng và lý do lựa chọn', 1)
    doc.add_heading('Phát biểu bài toán', 2)
    para(doc, 'Một nhóm làm việc cần có nơi để thông báo chung, trao đổi theo chủ đề, nói chuyện riêng và tìm lại quyết định cũ. Nếu toàn bộ nội dung nằm trong một luồng chat duy nhất, các chủ đề dễ trộn lẫn và việc tìm thông tin trở nên khó hơn. Nếu phải cấu hình nhiều dịch vụ cho một bản trình diễn nhỏ, nhóm gặp thêm công việc vận hành. Bài toán của HKchat là tạo một hệ thống di động có kênh, DM, liên kết trả lời và tìm kiếm, chạy được trên server do nhóm quản lý.')
    doc.add_heading('Đối tượng và bối cảnh sử dụng', 2)
    table(doc, ['Nhân vật', 'Nhu cầu', 'Tình huống tiêu biểu'], [
        ('Thành viên mới', 'Tạo tài khoản, vào kênh chung', 'Nhập URL server, đăng ký, thấy General và Random'),
        ('Thành viên đang làm việc', 'Trao đổi chung và riêng', 'Mở kênh theo chủ đề hoặc DM một đồng nghiệp'),
        ('Người cần tra cứu', 'Tìm lại một tin và ngữ cảnh', 'Gõ từ khóa, chọn kết quả, trở lại hội thoại'),
        ('Người vận hành', 'Khởi động API và giữ dữ liệu', 'Docker Compose, healthcheck, SQLite volume'),
    ], [3.2, 5.8, 7.7])
    doc.add_heading('Giá trị cốt lõi và phạm vi khả thi', 2)
    para(doc, 'Giá trị cốt lõi của bản HKchat là tính liên tục của một vòng trao đổi: vào đúng server, đăng nhập, chọn đúng cuộc trò chuyện, gửi tin, trả lời và tìm lại. Vì vậy, nhóm ưu tiên chức năng có thể nối thành một hành trình sử dụng hoàn chỉnh. Kênh và DM dùng chung mô hình messages nhưng có điều kiện quyền khác nhau. Đây là quyết định kỹ thuật để giảm sự trùng lặp logic và giúp kiểm thử quyền truy cập theo cùng một chuẩn.')
    para(doc, 'Trong bản đang chạy, các thao tác văn bản và tìm kiếm đã được triển khai. Hội thoại nhóm bốn người được chuẩn bị sẵn làm dữ liệu trình diễn; API có thể tạo nhóm nhưng giao diện chưa có nút tạo nhóm. Push notification, tải tệp và cuộc gọi chưa được xem là chức năng của bản này. Cách giới hạn này giúp tiêu chí nghiệm thu dựa trên thứ có thể quan sát được thay vì những ý tưởng chưa có mã hoặc bằng chứng.')
    doc.add_heading('Mục tiêu có thể kiểm chứng', 2)
    table(doc, ['Mục tiêu', 'Cách kiểm chứng', 'Minh chứng trong dự án'], [
        ('Tài khoản và phiên', 'Đăng ký, đăng nhập, đăng xuất, thử mật khẩu sai', 'API test và màn hình xác thực'),
        ('Trao đổi có quyền', 'Thử thành viên và người ngoài đọc DM/kênh', 'server.test.mjs, HTTP 403'),
        ('Giữ ngữ cảnh', 'Gửi reply, đọc trích dẫn và mở thread', 'reply_to, API, ảnh hội thoại'),
        ('Tra cứu', 'Tìm từ khóa rồi mở hội thoại', 'GET /api/search, ảnh Android'),
        ('Vận hành lặp lại', 'Khởi động Docker, gọi healthcheck', 'compose.yaml, README'),
    ], [4.0, 5.9, 6.8])


def acceptance_chapter(doc, table, para):
    doc.add_heading('Tiêu chí nghiệm thu theo hành trình người dùng', 2)
    cases = [
        ('US01', 'Là người mới, tôi muốn đăng ký để tham gia nhóm.', 'Tên 3–32 ký tự, email hợp lệ, mật khẩu ≥8; dữ liệu đúng tạo user và phiên; trùng trả 409.'),
        ('US02', 'Là thành viên, tôi muốn đăng nhập để xem cuộc trò chuyện của mình.', 'Tên hoặc email và mật khẩu đúng trả token; sai trả 401; client tải lại danh sách kênh.'),
        ('US03', 'Tôi muốn tạo kênh công khai để trao đổi theo chủ đề.', 'Tên 2–80 ký tự; người tạo trở thành thành viên; kênh hiện trong danh sách.'),
        ('US04', 'Tôi muốn tham gia kênh công khai đã có.', 'Kênh công khai chưa tham gia xuất hiện riêng; bấm Tham gia thêm membership.'),
        ('US05', 'Tôi muốn nhắn riêng cho một người.', 'Cùng cặp tài khoản mở lại cùng DM; người thứ ba nhận 403 khi đọc.'),
        ('US06', 'Tôi muốn gửi và xem tin trong hội thoại.', 'Tin 1–4000 ký tự được lưu; danh sách trả tối đa 100 tin; người ngoài bị từ chối.'),
        ('US07', 'Tôi muốn trả lời một tin cụ thể.', 'replyTo phải là tin còn tồn tại cùng kênh; tin mới hiển thị trích dẫn.'),
        ('US08', 'Tôi muốn sửa hoặc xóa tin do mình viết.', 'Tác giả thao tác được; người khác nhận 403; tin xóa không xuất hiện trong danh sách.'),
        ('US09', 'Tôi muốn thể hiện cảm xúc với tin.', 'Cùng người và emoji không tạo trùng; bỏ cảm xúc cập nhật tổng số.'),
        ('US10', 'Tôi muốn tìm và mở lại nội dung.', 'Chỉ trả tin trong kênh có quyền; chạm kết quả mở đúng cuộc trò chuyện.'),
    ]
    table(doc, ['Mã', 'Câu chuyện người dùng', 'Tiêu chí nghiệm thu'], cases, [1.3, 6.3, 9.1])
    para(doc, 'Các tiêu chí trên được viết theo trạng thái hiện có của mã nguồn và bài test. Một số tiêu chí về giao diện được đối chiếu qua ảnh Android và prototype Figma; chúng không thay thế cho kiểm thử định lượng với người dùng thật.')


def test_case_matrix(doc, table, para):
    doc.add_heading('Bảng kịch bản kiểm thử chuẩn hóa', 2)
    para(doc, 'Mỗi ca dưới đây nêu dữ liệu đầu vào và kết quả mong đợi, tương ứng với các assertion trong server.test.mjs. “Đạt” ở đây chỉ có nghĩa các ca tự động đã chạy qua trong môi trường kiểm thử local; chưa suy ra độ ổn định khi tải lớn hoặc trên mọi thiết bị.')
    cases = [
        ('TC-01', 'Đăng ký hợp lệ', 'Năm tài khoản thử, gồm tên Đạt', '201 cho từng tài khoản'),
        ('TC-02', 'Nhóm sai thành viên', 'Danh sách có userId không tồn tại', '400; không tạo nhóm'),
        ('TC-03', 'Sai mật khẩu', 'Tài khoản đúng, mật khẩu sai', '401; không cấp phiên'),
        ('TC-04', 'Không có token', 'GET /api/channels thiếu Authorization', '401; không trả dữ liệu'),
        ('TC-05', 'Tạo kênh', 'Tên kênh hợp lệ', '201; người tạo là thành viên'),
        ('TC-06', 'Tham gia kênh', 'POST join kênh public', '200; kênh trong danh sách'),
        ('TC-07', 'Gửi tin', 'Body hợp lệ trong kênh đã tham gia', '201; đọc lại thấy nội dung'),
        ('TC-08', 'Sửa thành tin rỗng', 'PATCH body chỉ có khoảng trắng', '400; không ghi nội dung rỗng'),
        ('TC-09', 'Tạo DM', 'Alice mở DM với Bob', '200; trả về channel và id'),
        ('TC-10', 'Người ngoài đọc DM', 'User thứ ba GET messages DM', '403; không lộ nội dung'),
        ('TC-11', 'Reply sai đích', 'replyTo = 999999 không tồn tại', '400; không ghi phản hồi'),
        ('TC-12', 'Reply hợp lệ', 'replyTo là tin còn tồn tại cùng kênh', '201; có liên kết tới tin gốc'),
        ('TC-13', 'Sửa tin của người khác', 'PATCH bằng token người khác', '403; nội dung không đổi'),
        ('TC-14', 'Xóa tin của người khác', 'DELETE bằng token người khác', '403; tin còn đọc được'),
        ('TC-15', 'Cảm xúc trùng', 'Cùng user thả cùng emoji hai lần', 'Một reaction; tổng không tăng lặp'),
        ('TC-16', 'Tìm kiếm theo quyền', 'Từ khóa có trong DM và kênh ngoài quyền', 'Chỉ trả tin được phép xem'),
        ('TC-17', 'Dữ liệu sau khởi động lại', 'Ghi tin rồi khởi động lại server cùng DB', 'Tin và cảm xúc còn tồn tại'),
    ]
    table(doc, ['ID', 'Mô tả', 'Dữ liệu đầu vào', 'Kết quả mong đợi'], cases, [1.4, 3.9, 5.5, 5.9])


def constraints_chapter(doc, table, para):
    doc.add_heading('Ràng buộc và giả định', 1)
    doc.add_heading('Ràng buộc triển khai', 2)
    para(doc, 'Bản server được cấu hình để chạy trên máy của nhóm. Android Emulator gọi host qua 10.0.2.2; iPhone chạy Expo Go dùng IP LAN. Hai thiết bị chỉ trao đổi được khi cùng mạng và server bind đúng địa chỉ. Nếu Docker Desktop chưa chạy hoặc cổng 8070 bị chiếm, app không thể đăng nhập dù client đã build thành công.')
    para(doc, 'Client React Native native có dự án iOS nhưng Windows không thể build IPA bằng Xcode. Bản trên iPhone được kiểm thử qua Expo Go SDK 58, là môi trường xem thử dùng cùng giao diện và API. Đây không phải bằng chứng cho bản iOS đã ký và phát hành. Thông báo đẩy khi app đóng cần cấu hình Firebase/Apple riêng và không được nghiệm thu trong báo cáo này.')
    doc.add_heading('Giả định trong kịch bản thử', 2)
    table(doc, ['Giả định', 'Ý nghĩa đối với kết quả'], [
        ('Server cùng dữ liệu SQLite còn hoạt động', 'Tài khoản và hội thoại mẫu hiện được; đổi volume có thể làm mất dữ liệu mẫu.'),
        ('Người kiểm thử có tài khoản thuộc nhóm', 'Có quyền đọc và gửi trong hội thoại mẫu.'),
        ('Thiết bị kết nối cùng LAN khi thử iPhone', 'URL IP của máy chủ có thể được truy cập từ Safari và Expo Go.'),
        ('Chưa có bài đo tải hoặc nghiên cứu người dùng', 'Không đưa ra chỉ tiêu FPS, độ trễ, tải đồng thời hay mức hài lòng.'),
    ], [6.2, 10.5])
    doc.add_heading('Giới hạn chức năng và hướng phát triển', 2)
    para(doc, 'Giao diện hiện chưa có luồng tự tạo nhóm dù API hỗ trợ nhóm; tìm kiếm chỉ theo từ khóa, chưa có bộ lọc nâng cao và chưa tự cuộn đến đúng tin sau khi mở kết quả. App chưa có tải tệp, cuộc gọi hay push khi đã đóng. Các migration có thể chứa bảng cho kế hoạch tương lai nhưng sự tồn tại của bảng không phải bằng chứng chức năng đã hoàn thành.')
    para(doc, 'Nếu tiếp tục phát triển, nhóm nên ưu tiên màn hình tạo/quản lý nhóm, điều hướng tới đúng tin từ kết quả tìm kiếm, phân trang lịch sử, kiểm thử thông báo đẩy và chạy thử trên nhiều thiết bị. Mỗi mục cần có tiêu chí nghiệm thu, ca test và ảnh hoặc log kết quả trước khi đưa vào báo cáo như một chức năng có thật.')


def academic_conclusion(doc, para):
    doc.add_heading('Bài học kỹ thuật và kết luận', 2)
    para(doc, 'Việc dùng chung channels và messages cho kênh, DM và nhóm giúp thống nhất luồng gửi tin nhưng đòi hỏi kiểm tra membership nhất quán. Trong kiểm thử, khả năng từ chối người ngoài đọc DM và sửa tin của người khác quan trọng ngang với việc gửi tin thành công. Thiết kế database có khóa ngoại, ràng buộc duy nhất và xóa mềm giúp các thao tác này có trạng thái rõ ràng.')
    para(doc, 'Một bài học vận hành là build client thành công không đồng nghĩa API có thể kết nối. Việc kiểm tra Docker engine, cổng 8070 và /api/health phải diễn ra trước khi thử đăng nhập. Trên iPhone, địa chỉ 10.0.2.2 của Android Emulator không có tác dụng; phải nhập IP LAN của máy Windows. Báo cáo ghi lại hai đường chạy này để nhóm khác tái hiện đúng môi trường.')
    para(doc, 'Kết quả của đồ án là một ứng dụng nhắn tin văn bản chạy local với đăng ký, đăng nhập, kênh, DM, hội thoại nhóm mẫu, trả lời, cảm xúc, sửa/xóa và tìm kiếm. Mã nguồn, migration, bộ kiểm thử API, ảnh Android và prototype Figma là các minh chứng cho phạm vi đó. Các giới hạn ở chương trước xác định rõ phần chưa được nghiệm thu và là cơ sở cho vòng phát triển tiếp theo.')
