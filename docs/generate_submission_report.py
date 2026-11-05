"""Build the HKchat submission report from existing implementation and design evidence."""

from pathlib import Path
import re
from docx import Document
from docx.enum.table import WD_CELL_VERTICAL_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_TAB_ALIGNMENT, WD_TAB_LEADER
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor
from report_detail import architecture, data_model, design, glossary, manual_walkthrough, overview, protocol_detail, requirements, stories, testing, workflows
from report_revision import academic_conclusion, acceptance_chapter, constraints_chapter, idea_chapter, market_research, test_case_matrix
from report_usecases import add_usecases

HERE = Path(__file__).resolve().parent
OUT = HERE / "bao-cao-HKchat-ban-hoc-thuat.docx"
IMG = HERE / "report-images"
FIGMA = "https://www.figma.com/design/95mjvVcx7H8xI4mxwJG2OH/HKchat-%E2%80%93-M%C3%A0n-h%C3%ACnh-%E1%BB%A9ng-d%E1%BB%A5ng--b%C3%A1o-c%C3%A1o-"
PURPLE, LIGHT = "301542", "F9F5F9"


def shade(cell, value):
    node = OxmlElement("w:shd")
    node.set(qn("w:fill"), value)
    cell._tc.get_or_add_tcPr().append(node)


def table(doc, headers, rows, widths):
    key = tuple(headers)
    retained = (
        headers[0] in {"STT", "Khối", "Tiêu chí", "Chức năng", "Bảng.trường"}
        or key == ("ID", "Mô tả", "Dữ liệu đầu vào", "Kết quả mong đợi")
        or key == ("Yêu cầu", "Use case", "Màn hình", "Thành phần/API")
    )
    redundant = (
        key in {
            ("Nhu cầu", "Bước trên ứng dụng", "Dữ liệu liên quan"),
            ("Sản phẩm", "Cách tổ chức trò chuyện", "Áp dụng trong HKchat"),
            ("Nhóm", "Thao tác"),
            ("User story", "Mục tiêu", "Tiêu chí nghiệm thu và bằng chứng"),
            ("Tầng", "Tệp trong mã nguồn", "Vai trò"),
            ("Bảng", "Thuộc tính chính", "Ý nghĩa"),
            ("Tác vụ", "Endpoint", "Kết quả"),
            ("Thư mục hoặc tệp", "Nội dung", "Liên hệ khi chạy"),
            ("Kiểm tra", "Kết quả", "Phạm vi"),
            ("Trường hợp API", "Kết quả được kiểm tra"),
            ("ID", "Dữ liệu hoặc thao tác", "Kết quả được assert trong test"),
            ("Bước", "Thao tác trên app", "Dấu hiệu cần quan sát"),
        }
    )
    if redundant:
        return
    if not retained:
        for row in rows:
            p = doc.add_paragraph(style="List Bullet")
            if key == ("Method", "Endpoint", "Quyền", "Mục đích"):
                p.add_run(f"{row[0]} {row[1]}. ").bold = True
                p.add_run(f"Quyền truy cập: {row[2]}. Mục đích: {row[3]}.")
                continue
            p.add_run(str(row[0]).rstrip(".") + ". ").bold = True
            for index, value in enumerate(row[1:], 1):
                value = str(value).strip()
                if not value:
                    continue
                if index > 1:
                    p.add_run(" ")
                if len(headers) > 2:
                    p.add_run(headers[index] + ": ").italic = True
                p.add_run(value if value.endswith((".", "!", "?")) else value + ".")
        return
    item = doc.add_table(rows=1, cols=len(headers))
    item.autofit = False
    for col, width in zip(item.columns, widths):
        col.width = Cm(width)
    for i, text in enumerate(headers):
        item.rows[0].cells[i].text = text
        shade(item.rows[0].cells[i], PURPLE)
    for index, row in enumerate(rows):
        cells = item.add_row().cells
        for i, text in enumerate(row):
            cells[i].text = str(text)
            if index % 2:
                shade(cells[i], LIGHT)
    for row_index, row in enumerate(item.rows):
        for i, cell in enumerate(row.cells):
            cell.width = Cm(widths[i])
            cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
            margin = OxmlElement("w:tcMar")
            for edge in ("top", "start", "bottom", "end"):
                side = OxmlElement("w:" + edge)
                side.set(qn("w:w"), "110")
                side.set(qn("w:type"), "dxa")
                margin.append(side)
            cell._tc.get_or_add_tcPr().append(margin)
            for p in cell.paragraphs:
                p.paragraph_format.space_after = Pt(0)
                for r in p.runs:
                    r.font.size = Pt(9)
                    if row_index == 0:
                        r.bold = True
                        r.font.color.rgb = RGBColor(255, 255, 255)
    doc.add_paragraph().paragraph_format.space_after = Pt(0)


