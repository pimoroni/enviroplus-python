import st7735
from PIL import Image, ImageDraw

from enviroplus.noise import Noise

print("""noise-amps-at-freqs.py - Measure amplitude from specific frequency bins

This example retrieves the median amplitude from 3 user-specified frequency ranges and plots them in Blue, Green and Red on the Enviro+ display.

As you play a continuous rising tone on your phone, you should notice peaks that correspond to the frequency entering each range.

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
    amps = noise.get_amplitudes_at_frequency_ranges([
        (100, 200),
        (500, 600),
        (1000, 1200)
    ])
    amps = [n * 32 for n in amps]
    img2 = img.copy()
    draw.rectangle((0, 0, disp.width, disp.height), (0, 0, 0))
    img.paste(img2, (1, 0))
    draw.line((0, 0, 0, amps[0]), fill=(0, 0, 255))
    draw.line((0, 0, 0, amps[1]), fill=(0, 255, 0))
    draw.line((0, 0, 0, amps[2]), fill=(255, 0, 0))

    disp.display(img)
