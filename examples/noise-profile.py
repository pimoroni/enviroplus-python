import st7735
from PIL import Image, ImageDraw

from enviroplus.noise import Noise

print("""noise-profile.py - Get a simple noise profile.

This example grabs a basic 3-bin noise profile of low, medium and high frequency noise, plotting the noise characteristics as coloured bars.

Press Ctrl+C to exit!

""")

noise = Noise()

disp = st7735.ST7735(
    port=0,
    cs=1,
    dc="GPIO9",
    backlight="GPIO12",
    rotation=270,
    spi_speed_hz=10000000
)

disp.begin()

img = Image.new("RGB", (disp.width, disp.height), color=(0, 0, 0))
draw = ImageDraw.Draw(img)


while True:
    low, mid, high, amp = noise.get_noise_profile()
    low *= 128
    mid *= 128
    high *= 128
    amp *= 64

    img2 = img.copy()
    draw.rectangle((0, 0, disp.width, disp.height), (0, 0, 0))
    img.paste(img2, (1, 0))
    draw.line((0, 0, 0, amp), fill=(int(low), int(mid), int(high)))

    disp.display(img)