def para(doc, text=""):
    return doc.add_paragraph(text)


def hyperlink(paragraph, label, url):
    relationship = paragraph.part.relate_to(url, "http://schemas.openxmlformats.org/officeDocument/2006/relationships/hyperlink", is_external=True)
    node = OxmlElement("w:hyperlink")
    node.set(qn("r:id"), relationship)
    run = OxmlElement("w:r")
    properties = OxmlElement("w:rPr")
    color = OxmlElement("w:color")
    color.set(qn("w:val"), "A81C7F")
    properties.append(color)
    underline = OxmlElement("w:u")
    underline.set(qn("w:val"), "single")
    properties.append(underline)
    run.append(properties)
    text_node = OxmlElement("w:t")
    text_node.text = label
    run.append(text_node)
    node.append(run)
    paragraph._p.append(node)


def image(doc, filename, caption, width=15.7):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.add_run().add_picture(str(IMG / filename), width=Cm(width))
    p.paragraph_format.keep_with_next = True
    c = doc.add_paragraph(caption)
    c.alignment = WD_ALIGN_PARAGRAPH.CENTER
    c.runs[0].italic = True
    c.runs[0].font.size = Pt(9)
    c.paragraph_format.space_after = Pt(10)


def screen_pair(doc, first, second, labels):
    t = doc.add_table(rows=1, cols=2)
    for i, filename in enumerate((first, second)):
        cell = t.cell(0, i)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(labels[i])
        r.bold = True
        r.font.size = Pt(9)
        pic = cell.add_paragraph()
        pic.alignment = WD_ALIGN_PARAGRAPH.CENTER
        pic.add_run().add_picture(str(IMG / filename), width=Cm(7.1))
    t.rows[0]._tr.get_or_add_trPr().append(OxmlElement("w:cantSplit"))
    doc.add_paragraph()


def screen_detail(doc, filename, heading, before, after, figure_number):
    doc.add_heading(heading, 2)
    para(doc, before)
    image(doc, filename, f"Hình {figure_number}. {heading}", 7.9)
    para(doc, after)
    doc.add_page_break()


