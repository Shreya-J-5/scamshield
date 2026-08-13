import os
from PIL import Image, ImageDraw

icons_dir = os.path.join(os.path.dirname(__file__), "extension", "icons")
os.makedirs(icons_dir, exist_ok=True)

sizes = [16, 32, 48, 128]

for size in sizes:
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Outer circle / background rounded rect
    margin = max(1, size // 16)
    bg_color = (24, 24, 27, 255) # dark zinc #18181b
    border_color = (39, 39, 42, 255) # zinc-800
    
    draw.rounded_rectangle(
        [margin, margin, size - margin, size - margin],
        radius=size // 4,
        fill=bg_color,
        outline=border_color,
        width=max(1, size // 16)
    )
    
    # Shield shape points
    w, h = size, size
    cx = w // 2
    top_y = int(h * 0.25)
    mid_y = int(h * 0.55)
    bot_y = int(h * 0.8)
    left_x = int(w * 0.28)
    right_x = int(w * 0.72)
    
    shield_pts = [
        (cx, top_y),
        (right_x, top_y + size // 12),
        (right_x, mid_y),
        (cx, bot_y),
        (left_x, mid_y),
        (left_x, top_y + size // 12),
    ]
    
    # Fill shield
    shield_fill = (52, 211, 153, 255) # emerald-400 #34d399
    draw.polygon(shield_pts, fill=shield_fill)
    
    out_path = os.path.join(icons_dir, f"icon{size}.png")
    img.save(out_path, "PNG")
    print(f"Generated {out_path}")
