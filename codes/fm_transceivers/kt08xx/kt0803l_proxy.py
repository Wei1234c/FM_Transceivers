try:
    # from utilities.adapters.peripherals import I2C
    from ..si47xx.si4713_proxy import Si4713_proxy
except:
    # from peripherals import I2C
    from si4713_proxy import Si4713_proxy



def _value_key(dictionary):
    return {v: k for k, v in dictionary.items()}



class KT0803L_proxy(Si4713_proxy):
    I2C_ADDRESS = 0x3E

    REGISTERS_ADDRESSES = (0x00, 0x01, 0x02, 0x04, 0x0b, 0x0c, 0x0e, 0x0f, 0x10, 0x12, 0x13, 0x14, 0x15, 0x16, 0x17,
                           0x1e, 0x26, 0x27,)
    REG_ADDRESS_MAX = max(REGISTERS_ADDRESSES)

    DEFAULT_REGISTERS_VALUES = ((0x00, 0x5c),
                                (0x01, 0xc3),
                                (0x02, 0x44),
                                (0x04, 0x82),
                                (0x0b, 0x00),
                                (0x0c, 0x00),
                                (0x0e, 0x02),
                                (0x0f, 0x00),
                                (0x10, 0x00),
                                (0x12, 0x00),
                                (0x13, 0x80),
                                (0x14, 0x00),
                                (0x15, 0xe0),
                                (0x16, 0x00),
                                (0x17, 0x20),
                                (0x1e, 0x00),
                                (0x26, 0x80),
                                (0x27, 0x00))
    READ_ONLY_REGISTERS = [0x0F]

    FREQ_DEFAULT = 88.8e6
    FREQ_MIN = int(70e6)
    FREQ_MAX = int(108e6)
    FREQ_STEP = int(50e3)

    PGA_GAINS = {12: 7, 8: 6, 4: 5, 0: 0, -4: 1, -8: 2, -12: 3}
    PGA_GAINS_value_key = _value_key(PGA_GAINS)

    AUDIO_DEVIATIONS = {75e3: 0, 112.5e3: 1}
    EMPHASIS = {75: 0, 50: 1, None: 2}

    PA_GAINS = {95.5 : 0, 96.5: 1, 97.5: 2, 98.2: 3, 98.9: 4, 100: 5, 101.5: 6, 102.8: 7, 105.1: 8,
                105.6: 9, 106.2: 10, 106.5: 11, 107: 12, 107.4: 13, 107.7: 14, 108: 15}
    PA_GAINS_value_key = _value_key(PA_GAINS)


    def __init__(self, bus, i2c_address = I2C_ADDRESS,
                 freq = FREQ_DEFAULT, emphasis_us = 75, audio_deviation = 75e3,
                 input_level_dB = 0, tx_power_dBuV = 108):

        self._bus = bus
        self._i2c_address = i2c_address

        self._frequency = freq
        self._emphasis_us = emphasis_us
        self._audio_deviation = audio_deviation

        self._input_level_dB = input_level_dB
        self._tx_power_dBuV = tx_power_dBuV

        self.init()


    def init(self):
        self.write_all_registers(self.DEFAULT_REGISTERS_VALUES)
        self.set_frequency(self._frequency)
        self.set_emphasis(self._emphasis_us)
        self.set_audio_deviation(self._audio_deviation)

        self.set_line_input_level(self._input_level_dB)
        self.set_power(self._tx_power_dBuV)

        self.enable()


    def enable(self, value = True):
        self.write_register(0x0B, self._set_element_value(0x0B, 5, 1, int(bool(not value))))


    def set_emphasis(self, emphasis_us = 75):
        valids = self.EMPHASIS.keys()
        assert emphasis_us in valids, 'valid emphasis_us:{}'.format(valids)

        self.write_register(0x02, self._set_element_value(0x02, 0, 1, self.EMPHASIS[emphasis_us]))


    def set_audio_deviation(self, deviation = 75e3):
        self.write_register(0x04, self._set_element_value(0x04, 2, 2, self.AUDIO_DEVIATIONS[deviation]))


    @property
    def input_level_dB(self):
        self._input_level_dB = self.PGA_GAINS_value_key[self._get_element_value(0x01, 3, 3)]
        return self._input_level_dB


    def set_line_input_level(self, input_level_dB = 0):
        valids = self.PGA_GAINS.keys()
        assert input_level_dB in valids, 'valid dBm: {}'.format(valids)

        self._input_level_dB = input_level_dB
        self.write_register(0x01, self._set_element_value(0x01, 3, 3, self.PGA_GAINS[input_level_dB]))


    def _set_pa_gain(self, output_dBuV = 108):
        valids = self.PA_GAINS.keys()
        assert output_dBuV in valids, 'valid dBm: {}'.format(valids)

        gain = self.PA_GAINS[output_dBuV]
        self.write_register(0x02, self._set_element_value(0x02, 6, 1, gain >> 3 & 0x01))
        self.write_register(0x13, self._set_element_value(0x13, 7, 1, gain >> 2 & 0x01))
        self.write_register(0x01, self._set_element_value(0x01, 6, 2, gain >> 0 & 0x03))


    @property
    def tx_power(self):
        gain = self._get_element_value(0x02, 6, 1) << 3
        gain |= self._get_element_value(0x13, 7, 1) << 2
        gain |= self._get_element_value(0x01, 6, 2) << 0
        return self.PA_GAINS_value_key[gain]


    def set_power(self, output_dBuV = 108):
        self._set_pa_gain(output_dBuV)


    @property
    def frequency(self):
        freq = self._get_element_value(0x01, 0, 3) << 9
        freq |= self._get_element_value(0x00, 0, 8) << 1
        freq |= self._get_element_value(0x02, 7, 1) << 0

        return freq * self.FREQ_STEP


    def set_frequency(self, freq):
        if freq is not None:
            freq = round(freq / self.FREQ_STEP)

            self.write_register(0x01, self._set_element_value(0x01, 0, 3, freq >> 9 & 0x07))
            self.write_register(0x00, self._set_element_value(0x00, 0, 8, freq >> 1 & 0xFF))
            self.write_register(0x02, self._set_element_value(0x02, 7, 1, freq >> 0 & 0x01))

            self._frequency = freq * self.FREQ_STEP


    def mute(self, value = True):
        self.write_register(0x02, self._set_element_value(0x02, 3, 1, int(bool(value))))


    def mute_line_input(self, value = True):
        self.mute(value)


    def power_up(self):
        self.enable(True)


    def power_down(self):
        self.enable(False)


    @property
    def stereo(self):
        return self._get_element_value(0x04, 6, 1) == 0


    @stereo.setter
    def stereo(self, value = True):
        self.write_register(0x04, self._set_element_value(0x04, 6, 1, int(bool(not value))))


    # =================================================================

    def write_register(self, reg_address, value):
        if reg_address not in self.READ_ONLY_REGISTERS:
            return self._bus.write_addressed_byte(self._i2c_address, reg_address, value)


    def read_register(self, reg_address):
        reg_values = self._bus.read_bytes(self._i2c_address, self.REG_ADDRESS_MAX + 1)
        return reg_values[reg_address]
