from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np
import shutil

W, H = 1200, 630
og = Image.new("RGB", (W, H), (255, 255, 255))

# Atmospheric soft glow
glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
gd = ImageDraw.Draw(glow)
cx, cy = W // 2, int(H * 0.40)
for r in range(350, 0, -5):
    t = 1.0 - (r / 350)
    alpha_val = int(55 * (t ** 1.8))
    cr = int(229 * (1 - t) + 153 * t)
    cg = int(160 * (1 - t) + 0 * t)
    cb = int(253 * (1 - t) + 204 * t)
    gd.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(cr, cg, cb, alpha_val))

glow = glow.filter(ImageFilter.GaussianBlur(35))
og.paste(glow, (0, 0), glow)

# Measure text with Geist
font_geist = ImageFont.truetype("assets/fonts/Geist-Variable.ttf", 145)
dummy = Image.new("RGBA", (100, 100))
dd = ImageDraw.Draw(dummy)
bbox = dd.textbbox((0, 0), "Coming Soon", font=font_geist)
tw = bbox[2] - bbox[0]
th = bbox[3] - bbox[1]
tx = (W - tw) // 2
ty = int(H * 0.52)

# Draw 'Coming Soon' behind portrait in black
cd = ImageDraw.Draw(og)
cd.text((tx, ty), "Coming Soon", font=font_geist, fill=(10, 10, 10))

# Paste portrait
cutout = Image.open("assets/alabi-portrait.png")
pw, ph = cutout.size
target_h = int(H * 0.96)
target_w = int(pw * (target_h / ph))
p_resized = cutout.resize((target_w, target_h), Image.Resampling.LANCZOS)
px = (W - target_w) // 2
py = H - target_h
og.paste(p_resized, (px, py), p_resized)

# Logo top-left
logo = Image.open("assets/alabi-logo.png")
logo_disp_h = 44
logo_disp_w = int(logo.width * (logo_disp_h / logo.height))
l_resized = logo.resize((logo_disp_w, logo_disp_h), Image.Resampling.LANCZOS)
og.paste(l_resized, (56, 44), l_resized)

og.save("app/opengraph-image.png", optimize=True)
shutil.copy("app/opengraph-image.png", "app/twitter-image.png")
shutil.copy("app/opengraph-image.png", "public/og.png")
print("Saved opengraph-image.png and twitter-image.png (1200x630)")
