try:
    from ..fm_transceiver import Device, FREQ_DEFAULT
    from fm_transceivers.rda58xx.reg_map.registers_map import _get_registers_map, Register
    import fx2lp
except:
    from fm_transceiver import Device, FREQ_DEFAULT
    from registers_map import _get_registers_map

import struct
import time



def _value_key(dictionary):
    return {v: k for k, v in dictionary.items()}



class RDA58xx(Device):
    I2C_ADDRESS = 0x11
    READ_ONLY_REGISTERS = [0]

    LNA_INPUT_PORTS = {None: 0, 'LNAN': 1, 'LNAP': 2, 'Dual_Ports': 3}
    PGA_GAINS = {1.2: 0, 0.6: 1, 0.3: 2, 0.15: 3, 0.075: 4, 0.037: 5, 0.018: 6, 0.009: 7}
    PA_GAINS = {3: 0x3F, 0: 0x27, -3: 0x19, -32: 0}

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


    #
    PRE_EMPHASIS = {75: 0, 50: 1, None: 2}
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


        def __del__(self):
            self._parent = None


    class _IO(_Base):

        def __init__(self, parent):
            super().__init__(parent)
            self._status = status


        @property
        def status(self):
            self._status.load_value(self._read_byte())
            return self._status


        @property
        def _is_clear_to_send(self):
            return self.status.elements['CTS'].value == 1


        def _get_interrupt_status(self):
            self._send_command(self._parent.commands['GET_INT_STATUS'])
            return self.status


        def _set_property(self, property: Register):
            command = self._parent.commands['SET_PROPERTY']
            command.arguments.elements['PROPH']['element'].value = property.address >> 8 & 0xFF
            command.arguments.elements['PROPL']['element'].value = property.address & 0xFF
            command.arguments.elements['PROPDH']['element'].value = property.value >> 8 & 0xFF
            command.arguments.elements['PROPDL']['element'].value = property.value & 0xFF
            result = self._send_command(command)
            time.sleep(0.01)  # set_property takes 10ms
            return result


        def _get_property(self, property: Register):
            command = self._parent.commands['GET_PROPERTY']
            command.arguments.elements['PROPH']['element'].value = property.address >> 8 & 0xFF
            command.arguments.elements['PROPL']['element'].value = property.address & 0xFF
            self._send_command(command)

            value = command.responses.value_of_element('PROPDH') << 8 | command.responses.value_of_element('PROPDL')
            property.load_value(value)
            return property


        def _write_register(self, register, reset = False):
            if register.address not in self._parent.READ_ONLY_REGISTERS:
                Device._write_register(self._parent, register, reset = reset)
                return self._set_property(register)


        def _read_register(self, register):
            property = self._get_property(register)
            self._parent._show_bus_data(property.bytes, address = property.address, reading = True)
            self._parent._print_register(property)
            return property.value


        def _write_register_by_name(self, register_name, value):
            return self._parent._write_register_by_name(register_name, value)


        def _read_element_by_name(self, element_name):
            return self._parent._read_element_by_name(element_name)


        def _write_element_by_name(self, element_name, value):
            return self._parent._write_element_by_name(element_name, value)


        def _write_bytes(self, bytes_array):
            return self._parent._bus.write_bytes(self._parent._i2c_address, bytes_array)


        def _read_bytes(self, n_bytes):
            return self._parent._bus.read_bytes(self._parent._i2c_address, n_bytes)


        def _read_byte(self):
            return self._parent._bus.read_bytes(self._parent._i2c_address, n_bytes = 1)[0]


        def _send_command(self, command):
            bytes_array = array('B', [command.code] + [arg.value for arg in command.arguments._registers])
            self._write_bytes(bytes_array)
            self._wait_for_CTS()
            self._read_n_load_responses(command)
            return command.responses


        def _read_n_load_responses(self, command):
            n_responses = len(command.responses._registers)
            if n_responses > 0:
                bytes_responses = self._read_bytes(n_responses + 1)
                for r, v in zip(command.responses._registers, bytes_responses[1:]):
                    r.load_value(v)


        def _wait_for_CTS(self):
            if not self._parent.is_virtual_device:
                start = time.time()
                while not self._is_clear_to_send:
                    if time.time() - start > self._parent._timeout_seconds:
                        raise RuntimeError("Timeout.")


    class _ReferenceClock(_Base):

        def _set_reference_clock(self, freq_ref, prescaler = 1):
            self._parent.io._write_register_by_name('REFCLK_FREQ', freq_ref)
            self._parent.io._write_element_by_name('REFCLKP', prescaler)


    class _PowerControl(_Base):

        def _assert_reset(self):
            if not self._parent.is_virtual_device:
                self._parent._pin_reset.high()
                time.sleep(0.01)
                self._parent._pin_reset.low()
                time.sleep(0.01)
                self._parent._pin_reset.high()


        def power_up(self,
                     cts_interrupt_enabled = False,
                     gpo2_output_enabled = False,
                     patch_enabled = False,
                     crystal_oscillator_enabled = True,
                     transmit = True,
                     analog_audio_inputs = True):
            command = self._parent.commands['POWER_UP']
            command.arguments.elements['CTSIEN']['element'].value = int(cts_interrupt_enabled)
            command.arguments.elements['GPO2OEN']['element'].value = int(gpo2_output_enabled)
            command.arguments.elements['PATCH']['element'].value = int(patch_enabled)
            command.arguments.elements['XOSCEN']['element'].value = int(crystal_oscillator_enabled)
            command.arguments.elements['FUNC']['element'].value = 2 if transmit else 15
            command.arguments.elements['OPMODE']['element'].value = 0x50 if analog_audio_inputs else 0x0F
            self._parent.io._send_command(command)

            time.sleep(0.2)  # need 110ms to power up.


        def power_down(self):
            self._parent.io._send_command(self._parent.commands['POWER_DOWN'])


    class _LineInput(_Base):

        @property
        def input_level(self):
            return struct.unpack("b", self._parent.asq.asq_status.value_of_element('INLEVEL').to_bytes(1, 'big'))[0]


        @property
        def _input_audio_level_high_threshold_exceeded(self):
            return self._parent.asq.asq_status.value_of_element('IALH') == 1


        @property
        def _input_audio_level_low_threshold_exceeded(self):
            return self._parent.asq.asq_status.value_of_element('IALL') == 1


        def mute(self, value = True):
            self._parent.io._write_register_by_name('TX_LINE_INPUT_MUTE', 0x03 if value else 0x00)


        def _set_input_level(self, attenuation_level = 3, line_level = None):
            line_level = self._parent.MAX_LINE_INPUT_LEVELS_mV_pk[
                attenuation_level] if line_level is None else line_level
            self._parent.io._write_element_by_name('LIATTEN', attenuation_level)
            self._parent.io._write_element_by_name('LILEVEL', line_level)


    class _DigitalInput(_Base):

        def power_up_digital_mode(self, *args, **kwargs):
            self._parent.power_control.power_up(analog_audio_inputs = False, *args, **kwargs)


        def _set_digital_input(self, digital_mode = 'I2S', sample_on_dclk_falling_edge = False,
                               digital_audio_sample_bits = 16, sample_rate = 48000, mono_audio_mode = False,
                               enable = True):
            if enable:
                property = self._parent.properties['DIGITAL_INPUT_FORMAT']
                property.elements['IFALL'].value = int(sample_on_dclk_falling_edge)
                property.elements['IMODE'].value = self._parent.DIGITAL_MODES[digital_mode]
                property.elements['IMONO'].value = int(mono_audio_mode)
                property.elements['ISIZE'].value = self._parent.DIGITAL_AUDIO_SAMPLE_PRECISION[
                    digital_audio_sample_bits]
                self._parent.io._set_property(property)

            assert sample_rate == 0 or 32000 <= sample_rate <= 48000
            self._parent.io._write_register_by_name('DIGITAL_INPUT_SAMPLE_RATE', sample_rate if enable else 0)


    class _Compressor(_Base):

        def _set_audio_dynamic_range_control(self, threshold_dBFS = -40., gain_dB = 15,
                                             attack_time_ms = 0.5, release_time_ms = 1000,
                                             enable = True):
            # Enable the audio dynamic range control
            # In general the greater the sum of threshold and gain, the greater the perceived audio volume. The following
            # examples demonstrate minimal and aggressive compression schemes.
            # When using the audio dynamic range control, care must be taken to configure the device such that
            # the sum of the threshold and gain is zero, or less, as not to distort or overmodulate.
            # In practice, the sum of the threshold and gain will be less than zero to minimize the possibility for distortion.

            if enable:
                assert -40 <= threshold_dBFS <= 0
                assert threshold_dBFS + gain_dB <= 0

                self._parent.io._write_register_by_name('TX_ACOMP_THRESHOLD', 2 ** 16 + round(threshold_dBFS))
                self._parent.io._write_register_by_name('TX_ACOMP_GAIN', gain_dB)
                self._parent.io._write_register_by_name('TX_ACOMP_ATTACK_TIME',
                                                        self._parent.AUDIO_DYNAMIC_RANGE_CONTROL_ATTACK_TIMES[
                                                            attack_time_ms])
                self._parent.io._write_register_by_name('TX_ACOMP_RELEASE_TIME',
                                                        self._parent.AUDIO_DYNAMIC_RANGE_CONTROL_RELEASE_TIMES[
                                                            release_time_ms])

            self._parent.io._write_element_by_name('ACEN', int(enable))


    class _AudioSignalQualityControl(_Base):

        @property
        def _asq_ready(self):
            raise NotImplementedError()


        @property
        def asq_status(self):
            raise NotImplementedError()


        def _clear_ASQINT(self):
            raise NotImplementedError()


        def _set_limiter(self, level_low_dB = -50, level_high_dB = -20,
                         duration_low_ms = 0, duration_high_ms = 0,
                         release_time_ms = 5.01,
                         overmodulation_detection_enable = True,
                         input_audio_level_detection_high_threshold_enable = True,
                         input_audio_level_detection_low_threshold_enable = True,
                         enable = True):
            raise NotImplementedError()


    class _Tuner(_Base):

        @property
        def _stc_ready(self):
            raise NotImplementedError()


        @property
        def _tune_completed(self):
            raise NotImplementedError()


        def _clear_STCINT(self):
            raise NotImplementedError()


        @property
        def _tune_status(self):
            raise NotImplementedError()


        def _valiate_freq(self, freq):
            assert self._parent.FREQ_MIN <= freq <= self._parent.FREQ_MAX
            assert (freq // 1e3) % 50 == 0


        @property
        def frequency(self):
            raise NotImplementedError()


        def set_frequency(self, freq):
            raise NotImplementedError()


        def _valiate_capacitance(self, capacitance):
            raise NotImplementedError()


        @property
        def capacitance(self):
            raise NotImplementedError()


        def _set_capacitance(self, capacitance = 0):
            raise NotImplementedError()


        def _wait_for_tune_completed(self):
            raise NotImplementedError()


    class _Transmitter(_Base):

        @property
        def _output_signal_above_requested_modulation_level(self):
            raise NotImplementedError()


        @property
        def tx_power(self):
            raise NotImplementedError()


        def _valiate_power(self, power):
            raise NotImplementedError()


        def set_power(self, power):
            raise NotImplementedError()


        def mute(self, value = True):
            raise NotImplementedError()


        @property
        def stereo(self):
            raise NotImplementedError()


        @stereo.setter
        def stereo(self, value = True):
            raise NotImplementedError()


        def _set_audio_frequency_deviation(self, deviation_Hz = 68.25e3):
            raise NotImplementedError()


        def _set_pre_emphasis(self, pre_emphasis_us = 75):
            raise NotImplementedError()


        def _set_pilot(self, freq_Hz = 19e3, deviation_Hz = 6.75e3):
            raise NotImplementedError()


    class _Receiver(_Base):

        def noise_level_dBuV(self, freq, capacitance = 0):
            raise NotImplementedError()


        def scan_noise_levels(self, freq_start = None, freq_end = None, step = None):
            freq_start = self._parent.FREQ_MIN if freq_start is None else freq_start
            freq_end = self._parent.FREQ_MAX if freq_end is None else freq_end
            step = self._parent.FREQ_STEP if step is None else step

            assert step % self._parent.FREQ_STEP == 0

            # push
            _current_freq = self._parent.tuner.frequency
            _current_power = self._parent.transmitter.tx_power

            freqs = range(round(freq_start // step) * step, round(freq_end // step) * step + 1, step)
            noise_levels = [(freq, self.noise_level_dBuV(freq)) for freq in freqs]

            # pop
            self._parent.tuner.set_frequency(_current_freq)
            self._parent.transmitter.set_power(_current_power)

            return noise_levels


    class _RDS(_Base):

        @property
        def _rds_ready(self):
            raise NotImplementedError()


        def set_rds_ps(self, station_name):
            raise NotImplementedError()


        def set_rds_buffer(self, radio_text, use_FIFO = False, load_rds_group_buffer = True, clear_RDSINT = False):
            raise NotImplementedError()


        def set_rds(self, program_id = 0x0000, station_name = None, radio_text = None, program_type_code = 4,
                    repeat_count = 3, message_count = 1, rds_mix_ratio = 50, rds_fifo_size = 0, deviation_Hz = 200,
                    enable = True):
            raise NotImplementedError()


    class _Gpio(_Base):

        def _set_pin_direction(self, idx, as_output = False):
            raise NotImplementedError()


        def _set_pin_value(self, idx, as_high = False):
            raise NotImplementedError()


        def Pin(self, id, value = None, invert = False):
            return Pin(gpio = self, id = id, value = value, invert = invert)


    def _build(self):
        self.io = self._IO(self)
        self.reference_clock = self._ReferenceClock(self)
        self.power_control = self._PowerControl(self)
        self.line_input = self._LineInput(self)
        self.digital_input = self._DigitalInput(self)
        self.compressor = self._Compressor(self)
        self.asq = self._AudioSignalQualityControl(self)
        self.tuner = self._Tuner(self)
        self.transmitter = self._Transmitter(self)
        self.receiver = self._Receiver(self)
        self.rds = self._RDS(self)
        self.gpio = self._Gpio(self)


    def __init__(self, bus: fx2lp.I2C, i2c_address = I2C_ADDRESS, ref_freq = FREQ_REF,
                 freq = FREQ_DEFAULT, tx_power = 115, capacitance = 0,
                 pre_emphasis_us = 75,
                 registers_map = None, registers_values = None,
                 timeout_seconds = 0.2, seek_timeout_seconds = 5):

        registers_map = _get_registers_map() if registers_map is None else registers_map

        super().__init__(freq = freq,
                         registers_map = registers_map, registers_values = registers_values)

        self._bus = bus
        self._i2c_address = i2c_address
        self._ref_freq = ref_freq

        self._tx_power = tx_power
        self._capacitance = capacitance  # 0 as auto

        self._pre_emphasis_us = pre_emphasis_us
        self._timeout_seconds = timeout_seconds
        self._seek_timeout_seconds = seek_timeout_seconds
        self.init()


    def init(self):

        self._action = 'init'

        self._build()

        self._action = 'init'
        self.power_control._assert_reset()
        self.map.reset()

        # Powerup in Analog Mode
        self.power_control.power_up()

        # Configuration
        self.io._write_register_by_name('GPO_IEN', 0x00C7)  # sources for the GPO2/INT interrupt pin
        self.reference_clock._set_reference_clock(freq_ref = self.FREQ_REF, prescaler = self.REFCLK_PRESCALE)
        self.line_input.mute(False)
        self.transmitter._set_pre_emphasis(pre_emphasis_us = self._pre_emphasis_us)
        self.transmitter._set_audio_frequency_deviation(deviation_Hz = 66.25e3)

        # Tuning
        if self._frequency is not None:
            self.tuner.set_frequency(self._frequency)
        self.transmitter.set_power(self._tx_power)
        self.tuner._set_capacitance(self._capacitance)

        # Stereo & Pilot
        self.transmitter._set_pilot(freq_Hz = 19e3, deviation_Hz = 6.75e3)
        self.transmitter.stereo = True

        # Audio Dynamic Range Control (Compressor) and Limiter
        self.compressor._set_audio_dynamic_range_control(threshold_dBFS = -40.,
                                                         gain_dB = self.AUDIO_DYNAMIC_RANGE_CONTROL_GAIN_dB,
                                                         attack_time_ms = 1.5, release_time_ms = 1000)
        # Audio Signal Quality
        self.line_input._set_input_level(attenuation_level = 0)
        self.asq._set_limiter(level_low_dB = -50, level_high_dB = -20, duration_low_ms = 10000, duration_high_ms = 5000,
                              release_time_ms = 39.38)

        self.start()


    def reset(self):
        self.init()


    def _select_LNA_input_port(self, port = 'LNAP'):
        self._write_element_by_name('LNA_PORT_SEL', self.LNA_INPUT_PORTS[port])


    def _set_pga_gain(self, input_level_v = 0.6):
        self._write_element_by_name('FMTX_PGA_GAIN', self.PGA_GAINS[input_level_v])


    def _set_pa_gain(self, output_dBm = -32):
        self._write_element_by_name('TXPA_GAIN', self.PA_GAINS[output_dBm])


    @property
    def band(self):
        return self.BANDS_value_key[self._read_element_by_name('BAND').value]


    def _set_band(self, band = 'US_Europe'):
        self._write_element_by_name('BAND', self.BANDS[band])


    @property
    def channel_spacing_KHz(self):
        return self.CHANNEL_SPACING_KHZ_value_key[self._read_element_by_name('SPACE').value]


    @property
    def freq_min(self):
        return {0: 87e6, 1: 76e6, 2: 76e6, 3: 65e6}[self._read_element_by_name('BAND').value]


    def _set_channel_spacing(self, KHz = 100):
        self._write_element_by_name('SPACE', self.CHANNEL_SPACING_KHZ[KHz])


    @property
    def frequency(self):
        return self.channel_spacing_KHz * 1e3 * self._read_element_by_name('READCHAN').value + self.freq_min


    def set_frequency(self, freq):
        spacing = self.channel_spacing_KHz * 1e3
        freq = freq // spacing * spacing
        chan = round((freq - self.freq_min) / spacing)

        self.map.elements['TUNE']['element'].value = 1
        self._write_element_by_name('CHAN', chan)
        self._wait_for_tune_seek_complete(self._timeout_seconds)
        self._frequency = freq


    def _set_freq_mode(self, value = True):
        self._write_element_by_name('FREQ_MODE', int(bool(value)))


    @property
    def rssi(self):
        time.sleep(0.3)  # if following set_frequency, delay 0.x seconds
        return self._read_element_by_name('RSSI').value


    @property
    def is_station(self):
        return self._read_element_by_name('FM_TRUE').value == 1


    @property
    def fm_ready(self):
        return self._read_element_by_name('FM_READY').value == 1


    def set_work_mode(self, mode = 'FM_Receiver'):
        valids = self.WORK_MODES.keys()
        assert mode in valids, 'valid mode: {}'.format(valids)

        self._write_element_by_name('WORK_MODE', self.WORK_MODES[mode])


    def _set_synthesizer1_frequency(self, freq):
        self._write_element_by_name('TXPA_GAIN', round(freq / self._ref_freq))


    def _set_clock_mode(self, mode = 32768):
        self._write_element_by_name('CLK_MODE', self.CLK_MODES[mode] & 0x07)


    def _enable_rds(self, value = True):
        self._write_element_by_name('RDS_EN', int(bool(value)))


    def _set_rds_block(self, block = 'A', word = 0x0000):
        self._write_element_by_name('RDS{}'.format(block), word)


    def _soft_reset(self):
        self._write_element_by_name('SOFT_RESET', 1)
        time.sleep(0.4)
        self._write_element_by_name('SOFT_RESET', 0)


    @property
    def i2s_enabled(self):
        return self._read_element_by_name('I2S_ENABLED') == 1


    def _set_as_i2s_master(self, value = True):
        self._write_element_by_name('I2S_MODE5', int(not value))


    def _set_i2s_ws0_as_left(self, ws0_as_left = True):
        self._write_element_by_name('SW_LR', int(ws0_as_left))


    def _set_i2s_sclk_inverted(self, value = True):
        self._write_element_by_name('SCLK_I_EDGE', int(value))


    def _set_i2s_master_sclk_inverted(self, value = True):
        self._write_element_by_name('SCLK_O_EDGE', int(value))


    def _set_i2s_ws_inverted(self, value = True):
        self._write_element_by_name('WS_I_EDGE', int(value))


    def _set_i2s_master_ws_inverted(self, value = True):
        self._write_element_by_name('SW_O_EDGE', int(value))


    def _set_i2s_data_signed(self, value = True):
        self._write_element_by_name('DATA_SIGNED', int(value))


    def _set_i2s_sampling_rate(self, freq = 48e3):
        self._write_element_by_name('I2S_SW_CNT', self.I2S_SAMPLING_RATES[freq])


    def _enable_i2s(self, value = True):
        #  When setting I2SEN bit high,
        #  RDA5820NS will output SCK, WS, SD signals from GPIO3, GPIO1, GPIO2
        #  as I2S master and transmitter, the sample rate is 42Kbps.
        self._write_element_by_name('I2S_ENABLED', int(value))


    def _left_channel_delay_1T(self, value = True):
        self._write_element_by_name('L_DELY', int(value))


    def _right_channel_delay_1T(self, value = True):
        self._write_element_by_name('R_DELY', int(value))


    def _set_soft_blend_threshold_for_noise(self, threshold):
        self._write_element_by_name('TH_SOFRBLEND', threshold)


    def _enable_soft_blend(self, value = True):
        self._write_element_by_name('SOFTBLEND_EN', int(bool(value)))


    def _set_east_europe_min_freq(self, as_65MHz = True):
        self._write_element_by_name('65M_50M', int(bool(as_65MHz)))


    def power_up(self):
        self._write_element_by_name('ENABLE', 1)
        time.sleep(0.6)


    def _set_digital_input(self, digital_mode = 'I2S', sample_on_dclk_falling_edge = False,
                           digital_audio_sample_bits = 16, sample_rate = 48000, mono_audio_mode = False,
                           enable = True):
        raise NotImplementedError()


    def power_down(self):
        self._write_element_by_name('ENABLE', 0)


    @property
    def _tune_status(self):
        raise NotImplementedError()


    def _valiate_freq(self, freq):
        raise NotImplementedError()


    def _set_gpio_mode(self, idx, mode = 'High_Impedance'):
        if not (mode == 'High_Impedance' or (mode == 'Reserved' and idx == 1)):
            self._enable_i2s(False)
        self._write_element_by_name('GPIO{}'.format(idx), self.GPIO_MODES[mode] & 0x03)


    def _gpio_as_High_Impedance(self, idx):
        self._set_gpio_mode(idx = idx, mode = 'High_Impedance')


    def _gpio2_as_stcint(self):
        self._set_gpio_mode(idx = 2, mode = 'STCIEN')


    def _gpio3_as_stereo_indicator(self):
        self._set_gpio_mode(idx = 3, mode = 'Stereo_Indicator')


    def _get_pin_value(self, pin_idx):
        return self._read_element_by_name('GPIO{}'.format(pin_idx)).value == 3


    def _set_pin_value(self, pin_idx, level = 0):
        self._write_element_by_name('GPIO{}'.format(pin_idx), 3 if bool(level) else 2)


    def Pin(self, id, value = None, invert = False):
        assert not self.i2s_enabled, 'I2S is enabled.'
        return Pin(gpio = self, id = id, value = value, invert = invert)


    def set_rds_ps(self, station_name):
        raise NotImplementedError()


    def set_rds_buffer(self, radio_text, use_FIFO = False, load_rds_group_buffer = True, clear_RDSINT = False):
        raise NotImplementedError()


    def set_rds(self, program_id = 0x0000, station_name = None, radio_text = None, program_type_code = 4,
                repeat_count = 3, message_count = 1, rds_mix_ratio = 50, rds_fifo_size = 0, deviation_Hz = 200,
                enable = True):
        raise NotImplementedError()


    @property
    def input_level(self):
        raise NotImplementedError()


    @property
    def output_signal_above_requested_modulation_level(self):
        raise NotImplementedError()


    @property
    def input_audio_level_high_threshold_exceeded(self):
        raise NotImplementedError()


    @property
    def input_audio_level_low_threshold_exceeded(self):
        raise NotImplementedError()


    @property
    def line_level(self):
        raise NotImplementedError()


    def noise_level_dBuV(self, freq, capacitance = 0):
        raise NotImplementedError()


    def mute_line_input(self, value = True):
        raise NotImplementedError()


    def mute(self, value = True):
        self._write_element_by_name('DMUTE', int(not value))


    def _enable_soft_mute(self, value = True):
        self._write_element_by_name('SOFTMUTE_EN', int(value))


    @property
    def tx_power(self):
        raise NotImplementedError()


    def _valiate_power(self, power):
        raise NotImplementedError()


    def set_power(self, power):
        raise NotImplementedError()


    def _set_tx_pa_common_voltage(self, voltage = 0):
        self._write_element_by_name('TXPA_VCOM', voltage)


    def _set_tx_pa_bias_current(self, current = 7):
        self._write_element_by_name('TXPA_IBIT', current)


    def _set_tx_pa_gain(self, gain = 0):
        assert 0 <= gain <= 63, '0 ~ 63'
        self._write_element_by_name('TXPA_GAIN', gain)


    def _set_fmtx_audio_deviation(self, deviation = 0xF0):
        self._write_element_by_name('FMTX_AUDIO_DEV', deviation)


    def _set_fmtx_pilot_deviation(self, deviation = 0x0E):
        self._write_element_by_name('FMTX_PILOT_DEV', deviation)


    def _set_fmtx_rds_deviation(self, deviation = 0x10):
        self._write_element_by_name('FMTX_RDS_DEV', deviation)


    def _set_fmtx_pga_gain(self, gain = 1):
        assert 0 <= gain <= 7, '0 ~ 7'
        self._write_element_by_name('FMTX_PGA_GAIN', gain)


    def _set_fmtx_adc_gain(self, gain = 0):
        assert 0 <= gain <= 7, '0 ~ 7'
        self._write_element_by_name('FMTX_ADC_GAIN', gain)


    @property
    def volume(self):
        return self._read_element_by_name('VOLUME').value


    def set_volume(self, gain = 0x0F):
        self._write_element_by_name('VOLUME', gain & 0x0F)


    @property
    def stereo(self):
        return self._read_element_by_name('ST').value == 1


    @stereo.setter
    def stereo(self, value = True):
        self._write_element_by_name('MONO', int(not value))


    def _enable_audio_output(self, value = True):
        self._write_element_by_name('DHIZ', int(value))


    def _enable_bass_boost(self, value = True):
        self._write_element_by_name('BASS', int(value))


    @property
    def seeking_is_in_up_direction(self):
        return self._read_element_by_name('SEEKUP').value == 1


    @property
    def seek_threshold(self):
        return self._read_element_by_name('SEEKTH').value


    def _set_seek_threshold(self, threshold):
        self._write_element_by_name('SEEKTH', threshold & 0x0F)


    def _seek_in_up_direction(self, value = True):
        self._write_element_by_name('SEEKUP', int(value))


    def _seek_up(self):
        self._seek_in_up_direction(True)
        self._seek()


    def _seek_down(self):
        self._seek_in_up_direction(False)
        self._seek()


    def _seek_mode_wrap_around(self, value = True):
        self._write_element_by_name('SKMODE', int(not value))


    def _set_seek_threshold(self, threshold):
        self._write_element_by_name('SEEKTH', threshold)


    def _set_seek_threshold_for_old_seek_mode(self, threshold):
        self._write_element_by_name('SEEK_TH_OLD', threshold)


    def _enable_stc_interrupt(self, value = True):
        self._write_element_by_name('STCIEN', int(bool(value)))


    def _enable_rds_interrupt(self, value = True):
        self._write_element_by_name('RDSIEN', int(bool(value)))


    @property
    def _is_fm_station(self):
        return self._read_element_by_name('FM_TRUE').value == 1


    @property
    def _fm_ready(self):
        return self._read_element_by_name('FM_READY').value == 1


    @property
    def seek_tune_completed(self):
        return self._read_element_by_name('STC').value == 1


    def _clear_stc_interrupt(self):
        return self._write_element_by_name('STC', 0)


    def _wait_for_tune_seek_complete(self, timeout_seconds):
        if not self.is_virtual_device:
            start = time.time()
            while not self.seek_tune_completed:
                if time.time() - start > timeout_seconds:
                    raise RuntimeError("Timeout.")

            self._clear_stc_interrupt()  # cannot be cleared, automatically cleared when starts tuning.


    def _seek(self):
        self._write_element_by_name('SEEK', 1)
        self._wait_for_tune_seek_complete(self._seek_timeout_seconds)
        self._write_element_by_name('SEEK', 0)


    @property
    def seek_successful(self):
        return self._read_element_by_name('SF').value == 0


    def _enable_afc(self, value = True):
        self._write_element_by_name('AFCD', int(not value))


    @property
    def chip_id(self):
        return self._read_register_by_address(0).value


    def enable_output(self, value = True):
        pass
        # raise NotImplementedError()


    @property
    def status(self):
        raise NotImplementedError()


    @property
    def _rds_ready(self):
        return self._read_element_by_name('RDSR').value == 1


    @property
    def _stc_ready(self):
        return self._read_element_by_name('STC').value == 1


    @property
    def _tune_completed(self):
        # self._get_interrupt_status()
        return self._stc_ready


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

    @property
    def part_number(self):
        command = self.commands['GET_REV']
        self.io._send_command(command)
        return command.responses.value_of_element('PN')


    def enable_output(self, value = True):
        self._action = 'enable_output: {}'.format(value)
        self.transmitter.mute(not value)


    # ===========================

    @property
    def status(self):
        return self.io.status


    def set_frequency(self, freq):
        self.tuner.set_frequency(freq)


    @property
    def current_frequency(self):
        return self.tuner.frequency


    def set_power(self, power):
        self.transmitter.set_power(power)


    @property
    def tx_power(self):
        return self.transmitter.tx_power


    def mute_line_input(self, value = True):
        self.line_input.mute(value)


    def mute(self, value = True):
        self.transmitter.mute(value)


    @property
    def stereo(self):
        return self.transmitter.stereo


    @stereo.setter
    def stereo(self, value = True):
        self.transmitter.stereo = value


    # =================================================================

    def _read_register(self, register):
        return self.io._read_register(register)


    def _write_register(self, register, reset = False):
        return self.io._write_register(register, reset = reset)

    # =============================================================



class Pin(fx2lp.Pin):

    def __init__(self, gpio: RDA58xx, id, value = None, invert = False):
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
