try:
    from ..fm_transceiver import Device, FREQ_DEFAULT
    from fm_transceivers.kt08xx.reg_map.registers_map import _get_registers_map, Register
    import fx2lp
except:
    from fm_transceiver import Device, FREQ_DEFAULT
    from registers_map import _get_registers_map



def _value_key(dictionary):
    return {v: k for k, v in dictionary.items()}



def _get_element_value(reg_address, idx_lowest_bit, n_bits):
    mask = (2 ** n_bits - 1) << idx_lowest_bit
    return (reg_address & mask) >> idx_lowest_bit



class KT08xx(Device):
    I2C_ADDRESS = 0x3E
    READ_ONLY_REGISTERS = [0x0F]

    CLK_MODES = {32768: 0, 6.5e6: 1, 7.6e6: 2, 12e6: 3, 13e6: 4, 15.2e6: 5, 19.2e6: 6, 24e6: 7, 26e6: 16}
    XTALS = {32768: 0, 7.6e6: 1}

    FREQ_REF = 32768

    FREQ_MIN = int(70e6)
    FREQ_MAX = int(108e6)
    FREQ_STEP = int(50e3)

    BANDS = {'US_Europe': 0, 'Japan': 1, 'World_wide': 2, 'East_Europe': 3}
    BANDS_value_key = _value_key(BANDS)
    BANDS_FREQ_MIN = {0: 87e6, 1: 76e6, 2: 76e6, 3: 65e6}

    AUDIO_DEVIATIONS = {75e3: 0, 112.5e3: 1}
    LNA_INPUT_PORTS = {None: 0, 'LNAN': 1, 'LNAP': 2, 'Dual_Ports': 3}
    PGA_GAINS = {12: 7, 8: 6, 4: 5, 0: 0, -4: 1, -8: 2, -12: 3}
    PGA_GAINS_value_key = _value_key(PGA_GAINS)

    BASS_LEVELS = {None: 0, 5: 1, 11: 2, 17: 3}

    EMPHASIS = {75: 0, 50: 1, None: 2}

    PA_GAINS = {95.5 : 0, 96.5: 1, 97.5: 2, 98.2: 3, 98.9: 4, 100: 5, 101.5: 6, 102.8: 7, 105.1: 8,
                105.6: 9, 106.2: 10, 106.5: 11, 107: 12, 107.4: 13, 107.7: 14, 108: 15}
    PA_GAINS_value_key = _value_key(PA_GAINS)

    SILENCE_THRESHOLDS_LOW = {0.25: 0, 0.5: 1, 1: 2, 2: 3, 4: 4, 8: 5, 16: 6, 32: 7}
    SILENCE_THRESHOLDS_HIGH = {0.5: 0, 1: 1, 2: 2, 4: 3, 8: 4, 16: 5, 32: 6, 64: 7}
    SILENCE_DURATIONS = {50: 0, 100: 1, 200: 2, 400: 3, 1000: 4, 2000: 5, 4000: 6, 8000: 7}
    SILENCE_COUNT_THRESHOLDS = {15: 0, 31: 1, 63: 2, 127: 3, 255: 4, 511: 5}
    SILENCE_LOW_COUNTS = {1: 0, 2: 1, 4: 2, 8: 3, 16: 4, 32: 5, 64: 6, 128: 7}

    ALC_DURATIONS = {0.025: 0, 0.05: 1, 0.075: 2, 0.1: 3, 0.125: 4, 0.15: 5, 0.175: 6, 0.2: 7, 50: 8, 100: 9, 150: 10,
                     200  : 11, 250: 12, 300: 13, 350: 14, 400: 15}
    ALC_COMPRESSED_GAINS = {6: 4, 3: 5, 0: 6, -3: 7, -6: 0, -9: 1, -12: 2, -15: 3}
    ALC_HOLD_TIME = {50: 0, 100: 1, 150: 2, 200: 3, 1000: 4, 5000: 5, 10000: 6, 15000: 7}
    ALC_LOW_THRESHOLD = {0.25  : 0, 0.2: 1, 0.15: 2, 0.1: 3, 0.05: 4, 0.03: 5, 0.02: 6, 0.01: 7, 0.005: 8, 0.001: 9,
                         0.0005: 10, 0.0001: 11}
    ALC_HIGH_THRESHOLD = {0.6: 0, 0.5: 1, 0.4: 2, 0.3: 3, 0.2: 4, 0.1: 5, 0.05: 6, 0.01: 7}


    class _Base:

        def __init__(self, parent):
            self._parent = parent


    class _IO(_Base):

        @property
        def status(self):
            raise NotImplementedError()


    class _ReferenceClock(_Base):

        def _disable_crystal_oscillator(self, value = True):
            self._parent._write_element_by_name('XTALD', int(bool(value)))


        def _enable_multiple_reference_clock_selection(self, value = True):
            self._parent._write_element_by_name('DCLK', int(bool(value)))


        def _set_clock_mode(self, mode = 32768):
            self._parent._write_element_by_name('REF_CLK', self._parent.CLK_MODES[mode])


        def _select_xtal(self, mode = 32768):
            self._parent._write_element_by_name('XTAL_SEL', self._parent.XTALS[mode])


    class _Control(_Base):

        @property
        def power_ok(self):
            return self._parent._read_element_by_name('PW_OK').value == 1


        def power_up(self):
            self._parent._write_element_by_name('PDPA', 0)


        def power_down(self):
            self._parent._write_element_by_name('PDPA', 1)


        def _enable_auto_power_down(self, value = True):
            self._parent._write_element_by_name('AUTO_PADN', int(bool(value)))


        def standby(self, value = True):
            self._parent._write_element_by_name('Standby', int(bool(value)))


    class _SilenceDetector(_Base):

        def setup(self,
                  low_threshold_mV = 0.25,
                  high_threshold_mV = 0.25,
                  duration_ms = 50,
                  threshold_count = 15,
                  low_counter = 1,
                  enable = True):

            if enable:
                self._set_low_threshold(threshold_mV = low_threshold_mV)
                self._set_high_threshold(threshold_mV = high_threshold_mV)
                self._set_duration(duration_ms = duration_ms)
                self._set_counter_threshold(threshold_count = threshold_count)
                self._set_low_counter(count = low_counter)

            self._enable(enable)


        @property
        def silence_detected(self):
            return self._parent._read_element_by_name('SLNCID').value == 1


        def _enable(self, value = True):
            self._parent._write_element_by_name('SLNCDIS', int(bool(not value)))


        def _set_low_threshold(self, threshold_mV = 0.25):
            valids = self._parent.SILENCE_THRESHOLDS_LOW.keys()
            assert threshold_mV in valids, 'valid threshold_mV: {}'.format(valids)

            self._parent._write_element_by_name('SLNCTHL', self._parent.SILENCE_THRESHOLDS_LOW[threshold_mV])


        def _set_high_threshold(self, threshold_mV = 0.5):
            valids = self._parent.SILENCE_THRESHOLDS_HIGH.keys()
            assert threshold_mV in valids, 'valid threshold_mV: {}'.format(valids)

            self._parent._write_element_by_name('SLNCTHH', self._parent.SILENCE_THRESHOLDS_HIGH[threshold_mV])


        def _set_duration(self, duration_ms = 50, long_duration = False):
            valids = self._parent.SILENCE_DURATIONS.keys()
            assert duration_ms in valids, 'valid duration_ms: {}'.format(valids)

            self._parent._write_element_by_name('SLNCTIME_2_0', self._parent.SILENCE_DURATIONS[duration_ms])
            self._parent._write_element_by_name('SLNCTIME_3', int(bool(long_duration)))


        def _set_counter_threshold(self, threshold_count = 15):
            valids = self._parent.SILENCE_COUNT_THRESHOLDS.keys()
            assert threshold_count in valids, 'valid threshold_count: {}'.format(valids)

            self._parent._write_element_by_name('SLNCCNTHIGH', self._parent.SILENCE_COUNT_THRESHOLDS[threshold_count])


        def _set_low_counter(self, count = 1):
            valids = self._parent.SILENCE_LOW_COUNTS.keys()
            assert count in valids, 'valid count: {}'.format(valids)

            self._parent._write_element_by_name('SLNCCNTLOW', self._parent.SILENCE_LOW_COUNTS[count])


    class _AutomaticLevelControl(_Base):

        # KT0803 vs. Si4713
        # Decay time = Attack Time,
        # ALCHIGHTH = ???
        # ALCLOWTH = threshold
        # hold time + attack time = release time

        def setup(self,
                  decay_duration_ms = 0.025,
                  hold_duration_ms = 1000,
                  attack_duration_ms = 0.025,
                  low_threshold = 0.25,
                  high_threshold = 0.6,
                  gain_dB = -3,
                  enable = True):
            if enable:
                self._set_decay_time(duration_ms = decay_duration_ms)
                self._set_attack_time(duration_ms = attack_duration_ms)
                self._set_hold_time(duration_ms = hold_duration_ms)
                self._set_low_threshold(threshold = low_threshold)
                self._set_high_threshold(threshold = high_threshold)
                self._set_gain(gain_dB = gain_dB)

            self._enable(enable)


        def _enable(self, value = True):
            self._parent._write_element_by_name('ALC_EN', int(bool(value)))


        def _set_decay_time(self, duration_ms = 0.025):
            valids = self._parent.ALC_DURATIONS.keys()
            assert duration_ms in valids, 'valid duration_ms: {}'.format(valids)

            self._parent._write_element_by_name('ALC_DECAY_TIME', self._parent.ALC_DURATIONS[duration_ms])


        def _set_attack_time(self, duration_ms = 0.025):
            valids = self._parent.ALC_DURATIONS.keys()
            assert duration_ms in valids, 'valid duration_ms: {}'.format(valids)

            self._parent._write_element_by_name('ALC_ATTACK_TIME', self._parent.ALC_DURATIONS[duration_ms])


        def _set_hold_time(self, duration_ms = 5):
            valids = self._parent.ALC_HOLD_TIME.keys()
            assert duration_ms in valids, 'valid duration_ms: {}'.format(valids)

            self._parent._write_element_by_name('ALCHOLD', self._parent.ALC_HOLD_TIME[duration_ms])


        def _set_low_threshold(self, threshold = 0.25):
            valids = self._parent.ALC_LOW_THRESHOLD.keys()
            assert threshold in valids, 'valid threshold: {}'.format(valids)

            self._parent._write_element_by_name('ALCLOWTH', self._parent.ALC_LOW_THRESHOLD[threshold])


        def _set_high_threshold(self, threshold = 0.6):
            valids = self._parent.ALC_HIGH_THRESHOLD.keys()
            assert threshold in valids, 'valid threshold: {}'.format(valids)

            self._parent._write_element_by_name('ALCHIGHTH', self._parent.ALC_HIGH_THRESHOLD[threshold])


        def _set_gain(self, gain_dB = -3):
            valids = self._parent.ALC_COMPRESSED_GAINS.keys()
            assert gain_dB in valids, 'valid gain_dB: {}'.format(valids)

            self._parent._write_element_by_name('ALCCMPGAIN', self._parent.ALC_COMPRESSED_GAINS[gain_dB])


    class _Tuner(_Base):

        @property
        def stereo(self):
            return self._parent._read_element_by_name('MONO').value == 0


        @stereo.setter
        def stereo(self, value = True):
            self._parent._write_element_by_name('MONO', int(not value))


        def _set_emphasis(self, emphasis_us = 75):
            valids = self._parent.EMPHASIS.keys()
            assert emphasis_us in valids, 'valid emphasis_us:{}'.format(valids)

            self._parent._write_element_by_name('PHTCNST', self._parent.EMPHASIS[emphasis_us])


        @property
        def frequency(self):
            freq = self._parent._read_element_by_name('CHSEL_11_9').value << 9
            freq |= (self._parent._read_element_by_name('CHSEL_8_1').value << 1)
            freq |= self._parent._read_element_by_name('CHSEL_0').value

            return freq * self._parent.FREQ_STEP


        def set_frequency(self, freq):
            if freq is not None:
                self._valiate_freq(freq)
                freq = round(freq / self._parent.FREQ_STEP)

                self._parent._write_element_by_name('CHSEL_11_9', _get_element_value(freq, 9, 3))
                self._parent._write_element_by_name('CHSEL_8_1', _get_element_value(freq, 1, 8))
                self._parent._write_element_by_name('CHSEL_0', _get_element_value(freq, 0, 1))

                self._frequency = freq * self._parent.FREQ_STEP


        def _set_channel_switching_mode(self, pa_off = True):
            self._parent._write_element_by_name('SW_MOD', int(bool(pa_off)))


        def _valiate_freq(self, freq):
            assert self._parent.FREQ_MIN <= freq <= self._parent.FREQ_MAX
            assert (freq // 1e3) % 50 == 0


    class _PGA(_Base):

        def _set_pga_mode(self, as_1dB_step = True):
            self._parent._write_element_by_name('PGAMOD', int(bool(as_1dB_step)))


        @property
        def input_level_dB(self):
            self._input_level_dB = \
                self._parent.PGA_GAINS_value_key[self._parent._read_element_by_name('PGA').value]
            return self._input_level_dB


        def set_input_level(self, input_level_dB = 0):
            valids = self._parent.PGA_GAINS.keys()
            assert input_level_dB in valids, 'valid dBm: {}'.format(valids)

            self._input_level_dB = input_level_dB
            self._parent._write_element_by_name('PGA', self._parent.PGA_GAINS[input_level_dB])


    class _DSP(_Base):

        def _set_bass_boost_level(self, dB = None):
            self._parent._write_element_by_name('BASS', self._parent.BASS_LEVELS[dB])


        def _enable_audio_frequency_response_enhancement(self, value = True):
            self._parent._write_element_by_name('AU_ENHANCE', int(bool(value)))


    class _Transmitter(_Base):

        def mute(self, value = True):
            self._parent._write_element_by_name('MUTE', int(bool(value)))


        def _set_audio_deviation(self, deviation = 75e3):
            self._parent._write_element_by_name('FDEV', self._parent.AUDIO_DEVIATIONS[deviation])


        def _enable_pa_bias(self, value = True):
            self._parent._write_element_by_name('PA_BIAS', int(bool(value)))


        def _set_pa_gain(self, output_dBuV = 108):
            valids = self._parent.PA_GAINS.keys()
            assert output_dBuV in valids, 'valid dBm: {}'.format(valids)

            gain = self._parent.PA_GAINS[output_dBuV]
            self._parent._write_element_by_name('RFGAIN_3', _get_element_value(gain, 3, 1))
            self._parent._write_element_by_name('RFGAIN_2', _get_element_value(gain, 2, 1))
            self._parent._write_element_by_name('RFGAIN_1_0', _get_element_value(gain, 0, 2))


        def _set_pilot_tone_amplitude_high(self, value = True):
            self._parent._write_element_by_name('PLTADJ', int(bool(value)))


        @property
        def tx_power(self):
            gain = self._parent._read_element_by_name('RFGAIN_3').value << 3
            gain |= self._parent._read_element_by_name('RFGAIN_2').value << 2
            gain |= self._parent._read_element_by_name('RFGAIN_1_0').value
            return self._parent.PA_GAINS_value_key[gain]


        def set_power(self, output_dBuV = 108):
            self._set_pa_gain(output_dBuV)


    def __init__(self, bus, i2c_address = I2C_ADDRESS, ref_freq = FREQ_REF,
                 freq = FREQ_DEFAULT, emphasis_us = 75, audio_deviation = 112.5e3,
                 input_level_dB = 12, tx_power_dBuV = 108, bass_boost_level_dB = 11,
                 registers_map = None, registers_values = None):

        registers_map = _get_registers_map() if registers_map is None else registers_map

        super().__init__(freq = freq,
                         registers_map = registers_map, registers_values = registers_values)

        self._reg_address_max = max([reg.address for reg in self.map._registers])

        self._bus = bus
        self._i2c_address = i2c_address
        self._ref_freq = ref_freq

        self._emphasis_us = emphasis_us
        self._audio_deviation = audio_deviation

        self._input_level_dB = input_level_dB
        self._tx_power_dBuV = tx_power_dBuV
        self._bass_boost_level_dB = bass_boost_level_dB

        self.init()


    def _build(self):
        self.control = self._Control(self)
        self.alc = self._AutomaticLevelControl(self)
        self.silence_detector = self._SilenceDetector(self)
        self.dsp = self._DSP(self)
        self.io = self._IO(self)
        self.pga = self._PGA(self)
        self.line_input = self.pga
        self.reference_clock = self._ReferenceClock(self)
        self.transmitter = self._Transmitter(self)
        self.tuner = self._Tuner(self)


    def init(self):

        self._action = 'init'
        self.map.reset()

        self._build()

        self.control.power_up()
        self.control._enable_auto_power_down(False)

        self.reference_clock._set_clock_mode(mode = self._ref_freq)
        self.reference_clock._select_xtal(mode = self._ref_freq)
        self.reference_clock._enable_multiple_reference_clock_selection(False)
        self.reference_clock._disable_crystal_oscillator(False)

        self.pga.set_input_level(input_level_dB = self._input_level_dB)
        self.pga._set_pga_mode(as_1dB_step = False)

        self.alc.setup(decay_duration_ms = 0.025, hold_duration_ms = 1000, attack_duration_ms = 0.025,
                       low_threshold = 0.25, high_threshold = 0.6, gain_dB = -3)

        self.silence_detector.setup(low_threshold_mV = 0.25, high_threshold_mV = 0.5,
                                    duration_ms = 50, threshold_count = 15, low_counter = 1)

        self.dsp._set_bass_boost_level(dB = self._bass_boost_level_dB)
        self.dsp._enable_audio_frequency_response_enhancement(True)

        self.transmitter._enable_pa_bias(True)
        self.transmitter._set_audio_deviation(self._audio_deviation)
        self.transmitter._set_pilot_tone_amplitude_high(True)
        self.transmitter.set_power(self._tx_power_dBuV)
        self.transmitter.mute(False)

        self.tuner._set_channel_switching_mode(pa_off = False)
        self.tuner._set_emphasis(self._emphasis_us)
        self.stereo = True

        if self._frequency is not None:
            self.tuner.set_frequency(self._frequency)

        self.start()


    def reset(self):
        self.init()


    @property
    def status(self):
        return self.io.status


    @property
    def frequency(self):
        return self.tuner.frequency


    @property
    def current_frequency(self):
        return self.frequency


    def set_frequency(self, freq):
        self.tuner.set_frequency(freq)


    def set_power(self, output_dBuV = 108):
        self.transmitter.set_power(output_dBuV)


    @property
    def stereo(self):
        return self.tuner.stereo


    @stereo.setter
    def stereo(self, value = True):
        self.tuner.stereo = value


    def mute(self, value = True):
        self.transmitter.mute(value)


    def enable_output(self, value = True):
        self._action = 'enable_output: {}'.format(value)
        if value:
            self.control.power_up()
        else:
            self.control.power_down()


    def print_register(self, register_address):
        self._read_register_by_address(register_address).print()


    # =================================================================

    def _write_register(self, register, reset = False):
        if register.address not in self.READ_ONLY_REGISTERS:
            super()._write_register(register, reset = reset)
            return self._bus.write_addressed_byte(self._i2c_address, register.address, register.value)


    def _read_register(self, register):
        reg_values = self._bus.read_bytes(self._i2c_address, self._reg_address_max + 1)
        value = reg_values[register.address]
        register.load_value(value)
        self._show_bus_data(register.bytes, address = register.address, reading = True)
        self._print_register(register)
        return register.value
