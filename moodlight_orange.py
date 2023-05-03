import board 
import neopixel

# D18 means connect to GPIO18 on Raspberry Pi. 2 means 2 leds 
pixels = neopixel.NeoPixel(board.D18, 2)

# led on back of OLED driver board
# (255, 0 , 0 ) is RGB format of the light, value from 0-255
# (255,0,0) means (red, green, blue) it will turn on the light to red color.
# (0, 0, 0 ) will turn off the color. 

# Set LED to Blue
pixels[0] = (255, 165, 0) 

# led on fan 
# turn on fan color to blue 
pixels[1] = (255, 165, 0)

# turn off all leds
#pixels.fill((0,0,0))
