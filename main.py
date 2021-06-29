import machine
import utime
import sh1106

# Variables
fan_status = "OFF"
pad_status = "OFF"

# Screen
spi = machine.SPI(1, baudrate=1000000)
display = sh1106.SH1106_SPI(128, 64, machine.SPI(1), machine.Pin(5), machine.Pin(2), machine.Pin(4), False)
display.rotate(180)

# Sensor
i2c = machine.I2C(0, scl=machine.Pin(9), sda=machine.Pin(8), freq=400000)

# Heating pad
pad = machine.Pin(28, machine.Pin.OUT)

# Fan
fan = machine.Pin(27, machine.Pin.OUT)

# RGB LED
led_r = machine.Pin(13, machine.Pin.OUT)
led_g = machine.Pin(14, machine.Pin.OUT)
led_b = machine.Pin(15, machine.Pin.OUT)
# Clear common anode
led_r.value(1)
led_g.value(1)
led_b.value(1)

# Buttons
btn_prev = machine.Pin(21, machine.Pin.IN, machine.Pin.PULL_UP)
btn_next = machine.Pin(20, machine.Pin.IN, machine.Pin.PULL_UP)
btn_up = machine.Pin(19, machine.Pin.IN, machine.Pin.PULL_UP)
btn_down = machine.Pin(18, machine.Pin.IN, machine.Pin.PULL_UP)
btn_prev_last = utime.ticks_ms()
btn_next_last = utime.ticks_ms()
btn_up_last = utime.ticks_ms()
btn_down_last = utime.ticks_ms()


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


def toggle(component):
    global fan_status, pad_status
    if component == "fan":
        print('toggle fan')
        if fan_status == "ON":
            fan.value(0)
            fan_status = "OFF"
            rgb_led("clear")
        else:
            fan.value(1)
            fan_status = "ON"
            rgb_led("blue")
    elif component == "pad":
        print('toggle pad')
        if pad_status == "ON":
            pad.value(0)
            pad_status = "OFF"
            rgb_led("clear")
        else:
            pad.value(1)
            pad_status = "ON"
            rgb_led("red")


def button_handler(pin):
    global btn_prev, btn_next, btn_up, btn_down, btn_prev_last, btn_next_last, btn_up_last, btn_down_last
    btn_delay = 200

    if pin is btn_prev:
        if utime.ticks_diff(utime.ticks_ms(), btn_prev_last) > btn_delay:
            toggle("fan")
            btn_prev_last = utime.ticks_ms()
    elif pin is btn_next:
        if utime.ticks_diff(utime.ticks_ms(), btn_next_last) > btn_delay:
            toggle("pad")
            btn_next_last = utime.ticks_ms()
    # elif pin is btn_up:
    #     if utime.ticks_diff(utime.ticks_ms(), btn_up_last) > btn_delay:
    #         rgb_led("green")
    #         btn_up_last = utime.ticks_ms()
    # elif pin is btn_down:
    #     if utime.ticks_diff(utime.ticks_ms(), btn_down_last) > btn_delay:
    #         rgb_led("green")
    #         btn_down_last = utime.ticks_ms()



# Buttons handler
btn_prev.irq(trigger=machine.Pin.IRQ_RISING, handler=button_handler)
btn_next.irq(trigger=machine.Pin.IRQ_RISING, handler=button_handler)
btn_up.irq(trigger=machine.Pin.IRQ_RISING, handler=button_handler)
btn_down.irq(trigger=machine.Pin.IRQ_RISING, handler=button_handler)


while True:
    
    # I2C data
    try:
        i2c.writeto(0x44, bytes([0x2C, 0x06]))
        utime.sleep(0.5)
        data = i2c.readfrom_mem(0x44, 0x00, 6)
        i2c_data = True
    except:
        i2c_data = False

    # Temperature and humidity
    if i2c_data:
        temp = data[0] * 256 + data[1]
        temp_c = -45 + (175 * temp / 65535.0)
        temp_c_unit = str(round(temp_c, 2)) + "C"
        humidity = 100 * (data[3] * 256 + data[4]) / 65535.0
        humidity_unit = str(round(humidity, 2)) + "%"
    else:
        temp_c_unit = "no data"
        humidity_unit = "no data"

    # Screen update
    display.fill(0)
    utime.sleep(1)
    display.text("TEMP:" + temp_c_unit, 20, 10)
    display.text("HUMI:" + humidity_unit, 20, 20)
    display.text("FAN :" + fan_status, 20, 30)
    display.text("PAD :" + pad_status, 20, 40)
    display.show()