def setup(doc):
    s = doc.sections[0]
    s.page_width, s.page_height = Cm(21), Cm(29.7)
    s.top_margin, s.bottom_margin = Cm(2), Cm(1.8)
    s.left_margin = s.right_margin = Cm(2.15)
    normal = doc.styles["Normal"]
    normal.font.name = "Times New Roman"
    normal.font.size = Pt(11)
    normal.paragraph_format.space_after = Pt(6)
    normal.paragraph_format.line_spacing = 1.2
    for name, size in (("Heading 1", 16), ("Heading 2", 13), ("Heading 3", 12)):
        style = doc.styles[name]
        style.font.name = "Times New Roman"
        style.font.size = Pt(size)
        style.font.bold = True
        style.font.color.rgb = RGBColor(0, 0, 0)
        style.paragraph_format.space_before = Pt(12)
        style.paragraph_format.keep_with_next = True
        if name == "Heading 1":
            style.paragraph_format.page_break_before = True
    title = doc.styles["Title"]
    title.font.name = "Times New Roman"
    title.font.size = Pt(25)
    title.font.bold = True
    title.font.color.rgb = RGBColor(0, 0, 0)
    border = OxmlElement("w:pBdr")
    bottom = OxmlElement("w:bottom")
    bottom.set(qn("w:val"), "nil")
    border.append(bottom)
    title.element.get_or_add_pPr().append(border)
    foot = s.footer.paragraphs[0]
    foot.alignment = WD_ALIGN_PARAGRAPH.CENTER
    foot.add_run("HKchat  |  Báo cáo đồ án ứng dụng di động  |  ")
    field = OxmlElement("w:fldSimple")
    field.set(qn("w:instr"), "PAGE")
    foot._p.append(field)


def renumber_headings(doc):
    chapter = subsection = 0
    for p in doc.paragraphs:
        if p.style.name not in ("Heading 1", "Heading 2"):
            continue
        label = re.sub(r"^\d+(?:\.\d+)?\s+", "", p.text).strip()
        if label in ("Mục lục", "Thông tin dự án", "Bảng phân công công việc", "Tài liệu tham khảo") or label.startswith("Phụ lục"):
            continue
        if p.style.name == "Heading 1":
            chapter += 1
            subsection = 0
            p.text = f"{chapter}. {label}"
        else:
            subsection += 1
            p.text = f"{chapter}.{subsection} {label}"


