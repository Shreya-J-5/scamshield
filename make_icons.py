import os
from PIL import Image, ImageDraw

icons_dir = os.path.join(os.path.dirname(__file__), "extension", "icons")
os.makedirs(icons_dir, exist_ok=True)

sizes = [16, 32, 48, 128]

for target_size in sizes:
    # Supersampling factor for crisp anti-aliasing
    scale = 8
    size = target_size * scale
    
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Outer Rounded Rectangle / Container (Flat ScamShield Blue #1683FF)
    margin = int(size * 0.04)
    radius = int(size * 0.22)
    
    draw.rounded_rectangle(
        [margin, margin, size - margin, size - margin],
        radius=radius,
        fill=(22, 131, 255, 255)  # #1683FF ScamShield Blue
    )
    
    # Draw White Security Shield & Lock emblem inside
    cx = size // 2
    cy = size // 2
    
    # Security Shield Path Points
    top_y = int(size * 0.22)
    shoulder_y = int(size * 0.32)
    mid_y = int(size * 0.58)
    tip_y = int(size * 0.78)
    
    left_x = int(size * 0.26)
    right_x = int(size * 0.74)
    
    shield_pts = [
        (cx, top_y),
        (right_x, shoulder_y),
        (right_x, mid_y),
        (cx, tip_y),
        (left_x, mid_y),
        (left_x, shoulder_y),
    ]
    
    # Inner White Security Shield Fill
    draw.polygon(shield_pts, fill=(255, 255, 255, 255))
    
    # Cutout Security Lock / Keyhole in Blue (#1683FF) inside the shield
    lock_cx = cx
    lock_top = int(size * 0.40)
    lock_w = int(size * 0.16)
    lock_h = int(size * 0.14)
    
    # Lock Shackle (Arch)
    shackle_r = int(size * 0.08)
    shackle_box = [lock_cx - shackle_r, lock_top - shackle_r, lock_cx + shackle_r, lock_top + shackle_r]
    draw.arc(shackle_box, start=180, end=0, fill=(22, 131, 255, 255), width=int(size * 0.04))
    
    # Lock Body Box
    lock_body = [
        lock_cx - lock_w // 2,
        lock_top,
        lock_cx + lock_w // 2,
        lock_top + lock_h
    ]
    draw.rounded_rectangle(lock_body, radius=int(size * 0.03), fill=(22, 131, 255, 255))
    
    # Lock Keyhole Circle & Stem
    keyhole_r = int(size * 0.025)
    keyhole_cy = lock_top + lock_h // 2 - int(size * 0.01)
    draw.ellipse(
        [lock_cx - keyhole_r, keyhole_cy - keyhole_r, lock_cx + keyhole_r, keyhole_cy + keyhole_r],
        fill=(255, 255, 255, 255)
    )
    draw.rectangle(
        [lock_cx - int(size * 0.012), keyhole_cy, lock_cx + int(size * 0.012), keyhole_cy + int(size * 0.03)],
        fill=(255, 255, 255, 255)
    )

    # Downsample using Lanczos for razor-sharp antialiased icons
    final_img = img.resize((target_size, target_size), resample=Image.Resampling.LANCZOS)
    
    out_path = os.path.join(icons_dir, f"icon{size // scale}.png")
    final_img.save(out_path, "PNG")
    print(f"Generated {out_path}")

print("All security icons generated successfully.")
