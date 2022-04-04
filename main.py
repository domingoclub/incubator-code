from machine import Pin, I2C
import sh1106
import utime
import framebuf
from fdrawer import FontDrawer

# Variables
FAN_STATUS = "OFF"
PAD_STATUS = "OFF"
WIDTH  = 128
HEIGHT = 64
CURRENT_SCREEN = "temp_display"
TEMP_DISPLAY = True
TEMP_IDEAL = 30
TEMP_MARGIN = 2

# Sensor
i2c_sensor = I2C(0, scl = Pin(13), sda = Pin(12), freq = 400000)


# Display
i2c_display = I2C(1, scl = Pin(27), sda = Pin(26), freq = 400000)
display = sh1106.SH1106_I2C(128, 64, i2c_display, Pin(16), 0x3c)
display.rotate(180)
display.fill(0)

# Heating pad
pad = Pin(5, Pin.OUT)

# Fan
fan = Pin(6, Pin.OUT)
fan.value(0)

# RGB LED
led_r = Pin(22, Pin.OUT)
led_r = Pin(22, Pin.OUT)
led_g = Pin(21, Pin.OUT)
led_b = Pin(20, Pin.OUT)
# Clear common anode
led_r.value(1)
led_g.value(1)
led_b.value(1)

# Buttons
btn_prev = Pin(19, Pin.IN, Pin.PULL_UP)
btn_next = Pin(18, Pin.IN, Pin.PULL_UP)
btn_up = Pin(16, Pin.IN, Pin.PULL_UP)
btn_down = Pin(17, Pin.IN, Pin.PULL_UP)
btn_prev_last = utime.ticks_ms()
btn_next_last = utime.ticks_ms()
btn_up_last = utime.ticks_ms()
btn_down_last = utime.ticks_ms()

# Fonts
# Normal FrameBuffer operation
display.rect( 0, 0, WIDTH, HEIGHT, 0)
display.show()

# Use a font drawer to draw font to FrameBuffer
fd_sm = FontDrawer( frame_buffer = display, font_name = 'vera_10' )
fd_md = FontDrawer( frame_buffer = display, font_name = 'vera_15' )
fd_lg = FontDrawer( frame_buffer = display, font_name = 'vera_23' )
fd_ar = FontDrawer( frame_buffer = display, font_name = 'arrows_15' )

# Images

