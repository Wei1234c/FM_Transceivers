# try:
#     from utilities.adapters.peripherals import I2C
# except:
#     from peripherals import I2C

import time
from array import array


FREQ_UNIT = int(10e3)
FREQ_MIN = int(76e6)
FREQ_MAX = int(108e6)



class Si4713_proxy:
    I2C_ADDRESS = 0x63

    REGISTERS_ADDRESSES = [1, 257, 259, 513, 514, 8448, 8449, 8450, 8451, 8452, 8453, 8454, 8455, 8704, 8705, 8706,
                           8707, 8708, 8709, 8960, 8961, 8962, 8963, 8964, 11264, 11265, 11266, 11267, 11268, 11269,
                           11270, 11271]

    DEFAULT_REGISTERS_VALUES = ((1, 199), (257, 0), (259, 0), (513, 32768), (514, 1), (8448, 3), (8449, 6625),
                                (8450, 675), (8451, 0), (8452, 190), (8453, 0), (8454, 0), (8455, 19000), (8704, 3),
                                (8705, 65496), (8706, 2), (8707, 4), (8708, 15), (8709, 13), (8960, 7), (8961, 206),
                                (8962, 10000), (8963, 236), (8964, 5000), (11264, 0), (11265, 0), (11266, 0),
                                (11267, 0), (11268, 0), (11269, 0), (11270, 0), (11271, 0))
    FREQ_DEFAULT = 88.8e6
    POWER_DEFAULT = 115


    def __init__(self, bus, pin_reset, i2c_address = I2C_ADDRESS,
                 freq = FREQ_DEFAULT, tx_power = POWER_DEFAULT, stereo = True):

        self._bus = bus
        self._i2c_address = i2c_address
        self._pin_reset = pin_reset

        self.init()

        self.set_frequency(freq)
        self.set_power(tx_power)
        self.stereo = stereo


    def init(self):
        self.power_up()
        self.write_all_registers(self.DEFAULT_REGISTERS_VALUES)
        self.set_frequency(self.FREQ_DEFAULT)
        self.set_power(self.POWER_DEFAULT)


    def reset(self):
        self.init()


    def power_up(self, analog_audio_inputs = True):
        self._assert_reset()
        self._write_bytes(array('B', [0x01, 0x12, 0x50 if analog_audio_inputs else 0x0F]))
        time.sleep(0.2)  # need 110ms to power up.


    def power_down(self):
        self._write_bytes(array('B', [0x11]))


    def _assert_reset(self):
        self._pin_reset.high()
        time.sleep(0.01)
        self._pin_reset.low()
        time.sleep(0.01)
        self._pin_reset.high()


    @property
    def frequency(self):
        self._write_bytes(array('B', [0x33, 1]))
        bytes_array = self._read_bytes(8)

        freq = bytes_array[2] << 8 | bytes_array[3]
        self._frequency = freq * 10e3
        return self._frequency


    def set_frequency(self, freq):
        assert FREQ_MIN <= freq <= FREQ_MAX
        assert (freq // 1e3) % 50 == 0

        self._frequency = freq
        freq = round(freq // FREQ_UNIT)
        self._write_bytes(array('B', [0x30, 0x00, freq >> 8 & 0xFF, freq & 0xFF]))
        time.sleep(0.2)  # need 100ms


    @property
    def tx_power(self):
        self._write_bytes(array('B', [0x33, 1]))
        bytes_array = self._read_bytes(8)

        self._tx_power = bytes_array[5]
        return self._tx_power


    def set_power(self, power):
        assert power == 0 or (88 <= power <= 115)

        self._tx_power = round(power)
        self._write_bytes(array('B', [0x31, 0, 0, self._tx_power, 0]))
        time.sleep(0.2)  # need 100ms


    def mute(self, value = True):
        if value:
            self._write_bytes(array('B', [0x31, 0, 0, 0, 0]))
        else:
            self.set_power(self._tx_power)


    def mute_line_input(self, value = True):
        self.write_register(0x2105, 0x03 if value else 0x00)


    @property
    def stereo(self):
        return (self.read_register(0x2100) & 0x03) == 0x03


    @stereo.setter
    def stereo(self, value = True):
        current_value = self.read_register(0x2100)
        self.write_register(0x2100, current_value & ~3 | (3 if value else 0))
        time.sleep(0.01)  # status: 0x84


    def enable(self, value = True):
        self.mute(not value)


    def _read_bytes(self, n_bytes):
        return self._bus.read_bytes(self._i2c_address, n_bytes)


    def _write_bytes(self, bytes_array):
        self._bus.write_bytes(self._i2c_address, bytes_array)
        time.sleep(0.01)  # wait for CTS
        return self._read_bytes(1)[0]


    def _set_property(self, address, value):
        self._write_bytes(array('B', [0x12, 0,
                                      address >> 8 & 0xFF, address & 0xFF,
                                      value >> 8 & 0xFF, value & 0xFF]))
        time.sleep(0.01)  # set_property takes 10ms


    def _get_property(self, address):
        self._write_bytes(array('B', [0x13, 0, address >> 8 & 0xFF, address & 0xFF]))
        bytes_array = self._read_bytes(4)
        return bytes_array[2] << 8 | bytes_array[3]


    def read_register(self, reg_address):
        return self._get_property(reg_address)


    def write_register(self, reg_address, value):
        return self._set_property(reg_address, value)


    def read_all_registers(self):
        addressed_values = []
        for address in self.REGISTERS_ADDRESSES:
            try:
                value = self.read_register(address)
                addressed_values.append((address, value))
            except:
                pass
        return addressed_values


    def write_all_registers(self, addressed_values):
        for (address, value) in addressed_values:
            try:
                self.write_register(address, value)
            except:
                pass
