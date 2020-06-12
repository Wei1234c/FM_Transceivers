try:
    # from utilities.adapters.peripherals import I2C
    from ..si47xx.si4713_proxy import Si4713_proxy
except:
    # from peripherals import I2C
    from si4713_proxy import Si4713_proxy

import time
from array import array



def _value_key(dictionary):
    return {v: k for k, v in dictionary.items()}



class RDA5820N_proxy(Si4713_proxy):
    I2C_ADDRESS = 0x11

    REGISTERS_ADDRESSES = (0, 2, 3, 4, 5, 6, 7, 10, 11, 12, 13, 14, 15, 64, 65, 103, 104)

    # DEFAULT_REGISTERS_VALUES = ((0x00, 0x5820),
    #                             (0x04, 0x4400),
    #                             (0x05, 0x8881),
    #                             (0x06, 0x0800),
    #                             (0x07, 0x5EC4),
    #                             (0x0A, 0x0400),
    #                             (0x0C, 0x5820),
    #                             (0x0D, 0x5820),
    #                             (0x0E, 0x5805),
    #                             (0x0F, 0x5805),
    #                             (0x41, 0x093F),
    #                             (0x67, 0x0E10),
    #                             (0x68, 0x0fff))

    FREQ_MIN = int(65e6)
    FREQ_MAX = int(115e6)
    FREQ_STEP = int(50e3)

    BANDS = {'US_Europe': 0, 'Japan': 1, 'World_wide': 2, 'East_Europe': 3}
    BANDS_value_key = _value_key(BANDS)
    BANDS_FREQ_MIN = {0: 87e6, 1: 76e6, 2: 76e6, 3: 65e6}

    CHANNEL_SPACING_KHZ = {100: 0, 200: 1, 50: 2, 25: 3}
    CHANNEL_SPACING_KHZ_value_key = _value_key(CHANNEL_SPACING_KHZ)

    FREQ_DEFAULT = 88.8e6

    PGA_GAINS = {1.2: 0, 0.6: 1, 0.3: 2, 0.15: 3, 0.075: 4, 0.037: 5, 0.018: 6, 0.009: 7}
    PGA_GAINS_value_key = _value_key(PGA_GAINS)

    PA_GAINS = {3: 0x3F, 0: 0x27, -1.47: 0x20, -3: 0x19, -32: 0}
    PA_GAINS_value_key = _value_key(PA_GAINS)

    WORK_MODES = {'Receiver': 0, 'Transmitter': 1, 'Audio_Amplifier': 8, 'CODEC': 12, 'ADC': 14}


    def __init__(self, bus, i2c_address = I2C_ADDRESS,
                 work_mode = 'Receiver',
                 freq = FREQ_DEFAULT, stereo = True, audio_deviation = 0xFF,
                 input_level_v = 0.6, adc_gain = 7, tx_power_dBm = 3, volume = 1):

        self._bus = bus
        self._i2c_address = i2c_address

        self._frequency = freq
        self._stereo = stereo
        self._audio_deviation = audio_deviation

        self._input_level_v = input_level_v
        self._adc_gain = adc_gain
        self._tx_power_dBm = tx_power_dBm
        self._volume = volume

        self._work_mode = work_mode
        self.init()


    @property
    def rssi(self):
        return self._get_element_value(0x0B, 9, 7)


    def init(self):
        self.boot()
        self.write_register(0x40, self._set_element_value(0x40, 0, 4, self.WORK_MODES[self._work_mode]))

        self.set_frequency(self._frequency)
        self.set_power(self._tx_power_dBm)
        self.stereo = self._stereo
        self.set_audio_deviation(self._audio_deviation)

        self.set_line_input_level(self._input_level_v)
        self.set_adc_gain(self._adc_gain)
        self.set_volume(self._volume)

        self.enable()


    def set_adc_gain(self, gain = 0):
        assert 0 <= gain <= 7, '0 ~ 7'
        self.write_register(0x68, self._set_element_value(0x68, 8, 3, gain))


    def set_audio_deviation(self, deviation = 0xFF):
        self.write_register(0x68, self._set_element_value(0x68, 0, 8, deviation))


    def power_up(self, analog_audio_inputs = True):
        self.write_register(0x02, self._set_element_value(0x02, 0, 1, 1))


    def power_down(self):
        self.write_register(0x02, self._set_element_value(0x02, 0, 1, 0))


    def _assert_reset(self):
        self.write_register(0x02, self._set_element_value(0x02, 1, 1, 1))
        time.sleep(0.1)
        self.write_register(0x02, self._set_element_value(0x02, 1, 1, 0))
        self.write_register(0x02, self._set_element_value(0x02, 14, 2, 3))


    def boot(self):
        self._assert_reset()
        self.power_up()


    def set_work_mode(self, mode = 'Receiver'):
        valids = self.WORK_MODES.keys()
        assert mode in valids, 'valid mode: {}'.format(valids)

        self._work_mode = mode
        self.init()


    @property
    def channel_spacing_KHz(self):
        return self.CHANNEL_SPACING_KHZ_value_key[self._get_element_value(0x03, 0, 2)]


    @property
    def freq_min(self):
        return self.BANDS_FREQ_MIN[self._get_element_value(0x03, 2, 2)]


    @property
    def frequency(self):
        return self.channel_spacing_KHz * 1e3 * self._get_element_value(0x0A, 0, 10) + self.freq_min


    def set_frequency(self, freq):
        spacing = self.channel_spacing_KHz * 1e3
        freq = freq // spacing * spacing
        chan = round((freq - self.freq_min) / spacing)

        value = self._set_element_value(0x03, 6, 10, chan)
        value = value & ~(1 << 4) | (1 << 4)  # enable TUNE
        self.write_register(0x03, value)
        time.sleep(0.1)
        self._frequency = freq


    def seek(self, up = True):
        if self._work_mode == 'Receiver':
            self.write_register(0x02, self._set_element_value(0x02, 9, 1, int(bool(up))))
            self.write_register(0x02, self._set_element_value(0x02, 8, 1, 1))
            time.sleep(1)
            self.write_register(0x02, self._set_element_value(0x02, 8, 1, 0))


    @property
    def tx_power(self):
        return self.PA_GAINS_value_key[self._get_element_value(0x41, 0, 6)]


    def set_power(self, output_dBm = -32):
        valids = self.PA_GAINS.keys()
        assert output_dBm in valids, 'valid dBm: {}'.format(valids)

        self._tx_power_dBm = output_dBm
        self.write_register(0x41, self._set_element_value(0x41, 0, 6, self.PA_GAINS[output_dBm]))


    @property
    def volume(self):
        self._volume = self._get_element_value(0x05, 0, 4)
        return self._volume


    def set_volume(self, volume = 0x0F):
        self._volume = volume
        self.write_register(0x05, self._set_element_value(0x05, 0, 4, volume))


    def mute(self, value = True):
        if self._work_mode in ('Receiver', 'Transmitter'):
            self.write_register(0x02, self._set_element_value(0x02, 14, 2, 0 if value else 3))


    def mute_line_input(self, value = True):
        raise NotImplementedError()


    @property
    def input_level_v(self):
        self._input_level_v = self.PGA_GAINS_value_key[self._get_element_value(0x68, 11, 3)]
        return self._input_level_v


    def set_line_input_level(self, input_level_v = 0.6):
        valids = self.PGA_GAINS.keys()
        assert input_level_v in valids, 'valid dBm: {}'.format(valids)

        self._input_level_v = input_level_v
        self.write_register(0x68, self._set_element_value(0x68, 11, 3, self.PGA_GAINS[input_level_v]))


    @property
    def stereo(self):
        mono = self._get_element_value(0x02, 13, 1)
        st = self._get_element_value(0x0A, 10, 1)

        if self._work_mode == 'Transmitter':
            return mono == 0
        if self._work_mode == 'Receiver':
            return mono == 0 and st == 1


    @stereo.setter
    def stereo(self, value = True):
        self.write_register(0x02, self._set_element_value(0x02, 13, 1, int(bool(not value))))


    # =================== data access ======================

    def read_register(self, reg_address):
        bytes_array = self._bus.read_addressed_bytes(self._i2c_address, reg_address, 2)
        return bytes_array[0] << 8 | bytes_array[1]


    def write_register(self, reg_address, value):
        return self._bus.write_addressed_bytes(self._i2c_address, reg_address,
                                               array('B', [value >> 8 & 0xFF, value & 0xFF]))
