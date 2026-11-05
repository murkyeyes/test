"""Create Behance-ready visual panels from HKchat's existing app captures."""

from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent / "panels"
SHOTS = ROOT / "docs" / "report-images"
OUT.mkdir(parents=True, exist_ok=True)

W = 1600
DARK = "#301542"
ACCENT = "#A81C7F"
PINK = "#F553AB"
PALE = "#FFD1E9"
TEXT = "#37213F"
MUTED = "#796B82"
BG = "#FBF8FC"
WHITE = "#FFFFFF"
FONT = Path("C:/Windows/Fonts")
REG = FONT / "segoeui.ttf"
BOLD = FONT / "segoeuib.ttf"


def font(size, bold=False):
    return ImageFont.truetype(str(BOLD if bold else REG), size)


def new(h, bg=BG):
    im = Image.new("RGB", (W, h), bg)
    return im, ImageDraw.Draw(im)


def text(draw, xy, value, size=32, color=TEXT, bold=False, spacing=12):
    draw.multiline_text(xy, value, font=font(size, bold), fill=color, spacing=spacing)


def wrap(draw, value, max_width, size=31, bold=False):
    words = value.split()
    lines, current = [], ""
    face = font(size, bold)
    for word in words:
        trial = f"{current} {word}".strip()
        if current and draw.textbbox((0, 0), trial, font=face)[2] > max_width:
            lines.append(current)
            current = word
        else:
            current = trial
    if current:
        lines.append(current)
    return "\n".join(lines)


def rounded(draw, box, fill, radius=26, outline=None, width=2):
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def eyebrow(draw, label, x=90, y=80, color=ACCENT):
    text(draw, (x, y), label.upper(), 24, color, True)


def title(draw, label, x=90, y=128, color=TEXT, size=64):
    text(draw, (x, y), label, size, color, True, 9)


def chip(draw, label, x, y, bg=PALE, fg=ACCENT):
    width = draw.textbbox((0, 0), label, font=font(22, True))[2] + 44
    rounded(draw, (x, y, x + width, y + 47), bg, 23)
    text(draw, (x + 22, y + 7), label, 22, fg, True)
    return width


def phone(im, filename, x, y, width=380, height=None):
    shot = Image.open(SHOTS / filename).convert("RGB")
    h = height or round(width * shot.height / shot.width)
    shot = shot.resize((width, h), Image.Resampling.LANCZOS)
    shadow = Image.new("RGBA", (width + 44, h + 44))
    sd = ImageDraw.Draw(shadow)
    sd.rounded_rectangle((22, 18, width + 22, h + 18), 40, fill=(0, 0, 0, 80))
    shadow = shadow.filter(ImageFilter.GaussianBlur(18))
    im.paste(shadow, (x - 22, y - 12), shadow)
    border = Image.new("RGB", (width + 14, h + 14), DARK)
    mask = Image.new("L", border.size)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, border.width, border.height), 38, fill=255)
    im.paste(border, (x - 7, y - 7), mask)
    crop_mask = Image.new("L", (width, h))
    ImageDraw.Draw(crop_mask).rounded_rectangle((0, 0, width, h), 30, fill=255)
    im.paste(shot, (x, y), crop_mask)


def foot(draw, number, dark=False):
    fg = "#DCCBE2" if dark else MUTED
    text(draw, (90, draw.im.size[1] - 70), f"HKchat  /  CASE STUDY                                      {number:02d} / 08", 20, fg, True)


def save(im, name):
    im.save(OUT / name, quality=95)


# 01 Cover
im, d = new(1100, DARK)
d.ellipse((910, -230, 1660, 520), fill="#4A205D")
d.ellipse((650, 620, 1360, 1330), fill="#3B194E")
icon = Image.open(ROOT / "appicon.webp").convert("RGB")
icon = icon.crop((300, 135, 900, 765)).resize((250, 250), Image.Resampling.LANCZOS)
im.paste(icon, (90, 150))
text(d, (90, 455), "HKchat", 112, WHITE, True)
text(d, (95, 615), "Nhắn tin nội bộ.\nGiữ mạch công việc.", 48, "#F7D5EA", True, 18)
chip(d, "MOBILE APP", 95, 820, "#6B2B76", WHITE)
chip(d, "UI/UX CASE STUDY", 285, 820, "#6B2B76", WHITE)
phone(im, "03-hoi-thoai-do-an.png", 1030, 60, 420)
foot(d, 1, True)
save(im, "01-cover.png")

