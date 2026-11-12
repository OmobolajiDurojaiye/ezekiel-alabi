import numpy as np
from PIL import Image, ImageFilter
from collections import deque

img = Image.open('headshot.jpg').convert('RGB')
w, h = img.size
a = np.array(img)
b = a.max(axis=2)

# BFS floodfill from boundary
visited = np.zeros((h, w), dtype=bool)
q = deque()

# Add all 4 borders if b <= 20
for x in range(w):
    if b[0, x] <= 20: q.append((0, x)); visited[0, x] = True
    if b[h-1, x] <= 20: q.append((h-1, x)); visited[h-1, x] = True
for y in range(h):
    if b[y, 0] <= 20: q.append((y, 0)); visited[y, 0] = True
    if b[y, w-1] <= 20: q.append((y, w-1)); visited[y, w-1] = True

while q:
    y, x = q.popleft()
    for dy, dx in [(-1,0), (1,0), (0,-1), (0,1)]:
        ny, nx = y + dy, x + dx
        if 0 <= ny < h and 0 <= nx < w and not visited[ny, nx]:
            if b[ny, nx] <= 18:
                visited[ny, nx] = True
                q.append((ny, nx))

# Initial raw foreground alpha
raw_fg = np.where(visited, 0, 255).astype(np.uint8)
raw_alpha_img = Image.fromarray(raw_fg)

# Erode by 3 pixels to completely eliminate the dark background fringe
# MinFilter(5) contracts foreground by 2-3px
eroded_alpha = raw_alpha_img.filter(ImageFilter.MinFilter(5))

# Progressive Gaussian feather: 3.5px blur for soft, photographic edge transition
smooth_alpha = eroded_alpha.filter(ImageFilter.GaussianBlur(3.5))

# Soft edge illumination:
# Because studio portraits on light backgrounds have gentle rim light,
# we brighten the outer perimeter of the subject slightly (ambient wrap)
alpha_np = np.array(smooth_alpha).astype(np.float32) / 255.0

# Edge zone: where alpha is between 0.05 and 0.95
edge_zone = (alpha_np > 0.02) & (alpha_np < 0.92)
brightened_rgb = a.astype(np.float32).copy()

# Add subtle warm studio rim wrap on the edge pixels
brightened_rgb[edge_zone] = np.clip(
    brightened_rgb[edge_zone] + (1.0 - alpha_np[edge_zone, None]) * 110,
    0, 255
)

# Also feather the side edges gently so the shoulders/arms blend seamlessly into the sides
x_coords = np.linspace(-1, 1, w)[None, :]
side_mask = np.clip(1.0 - np.maximum(0, (np.abs(x_coords) - 0.78) / 0.2), 0, 1)
final_alpha = np.clip(alpha_np * side_mask * 255, 0, 255).astype(np.uint8)

final_rgba = np.dstack([brightened_rgb.astype(np.uint8), final_alpha])
portrait_out = Image.fromarray(final_rgba, 'RGBA')
portrait_out.save('assets/alabi-portrait.png', optimize=True)
print('Generated perfectly blended assets/alabi-portrait.png!')

# Preview on pure white background
preview = Image.new('RGB', (w, h), (255, 255, 255))
preview.paste(portrait_out, (0, 0), portrait_out)
preview.save('test_blended_portrait.jpg', quality=95)
print('Saved test_blended_portrait.jpg!')