# 40x40 sun icon pixel array
temperature = bytearray(b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00?>p\xcf\x87\xcf\xc0\xc3\xf4\t\xf0\xf8\x00\x00\x00\x00?~p\xcf\xcf\xc7\xc1\xc3\xf2\t\xf8\xf8\x00\x00\x00\x00\x08 Q\xc8D\x08a\xa0\x84\t\t\x80\x00\x00\x00\x00\x08 Y\xc8d\x08!`\x82\t\x08\x80\x00\x00\x00\x00\x08|YIG\x87\xc3 \x84\t\xf8\xf0\x00\x00\x00\x00\x04 KO\xc4\x0f\x83\xb0B\x19\xf0\x80\x00\x00\x00\x00\x08 NM\x0c\x04CP\x83\x11\x10\x80\x00\x00\x00\x00\x08>NH\x07\xc8f\x10\x83\xf1\x19\xf8\x00\x00\x00\x00\x04~FH\x07\xe4&\x08A\xe1\x0c\xfc\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00 \x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x10 \x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x10\x00@\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x08@\x80\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x08A\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x0c\x08B\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x03\x04\x84\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x84\x08\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00b\x90\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x1a \x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x05\xa5p\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x1f\xab\xda\x80\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00+\xa0\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x0f\xa0\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00P\x8e\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x85!\xa0\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x06\x04\xb0\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x08\t\x08\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x10\x88\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x10\x84\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x10\x83\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00 \x80\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00@\x80\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00@\x80\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00@\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x80\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x80\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\xc0\x02\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00`\x07R\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00p\x07\xff\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x7f\xf8\x02\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00[p\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00`\x00\x80\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xc0\x00@\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x80\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')
sun = bytearray(b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x0c\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x10\x00\x0c\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x008\x00\x06\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x1c\x00\x06\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x06\x00\x06\x00\x01\x80\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x07\x00\x06\x00\x03\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x80\x06\x00\x07\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\xc0\x06\x00\x06\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xe0\x06\x00\x0c\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00p\x03\x00\x18\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x008\x07\x008\x00\x00\x00\x00\x00\x00\x00\x00\x00\x000\x00\x1c\x03\x00p\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x1c\x00\x0e\x03\x00`\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x0f\x80\x07\x03\x00\xc0\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\xe0\x03\x83\x01\x80\x00\x04\x00\x00\x00\x00\x00\x00\x00\x00\x00|\x01\x83\x03\x80\x00>\x00\x00\x00\x00\x00\x00\x00\x00\x00\x0f\x00\xe3\x87\x00\x01\xf0\x00\x00\x00\x00\x00\x00\x00\x00\x00\x03\xc0a\x0e\x00\x0f\xc0\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xf03\x8c\x00~\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x1c\x19\x98\x01\xf0\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x0f\x8d\xb8\x0f\x80\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\xe7\xb0~\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x7f\xe3\xf0\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x1f\xef\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x7f\xff\xff\xef\xfc\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00U\xabw\xff\xfe\x80\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x0f\xf7\xf0\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x009\xf8_\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00sn\x05\xe0\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\xe3c\x00~\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x03\x831\xc0\x07\xe0\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x07\x03\x18\xe0\x00~\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x0e\x06\x180\x00\x07\x00\x00\x00\x00\x00\x00\x00\x00\x00\x008\x06\x0c\x1c\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00p\x06\x0c\x0e\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xe0\x0e\x06\x03\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x03\xc0\x04\x06\x01\xc0\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x07\x00\x0c\x03\x00\xe0\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x0e\x00\x0c\x03\x808\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00<\x00\x0c\x01\x80\x1c\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00p\x00\x1c\x00\xc0\x07\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00`\x00\x18\x00\xc0\x03\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x18\x00\xe0\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x18\x00`\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x18\x000\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x008\x000\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x000\x00\x18\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x000\x00\x18\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x000\x00\x0c\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x04\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')


def rgb_led(color):
    if color == "red":
        led_r.value(0)
        led_g.value(1)
        led_b.value(1)
    elif color == "green":
        led_r.value(1)
        led_g.value(0)
        led_b.value(1)
    elif color == "blue":
        led_r.value(1)
        led_g.value(1)
        led_b.value(0)
    elif color == "clear":
        led_r.value(1)
        led_g.value(1)
        led_b.value(1)
        
def button_handler(pin):
    global CURRENT_SCREEN, TEMP_IDEAL, btn_prev, btn_next, btn_up, btn_down, btn_prev_last, btn_next_last, btn_up_last, btn_down_last
    btn_delay = 200

    if pin is btn_prev:
        if utime.ticks_diff(utime.ticks_ms(), btn_prev_last) > btn_delay:
            print('prev')
            if (CURRENT_SCREEN == "temp_set"):
                CURRENT_SCREEN = "temp_display"
            else:
                CURRENT_SCREEN = "temp_set"
            btn_prev_last = utime.ticks_ms()
    elif pin is btn_next:
        if utime.ticks_diff(utime.ticks_ms(), btn_next_last) > btn_delay:
            print('next')
            if (CURRENT_SCREEN == "temp_set"):
                CURRENT_SCREEN = "temp_display"
            else:
                CURRENT_SCREEN = "temp_set"
            btn_next_last = utime.ticks_ms()
    elif pin is btn_up:
        if utime.ticks_diff(utime.ticks_ms(), btn_up_last) > btn_delay:
            print('up')
            if (CURRENT_SCREEN == "temp_set"):
                TEMP_IDEAL = TEMP_IDEAL + 1
            btn_up_last = utime.ticks_ms()
    elif pin is btn_down:
        if utime.ticks_diff(utime.ticks_ms(), btn_down_last) > btn_delay:
            print('down')
            if (CURRENT_SCREEN == "temp_set"):
                TEMP_IDEAL = TEMP_IDEAL - 1
            btn_down_last = utime.ticks_ms()
            
# Buttons handler
btn_prev.irq(trigger=Pin.IRQ_RISING, handler=button_handler)
btn_next.irq(trigger=Pin.IRQ_RISING, handler=button_handler)
btn_up.irq(trigger=Pin.IRQ_RISING, handler=button_handler)
btn_down.irq(trigger=Pin.IRQ_RISING, handler=button_handler)


# Sun
def display_sun():
    display.fill(0)
    fb = framebuf.FrameBuffer(sun, 128, 64, framebuf.MONO_HLSB)
    display.blit(fb, 0, 0)
    display.show()

def display_temp(temp):
    display.fill(0)
    display.rect(0, 0, WIDTH, HEIGHT, 1)
    fd_sm.print_str('TEMPERATURE',20,2)
    display.fill_rect(0, 15, WIDTH, 2, 1)
    fd_lg.print_str(temp,30,26)
    fd_ar.print_str("B", 5, 42)
    display.fill_rect(9, 42, 20, 20, 0)
    fd_ar.print_str("A", 106, 42)
    display.fill_rect(99, 42, 20, 20, 0)
    display.show()
    TEMP_DISPLAY = True

def display_temp_set(temp):
    display.fill(0)
    display.rect(0, 0, WIDTH, HEIGHT, 1)
    fd_sm.print_str('SET IDEAL',40,2)
    display.fill_rect(0, 15, WIDTH, 2, 1)
    fd_lg.print_str(str(temp),50,26)
    fd_ar.print_str("B", 5, 42)
    display.fill_rect(9, 42, 20, 20, 0)
    fd_ar.print_str("A", 106, 42)
    display.fill_rect(99, 42, 20, 20, 0)

    display.show()
    TEMP_DISPLAY = False

display_sun()
utime.sleep(1)


while True:
    
    # I2C data
    try:
        i2c_sensor.writeto(0x44, bytes([0x2C, 0x06]))
        utime.sleep(0.5)
        data = i2c_sensor.readfrom_mem(0x44, 0x00, 6)
        i2c_sensor_data = True
    except:
        i2c_sensor_data = False

    # Temperature and humidity
    if i2c_sensor_data:
        temp = data[0] * 256 + data[1]
        temp_c = -45 + (175 * temp / 65535.0)
        temp_c_unit = str(round(temp_c, 1)) + "°C"
        humidity = 100 * (data[3] * 256 + data[4]) / 65535.0
        humidity_unit = str(round(humidity, 2)) + "%"
    else:
        temp_c = 0
        humidity = 0
        temp_c_unit = ""
        humidity_unit = ""

    if temp_c < TEMP_IDEAL:
        pad.on()
        fan.on()
        rgb_led("red")
    elif temp_c >= TEMP_IDEAL and temp_c <= TEMP_IDEAL + TEMP_MARGIN:
        fan.off()
        pad.off()
        rgb_led("green")
    elif temp_c > TEMP_IDEAL + TEMP_MARGIN:
        pad.off()
        fan.on()
        rgb_led("blue")
    else:
        pad.off()
        fan.off()
        rgb_led("clear")

    print(CURRENT_SCREEN)
    if CURRENT_SCREEN == "temp_set":
        display_temp_set(TEMP_IDEAL)
    elif CURRENT_SCREEN == "temp_display":
        display_temp(temp_c_unit)
    

    print("temp: " + temp_c_unit)
    print("humi: " + humidity_unit)
    utime.sleep(.1)
        
    
    
