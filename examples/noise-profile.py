import ST7735
from PIL import Image, ImageDraw
from enviroplus.noise import Noise

SAMPLERATE = 16000

FREQ_LOW = 100.0
FREQ_HIGH = 2000.0
WIDTH = 100

noise = Noise()

disp = ST7735.ST7735(
        port=0,
        cs=ST7735.BG_SPI_CS_FRONT,
        dc=9,
        backlight=12,
        rotation=90)

disp.begin()

img = Image.new('RGB', (disp.width, disp.height), color=(0, 0, 0))
draw = ImageDraw.Draw(img)


while True:
    low, mid, high, amp = noise.measure()
    low *= 128
    mid *= 128
    high *= 128
    amp *= 64

    img2 = img.copy()
    draw.rectangle((0, 0, disp.width, disp.height), (0, 0, 0))
    img.paste(img2, (1, 0))
    draw.line((0, 0, 0, amp), fill=(int(low), int(mid), int(high)))

    disp.display(img)