def build():
    d = Document()
    setup(d)
    para(d, "Trường: ______________________________________________").alignment = WD_ALIGN_PARAGRAPH.CENTER
    para(d, "Khoa: ________________________________________________").alignment = WD_ALIGN_PARAGRAPH.CENTER
    para(d, "Môn học: _____________________________________________").alignment = WD_ALIGN_PARAGRAPH.CENTER
    para(d, "BÁO CÁO ĐỒ ÁN ỨNG DỤNG DI ĐỘNG").alignment = WD_ALIGN_PARAGRAPH.CENTER
    d.add_paragraph("HKchat", style="Title").alignment = WD_ALIGN_PARAGRAPH.CENTER
    para(d, "Ứng dụng nhắn tin nội bộ cho nhóm làm việc").alignment = WD_ALIGN_PARAGRAPH.CENTER
    para(d, "Nhóm HK").alignment = WD_ALIGN_PARAGRAPH.CENTER
    para(d, "Phạm Đăng Khải  ·  Trần Vũ Đình Huy").alignment = WD_ALIGN_PARAGRAPH.CENTER
    para(d, "Tháng 11 năm 2026").alignment = WD_ALIGN_PARAGRAPH.CENTER
    para(d, "\n\n")
    para(d, "HKchat kết hợp kênh thảo luận, trò chuyện trực tiếp và tìm kiếm tin nhắn trong một ứng dụng di động. Báo cáo trình bày phần mềm đã xây dựng, thiết kế giao diện, dữ liệu và kết quả kiểm thử có trong dự án.")
    d.add_page_break()
    d.add_heading("Mục lục", 1)
    for title, page in [
        ("Bảng phân công công việc", 3),
        ("1. Giới thiệu chung và Nghiên cứu thị trường", 4),
        ("2. Hình thành ý tưởng và lý do lựa chọn", 7),
        ("3. Phân tích yêu cầu hệ thống", 9),
        ("4. Câu chuyện người dùng và phạm vi MVP", 12),
        ("5. Kiến trúc hệ thống và đặc tả kỹ thuật", 18),
        ("6. Luồng vận hành hệ thống", 22),
        ("7. Mô hình dữ liệu", 26),
        ("8. Thiết kế giao diện và trải nghiệm", 29),
        ("9. Triển khai và kiểm thử", 36),
        ("10. Ràng buộc và giả định", 40),
        ("11. Kết luận và hướng phát triển", 41),
        ("Tài liệu tham khảo", 43),
    ]:
        p = para(d, title)
        p.paragraph_format.tab_stops.add_tab_stop(Cm(16.5), WD_TAB_ALIGNMENT.RIGHT, WD_TAB_LEADER.DOTS)
        p.add_run(f"\t{page}")
    d.add_heading("Thông tin dự án", 2)
    table(d, ["Mục", "Nội dung"], [
        ("Ứng dụng", "HKchat"), ("Nhóm", "HK: Phạm Đăng Khải và Trần Vũ Đình Huy"),
        ("Client", "React Native cho Android; bản Expo Go để thử trên iPhone"),
        ("Server", "Node.js API và SQLite chạy trong Docker"),
        ("Thiết kế", "Figma với 18 trạng thái màn hình và trang Design System"),
    ], [4.0, 12.7])

    d.add_heading("Bảng phân công công việc", 1)
    para(d, "Điền mã số sinh viên, nhiệm vụ thực tế và tỷ lệ hoàn thành của từng thành viên trước khi nộp.")
    table(d, ["STT", "Họ và tên", "MSSV", "Công việc thực hiện", "Tỷ lệ hoàn thành"], [
        ("1", "Phạm Đăng Khải", "", "", ""),
        ("2", "Trần Vũ Đình Huy", "", "", ""),
    ], [1.1, 4.4, 2.2, 6.1, 2.9])

    d.add_heading("Giới thiệu chung và Nghiên cứu thị trường", 1)
    d.add_heading("1.1 Bối cảnh và mục tiêu", 2)
    para(d, "Nhóm làm việc thường cần thông báo chung, trao đổi theo chủ đề và nhắn riêng giữa hai thành viên. HKchat đưa các cách trao đổi này vào cùng một ứng dụng di động. Người dùng có thể quay lại lịch sử hội thoại và tìm nội dung theo từ khóa.")
    para(d, "Bản hiện tại tập trung vào giao tiếp bằng văn bản: tạo tài khoản, đăng nhập, kênh công khai, DM, hội thoại nhóm mẫu, gửi tin, trả lời, cảm xúc, sửa/xóa và tìm kiếm. Dữ liệu được lưu trên máy chủ local để nhóm vận hành và kiểm thử.")
    market_research(d, table, para)
    d.add_heading("Mục tiêu và phạm vi đồ án", 2)
    para(d, "Từ việc đối chiếu năm sản phẩm, nhóm lựa chọn một vòng giao tiếp cốt lõi gồm kênh, tin nhắn trực tiếp, trả lời và tìm kiếm. Mục tiêu kỹ thuật là xây dựng client di động, API có xác thực và một database độc lập để mọi hành động trên có thể được kiểm tra bằng thao tác thật. Mục tiêu sản phẩm là giúp nhóm nhỏ trao đổi văn bản theo chủ đề trên server do nhóm vận hành.")
    overview(d, table, para)
    idea_chapter(d, table, para)
    d.add_heading("Business Model Canvas cho bản đồ án", 2)
    para(d, "Canvas mô tả cách HKchat phục vụ nhóm dùng thử trong phạm vi dự án hiện tại. Sản phẩm được vận hành trên server local và không thu phí người dùng.")
    table(d, ["Khối", "Nội dung của HKchat"], [
        ("Phân khúc người dùng", "Nhóm nhỏ và bộ phận nội bộ cần trao đổi theo kênh, DM."),
        ("Giá trị cung cấp", "Một giao diện di động cho nhắn tin, reply và tìm lại nội dung trên server riêng."),
        ("Kênh tiếp cận", "Bản demo Android, Figma prototype và hướng dẫn chạy trong README."),
        ("Quan hệ người dùng", "Thành viên tự đăng ký tài khoản trên máy chủ của nhóm."),
        ("Dòng doanh thu", "Không thu phí trong bản đồ án đang vận hành."),
        ("Nguồn lực chính", "Mã React Native, Node.js API, SQLite, Docker và thiết kế Figma."),
        ("Hoạt động chính", "Vận hành API, quản lý dữ liệu và kiểm thử các luồng giao tiếp."),
        ("Đối tác chính", "Hai thành viên nhóm HK phụ trách thiết kế và phát triển dự án."),
        ("Cơ cấu chi phí", "Thời gian phát triển và tài nguyên máy dùng chạy Docker, Android Emulator."),
    ], [4.0, 12.7])

    d.add_heading("Phân tích yêu cầu hệ thống", 1)
    d.add_heading("3.1 Chức năng đã triển khai", 2)
    para(d, "Ở tầng tài khoản, HKchat cho phép người dùng chọn địa chỉ server, đăng ký, đăng nhập bằng tên hoặc email, khôi phục phiên và đăng xuất. Sau khi vào ứng dụng, người dùng xem kênh đã tham gia, tạo hoặc tham gia kênh công khai, mở DM từ danh sách thành viên và đọc hội thoại nhóm mẫu. Trong hội thoại, người dùng gửi tin, trả lời, sửa hoặc xóa tin của mình và thả cảm xúc. Tab Tìm kiếm cho phép tìm từ khóa trong phạm vi hội thoại được phép đọc rồi mở lại cuộc trò chuyện. Các nhóm chức năng này được mô tả theo điều kiện đầu vào và phản hồi ở các mục sau.")
    table(d, ["Nhóm", "Thao tác"], [
        ("Tài khoản", "Đăng ký, đăng nhập bằng tên hoặc email, lưu phiên, đăng xuất, nhập URL server."),
        ("Kênh", "Xem kênh đã tham gia; tạo và tham gia kênh công khai."),
        ("Hội thoại", "Gửi tin trong kênh hoặc DM; mở hội thoại nhóm bốn người từ dữ liệu mẫu."),
        ("Tin nhắn", "Reply, sửa/xóa tin của mình, thêm hoặc bỏ cảm xúc."),
        ("Tìm kiếm", "Tìm tin trong kênh được phép xem và mở hội thoại từ kết quả."),
    ], [3.1, 13.6])
    d.add_heading("3.3 Ma trận tác động và công sức", 2)
    para(d, "Nhóm đánh giá tác động lên luồng giao tiếp và công sức triển khai tương đối. Các mục trong bảng đều có trong bản ứng dụng hiện tại.")
    table(d, ["Chức năng", "Tác động", "Công sức", "Lý do"], [
        ("Tài khoản và phiên", "Cao", "Vừa", "Xác định người dùng và quyền truy cập."),
        ("Kênh, DM, gửi tin", "Cao", "Vừa", "Hoàn thành giao tiếp hằng ngày."),
        ("Reply và tìm kiếm", "Cao", "Vừa", "Giữ ngữ cảnh và truy xuất nội dung."),
        ("Sửa, xóa, cảm xúc", "Vừa", "Thấp", "Hoàn thiện thao tác với tin."),
    ], [4.2, 2.2, 2.2, 8.1])
    requirements(d, table, para)
    d.add_heading("Câu chuyện người dùng và phạm vi MVP", 1)
    acceptance_chapter(d, table, para)
    add_usecases(d, image, para)
    stories(d, table, para)

    d.add_heading("Kiến trúc hệ thống và đặc tả kỹ thuật", 1)
    d.add_heading("4.1 Cấu trúc hệ thống", 2)
    para(d, "Client React Native gọi HTTP API tới máy chủ Node.js. API kiểm tra phiên, quyền thành viên và dữ liệu đầu vào rồi đọc/ghi SQLite. Docker Compose chạy API trên cổng 8070 và gắn volume cho cơ sở dữ liệu. Các migration SQL được áp dụng theo thứ tự phiên bản khi server khởi động.")
    table(d, ["Tầng", "Tệp trong mã nguồn", "Vai trò"], [
        ("Client", "hkchat/mobile/App.tsx", "Giao diện xác thực, kênh, DM, tin và tìm kiếm."),
        ("API", "hkchat/server/server.mjs", "Phiên, quyền truy cập và thao tác dữ liệu."),
        ("Database", "hkchat/server/migrations/*.sql", "Bảng và quan hệ trong SQLite."),
        ("Vận hành", "hkchat/compose.yaml", "Chạy server và giữ database trong Docker volume."),
    ], [2.3, 5.7, 8.7])
    d.add_heading("4.2 Mô hình dữ liệu", 2)
    table(d, ["Bảng", "Thuộc tính chính", "Ý nghĩa"], [
        ("users", "id, username, email, password_hash", "Tài khoản người dùng."),
        ("sessions", "token_hash, user_id, expires_at", "Phiên đăng nhập có thời hạn."),
        ("channels", "id, name, kind, dm_key", "Kênh công khai và DM."),
        ("channel_members", "channel_id, user_id, joined_at", "Thành viên của từng kênh."),
        ("messages", "id, channel_id, user_id, body, reply_to", "Tin nhắn và liên kết trả lời."),
        ("reactions", "message_id, user_id, emoji", "Cảm xúc của người dùng trên tin."),
        ("group_chats", "channel_id, creator_id, created_at", "Đánh dấu hội thoại nhóm."),
    ], [3.1, 6.3, 7.3])
    para(d, "Mật khẩu được dẫn xuất bằng scrypt với salt riêng; database lưu giá trị băm. Token phiên cũng được băm khi lưu. Truy vấn đọc tin và tìm kiếm chỉ trả nội dung thuộc kênh mà người dùng là thành viên.")
    d.add_heading("4.3 API chính", 2)
    table(d, ["Tác vụ", "Endpoint", "Kết quả"], [
        ("Xác thực", "POST /api/register, /api/login", "Tạo tài khoản và phiên."),
        ("Kênh / DM", "GET, POST /api/channels; POST /api/dm", "Xem và mở cuộc trò chuyện."),
        ("Tin", "GET, POST /api/channels/:id/messages", "Đọc và gửi tin."),
        ("Thread / sửa / xóa", "GET /api/messages/:id/thread; PATCH, DELETE /api/messages/:id", "Quản lý tin theo quyền."),
        ("Tìm kiếm", "GET /api/search", "Tìm tin trong phạm vi quyền xem."),
    ], [3.1, 7.1, 6.5])
    architecture(d, table, para, image)
    protocol_detail(d, table, para)

    d.add_heading("Luồng vận hành hệ thống", 1)
    para(d, "Hai sơ đồ mô tả đường đi trên giao diện: kết nối và xác thực, sau đó tìm tin và trả lời. Nhánh lỗi cho phép quay lại bước nhập dữ liệu tương ứng.")
    d.add_heading("5.1 Kết nối server và đăng nhập", 2)
    image(d, "flow-01-auth.png", "Hình 1. Kết nối server, xác thực và vào ứng dụng", 16.0)
    d.add_heading("5.2 Tìm tin và trả lời", 2)
    image(d, "flow-02-search-reply.png", "Hình 2. Tìm kiếm, mở hội thoại và trả lời tin", 16.0)
    workflows(d, table, para, image)

    d.add_heading("Mô hình và lược đồ dữ liệu", 1)
    data_model(d, table, para, image)

    d.add_heading("Thiết kế giao diện và trải nghiệm tương tác", 1)
    d.add_heading("6.1 Hệ thống thiết kế", 2)
    para(d, "Thiết kế dùng tím đậm ở màn hình xác thực và thanh tiêu đề, tím hồng cho nút chính và trạng thái chọn, nền sáng cho nội dung hội thoại. Figma có Color Styles, Text Styles và component variants cho nút, ô nhập, tab và bong bóng tin. Logo dự án lấy từ appicon.webp.")
    table(d, ["Vai trò", "Màu", "Ứng dụng"], [
        ("Nền đậm", "#301542", "Màn hình xác thực, thanh tiêu đề."),
        ("Màu nhấn", "#A81C7F", "Nút chính, tên tác giả, tab được chọn."),
        ("Hồng", "#F553AB", "Điểm nhấn tương tác."),
        ("Hồng nhạt", "#FFD1E9", "Bong bóng tin của người dùng."),
        ("Chữ", "#37213F", "Nội dung trên nền sáng."),
    ], [3.2, 2.7, 10.8])
    para(d, "Figma dùng font Inter Regular/Bold, khung 390 × 844 px và lưới khoảng cách 8 px. Bộ thiết kế gồm 18 trạng thái màn hình chỉnh sửa được theo layer. Sau khi chạy plugin, nhóm xác nhận có thể đi tới 18/18 màn hình từ Flow 1.")
    p = para(d, "Liên kết Figma: ")
    hyperlink(p, "Mở thiết kế và prototype HKchat", FIGMA)
    image(d, "07-figma-design-system.png", "Hình 3. Trang thiết kế và các style trong Figma")
    image(d, "08-figma-prototype.png", "Hình 4. Flow 1 và các đường nối trong prototype")
    d.add_heading("6.2 Cấu trúc điều hướng", 2)
    para(d, "Sau đăng nhập, người dùng chọn một trong ba tab Kênh, Mọi người và Tìm kiếm. Kênh hiển thị cuộc trò chuyện và thao tác tạo/tham gia. Mọi người mở DM. Tìm kiếm trả danh sách tin và mở lại hội thoại. Các thao tác reply, sửa/xóa và cảm xúc được đặt trong màn hình tin nhắn.")
    design(d, table, para)

    d.add_heading("Các khung nhìn giao diện tiêu biểu", 2)
    para(d, "Các hình dưới đây chụp từ bản chạy trên Android Emulator với dữ liệu mẫu của nhóm.")
    screen_pair(d, "01-dang-nhap-server.png", "02-danh-sach-kenh-nhom.png", ["Hình 5. Nhập URL server và đăng nhập", "Hình 6. Danh sách kênh, nhóm"])
    para(d, "Khung nhìn 1 — xác thực: Android Emulator dùng URL http://10.0.2.2:8070. Người dùng nhập tên hoặc email và mật khẩu; client gọi API rồi lưu phiên khi thành công. Lỗi xác thực và kết nối hiển thị ngay trong form. Khung nhìn 2 — danh sách: sau đăng nhập, tab Kênh liệt kê kênh đã tham gia, nhóm mẫu, ô tạo kênh và các kênh công khai có thể tham gia. API trả hai danh sách theo quyền riêng biệt.")
    d.add_page_break()
    screen_pair(d, "03-hoi-thoai-do-an.png", "04-tra-loi-trong-hoi-thoai.png", ["Hình 7. Hội thoại nhóm bốn người", "Hình 8. Trả lời tin có ngữ cảnh"])
    para(d, "Khung nhìn 3 — hội thoại: dữ liệu mẫu có Huy, Khải, Tân và Đạt; nội dung về đồ án chỉ dùng để minh họa nhiều tác giả trong nhóm làm việc. Tin của người đăng nhập có màu khác để dễ nhận diện. Khung nhìn 4 — trả lời: nhấn giữ một tin rồi chọn Trả lời làm xuất hiện thanh trích dẫn; request mang replyTo. Server kiểm tra tin gốc còn tồn tại và thuộc cùng kênh trước khi lưu.")
    d.add_page_break()
    screen_pair(d, "05-tim-kiem-tin-nhan.png", "06-mo-lai-hoi-thoai.png", ["Hình 9. Tìm tin theo từ khóa", "Hình 10. Mở hội thoại từ kết quả"])
    para(d, "Khung nhìn 5 — tìm kiếm: nhập từ khóa và nhận tối đa 50 tin mới nhất trong phạm vi kênh được phép xem; tin xóa không xuất hiện. Khung nhìn 6 — mở kết quả: chọn kết quả để quay về đúng cuộc trò chuyện. Bản hiện tại chưa tự cuộn tới vị trí của tin được chọn; đây là giới hạn điều hướng cần cải thiện.")

    d.add_heading("Triển khai và kịch bản kiểm thử", 1)
    d.add_heading("8.1 Môi trường chạy", 2)
    para(d, "Máy chủ Node.js và SQLite chạy bằng Docker Compose; database được giữ trong volume. Android Emulator dùng http://10.0.2.2:8070 để gọi API. Bản Expo Go trên iPhone dùng IP LAN của máy Windows khi hai thiết bị chung Wi-Fi. README.md ghi lệnh cài đặt, build và chạy.")
    d.add_heading("8.2 Kết quả kiểm thử", 2)
    para(d, "Bộ test server khởi tạo database tạm và gọi API thật. Test bao phủ xác thực, nhóm/kênh, quyền đọc DM, gửi/reply, sửa/xóa, cảm xúc, tìm kiếm và dữ liệu sau khi khởi động lại server.")
    table(d, ["Kiểm tra", "Kết quả", "Phạm vi"], [
        ("npm.cmd run typecheck", "Đạt", "Kiểu dữ liệu client React Native."),
        ("npm.cmd run test:server", "Đạt 1/1 bài test", "API, quyền truy cập, lưu trữ."),
        ("Android assembleDebug", "BUILD SUCCESSFUL", "Bản debug Android."),
        ("Figma prototype", "18/18 màn hình", "Nhóm xác nhận khả năng đi tới từ Flow 1."),
    ], [4.4, 4.1, 8.2])
    table(d, ["Trường hợp API", "Kết quả được kiểm tra"], [
        ("Sai mật khẩu", "HTTP 401."),
        ("Người ngoài đọc DM", "HTTP 403."),
        ("Reply tới tin không tồn tại", "HTTP 400."),
        ("Người khác sửa/xóa tin", "HTTP 403."),
        ("Tìm trong DM", "Chỉ thành viên nhìn thấy kết quả."),
        ("Khởi động lại server", "Tin và cảm xúc đã ghi vẫn đọc được."),
    ], [6.3, 10.4])
    testing(d, table, para)
    test_case_matrix(d, table, para)
    manual_walkthrough(d, table, para)

    constraints_chapter(d, table, para)
    d.add_heading("Kết luận và hướng phát triển", 1)
    para(d, "HKchat đã có client di động, API và database local cho luồng nhắn tin nội bộ. Kênh, DM, reply, cảm xúc, sửa/xóa và tìm kiếm hoạt động trên cùng mô hình dữ liệu có kiểm tra quyền thành viên. Thiết kế Figma, ảnh Android và kết quả kiểm thử là căn cứ để nhóm trình bày sản phẩm.")
    academic_conclusion(d, para)
    glossary(d, table, para)
    d.add_heading("Tài liệu tham khảo", 1)
    for name, url in [
        ("Slack Channels", "https://slack.com/features/channels"),
        ("Microsoft Teams channels overview", "https://learn.microsoft.com/en-us/microsoftteams/teams-channels-overview"),
        ("Google Chat help", "https://support.google.com/chat/answer/7659784?hl=en"),
        ("Zulip topics", "https://zulip.com/help/introduction-to-topics"),
        ("Rocket.Chat documentation", "https://docs.rocket.chat/docs"),
    ]:
        d.add_paragraph(f"{name}: {url}", style="List Bullet")
    renumber_headings(d)
    d.save(OUT)
    print(OUT)


if __name__ == "__main__":
    build()
