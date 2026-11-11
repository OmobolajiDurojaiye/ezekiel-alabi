import os
from PIL import Image
import numpy as np

os.makedirs("assets", exist_ok=True)
os.makedirs("public", exist_ok=True)

# 1. Inspect logo.jpg
print("Processing logo.jpg...")
logo_img = Image.open("logo.jpg").convert("RGB")
w, h = logo_img.size
print(f"Original logo size: {w}x{h}")

a = np.asarray(logo_img).astype(np.float32)
alpha = a.max(axis=2) / 255.0
alpha = np.clip((alpha - 0.04) / 0.96, 0, 1)  # kill noise
rgb = np.where(alpha[..., None] > 0, a / np.maximum(alpha[..., None], 1e-3), 0)
rgba = np.dstack([np.clip(rgb, 0, 255), alpha * 255]).astype(np.uint8)
out_logo = Image.fromarray(rgba, "RGBA")

# Crop empty black space
bbox = out_logo.getchannel("A").point(lambda v: 255 if v > 8 else 0).getbbox()
print(f"Logo bbox: {bbox}")
if bbox:
    cropped = out_logo.crop(bbox)
    pad = int(cropped.height * 0.12)
    canvas = Image.new("RGBA", (cropped.width + pad * 2, cropped.height + pad * 2), (0, 0, 0, 0))
    canvas.paste(cropped, (pad, pad))
    canvas.save("assets/alabi-logo.png", optimize=True)
    print(f"Saved assets/alabi-logo.png ({canvas.width}x{canvas.height})")
    
    # Also create app icon and apple icon
    # Square canvas with icon centered
    side = max(canvas.width, canvas.height) + 40
    icon_canvas = Image.new("RGBA", (side, side), (0, 0, 0, 255))
    x_pos = (side - canvas.width) // 2
    y_pos = (side - canvas.height) // 2
    icon_canvas.paste(canvas, (x_pos, y_pos), canvas)
    
    # 512x512
    icon_512 = icon_canvas.resize((512, 512), Image.Resampling.LANCZOS)
    icon_512.save("public/icon.png", optimize=True)
    
    # 180x180
    icon_180 = icon_canvas.resize((180, 180), Image.Resampling.LANCZOS)
    icon_180.save("public/apple-icon.png", optimize=True)
    
    # favicon.ico
    icon_32 = icon_canvas.resize((32, 32), Image.Resampling.LANCZOS)
    icon_32.save("public/favicon.ico", format="ICO", sizes=[(32, 32), (16, 16)])
    print("Generated icons in public/")

# 2. Inspect headshot.jpg
print("Processing headshot.jpg...")
portrait_img = Image.open("headshot.jpg").convert("RGB")
pw, ph = portrait_img.size
print(f"Original portrait size: {pw}x{ph}")

p = np.asarray(portrait_img).astype(np.float32)
# crush near-black (levels: input black point ~12) to pure black
p = np.clip((p - 12) / (255 - 12), 0, 1) * 255
out_portrait = Image.fromarray(p.astype(np.uint8))
out_portrait.save("assets/alabi-portrait.jpg", quality=92, optimize=True)
print(f"Saved assets/alabi-portrait.jpg ({pw}x{ph})")

print("Asset processing complete!")
