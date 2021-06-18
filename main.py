import machine
import time
import sh1106

counter = 0

# Buttons
btn_prev = machine.Pin(21, machine.Pin.IN, machine.Pin.PULL_UP)
btn_next = machine.Pin(20, machine.Pin.IN, machine.Pin.PULL_UP)
btn_up = machine.Pin(19, machine.Pin.IN, machine.Pin.PULL_UP)
btn_down = machine.Pin(18, machine.Pin.IN, machine.Pin.PULL_UP)
btn_prev_last = time.ticks_ms()
btn_next_last = time.ticks_ms()
btn_up_last = time.ticks_ms()
btn_down_last = time.ticks_ms()

# Screen
spi = machine.SPI(1, baudrate=1000000)
display = sh1106.SH1106_SPI(128, 64, machine.SPI(1), machine.Pin(5), machine.Pin(2), machine.Pin(4), False)
display.rotate(180)


def button_handler(pin):
    global btn_prev, btn_next, btn_up, btn_down, btn_prev_last, btn_next_last, btn_up_last, btn_down_last
    btn_delay = 200

    if pin is btn_prev:
        if time.ticks_diff(time.ticks_ms(), btn_prev_last) > btn_delay:
            screen_update("btn_prev")
            btn_prev_last = time.ticks_ms()
    elif pin is btn_next:
        if time.ticks_diff(time.ticks_ms(), btn_next_last) > btn_delay:
            screen_update("btn_next")
            btn_next_last = time.ticks_ms()
    elif pin is btn_up:
        if time.ticks_diff(time.ticks_ms(), btn_up_last) > btn_delay:
            screen_update("btn_up")
            btn_up_last = time.ticks_ms()
    elif pin is btn_down:
        if time.ticks_diff(time.ticks_ms(), btn_down_last) > btn_delay:
            screen_update("btn_down")
            btn_down_last = time.ticks_ms()


def screen_update(message):
    global counter
    display.fill(0)
    display.text(message + " / " + str(counter), 0, 0, 1)
    display.show()
    counter += 1


# Buttons handler
btn_prev.irq(trigger=machine.Pin.IRQ_RISING, handler=button_handler)
btn_next.irq(trigger=machine.Pin.IRQ_RISING, handler=button_handler)
btn_up.irq(trigger=machine.Pin.IRQ_RISING, handler=button_handler)
btn_down.irq(trigger=machine.Pin.IRQ_RISING, handler=button_handler)
