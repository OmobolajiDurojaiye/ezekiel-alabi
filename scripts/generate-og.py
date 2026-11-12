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
font_geist = ImageFont.truetype("assets/fonts/Geist-Variable.ttf", 140)
dummy = Image.new("RGBA", (100, 100))
dd = ImageDraw.Draw(dummy)
bbox_c = dd.textbbox((0, 0), "Coming", font=font_geist)
cw = bbox_c[2] - bbox_c[0]
bbox_s = dd.textbbox((0, 0), "Soon", font=font_geist)
sw = bbox_s[2] - bbox_s[0]
space_w = 30
total_text_w = cw + space_w + sw
start_x = (W - total_text_w) // 2
text_y = int(H * 0.52)

# Draw 'Coming' behind portrait in black
cd = ImageDraw.Draw(og)
cd.text((start_x, text_y), "Coming", font=font_geist, fill=(10, 10, 10))

# Paste portrait
cutout = Image.open("assets/alabi-portrait.png")
pw, ph = cutout.size
target_h = int(H * 0.96)
target_w = int(pw * (target_h / ph))
p_resized = cutout.resize((target_w, target_h), Image.Resampling.LANCZOS)
px = (W - target_w) // 2
py = H - target_h
og.paste(p_resized, (px, py), p_resized)

# Draw 'Soon' in front of portrait with half-white/half-black
soon_x = start_x + cw + space_w
s_white = Image.new("RGBA", (sw + 30, 200), (0, 0, 0, 0))
swd = ImageDraw.Draw(s_white)
swd.text((2, 2), "Soon", font=font_geist, fill=(0, 0, 0, 140))
swd.text((0, 0), "Soon", font=font_geist, fill=(255, 255, 255, 255))

s_black = Image.new("RGBA", (sw + 30, 200), (0, 0, 0, 0))
sbd = ImageDraw.Draw(s_black)
sbd.text((0, 0), "Soon", font=font_geist, fill=(10, 10, 10, 255))

mask_arr = np.zeros((200, sw + 30), dtype=np.float32)
split_col = int(sw * 0.40)
trans_w = 16
for c in range(sw + 30):
    if c < split_col:
        mask_arr[:, c] = 1.0
    elif c > split_col + trans_w:
        mask_arr[:, c] = 0.0
    else:
        mask_arr[:, c] = 1.0 - (c - split_col) / trans_w

arr_w = np.array(s_white).astype(np.float32)
arr_b = np.array(s_black).astype(np.float32)
res_arr = arr_w * mask_arr[..., None] + arr_b * (1.0 - mask_arr[..., None])
soon_final = Image.fromarray(res_arr.astype(np.uint8), "RGBA")
og.paste(soon_final, (soon_x, text_y), soon_final)

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

# Generate icons
icon_canvas = Image.new("RGB", (512, 512), (255, 255, 255))
ic_draw = ImageDraw.Draw(icon_canvas)
ic_draw.ellipse([24, 24, 488, 488], fill=(250, 245, 255), outline=(229, 160, 253), width=6)
lw = 440
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
print("Updated all icons with Brand Logo!")
