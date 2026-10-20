import board
import busio
import digitalio
import analogio
from kmk.kmk_keyboard import KMKKeyboard
from kmk.keys import KC
from kmk.scanners import DiodeOrientation
from kmk.scanners.digitalio import MatrixScanner
from kmk.hid import HIDModes
from kmk.modules.layers import Layers
from kmk.modules import Module
from adafruit_mcp230xx.mcp23017 import MCP23017
LCD_CLK = board.SCK
LCD_DIN = board.MOSI
LCD_CS = board.A0
LCD_DC = board.D6
LCD_RST = board.D9
LCD_BL = board.A1
LED_CAPS = board.D10
LED_NUM = board.D11
LED_BAT_LOW = board.D12
LED_BAT_GOOD = board.D13
try:
    BATTERY_PIN = board.VOLTAGE_MONITOR
except AttributeError:
    BATTERY_PIN = board.A6
i2c = busio.I2C(board.SCL, board.SDA, frequency=400000)
mcp1 = MCP23017(i2c, address=32)
mcp2 = MCP23017(i2c, address=33)
col_pins = [mcp1.get_pin(0), mcp1.get_pin(1), mcp1.get_pin(2), mcp1.get_pin(3), mcp1.get_pin(4), mcp1.get_pin(5), mcp1.get_pin(6), mcp1.get_pin(7), mcp1.get_pin(8), mcp1.get_pin(9), mcp1.get_pin(10), mcp1.get_pin(11), mcp1.get_pin(12), mcp1.get_pin(13), mcp1.get_pin(14), mcp1.get_pin(15), mcp2.get_pin(0), mcp2.get_pin(1), mcp2.get_pin(2), mcp2.get_pin(3), mcp2.get_pin(4)]
row_pins = [mcp2.get_pin(8), mcp2.get_pin(9), mcp2.get_pin(10), mcp2.get_pin(11), mcp2.get_pin(12), mcp2.get_pin(13)]
COLS = len(col_pins)
ROWS = len(row_pins)
keyboard = KMKKeyboard()
keyboard.matrix = MatrixScanner(cols=col_pins, rows=row_pins, diode_orientation=DiodeOrientation.COL2ROW)
_______ = KC.TRNS
XXXXXXX = KC.NO
_L0 = [KC.ESC, KC.F1, KC.F2, KC.F3, KC.F4, KC.F5, KC.F6, KC.F7, KC.F8, KC.F9, KC.F10, KC.F11, KC.F12, XXXXXXX, KC.PSCR, KC.SLCK, KC.PAUS, XXXXXXX, KC.MUTE, KC.VOLD, KC.VOLU, KC.GRV, KC.N1, KC.N2, KC.N3, KC.N4, KC.N5, KC.N6, KC.N7, KC.N8, KC.N9, KC.N0, KC.MINS, KC.EQL, KC.BSPC, KC.INS, KC.HOME, KC.PGUP, KC.NLCK, KC.PSLS, KC.PAST, KC.PMNS, KC.TAB, KC.Q, KC.W, KC.E, KC.R, KC.T, KC.Y, KC.U, KC.I, KC.O, KC.P, KC.LBRC, KC.RBRC, KC.BSLS, KC.DEL, KC.END, KC.PGDN, KC.P7, KC.P8, KC.P9, KC.PPLS, KC.CAPS, KC.A, KC.S, KC.D, KC.F, KC.G, KC.H, KC.J, KC.K, KC.L, KC.SCLN, KC.QUOT, KC.ENT, XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX, KC.P4, KC.P5, KC.P6, XXXXXXX, KC.LSFT, KC.Z, KC.X, KC.C, KC.V, KC.B, KC.N, KC.M, KC.COMM, KC.DOT, KC.SLSH, KC.RSFT, XXXXXXX, XXXXXXX, XXXXXXX, KC.UP, XXXXXXX, KC.P1, KC.P2, KC.P3, KC.PENT, KC.LCTL, KC.LGUI, KC.LALT, XXXXXXX, XXXXXXX, KC.SPC, XXXXXXX, XXXXXXX, XXXXXXX, KC.RALT, KC.MO(1), KC.RCTL, XXXXXXX, XXXXXXX, KC.LEFT, KC.DOWN, KC.RIGHT, KC.P0, XXXXXXX, KC.PDOT, XXXXXXX]
_L1 = [_______] * (ROWS * COLS)
_L1[0] = KC.HID
keyboard.keymap = [_L0, _L1]
layers = Layers()

def _out(pin):
    d = digitalio.DigitalInOut(pin)
    d.direction = digitalio.Direction.OUTPUT
    d.value = False
    return d

class StatusModule(Module):

    def __init__(self):
        self._n = 0
        self._frame = 0
        self._hid = None
        self.led_caps = self.led_num = self.led_low = self.led_good = None
        try:
            self.led_caps = _out(LED_CAPS)
            self.led_num = _out(LED_NUM)
            self.led_low = _out(LED_BAT_LOW)
            self.led_good = _out(LED_BAT_GOOD)
        except Exception as e:
            print('LED init failed:', e)
        self.batt = None
        try:
            self.batt = analogio.AnalogIn(BATTERY_PIN)
        except Exception as e:
            print('Battery init failed:', e)
        self._display = None
        self._petals = []
        self._px = self._py = self._pvx = self._pvy = []
        self._W = self._H = 0
        self._lbl = None
        try:
            self._setup_scene()
        except Exception as e:
            print('LCD init failed:', e)

    def _setup_scene(self):
        import displayio
        import vectorio
        import random
        import terminalio
        from adafruit_st7789 import ST7789
        from adafruit_display_text import label
        try:
            from fourwire import FourWire
        except ImportError:
            from displayio import FourWire
        self._rand = random
        displayio.release_displays()
        spi = board.SPI()
        bus = FourWire(spi, command=LCD_DC, chip_select=LCD_CS, reset=LCD_RST, baudrate=24000000)
        disp = ST7789(bus, width=320, height=170, rowstart=35, colstart=0, rotation=90)
        W, H = (320, 170)
        self._W, self._H = (W, H)