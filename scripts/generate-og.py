from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np
import shutil

W, H = 1200, 630
og = Image.new("RGBA", (W, H), (0, 0, 0, 255))

# Create glow
glow_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
glow_draw = ImageDraw.Draw(glow_layer)
# Radial gradient for glow behind head/shoulders
cx, cy = W // 2, int(H * 0.45)
max_r = 350
for r in range(max_r, 0, -5):
    t = 1.0 - (r / max_r)
    alpha = int(60 * (t ** 1.5))
    # blend from pink (229, 160, 253) to purple (153, 0, 204)
    cr = int(229 * (1 - t) + 153 * t)
    cg = int(160 * (1 - t) + 0 * t)
    cb = int(253 * (1 - t) + 204 * t)
    glow_draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(cr, cg, cb, alpha))

glow_layer = glow_layer.filter(ImageFilter.GaussianBlur(35))
og.paste(glow_layer, (0, 0), glow_layer)

# Paste portrait
portrait = Image.open("assets/alabi-portrait.jpg").convert("RGBA")
# Scale portrait so height fits nicely in 630 (say 580px tall)
target_h = int(H * 0.95)
scale = target_h / portrait.height
target_w = int(portrait.width * scale)
portrait_scaled = portrait.resize((target_w, target_h), Image.Resampling.LANCZOS)

# Apply feather mask to portrait edges
p_arr = np.asarray(portrait_scaled).astype(np.float32)
yy, xx = np.indices((target_h, target_w))
# center of mask
norm_x = (xx - target_w / 2) / (target_w / 2)
norm_y = (yy - target_h * 0.5) / (target_h * 0.5)
dist = (norm_x ** 2) / (0.75 ** 2) + (norm_y ** 2) / (0.95 ** 2)
mask = np.clip(1.0 - (dist - 0.4) / 0.6, 0.0, 1.0) * 255
p_rgba = p_arr.copy()
p_rgba[..., 3] = np.minimum(p_rgba[..., 3], mask)
portrait_feathered = Image.fromarray(p_rgba.astype(np.uint8), "RGBA")

px = (W - target_w) // 2
py = H - target_h
og.paste(portrait_feathered, (px, py), portrait_feathered)

# Paste logo top-left
logo = Image.open("assets/alabi-logo.png").convert("RGBA")
# display height ~ 36px in 630p
logo_h = 42
logo_w = int(logo.width * (logo_h / logo.height))
logo_scaled = logo.resize((logo_w, logo_h), Image.Resampling.LANCZOS)
og.paste(logo_scaled, (56, 48), logo_scaled)

# Add "Coming Soon" headline text
# Look for a clean system sans-serif font or fallback
draw = ImageDraw.Draw(og)
font = None
candidate_fonts = [
    "C:/Windows/Fonts/Inter-Medium.ttf",
    "C:/Windows/Fonts/Inter.ttf",
    "C:/Windows/Fonts/segoeui.ttf",
    "C:/Windows/Fonts/arial.ttf",
]
for fpath in candidate_fonts:
    try:
        font = ImageFont.truetype(fpath, 110)
        break
    except Exception:
        continue

if font is None:
    font = ImageFont.load_default()

text = "Coming Soon"
bbox = draw.textbbox((0, 0), text, font=font)
tw = bbox[2] - bbox[0]
th = bbox[3] - bbox[1]
tx = (W - tw) // 2
ty = int(H * 0.58)

# subtle shadow for text legibility
draw.text((tx, ty + 2), text, font=font, fill=(0, 0, 0, 180))
draw.text((tx, ty), text, font=font, fill=(255, 255, 255, 255))

og.save("app/opengraph-image.png", optimize=True)
shutil.copy("app/opengraph-image.png", "app/twitter-image.png")
shutil.copy("app/opengraph-image.png", "public/og.png")
print("Saved opengraph-image.png and twitter-image.png (1200x630)")
