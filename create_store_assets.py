import os
from PIL import Image, ImageDraw, ImageFont

output_dir = os.path.join(os.path.dirname(__file__), "store_assets")
os.makedirs(output_dir, exist_ok=True)

# 1. Store Icon (128x128 24-bit PNG, RGB no alpha)
icon_img = Image.new("RGB", (128, 128), (248, 250, 252)) # #F8FAFC
draw = ImageDraw.Draw(icon_img)

# Container Box (#1683FF)
margin = 8
draw.rounded_rectangle([margin, margin, 128 - margin, 128 - margin], radius=24, fill=(22, 131, 255))

# White Shield
shield_pts = [(64, 28), (95, 41), (95, 74), (64, 100), (33, 74), (33, 41)]
draw.polygon(shield_pts, fill=(255, 255, 255))

# Cutout Lock in Shield
draw.arc([54, 50, 74, 70], start=180, end=0, fill=(22, 131, 255), width=4)
draw.rounded_rectangle([52, 60, 76, 78], radius=3, fill=(22, 131, 255))
draw.ellipse([61, 65, 67, 71], fill=(255, 255, 255))
draw.rectangle([63, 68, 65, 74], fill=(255, 255, 255))

icon_path = os.path.join(output_dir, "store_icon_128x128.png")
icon_img.save(icon_path, "PNG")


# 2. Screenshot (1280x800 24-bit PNG, RGB no alpha)
scr_img = Image.new("RGB", (1280, 800), (248, 250, 252)) # #F8FAFC
draw = ImageDraw.Draw(scr_img)

# Simulated Web Browser Frame
draw.rectangle([0, 0, 1280, 50], fill=(255, 255, 255))
draw.line([(0, 50), (1280, 50)], fill=(226, 232, 240), width=1)
# Window dots
draw.ellipse([20, 18, 32, 30], fill=(239, 68, 68))
draw.ellipse([40, 18, 52, 30], fill=(245, 158, 11))
draw.ellipse([60, 18, 72, 30], fill=(34, 197, 94))
# Address Bar
draw.rounded_rectangle([100, 10, 800, 40], radius=6, fill=(241, 245, 249), outline=(226, 232, 240))

# Web page content mock
draw.rectangle([100, 100, 750, 720], fill=(255, 255, 255), outline=(226, 232, 240))
draw.rounded_rectangle([140, 140, 710, 190], radius=6, fill=(248, 250, 252))
draw.rounded_rectangle([140, 220, 710, 680], radius=6, fill=(248, 250, 252))

# Injected Extension Card Mockup (1280x800 presentation)
ext_x, ext_y = 860, 90
ext_w, ext_h = 360, 520

# Extension Shadow / Border
draw.rounded_rectangle([ext_x, ext_y, ext_x + ext_w, ext_y + ext_h], radius=12, fill=(255, 255, 255), outline=(226, 232, 240), width=2)
# Extension Header
draw.rounded_rectangle([ext_x, ext_y, ext_x + ext_w, ext_y + 54], radius=12, fill=(255, 255, 255))
draw.line([(ext_x, ext_y + 54), (ext_x + ext_w, ext_y + 54)], fill=(226, 232, 240), width=1)
draw.rounded_rectangle([ext_x + 16, ext_y + 14, ext_x + 42, ext_y + 40], radius=6, fill=(22, 131, 255))

# Result Badge (Low Risk)
draw.rounded_rectangle([ext_x + 20, ext_y + 80, ext_x + 80, ext_y + 104], radius=12, fill=(230, 244, 237), outline=(184, 230, 209))
# Verdict Title & Recommendation Box
draw.rounded_rectangle([ext_x + 20, ext_y + 160, ext_x + ext_w - 20, ext_y + 220], radius=8, fill=(255, 255, 255), outline=(226, 232, 240))
# Action Button
draw.rounded_rectangle([ext_x + 20, ext_y + 440, ext_x + ext_w - 20, ext_y + 490], radius=8, fill=(22, 131, 255))

scr_path = os.path.join(output_dir, "screenshot_1280x800.png")
scr_img.save(scr_path, "PNG")


# 3. Small Promo Tile (440x280 24-bit PNG, RGB no alpha)
sp_img = Image.new("RGB", (440, 280), (248, 250, 252))
draw = ImageDraw.Draw(sp_img)

# Background Accent Box
draw.rounded_rectangle([20, 20, 420, 260], radius=16, fill=(255, 255, 255), outline=(226, 232, 240), width=2)
# Large Shield Icon
draw.rounded_rectangle([50, 60, 130, 140], radius=16, fill=(22, 131, 255))
shield_pts = [(90, 75), (115, 85), (115, 110), (90, 125), (65, 110), (65, 85)]
draw.polygon(shield_pts, fill=(255, 255, 255))

# Decorative Badges
draw.rounded_rectangle([50, 170, 200, 200], radius=6, fill=(230, 244, 237), outline=(184, 230, 209))
draw.rounded_rectangle([215, 170, 390, 200], radius=6, fill=(241, 245, 249), outline=(226, 232, 240))

sp_path = os.path.join(output_dir, "small_promo_440x280.png")
sp_img.save(sp_path, "PNG")


# 4. Marquee Promo Tile (1400x560 24-bit PNG, RGB no alpha)
mq_img = Image.new("RGB", (1400, 560), (248, 250, 252))
draw = ImageDraw.Draw(mq_img)

# Hero Card Container
draw.rounded_rectangle([40, 40, 1360, 520], radius=24, fill=(255, 255, 255), outline=(226, 232, 240), width=2)

# Left Side Shield Emblem
draw.rounded_rectangle([100, 140, 320, 360], radius=36, fill=(22, 131, 255))
shield_pts = [(210, 175), (280, 200), (280, 275), (210, 325), (140, 275), (140, 200)]
draw.polygon(shield_pts, fill=(255, 255, 255))
draw.arc([190, 220, 230, 260], start=180, end=0, fill=(22, 131, 255), width=8)
draw.rounded_rectangle([185, 240, 235, 280], radius=4, fill=(22, 131, 255))

# Feature Cards on Right
draw.rounded_rectangle([800, 120, 1280, 210], radius=12, fill=(248, 250, 252), outline=(226, 232, 240))
draw.rounded_rectangle([800, 230, 1280, 320], radius=12, fill=(248, 250, 252), outline=(226, 232, 240))
draw.rounded_rectangle([800, 340, 1280, 430], radius=12, fill=(248, 250, 252), outline=(226, 232, 240))

mq_path = os.path.join(output_dir, "marquee_promo_1400x560.png")
mq_img.save(mq_path, "PNG")

print("All 4 Chrome Web Store assets generated perfectly.")