# 02 Product story
im, d = new(1130)
eyebrow(d, "01 / Tổng quan")
title(d, "Một nơi cho cuộc trò chuyện của nhóm")
text(d, (90, 250), wrap(d, "HKchat là ứng dụng di động cho nhóm làm việc trao đổi theo kênh, nhắn riêng và tìm lại nội dung đã gửi.", 1370, 36), 36, MUTED)
cards = [
    ("01", "Kênh chung", "Đặt các chủ đề trao đổi trong không gian dễ tìm."),
    ("02", "Tin nhắn riêng", "Trao đổi trực tiếp giữa hai thành viên."),
    ("03", "Tìm lại ngữ cảnh", "Tìm tin, mở hội thoại và trả lời đúng nội dung."),
]
for i, (num, head, body) in enumerate(cards):
    x = 90 + i * 485
    rounded(d, (x, 470, x + 440, 870), WHITE, 32, "#EADCEB")
    rounded(d, (x + 32, 508, x + 110, 586), PALE, 24)
    text(d, (x + 49, 520), num, 35, ACCENT, True)
    text(d, (x + 32, 630), head, 34, DARK, True)
    text(d, (x + 32, 704), wrap(d, body, 370, 27), 27, MUTED)
text(d, (90, 938), "Đối tượng: nhóm nhỏ, bộ phận nội bộ và nhóm học tập.", 28, TEXT)
foot(d, 2)
save(im, "02-product-story.png")

# 03 Flows
im, d = new(1360)
eyebrow(d, "02 / Hành trình người dùng")
title(d, "Từ kết nối đến trao đổi")
flows = [
    ("Luồng 01  ·  Vào ứng dụng", ["Nhập URL\nserver", "Đăng ký /\nĐăng nhập", "Danh sách\nkênh", "Mở hội\nthoại"]),
    ("Luồng 02  ·  Tìm và trả lời", ["Nhập từ\nkhóa", "Chọn kết\nquả", "Mở lại\nhội thoại", "Gửi tin\ntrả lời"]),
]
for row, (label, steps) in enumerate(flows):
    y = 305 + row * 440
    text(d, (90, y), label, 36, DARK, True)
    for i, step in enumerate(steps):
        x = 90 + i * 385
        rounded(d, (x, y + 85, x + 320, y + 280), WHITE, 27, "#EADCEB")
        rounded(d, (x + 22, y + 107, x + 75, y + 160), PALE, 16)
        text(d, (x + 37, y + 113), str(i + 1), 27, ACCENT, True)
        text(d, (x + 25, y + 190), step, 29, TEXT, True)
        if i < 3:
            d.line((x + 325, y + 185, x + 367, y + 185), fill=ACCENT, width=5)
            d.polygon([(x + 355, y + 173), (x + 355, y + 197), (x + 372, y + 185)], fill=ACCENT)
text(d, (90, 1214), "Các thao tác chính được thể hiện trong prototype Figma 18 màn hình.", 27, MUTED)
foot(d, 3)
save(im, "03-user-flows.png")

# 04 Design system
im, d = new(1350)
eyebrow(d, "03 / Visual identity")
title(d, "Hệ màu và thành phần")
swatches = [(DARK, "Dark", "#301542"), (ACCENT, "Accent", "#A81C7F"), (PINK, "Pink", "#F553AB"), (PALE, "Pale", "#FFD1E9"), (TEXT, "Text", "#37213F")]
for i, (col, label, code) in enumerate(swatches):
    x = 90 + i * 290
    rounded(d, (x, 285, x + 250, 440), col, 27)
    text(d, (x, 463), label, 27, TEXT, True)
    text(d, (x, 505), code, 22, MUTED)
