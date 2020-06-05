try:
    from ..fm_transceiver import Device, FREQ_DEFAULT
    from fm_transceivers.rda58xx.reg_map.registers_map import _get_registers_map, Register
    import fx2lp
except:
    from fm_transceiver import Device, FREQ_DEFAULT
    from registers_map import _get_registers_map

import time



def _value_key(dictionary):
    return {v: k for k, v in dictionary.items()}



class RDA58xx(Device):
    I2C_ADDRESS = 0x11
    READ_ONLY_REGISTERS = [0]

    LNA_INPUT_PORTS = {None: 0, 'LNAN': 1, 'LNAP': 2, 'Dual_Ports': 3}
    PGA_GAINS = {1.2: 0, 0.6: 1, 0.3: 2, 0.15: 3, 0.075: 4, 0.037: 5, 0.018: 6, 0.009: 7}
    PGA_GAINS_value_key = _value_key(PGA_GAINS)
    PA_GAINS = {3: 0x3F, 0: 0x27, -3: 0x19, -32: 0}
    PA_GAINS_value_key = _value_key(PA_GAINS)

    BANDS = {'US_Europe': 0, 'Japan': 1, 'World_wide': 2, 'East_Europe': 3}
    BANDS_value_key = _value_key(BANDS)
    CHANNEL_SPACING_KHZ = {100: 0, 200: 1, 50: 2, 25: 3}
    CHANNEL_SPACING_KHZ_value_key = _value_key(CHANNEL_SPACING_KHZ)
    FREQ_REF = 32768

    GPIO_MODES = {'High_Impedance'  : 0,
                  'Stereo_Indicator': 1,
                  'STCIEN'          : 1,
                  'Reserved'        : 1,
                  'Low'             : 2, 'High': 3}

    CLK_MODES = {32768: 0, 12e6: 1, 24e6: 5, 13e6: 2, 26e6: 6, 19.2e6: 3, 38.4e6: 7}

    I2S_SAMPLING_RATES = {48e3: 8, 44.1e3: 7, 32e3: 6, 24e3: 5, 22.05e3: 4, 16e3: 3, 12e3: 2, 11.025e3: 1, 8e3: 0}

    WORK_MODES = {'FM_Receiver': 0, 'FM_Transmitter': 1, 'Audio_Amplifier': 8, 'CODEC': 12, 'ADC': 14}

    # REFCLK_PRESCALE = 1
    # FREQ_UNIT = int(10e3)
    FREQ_MIN = int(65e6)
    FREQ_MAX = int(115e6)
    FREQ_STEP = int(50e3)

    EMPHASIS = {75: 0, 50: 1, None: 2}


    # MAX_LINE_INPUT_LEVELS_mV_pk = {0: 190, 1: 301, 2: 416, 3: 636}
    # AUDIO_DYNAMIC_RANGE_CONTROL_GAIN_dB = 15
    # AUDIO_DYNAMIC_RANGE_CONTROL_ATTACK_TIMES = {0.5: 0, 1: 1, 1.5: 2, 2: 3, 2.5: 4, 3: 5, 3.5: 6, 4: 7, 4.5: 8, 5: 9}
    # AUDIO_DYNAMIC_RANGE_CONTROL_RELEASE_TIMES = {100: 0, 200: 1, 350: 2, 525: 3, 1000: 4}
    #
    # LIMITER_RELEASE_TIMES = {102.39: 5, 85.33: 6, 73.14: 7, 63.99: 8, 51.19: 10, 39.38: 13, 30.11: 17, 20.47: 25,
    #                          10.03 : 51, 8.97: 57, 7.99: 64, 7.01: 73, 6.02: 85, 5.01: 102, 4.02: 127, 3: 170, 2: 255,
    #                          1     : 510, 0.5: 1000, 0.25: 2000}
    #
    # DIGITAL_MODES = {'default': 0, 'I2S': 1, 'Left_Justified_I2S': 7, 'MSB_at_1st_DCLK': 13, 'MSB_at_2nd_DCLK': 9}
    # DIGITAL_AUDIO_SAMPLE_PRECISION = {16: 0, 20: 1, 24: 2, 8: 3}
    #
    # RDS_MIX_RATIOS = {0: 0, 12.5: 1, 25: 2, 50: 3, 75: 4, 87.5: 5, 100: 6}

    class _Base:

        def __init__(self, parent):
            self._parent = parent
            self._gain = 1


        def __del__(self):
            self._parent = None


        @property
        def volume(self):
            return self._parent._read_element_by_name('VOLUME').value


        def set_volume(self, gain = 0x0F):
            self._gain = gain
            self._parent._write_element_by_name('VOLUME', gain & 0x0F)


        def restore_volume(self):
            self.set_volume(self._gain)


        def mute(self, value = True):
            self._enable_output(not value)


        def _enable_output(self, value = True):
            self._parent._write_element_by_name('DHIZ', int(value))
            self._parent._write_element_by_name('DMUTE', int(value))


    class _IO(_Base):

        @property
        def status(self):
            return self._parent._read_register_by_address(0x0A)


        def _enable_stc_interrupt(self, value = True):
            self._parent._write_element_by_name('STCIEN', int(bool(value)))


        def _enable_rds_interrupt(self, value = True):
            self._parent._write_element_by_name('RDSIEN', int(bool(value)))


        @property
        def _seek_tune_completed(self):
            return self._parent._read_element_by_name('STC').value == 1


        def _clear_stc_interrupt(self):
            return self._parent._write_element_by_name('STC', 0)


        def _wait_for_seek_tune_complete(self, timeout_seconds):
            if not self._parent.is_virtual_device:
                start = time.time()
                while not self._seek_tune_completed:
                    if time.time() - start > timeout_seconds:
                        raise RuntimeError("Timeout.")

                self._clear_stc_interrupt()  # cannot be cleared, automatically cleared when starts tuning.


    class _ReferenceClock(_Base):

        def _set_clock_mode(self, mode = 32768):
            self._parent._write_element_by_name('CLK_MODE', self._parent.CLK_MODES[mode] & 0x07)


    class _PowerControl(_Base):

        def _soft_reset(self):
            self._parent._write_element_by_name('SOFT_RESET', 1)
            time.sleep(0.1)
            self._parent._write_element_by_name('SOFT_RESET', 0)


        def power_up(self):
            self._parent._write_element_by_name('ENABLE', 1)
            time.sleep(0.2)


        def power_down(self):
            self._parent._write_element_by_name('ENABLE', 0)


        def reset(self):
            self._soft_reset()


        def boot(self):
            self.reset()
            self.power_up()


        def reboot(self):
            self.power_down()
            self.boot()


    class _DigitalIO(_Base):

        @property
        def enabled(self):
            return self._parent._read_element_by_name('I2S_ENABLED') == 1


        def enable(self, value = True):
            #  When setting I2SEN bit high,
            #  RDA5820NS will output SCK, WS, SD signals from GPIO3, GPIO1, GPIO2
            #  as I2S master and transmitter, the sample rate is 42Kbps.
            self._parent._write_element_by_name('I2S_ENABLED', int(value))


        def _set_as_master(self, value = True):
            self._parent._write_element_by_name('I2S_MODE5', int(not value))


        def _set_ws0_as_left(self, ws0_as_left = True):
            self._parent._write_element_by_name('SW_LR', int(ws0_as_left))


        def _set_sclk_inverted(self, value = True):
            self._parent._write_element_by_name('SCLK_I_EDGE', int(value))


        def _set_master_sclk_inverted(self, value = True):
            self._parent._write_element_by_name('SCLK_O_EDGE', int(value))


        def _set_ws_inverted(self, value = True):
            self._parent._write_element_by_name('WS_I_EDGE', int(value))


        def _set_master_ws_inverted(self, value = True):
            self._parent._write_element_by_name('SW_O_EDGE', int(value))


        def _set_data_signed(self, value = True):
            self._parent._write_element_by_name('DATA_SIGNED', int(value))


        def _set_sampling_rate(self, freq = 48e3):
            self._parent._write_element_by_name('I2S_SW_CNT', self._parent.I2S_SAMPLING_RATES[freq])


        def _left_channel_delay_1T(self, value = True):
            self._parent._write_element_by_name('L_DELY', int(value))


        def _right_channel_delay_1T(self, value = True):
            self._parent._write_element_by_name('R_DELY', int(value))


    class _Tuner(_Base):

        @property
        def stereo(self):
            return self._parent._read_element_by_name('ST').value == 1


        @stereo.setter
        def stereo(self, value = True):
            self._parent._write_element_by_name('MONO', int(not value))


        def _set_emphasis(self, emphasis_us = 75):
            self._parent._write_element_by_name('DE', self._parent.EMPHASIS[emphasis_us])


        @property
        def frequency(self):
            return self.channel_spacing_KHz * 1e3 * self._parent._read_element_by_name('READCHAN').value + self.freq_min


        def set_frequency(self, freq):
            spacing = self.channel_spacing_KHz * 1e3
            freq = freq // spacing * spacing
            chan = round((freq - self.freq_min) / spacing)

            self._parent.map.elements['TUNE']['element'].value = 1
            self._parent._write_element_by_name('CHAN', chan)
            self._parent.io._wait_for_seek_tune_complete(self._parent._timeout_seconds)
            self._frequency = freq


        def _set_freq_mode(self, value = True):
            self._parent._write_element_by_name('FREQ_MODE', int(bool(value)))


        def _set_east_europe_min_freq(self, as_65MHz = True):
            self._parent._write_element_by_name('65M_50M', int(bool(as_65MHz)))


        def _set_band(self, band = 'US_Europe'):
            self._parent._write_element_by_name('BAND', self._parent.BANDS[band])


        @property
        def band(self):
            return self._parent.BANDS_value_key[self._parent._read_element_by_name('BAND').value]


        @property
        def channel_spacing_KHz(self):
            return self._parent.CHANNEL_SPACING_KHZ_value_key[self._parent._read_element_by_name('SPACE').value]


        @property
        def freq_min(self):
            return {0: 87e6, 1: 76e6, 2: 76e6, 3: 65e6}[self._parent._read_element_by_name('BAND').value]


        def _set_channel_spacing(self, KHz = 100):
            self._parent._write_element_by_name('SPACE', self._parent.CHANNEL_SPACING_KHZ[KHz])


        @property
        def _tune_completed(self):
            # self._get_interrupt_status()
            return self._stc_ready


        def _valiate_freq(self, freq):
            assert self._parent.FREQ_MIN <= freq <= self._parent.FREQ_MAX
            assert (freq // 1e3) % 50 == 0


    class _AudioAmplifier(_Base):

        def mute(self, value = True):
            pass


    class _CODEC(_Base):
        pass


    class _ADC(_Base):

        def _set_gain(self, gain = 0):
            assert 0 <= gain <= 7, '0 ~ 7'
            self._parent._write_element_by_name('FMTX_ADC_GAIN', gain)


    class _DAC(_Base):
        pass


    class _PGA(_Base):

        def __init__(self, parent, input_level_v = 0.6):
            super().__init__(parent)
            self._input_level_v = input_level_v


        @property
        def input_level_v(self):
            self._input_level_v = \
                self._parent.PGA_GAINS_value_key[self._parent._read_element_by_name('FMTX_PGA_GAIN').value]
            return self._input_level_v


        def set_input_level(self, input_level_v = 0.6):
            valids = self._parent.PGA_GAINS.keys()
            assert input_level_v in valids, 'valid dBm: {}'.format(valids)

            self._input_level_v = input_level_v
            self._parent._write_element_by_name('FMTX_PGA_GAIN', self._parent.PGA_GAINS[input_level_v])


        def restore_input_level(self):
            self.set_input_level(self._input_level_v)


    class _DSP(_Base):

        def _enable_bass_boost(self, value = True):
            self._parent._write_element_by_name('BASS', int(value))


        def _enable_afc(self, value = True):
            self._parent._write_element_by_name('AFCD', int(not value))


        def _enable_soft_mute(self, value = True):
            self._parent._write_element_by_name('SOFTMUTE_EN', int(value))


        def _enable_soft_blend(self, value = True):
            self._parent._write_element_by_name('SOFTBLEND_EN', int(bool(value)))


        def _set_soft_blend_threshold_for_noise(self, threshold):
            self._parent._write_element_by_name('TH_SOFRBLEND', threshold)


    class _Transmitter(_Base):

        def _set_rssi(self, rssi):
            self._parent._write_element_by_name('SEEKTH', rssi)


        def _set_pilot_deviation(self, deviation = 0x0E):
            self._parent._write_element_by_name('FMTX_PILOT_DEV', deviation)


        def _set_audio_deviation(self, deviation = 0x20):
            self._parent._write_element_by_name('FMTX_AUDIO_DEV', deviation)


        def _set_pa_common_voltage(self, voltage = 0):
            self._parent._write_element_by_name('TXPA_VCOM', voltage)


        def _set_pa_bias_current(self, current = 7):
            self._parent._write_element_by_name('TXPA_IBIT', current)


        def _set_pa_gain(self, output_dBm = -32):
            valids = self._parent.PA_GAINS.keys()
            assert output_dBm in valids, 'valid dBm: {}'.format(valids)

            self._parent._write_element_by_name('TXPA_GAIN', self._parent.PA_GAINS[output_dBm])


        @property
        def tx_power(self):
            return self._parent.PA_GAINS_value_key[self._parent._read_element_by_name('TXPA_GAIN').value]


        def set_power(self, output_dBm = -32):
            self._set_pa_gain(output_dBm)


    class _Receiver(_Base):

        @property
        def is_station(self):
            return self._parent._read_element_by_name('FM_TRUE').value == 1


        @property
        def fm_ready(self):
            return self._parent._read_element_by_name('FM_READY').value == 1


        @property
        def seek_successful(self):
            return self._parent._read_element_by_name('SF').value == 0


        def _select_LNA_input_port(self, port = 'LNAP'):
            self._parent._write_element_by_name('LNA_PORT_SEL', self.LNA_INPUT_PORTS[port])


        @property
        def _fm_ready(self):
            return self._parent._read_element_by_name('FM_READY').value == 1


        @property
        def _is_fm_station(self):
            return self._parent._read_element_by_name('FM_TRUE').value == 1


        @property
        def seeking_is_in_up_direction(self):
            return self._parent._read_element_by_name('SEEKUP').value == 1


        @property
        def seek_threshold(self):
            return self._parent._read_element_by_name('SEEKTH').value


        def _set_seek_threshold(self, threshold):
            self._parent._write_element_by_name('SEEKTH', threshold & 0x0F)


        def _set_seek_direction(self, up = True):
            self._parent._write_element_by_name('SEEKUP', int(up))


        def seek(self):
            self._parent._write_element_by_name('SEEK', 1)
            self._parent.io._wait_for_seek_tune_complete(self._parent._seek_timeout_seconds)
            self._parent._write_element_by_name('SEEK', 0)


        def seek_up(self):
            self._set_seek_direction(True)
            self.seek()


        def seek_down(self):
            self._set_seek_direction(False)
            self.seek()


        def _seek_mode_wrap_around(self, value = True):
            self._parent._write_element_by_name('SKMODE', int(not value))


        def _set_seek_threshold_for_old_seek_mode(self, threshold):
            self._parent._write_element_by_name('SEEK_TH_OLD', threshold)


        @property
        def rssi(self):
            return self._parent._read_element_by_name('RSSI').value


        def noise_level_dBuV(self, freq, wait_seconds = 0.2):
            self._parent.tuner.set_frequency(freq)
            time.sleep(wait_seconds)
            return self.rssi


        def scan_noise_levels(self, freq_start = None, freq_end = None, step = None, wait_seconds = 0.2):
            freq_start = self._parent.FREQ_MIN if freq_start is None else freq_start
            freq_end = self._parent.FREQ_MAX if freq_end is None else freq_end
            step = self._parent.FREQ_STEP if step is None else step

            assert step % self._parent.FREQ_STEP == 0

            _current_freq = self._parent.tuner.frequency

            freqs = range(round(freq_start // step) * step, round(freq_end // step) * step + 1, step)
            noise_levels = [(freq, self.noise_level_dBuV(freq, wait_seconds)) for freq in freqs]

            self._parent.tuner.set_frequency(_current_freq)

            return noise_levels


    class _RDS(_Base):

        def set_ps(self, station_name):
            raise NotImplementedError()


        def set_buffer(self, radio_text, use_FIFO = False, load_rds_group_buffer = True, clear_RDSINT = False):
            raise NotImplementedError()


        def set_up(self, program_id = 0x0000, station_name = None, radio_text = None, program_type_code = 4,
                   repeat_count = 3, message_count = 1, rds_mix_ratio = 50, rds_fifo_size = 0, deviation_Hz = 200,
                   enable = True):
            raise NotImplementedError()


        def _set_deviation(self, deviation = 0x10):
            self._parent._write_element_by_name('FMTX_RDS_DEV', deviation)


        @property
        def _rds_ready(self):
            return self._parent._read_element_by_name('RDSR').value == 1


        def enable(self, value = True):
            self._parent._write_element_by_name('RDS_EN', int(bool(value)))


        def _set_block(self, block = 'A', word = 0x0000):
            self._parent._write_element_by_name('RDS{}'.format(block), word)


    class _Gpio(_Base):

        def _set_gpio_mode(self, idx, mode = 'High_Impedance'):
            if not (mode == 'High_Impedance' or (mode == 'Reserved' and idx == 1)):
                self._parent.digital_io.enable(False)
            self._parent._write_element_by_name('GPIO{}'.format(idx), self.GPIO_MODES[mode] & 0x03)


        def _gpio_as_High_Impedance(self, idx):
            self._set_gpio_mode(idx = idx, mode = 'High_Impedance')


        def _gpio2_as_stcint(self):
            self._set_gpio_mode(idx = 2, mode = 'STCIEN')


        def _gpio3_as_stereo_indicator(self):
            self._set_gpio_mode(idx = 3, mode = 'Stereo_Indicator')


        def _get_pin_value(self, pin_idx):
            return self._parent._read_element_by_name('GPIO{}'.format(pin_idx)).value == 3


        def _set_pin_value(self, pin_idx, level = 0):
            self._parent._write_element_by_name('GPIO{}'.format(pin_idx), 3 if bool(level) else 2)


        def Pin(self, id, value = None, invert = False):
            assert not self._parent.digital_io.i2s_enabled, 'I2S is enabled.'
            return Pin(gpio = self, id = id, value = value, invert = invert)


    def __init__(self, bus: fx2lp.I2C, i2c_address = I2C_ADDRESS, ref_freq = FREQ_REF,
                 work_mode = 'FM_Receiver',
                 freq = FREQ_DEFAULT, emphasis_us = 75, tx_power_dBm = 3,
                 registers_map = None, registers_values = None,
                 timeout_seconds = 0.2, seek_timeout_seconds = 5):

        registers_map = _get_registers_map() if registers_map is None else registers_map

        super().__init__(freq = freq,
                         registers_map = registers_map, registers_values = registers_values)

        self._bus = bus
        self._i2c_address = i2c_address
        self._ref_freq = ref_freq

        self._work_mode = work_mode
        self._emphasis_us = emphasis_us
        self._tx_power_dBm = tx_power_dBm

        self._timeout_seconds = timeout_seconds
        self._seek_timeout_seconds = seek_timeout_seconds

        self.init()

        self.tuner.set_frequency(freq)
        self.transmitter.set_power(tx_power_dBm)


    def _build(self):
        self.adc = self._ADC(self)
        self.audio_amplifier = self._AudioAmplifier(self)
        self.codec = self._CODEC(self)
        self.dac = self._DAC(self)
        self.digital_io = self._DigitalIO(self)
        self.dsp = self._DSP(self)
        self.gpio = self._Gpio(self)
        self.io = self._IO(self)
        self.pga = self._PGA(self)
        self.line_input = self.pga
        self.power_control = self._PowerControl(self)
        self.rds = self._RDS(self)
        self.receiver = self._Receiver(self)
        self.reference_clock = self._ReferenceClock(self)
        self.transmitter = self._Transmitter(self)
        # self.line_input = self._LineInput(self)
        self.tuner = self._Tuner(self)

        self.components = {'FM_Receiver'    : self.receiver,
                           'FM_Transmitter' : self.transmitter,
                           'Audio_Amplifier': self.audio_amplifier,
                           'CODEC'          : self.codec,
                           'ADC'            : self.adc}


    def init(self):

        self._action = 'init'
        self._build()

        self.map.reset()

        self.power_control.boot()

        self.io._enable_stc_interrupt(True)

        self.set_work_mode(self._work_mode)

        self.reference_clock._set_clock_mode(mode = self._ref_freq)

        self.pga.set_input_level(input_level_v = 0.15)

        self.adc._set_gain(7)

        self.dsp._enable_afc(True)
        self.dsp._enable_bass_boost(True)
        self.dsp._enable_soft_mute(False)

        self._active_component._enable_output(True)
        self._active_component.set_volume(1)

        self.receiver._seek_mode_wrap_around(True)
        self.receiver._set_seek_direction(up = True)
        self.receiver._set_seek_threshold(8)

        self.transmitter.set_power(self._tx_power_dBm)
        self.transmitter._set_audio_deviation(0xF0)
        self.transmitter._set_pilot_deviation(0x0E)

        self.tuner._set_band('US_Europe')
        self.tuner._set_channel_spacing(100)
        self.tuner._set_emphasis(self._emphasis_us)
        self.stereo = True

        if self._frequency is not None:
            self.tuner.set_frequency(self._frequency)

        self.start()


    def reset(self):
        self.init()


    def set_work_mode(self, mode = 'FM_Receiver'):
        valids = self.WORK_MODES.keys()
        assert mode in valids, 'valid mode: {}'.format(valids)

        self.power_control.reboot()

        self._work_mode = mode
        self._write_element_by_name('WORK_MODE', self.WORK_MODES[mode])
        self._active_component = self.components[mode]

        self.pga.restore_input_level()
        self._active_component.restore_volume()


    def _set_synthesizer1_frequency(self, freq):
        self._parent._write_element_by_name('TXPA_GAIN', round(freq / self._ref_freq))


    @property
    def chip_id(self):
        return self._read_register_by_address(0).value


    @property
    def status(self):
        return self.io.status


    @property
    def frequency(self):
        return self.tuner.frequency


    @property
    def current_frequency(self):
        return self.tuner.frequency


    def set_frequency(self, freq):
        self.tuner.set_frequency(freq)


    @property
    def stereo(self):
        return self.tuner.stereo


    @stereo.setter
    def stereo(self, value = True):
        self.tuner.stereo = value


    def mute(self, value = True):
        self._active_component.mute(value)


    def enable_output(self, value = True):
        self._action = 'enable_output: {}'.format(value)
        self.mute(not value)


    def print_register(self, register_address):
        self._read_register_by_address(register_address).print()


    # =================================================================

    def _write_register(self, register, reset = False):
        if register.address not in self.READ_ONLY_REGISTERS:
            super()._write_register(register, reset = reset)
            return self._bus.write_addressed_bytes(self._i2c_address, register.address, register.bytes)


    def _read_register(self, register):
        value = self._bus.read_addressed_bytes(self._i2c_address, register.address, 2)
        register.load_value(value[0] << 8 | value[1])
        self._show_bus_data(register.bytes, address = register.address, reading = True)
        self._print_register(register)
        return register.value

    # =====================================================================



class Pin(fx2lp.Pin):

    def __init__(self, gpio: RDA58xx._Gpio, id, value = None, invert = False):
        super().__init__(gpio = gpio, id = id, mode = fx2lp.Pin.OUT, value = value, invert = invert)


    def value(self, value = None):
        if value is None:
            return self._gpio._get_pin_value(pin_idx = self._id)
        else:
            self._gpio._set_pin_value(pin_idx = self._id, level = value)


    @fx2lp.Pin.mode.setter
    def mode(self, mode):
        assert mode == self.OUT, 'Only Pin.OUT supported.'
        self._mode = mode
