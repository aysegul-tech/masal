import sys
from PIL import Image, ImageFilter, ImageEnhance, ImageDraw
src = Image.open(sys.argv[1]).convert("RGB")
out = sys.argv[2]
W, H = 1200, 800

def tam():
    # Arka plan: resmin kendisinden bulanık, açık bir zemin; önde resmin tamamı
    # Zemin: resmin kâğıt rengi (en açık tonlarının ortalaması)
    px = sorted(src.resize((96, 128)).getdata(), key=sum)[-2000:]
    renk = tuple(sum(c[i] for c in px) // len(px) for i in range(3))
    bg = Image.new("RGB", (W, H), renk)
    h = H - 50
    fg = src.resize((int(h * src.width / src.height), h), Image.LANCZOS)
    mask = Image.new("L", fg.size, 0)
    ImageDraw.Draw(mask).rectangle((14, 14, fg.width - 14, fg.height - 14), fill=255)
    mask = mask.filter(ImageFilter.GaussianBlur(10))
    bg.paste(fg, ((W - fg.width) // 2, 25), mask)
    return bg

def kirp(x, y, w):
    h = round(w * 2 / 3)
    im = src.crop((x, y, x + w, y + h)).resize((W, H), Image.LANCZOS)
    return im.filter(ImageFilter.UnsharpMask(radius=2, percent=60, threshold=3))

sahneler = {
    1: tam(),
    2: kirp(250, 290, 330),   # Nur: ortadaki büyük nergis
    3: kirp(470, 375, 240),   # Minik: sağdaki küçük nergis
    4: kirp(95, 105, 300),    # kenardaki, yüzü gölgede nergis
    5: kirp(110, 95, 540),    # çiçeklerin hepsi birlikte
    6: kirp(225, 505, 300),   # aşağıdaki tomurcuk
    7: kirp(390, 160, 285),   # yukarıda yeni açmış çiçek
    8: tam(),
}
for i, im in sahneler.items():
    im.save(f"{out}/{i}.jpg", quality=86, optimize=True, progressive=True)
