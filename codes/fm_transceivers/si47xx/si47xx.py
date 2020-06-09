# reference and partially from: https://github.com/adafruit/Adafruit_CircuitPython_SI4713

try:
    from ..fm_transceiver import Device, FREQ_DEFAULT
    from fm_transceivers.si47xx.command_property.registers_map import _get_registers_map, Register, Element
    from fm_transceivers.si47xx.command_property.commands import _get_commands, status
    import fx2lp
except:
    from fm_transceiver import Device, FREQ_DEFAULT
    from registers_map import _get_registers_map, Register, Element
    from commands import _get_commands, status

import struct
import time
from array import array



class Si47xx(Device):
    I2C_ADDRESS = 0x63
    READ_ONLY_REGISTERS = []

    FREQ_REF = 32768
    REFCLK_PRESCALE = 1
    FREQ_UNIT = int(10e3)
    FREQ_MIN = int(76e6)
    FREQ_MAX = int(108e6)
    FREQ_STEP = int(50e3)

    EMPHASIS = {75: 0, 50: 1, None: 2}
    MAX_LINE_INPUT_LEVELS_mV_pk = {0: 190, 1: 301, 2: 416, 3: 636}
    AUDIO_DYNAMIC_RANGE_CONTROL_GAIN_dB = 15
    AUDIO_DYNAMIC_RANGE_CONTROL_ATTACK_TIMES = {0.5: 0, 1: 1, 1.5: 2, 2: 3, 2.5: 4, 3: 5, 3.5: 6, 4: 7, 4.5: 8, 5: 9}
    AUDIO_DYNAMIC_RANGE_CONTROL_RELEASE_TIMES = {100: 0, 200: 1, 350: 2, 525: 3, 1000: 4}

    LIMITER_RELEASE_TIMES = {102.39: 5, 85.33: 6, 73.14: 7, 63.99: 8, 51.19: 10, 39.38: 13, 30.11: 17, 20.47: 25,
                             10.03 : 51, 8.97: 57, 7.99: 64, 7.01: 73, 6.02: 85, 5.01: 102, 4.02: 127, 3: 170, 2: 255,
                             1     : 510, 0.5: 1000, 0.25: 2000}

    DIGITAL_MODES = {'default': 0, 'I2S': 1, 'Left_Justified_I2S': 7, 'MSB_at_1st_DCLK': 13, 'MSB_at_2nd_DCLK': 9}
    DIGITAL_AUDIO_SAMPLE_PRECISION = {16: 0, 20: 1, 24: 2, 8: 3}

    RDS_MIX_RATIOS = {0: 0, 12.5: 1, 25: 2, 50: 3, 75: 4, 87.5: 5, 100: 6}


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


    class _Control(_Base):

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
            self._parent.control.power_up(analog_audio_inputs = False, *args, **kwargs)


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
            return self._parent.io.status.elements['ASQINT'].value == 1


        @property
        def asq_status(self):
            command = self._parent.commands['TX_ASQ_STATUS']
            command.arguments.elements['INTACK']['element'].value = 1
            self._parent.io._send_command(command)
            return command.responses


        def _clear_ASQINT(self):
            command = self._parent.commands['TX_ASQ_STATUS']
            command.arguments.elements['INTACK']['element'].value = 1
            self._parent.io._send_command(command)


        def _set_limiter(self, level_low_dB = -50, level_high_dB = -20,
                         duration_low_ms = 0, duration_high_ms = 0,
                         release_time_ms = 5.01,
                         overmodulation_detection_enable = True,
                         input_audio_level_detection_high_threshold_enable = True,
                         input_audio_level_detection_low_threshold_enable = True,
                         enable = True):
            if enable:
                assert -70 <= level_low_dB <= 0
                assert -70 <= level_high_dB <= 0
                assert 0 <= duration_low_ms <= 65535
                assert 0 <= duration_high_ms <= 65535

                self._parent.io._write_register_by_name('TX_LIMITER_RELEASE_TIME',
                                                        self._parent.LIMITER_RELEASE_TIMES[release_time_ms])
                self._parent.io._write_register_by_name('TX_ASQ_LEVEL_LOW', 2 ** 8 + round(level_low_dB))
                self._parent.io._write_register_by_name('TX_ASQ_DURATION_LOW', duration_low_ms)
                self._parent.io._write_register_by_name('TX_ASQ_LEVEL_HIGH', 2 ** 8 + round(level_high_dB))
                self._parent.io._write_register_by_name('TX_ASQ_DURATION_HIGH', duration_high_ms)

                interrupts = int(overmodulation_detection_enable) << 2 | \
                             int(input_audio_level_detection_high_threshold_enable) << 1 | \
                             int(input_audio_level_detection_low_threshold_enable) & 0xFFFF
                self._parent.io._write_register_by_name('TX_ASQ_INTERRUPT_SELECT', interrupts)
                time.sleep(0.01)  # status: 0x82

            self._parent.io._write_element_by_name('LIMITEN', int(enable))


    class _Tuner(_Base):

        @property
        def _stc_ready(self):
            return self._parent.io.status.elements['STCINT'].value == 1


        @property
        def _tune_completed(self):
            self._parent.io._get_interrupt_status()
            return self._stc_ready


        def _clear_STCINT(self):
            command = self._parent.commands['TX_TUNE_STATUS']
            command.arguments.elements['INTACK']['element'].value = 1
            self._parent.io._send_command(command)


        @property
        def _tune_status(self):
            command = self._parent.commands['TX_TUNE_STATUS']
            command.arguments.elements['INTACK']['element'].value = 0
            self._parent.io._send_command(command)
            return command.responses


        def _valiate_freq(self, freq):
            assert self._parent.FREQ_MIN <= freq <= self._parent.FREQ_MAX
            assert (freq // 1e3) % 50 == 0


        @property
        def frequency(self):
            tune_status = self._tune_status
            freq = tune_status.value_of_element('READFREQH') << 8 | tune_status.value_of_element('READFREQL')
            self._frequency = freq * 10e3
            return self._frequency


        def set_frequency(self, freq):
            self._valiate_freq(freq)
            self._frequency = freq

            freq = round(freq // self._parent.FREQ_UNIT)
            command = self._parent.commands['TX_TUNE_FREQ']
            command.arguments.elements['FREQH']['element'].value = freq >> 8 & 0xFF
            command.arguments.elements['FREQL']['element'].value = freq & 0xFF
            self._parent.io._send_command(command)
            self._wait_for_tune_completed()


        def _valiate_capacitance(self, capacitance):
            assert capacitance == 0 or (0.25 <= capacitance <= 47.75)


        @property
        def capacitance(self):
            tune_status = self._tune_status
            self._capacitance = tune_status.value_of_element('READANTCAP') * 0.25
            return self._capacitance


        def _set_capacitance(self, capacitance = 0):
            self._valiate_capacitance(capacitance)
            self._capacitance = capacitance

            capacitance = round(capacitance / 0.25)
            command = self._parent.commands['TX_TUNE_POWER']
            command.arguments.elements['ANTCAP']['element'].value = capacitance & 0xFF  # 0 as auto
            self._parent.io._send_command(command)
            self._parent.tuner._wait_for_tune_completed()


        def _wait_for_tune_completed(self):
            if not self._parent.is_virtual_device:
                start = time.time()
                while not self._tune_completed:
                    time.sleep(0.01)
                    if time.time() - start > self._parent._timeout_seconds:
                        raise RuntimeError("Timeout.")

                self._clear_STCINT()


    class _Transmitter(_Base):

        @property
        def _output_signal_above_requested_modulation_level(self):
            return self._parent.asq.asq_status.value_of_element('OVERMOD') == 1


        @property
        def tx_power(self):
            return self._parent.tuner._tune_status.value_of_element('READRFdBμV')


        def _valiate_power(self, power):
            assert power == 0 or (88 <= power <= 115)


        def set_power(self, power):
            self._valiate_power(power)
            self._tx_power = power

            command = self._parent.commands['TX_TUNE_POWER']
            command.arguments.elements['RFdBμV']['element'].value = power & 0xFF
            self._parent.io._send_command(command)
            self._parent.tuner._wait_for_tune_completed()


        def mute(self, value = True):
            if value:
                command = self._parent.commands['TX_TUNE_POWER']
                command.arguments.elements['RFdBμV']['element'].value = 0
                self._parent.io._send_command(command)
                self._parent.tuner._wait_for_tune_completed()
            else:
                self.set_power(self._tx_power)


        @property
        def stereo(self):
            return self._parent.io._read_element_by_name('LMR').value == 1 and \
                   self._parent.io._read_element_by_name('PILOT').value == 1


        @stereo.setter
        def stereo(self, value = True):
            self._parent.io._write_element_by_name('LMR', int(value))
            time.sleep(0.01)  # status: 0x84
            self._parent.io._write_element_by_name('PILOT', int(value))
            time.sleep(0.01)  # status: 0x84


        def _set_audio_frequency_deviation(self, deviation_Hz = 68.25e3):
            # Audio frequency deviation is programmable from 0 Hz to 90 kHz in 10 Hz units.
            # Default is 6825 (68.25 kHz). Note that the total deviation of the audio, pilot, and
            # RDS must be less than 75 kHz to meet regulatory requirements.
            assert 0 <= deviation_Hz <= 90e3

            unit = 10
            self._parent.io._write_register_by_name('TX_AUDIO_DEVIATION', round(deviation_Hz // unit))


        def _set_pre_emphasis(self, pre_emphasis_us = 75):
            self._parent.io._write_register_by_name('TX_PREEMPHASIS', self._parent.EMPHASIS[pre_emphasis_us])


        def _set_pilot(self, freq_Hz = 19e3, deviation_Hz = 6.75e3):
            # Transmit Pilot Frequency Deviation.
            # Pilot tone frequency deviation is programmable from 0 Hz to 90 kHz in 10 Hz units.
            # Default is 675 (6.75 kHz). Note that the total deviation of the audio, pilot, and RDS
            # must be less than 75 kHz to meet regulatory requirements.
            assert 0 <= deviation_Hz <= 90e3
            unit = 10
            self._parent.io._write_register_by_name('TX_PILOT_DEVIATION', round(deviation_Hz // unit))

            # This property is used to set the frequency of the stereo pilot in 1 Hz steps.
            # The stereo pilot is nominally set to 19 kHz for stereo operation,
            # however the pilot can be set to any frequency from 0 Hz to 19 kHz to support the generation of an audible test tone.
            # When using the stereo pilot as an audible test generator it is recommended that the RDS bit (D2) be disabled.
            assert 0 <= deviation_Hz <= 19e3
            self._parent.io._write_register_by_name('TX_PILOT_FREQUENCY', round(freq_Hz))


    class _Receiver(_Base):

        def noise_level_dBuV(self, freq, capacitance = 0):
            self._parent.tuner._valiate_freq(freq)
            self._parent.tuner._valiate_capacitance(capacitance)

            freq = round(freq // self._parent.FREQ_UNIT)
            capacitance = round(capacitance / 0.25)

            command = self._parent.commands['TX_TUNE_MEASURE']
            command.arguments.elements['FREQH']['element'].value = freq >> 8 & 0xFF
            command.arguments.elements['FREQL']['element'].value = freq & 0xFF
            command.arguments.elements['ANTCAP']['element'].value = capacitance & 0xFF  # 0 as auto
            self._parent.io._send_command(command)
            self._parent.tuner._wait_for_tune_completed()

            return self._parent.tuner._tune_status.value_of_element('RNL')


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
            return self._parent.io.status.elements['RDSINT'].value == 1


        def set_rds_ps(self, station_name):
            len_max = 96
            length = len(station_name)
            assert length <= len_max

            buffer = (station_name + ' ' * (len_max - length)).encode()

            for i in range(0, len_max, 4):
                command = self._parent.commands['TX_RDS_PS']

                command.arguments.elements['PSID']['element'].value = i // 4
                command.arguments.elements['PSCHAR0']['element'].value = buffer[i + 0]
                command.arguments.elements['PSCHAR1']['element'].value = buffer[i + 1]
                command.arguments.elements['PSCHAR2']['element'].value = buffer[i + 2]
                command.arguments.elements['PSCHAR3']['element'].value = buffer[i + 3]

                self._parent.io._send_command(command)


        def set_rds_buffer(self, radio_text, use_FIFO = False, load_rds_group_buffer = True, clear_RDSINT = False):
            len_max = 104
            length = len(radio_text)
            assert length <= len_max

            buffer = (radio_text + ' ' * (len_max - length)).encode()

            for i in range(0, len_max, 4):
                command = self._parent.commands['TX_RDS_BUFF']
                command.arguments.elements['FIFO']['element'].value = int(use_FIFO)
                command.arguments.elements['LDBUFF']['element'].value = int(load_rds_group_buffer)
                command.arguments.elements['MTBUFF']['element'].value = int(i == 0)
                command.arguments.elements['INTACK']['element'].value = int(clear_RDSINT)

                command.arguments.elements['RDSBH']['element'].value = 0x20
                command.arguments.elements['RDSBL']['element'].value = i // 4
                command.arguments.elements['RDSCH']['element'].value = buffer[i + 0]
                command.arguments.elements['RDSCL']['element'].value = buffer[i + 1]
                command.arguments.elements['RDSDH']['element'].value = buffer[i + 2]
                command.arguments.elements['RDSDL']['element'].value = buffer[i + 3]

                self._parent.io._send_command(command)


        def set_rds(self, program_id = 0x0000, station_name = None, radio_text = None, program_type_code = 4,
                    repeat_count = 3, message_count = 1, rds_mix_ratio = 50, rds_fifo_size = 0, deviation_Hz = 200,
                    enable = True):

            self._parent.io._write_element_by_name('RDS', int(enable))
            time.sleep(0.01)  # status: 0x84

            if enable:
                assert 0 <= program_id <= 2 ** 16 - 1

                self._parent.transmitter._set_audio_frequency_deviation(deviation_Hz = 66.25e3)
                self._parent.io._write_register_by_name('TX_RDS_DEVIATION', deviation_Hz)
                self._parent.io._write_register_by_name('TX_RDS_INTERRUPT_SOURCE', 0x0001)
                self._parent.io._write_register_by_name('TX_RDS_PI', program_id)
                self._parent.io._write_register_by_name('TX_RDS_PS_MIX', self._parent.RDS_MIX_RATIOS[rds_mix_ratio])
                self._parent.io._write_register_by_name('TX_RDS_PS_MISC',
                                                        0x1808 & ~(1 << 12) | (
                                                                int(self._parent.transmitter.stereo) << 12))
                self._parent.io._write_element_by_name('RDSPTY', program_type_code)
                self._parent.io._write_register_by_name('TX_RDS_PS_REPEAT_COUNT', repeat_count)
                self._parent.io._write_register_by_name('TX_RDS_PS_MESSAGE_COUNT', message_count)
                self._parent.io._write_register_by_name('TX_RDS_PS_AF', 0xE0E0)
                self._parent.io._write_register_by_name('TX_RDS_FIFO_SIZE', rds_fifo_size)

                if station_name is not None:
                    self.set_rds_ps(station_name)
                if radio_text is not None:
                    self.set_rds_buffer(radio_text)


    class _Gpio(_Base):

        def _set_pin_direction(self, idx, as_output = False):
            command = self._parent.commands['GPIO_CTL']
            command.arguments.elements['GPO{}OEN'.format(idx)]['element'].value = int(bool(as_output))
            self._parent.io._send_command(command)


        def _set_pin_value(self, idx, as_high = False):
            command = self._parent.commands['GPIO_SET']
            command.arguments.elements['GPO{}LEVEL'.format(idx)]['element'].value = int(bool(as_high))
            self._parent.io._send_command(command)


        def Pin(self, id, value = None, invert = False):
            return Pin(gpio = self, id = id, value = value, invert = invert)


    def __init__(self, bus, pin_reset, i2c_address = I2C_ADDRESS,
                 freq = FREQ_DEFAULT, tx_power = 115, capacitance = 0,
                 pre_emphasis_us = 75,
                 registers_map = None, registers_values = None,
                 command_set = None,
                 timeout_seconds = 0.2):

        registers_map = _get_registers_map() if registers_map is None else registers_map

        super().__init__(freq = freq, registers_map = registers_map, registers_values = registers_values)

        self._bus = bus
        self._i2c_address = i2c_address
        self._pin_reset = pin_reset

        self._tx_power = tx_power
        self._capacitance = capacitance  # 0 as auto

        self._pre_emphasis_us = pre_emphasis_us

        self._command_set = _get_commands() if command_set is None else command_set
        self._timeout_seconds = timeout_seconds
        self.init()


    def init(self):

        self._action = 'init'

        self._build()

        self._action = 'init'
        self.control._assert_reset()
        self.map.reset()

        # Powerup in Analog Mode
        self.control.power_up()

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


    def _build(self):
        self.io = self._IO(self)
        self.reference_clock = self._ReferenceClock(self)
        self.control = self._Control(self)
        self.line_input = self._LineInput(self)
        self.digital_input = self._DigitalInput(self)
        self.compressor = self._Compressor(self)
        self.asq = self._AudioSignalQualityControl(self)
        self.tuner = self._Tuner(self)
        self.transmitter = self._Transmitter(self)
        self.receiver = self._Receiver(self)
        self.rds = self._RDS(self)
        self.gpio = self._Gpio(self)


    def reset(self):
        self.init()


    @property
    def commands(self):
        return self._command_set.commands


    @property
    def properties(self):
        return self.map.registers


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
    def frequency(self):
        return self.tuner.frequency


    @property
    def current_frequency(self):
        return self.frequency


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



try:

    class Pin(fx2lp.Pin):

        def __init__(self, gpio: Si47xx._Gpio, id, mode = fx2lp.Pin.OUT, value = None, invert = False):
            # self._value = None
            super().__init__(gpio = gpio, id = id, mode = mode, value = value, invert = invert)


        def value(self, value = None):
            if value is None:
                return self._value
            else:
                self._value = int(bool(value))
                self._gpio._set_pin_value(idx = self._id, as_high = bool(value))


        @fx2lp.Pin.mode.setter
        def mode(self, mode):
            assert mode in (self.IN, self.OUT), 'Only Pin.IN, Pin.OUT supported.'
            self._mode = mode
            self._gpio._set_pin_direction(idx = self._id, as_output = mode == self.OUT)

except (NameError, ImportError):
    pass
