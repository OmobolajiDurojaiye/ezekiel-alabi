from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np
import shutil

W, H = 1200, 630
og = Image.new("RGB", (W, H), (255, 255, 255))

# Atmospheric soft glow
glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
gd = ImageDraw.Draw(glow)
cx, cy = W // 2, int(H * 0.42)
for r in range(350, 0, -5):
    t = 1.0 - (r / 350)
    alpha_val = int(55 * (t ** 1.8))
    cr = int(229 * (1 - t) + 153 * t)
    cg = int(160 * (1 - t) + 0 * t)
    cb = int(253 * (1 - t) + 204 * t)
    gd.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(cr, cg, cb, alpha_val))

glow = glow.filter(ImageFilter.GaussianBlur(35))
og.paste(glow, (0, 0), glow)

# Headline 'Coming Soon' behind subject
font_sans = ImageFont.truetype("assets/fonts/InterTight-Variable.ttf", 150)
cd = ImageDraw.Draw(og)
bbox_cs = cd.textbbox((0, 0), "Coming Soon", font=font_sans)
csw = bbox_cs[2] - bbox_cs[0]
csx = (W - csw) // 2
csy = int(H * 0.52)
cd.text((csx, csy), "Coming Soon", font=font_sans, fill=(15, 23, 42))

# Center bottom-anchored portrait
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
logo_disp_h = 42
logo_disp_w = int(logo.width * (logo_disp_h / logo.height))
l_resized = logo.resize((logo_disp_w, logo_disp_h), Image.Resampling.LANCZOS)
og.paste(l_resized, (56, 44), l_resized)

og.save("app/opengraph-image.png", optimize=True)
shutil.copy("app/opengraph-image.png", "app/twitter-image.png")
shutil.copy("app/opengraph-image.png", "public/og.png")
print("Saved white-themed opengraph-image.png and twitter-image.png (1200x630)")

# Generate icons
# Square canvas with monogram / mark
icon_canvas = Image.new("RGB", (512, 512), (255, 255, 255))
ic_draw = ImageDraw.Draw(icon_canvas)
# Subtle brand gradient circle
ic_draw.ellipse([24, 24, 488, 488], fill=(250, 245, 255), outline=(229, 160, 253), width=6)
# Paste logo scaled inside
lw = 420
lh = int(logo.height * (lw / logo.width))
l_icon = logo.resize((lw, lh), Image.Resampling.LANCZOS)
icon_canvas.paste(l_icon, ((512 - lw) // 2, (512 - lh) // 2), l_icon)

icon_canvas.save("public/icon.png", optimize=True)
icon_canvas.save("app/icon.png", optimize=True)

apple_icon = icon_canvas.resize((180, 180), Image.Resampling.LANCZOS)
apple_icon.save("public/apple-icon.png", optimize=True)
apple_icon.save("app/apple-icon.png", optimize=True)

fav = icon_canvas.resize((32, 32), Image.Resampling.LANCZOS)
fav.save("public/favicon.ico", format="ICO", sizes=[(32, 32), (16, 16)])
fav.save("app/favicon.ico", format="ICO", sizes=[(32, 32), (16, 16)])
print("Updated all icons for white theme!")