text(d, (90, 610), "Typography", 35, DARK, True)
text(d, (90, 675), "Inter Bold  /  Tiêu đề và hành động", 31, TEXT, True)
text(d, (90, 730), "Inter Regular  /  Nội dung hội thoại", 29, MUTED)
text(d, (90, 840), "Components", 35, DARK, True)
rounded(d, (90, 920, 510, 1005), ACCENT, 19)
text(d, (217, 936), "Đăng nhập", 29, WHITE, True)
rounded(d, (575, 920, 990, 1005), WHITE, 19, "#EADCEB")
text(d, (606, 936), "Tên đăng nhập", 29, MUTED)
rounded(d, (1050, 920, 1500, 1052), PALE, 24)
text(d, (1082, 944), "Tin nhắn của tôi", 28, TEXT)
text(d, (90, 1150), "Lưới khoảng cách 8 px  ·  Frame 390 × 844 px  ·  Button, Input, Tab, Message variants", 27, MUTED)
foot(d, 4)
save(im, "04-design-system.png")

# 05 Authentication and channels
im, d = new(1540)
eyebrow(d, "04 / Màn hình chính")
title(d, "Bắt đầu trong vài bước")
text(d, (90, 225), wrap(d, "Nhập địa chỉ máy chủ, đăng nhập và chọn kênh trao đổi.", 1250, 32), 32, MUTED)
phone(im, "01-dang-nhap-server.png", 245, 365, 425)
phone(im, "02-danh-sach-kenh-nhom.png", 925, 365, 425)
chip(d, "01  /  ĐĂNG NHẬP", 205, 325)
chip(d, "02  /  KÊNH", 930, 325)
foot(d, 5)
save(im, "05-auth-channels.png")

# 06 Conversation
im, d = new(1540)
eyebrow(d, "05 / Hội thoại")
title(d, "Tin nhắn giữ được ngữ cảnh")
text(d, (90, 225), "Gửi tin trong nhóm và trả lời trực tiếp một nội dung cụ thể.", 32, MUTED)
phone(im, "03-hoi-thoai-do-an.png", 245, 365, 425)
phone(im, "04-tra-loi-trong-hoi-thoai.png", 925, 365, 425)
chip(d, "03  /  NHÓM", 205, 325)
chip(d, "04  /  REPLY", 930, 325)
foot(d, 6)
save(im, "06-conversation.png")

# 07 Search
im, d = new(1540)
eyebrow(d, "06 / Tìm kiếm")
title(d, "Tìm lại nội dung đã trao đổi")
text(d, (90, 225), "Tìm theo từ khóa, chọn kết quả và trở lại cuộc trò chuyện.", 32, MUTED)
phone(im, "05-tim-kiem-tin-nhan.png", 245, 365, 425)
phone(im, "06-mo-lai-hoi-thoai.png", 925, 365, 425)
chip(d, "05  /  TÌM KIẾM", 205, 325)
chip(d, "06  /  MỞ HỘI THOẠI", 930, 325)
foot(d, 7)
save(im, "07-search-prototype.png")

# 08 Prototype coverage
im, d = new(1240)
eyebrow(d, "07 / Prototype")
title(d, "18 trạng thái. Một luồng mạch lạc.")
text(d, (90, 225), "Bộ Figma cho phép chỉnh sửa từng layer và nối các màn hình thành Flow 1.", 31, MUTED)
rounded(d, (90, 315, 1030, 975), WHITE, 28, "#EADCEB")
figma = Image.open(SHOTS / "07-figma-design-system.png").convert("RGB")
figma.thumbnail((890, 600), Image.Resampling.LANCZOS)
im.paste(figma, (115, 342))
rounded(d, (1080, 315, 1510, 975), WHITE, 28, "#EADCEB")
text(d, (1112, 350), "Danh mục màn hình", 30, DARK, True)
for i, line in enumerate([
    "01–03  Xác thực",
    "04–06  Kênh",
    "07–08  Mọi người và DM",
    "09–14  Tin và tương tác",
    "15–17  Tìm kiếm",
    "18  Đăng xuất",
]):
    text(d, (1112, 435 + i * 75), line, 25, TEXT)
rounded(d, (1112, 890, 1478, 950), PALE, 18)
text(d, (1160, 902), "Flow 1   ·   18/18", 29, ACCENT, True)
text(d, (90, 1045), "Prototype tương tác và bộ component nằm trong file Figma của dự án.", 29, MUTED)
foot(d, 8)
save(im, "08-figma-coverage.png")

pdf_pages = [Image.open(p).convert("RGB") for p in sorted(OUT.glob("*.png"))]
pdf_pages[0].save(OUT.parent / "HKchat-case-study-preview.pdf", save_all=True, append_images=pdf_pages[1:], resolution=144)
print(f"Created {len(pdf_pages)} panels in {OUT}")
