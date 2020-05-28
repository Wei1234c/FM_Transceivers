try:
    from utilities.register import *
except:
    from register import *



def _get_all_registers():
    registers = []

    registers.append(Register(name = 'GPO_IEN', address = 1,
                              description = '''Configures the sources for the GPO2/INT interrupt pin. Valid sources are the lower 8 bits of the STATUS byte, including CTS, ERR, RDSINT, ASQINT, and STCINT bits. The corresponding bit is set before the interrupt occurs. The CTS bit (and optional interrupt) is set when it is safe to send the next command. The CTS interrupt enable (CTSIEN) can be set with this property and the POWER_UP command. The state of the CTSIEN bit set during the POWER_UP command can be read by reading the this property and modified by writing this property. This property may only be set or read when in powerup mode. The default is no interrupts enabled.''',
                              elements = [Element(name = 'Reserved_11', idx_lowest_bit = 11, n_bits = 5, value = 0,
                                                  read_only = True,
                                                  description = '''Always write to 0.'''),
                                          Element(name = 'RDSREP', idx_lowest_bit = 10, n_bits = 1, value = 0,
                                                  description = '''RDS Interrupt Repeat. (Si4711/13/21 Only)
0 = No interrupt generated when RDSINT is already set (default). 
1 = Interrupt generated even if RDSINT is already set.'''),
                                          Element(name = 'ASQREP', idx_lowest_bit = 9, n_bits = 1, value = 0,
                                                  description = '''ASQ Interrupt Repeat.
0 = No interrupt generated when ASQREP is already set (default).
 1 = Interrupt generated even if ASQREP is already set.'''),
                                          Element(name = 'STCREP', idx_lowest_bit = 8, n_bits = 1, value = 0,
                                                  description = '''STC Interrupt Repeat.
0 = No interrupt generated when STCREP is already set (default).
 1 = Interrupt generated even if STCREP is already set.'''),
                                          Element(name = 'CTSIEN', idx_lowest_bit = 7, n_bits = 1, value = 0,
                                                  description = '''CTS Interrupt Enable.
0 = No interrupt generated when CTS is set (default). 
1 = Interrupt generated when CTS is set.
After PowerUp, this bit will reflect the CTSIEN bit in ARG1 of PowerUp Command.'''),
                                          Element(name = 'ERRIEN', idx_lowest_bit = 6, n_bits = 1, value = 0,
                                                  description = '''ERR Interrupt Enable.
0 = No interrupt generated when ERR is set (default). 
1 = Interrupt generated when ERR is set.'''),
                                          Element(name = 'Reserved_3', idx_lowest_bit = 3, n_bits = 3, value = 0,
                                                  read_only = True,
                                                  description = '''Always write to 0.'''),
                                          Element(name = 'RDSIEN', idx_lowest_bit = 2, n_bits = 1, value = 0,
                                                  description = '''RDS Interrupt Enable (Si4711/13/21 Only).
0 = No interrupt generated when RDSINT is set (default). 
1 = Interrupt generated when RDSINT is set.'''),
                                          Element(name = 'ASQIEN', idx_lowest_bit = 1, n_bits = 1, value = 0,
                                                  description = '''Audio Signal Quality Interrupt Enable.
0 = No interrupt generated when ASQINT is set (default). 
1 = Interrupt generated when ASQINT is set.'''),
                                          Element(name = 'STCIEN', idx_lowest_bit = 0, n_bits = 1, value = 0,
                                                  description = '''Seek/Tune Complete Interrupt Enable.
0 = No interrupt generated when STCINT is set (default). 
1 = Interrupt generated when STCINT is set.'''),
                                          ], default_value = 0))

    registers.append(Register(name = 'DIGITAL_INPUT_FORMAT', address = 257,
                              description = '''Configures the digital input format. The CTS bit (and optional interrupt) is set when it is safe to send the next command. This property may only be set or read when in powerup mode.''',
                              elements = [Element(name = 'Reserved_8', idx_lowest_bit = 8, n_bits = 8, value = 0,
                                                  read_only = True,
                                                  description = '''Always write to 0.'''),
                                          Element(name = 'IFALL', idx_lowest_bit = 7, n_bits = 1, value = 0,
                                                  description = '''DCLK Falling Edge.
0 = Sample on DCLK rising edge (default). 
1 = Sample on DCLK falling edge.'''),
                                          Element(name = 'IMODE', idx_lowest_bit = 3, n_bits = 4, value = 0,
                                                  description = '''Digital Mode.
0000 = default 0001 = I2S Mode.
0111 = Left-justified mode.
1101 = MSB at 1st DCLK rising edge after DFS Pulse. 
1001 = MSB at 2nd DCLK rising edge after DFS Pulse.'''),
                                          Element(name = 'IMONO', idx_lowest_bit = 2, n_bits = 1, value = 0,
                                                  description = '''Mono Audio Mode.
0 = Stereo audio mode (default). 
1 = Mono audio mode.'''),
                                          Element(name = 'ISIZE', idx_lowest_bit = 0, n_bits = 2, value = 0,
                                                  description = '''Digital Audio Sample Precision.
00 = 16 bits (default)
01 = 20 bits
10 = 24 bits
11 = 8 bits'''),
                                          ], default_value = 0))

    registers.append(Register(name = 'DIGITAL_INPUT_SAMPLE_RATE', address = 259,
                              description = '''Configures the digital input sample rate in 1 Hz units. The input sample rate must be set to 0 before removing the DCLK input or reducing the DCLK frequency below 2 MHz. If this guideline is not followed, a device reset will be required. The CTS bit (and optional interrupt) is set when it is safe to send the next command. This property may only be set or read when in powerup mode. TX_TUNE_FREQ command must be sent after the POWER_UP command to start the internal clocking before setting this property.''',
                              elements = [Element(name = 'DISR', idx_lowest_bit = 0, n_bits = 16, value = 0,
                                                  description = '''Digital Input Sample Rate.
0 = Disabled. Required before removing DCLK or reducing DCLK frequency below 2 MHz. The range is 32000–48000 Hz.'''),
                                          ], default_value = 0))

    registers.append(Register(name = 'REFCLK_FREQ', address = 513,
                              description = '''Sets the frequency of the REFCLK from the output of the prescaler. (Figure 1 shows the relation between RCLK and REFCLK.) The REFCLK range is 31130 to 34406 Hz (32768 ±5% Hz) in 1 Hz steps, or 0 (to disable AFC). For example, an RCLK of 13 MHz would require a prescaler value of 400 to divide it to 32500 Hz REFCLK. The reference clock frequency property would then need to be set to 32500 Hz. RCLK frequencies between 31130 Hz and 40 MHz are supported, however, there are gaps in frequency coverage for prescaler values ranging from 1 to 10, or frequencies up to 311300 Hz. Table 7 summarizes these RCLK gaps.''',
                              elements = [Element(name = 'REFCLKF', idx_lowest_bit = 0, n_bits = 16, value = 0,
                                                  description = '''Frequency of Reference Clock in Hz.
The allowed REFCLK frequency range is between 31130 and 34406 Hz (32768 ±5%), or 0 (to disable AFC).'''),
                                          ], default_value = 0))

    registers.append(Register(name = 'REFCLK_PRESCALE', address = 514,
                              description = '''Sets the number used by the prescaler to divide the external RCLK down to the internal REFCLK. The range may be between 1 and 4095 in 1 unit steps. For example, an RCLK of 13 MHz would require a prescaler value of 400 to divide it to 32500 Hz. The reference clock frequency property would then need to be set to 32500 Hz. The RCLK must be valid 10 ns before and 10 ns after sending the TX_TUNE_MEASURE, TX_TUNE_FREQ, or TX_TUNE_POWER commands. In addition, the RCLK must be valid at all times when the carrier is enabled for proper AFC operation. The RCLK may be removed or reconfigured at other times. The CTS bit (and optional interrupt) is set when it is safe to send the next command. This property may only be set or read when in powerup mode. The default is 1.''',
                              elements = [Element(name = 'Reserved_13', idx_lowest_bit = 13, n_bits = 3, value = 0,
                                                  read_only = True,
                                                  description = '''Always write to 0.'''),
                                          Element(name = 'RCLKSEL', idx_lowest_bit = 12, n_bits = 1, value = 0,
                                                  description = '''RCLKSEL.
0 = RCLK pin is clock source.
1 = DCLK pin is clock source.'''),
                                          Element(name = 'REFCLKP', idx_lowest_bit = 0, n_bits = 12, value = 0,
                                                  description = '''Prescaler for Reference Clock.
Integer number used to divide the RCLK frequency down to REFCLK frequency. The allowed REFCLK frequency range is between 31130 and 34406 Hz (32768 ±5%), or 0 (to disable AFC).'''),
                                          ], default_value = 0))

    registers.append(Register(name = 'TX_COMPONENT_ENABLE', address = 8448,
                              description = '''Individually enables the stereo pilot, left minus right stereo and RDS components. The CTS bit (and optional interrupt) is set when it is safe to send the next command. This property may only be set or read when in powerup mode. The default is stereo pilot and left minus right stereo components enabled.''',
                              elements = [Element(name = 'Reserved_3', idx_lowest_bit = 3, n_bits = 13, value = 0,
                                                  read_only = True,
                                                  description = '''Always write 0.'''),
                                          Element(name = 'RDS', idx_lowest_bit = 2, n_bits = 1, value = 0,
                                                  description = '''RDS Enable (Si4711/13/21 Only).
0 = Disables RDS (default).
1 = Enables RDS to be transmitted.'''),
                                          Element(name = 'LMR', idx_lowest_bit = 1, n_bits = 1, value = 0,
                                                  description = '''Left Minus Right.
0 = Disables Left Minus Right.
1 = Enables Left minus Right (Stereo) to be transmitted (default).'''),
                                          Element(name = 'PILOT', idx_lowest_bit = 0, n_bits = 1, value = 0,
                                                  description = '''Pilot Tone.
0 = Disables Pilot.
1 = Enables the Pilot tone to be transmitted (default).'''),
                                          ], default_value = 0))

    registers.append(Register(name = 'TX_AUDIO_DEVIATION', address = 8449,
                              description = '''Sets the transmit audio deviation from 0 to 90 kHz in 10 Hz units. The sum of the audio deviation, pilot deviation and RDS deviation should not exceed regulatory requirements, typically 75 kHz. The CTS bit (and optional interrupt) is set when it is safe to send the next command. This property may only be set or read when in powerup mode. The default is 6825, or 68.25 kHz.''',
                              elements = [Element(name = 'TXADEV', idx_lowest_bit = 0, n_bits = 16, value = 0,
                                                  description = '''Transmit Audio Frequency Deviation.
Audio frequency deviation is programmable from 0 Hz to 90 kHz in 10 Hz units. Default is 6825 (68.25 kHz). 
Note that the total deviation of the audio, pilot, and RDS must be less than 75 kHz to meet regulatory requirements.'''),
                                          ], default_value = 0))

    registers.append(Register(name = 'TX_PILOT_DEVIATION', address = 8450,
                              description = '''Sets the transmit pilot deviation from 0 to 90 kHz in 10 Hz units. The sum of the audio deviation, pilot deviation and RDS deviation should not exceed regulatory requirements, typically 75 kHz. The CTS bit (and optional interrupt) is set when it is safe to send the next command. This property may only be set or read when in powerup mode. The default is 675, or 6.75 kHz.''',
                              elements = [Element(name = 'TXPDEV', idx_lowest_bit = 0, n_bits = 16, value = 0,
                                                  description = '''Transmit Pilot Frequency Deviation.
Pilot tone frequency deviation is programmable from 0 Hz to 90 kHz in 10 Hz units. Default is 675 (6.75 kHz). 
Note that the total deviation of the audio, pilot, and RDS must be less than 75 kHz to meet regulatory requirements.'''),
                                          ], default_value = 0))

    registers.append(Register(name = 'TX_RDS_DEVIATION', address = 8451,
                              description = '''Sets the RDS deviation from 0 to 7.5 kHz in 10 Hz units. The sum of the audio deviation, pilot deviation and RDS deviation should not exceed regulatory requirements, typically 75 kHz. The CTS bit (and optional interrupt) is set when it is safe to send the next command. This property may only be set or read when in powerup mode. The default is 200, or 2 kHz.''',
                              elements = [Element(name = 'TXRDEV', idx_lowest_bit = 0, n_bits = 16, value = 0,
                                                  description = '''Transmit RDS Frequency Deviation.
RDS frequency deviation is programmable from 0 Hz to 90 kHz in 10 Hz units. Default is 200 (2 kHz). 
Note that the total deviation of the audio, pilot, and RDS must be less than 75 kHz to meet regulatory requirements.'''),
                                          ], default_value = 0))

    registers.append(Register(name = 'TX_LINE_INPUT_LEVEL', address = 8452,
                              description = '''Sets the input resistance and maximum audio input level for the LIN/RIN pins. An application providing a 150 mVPK input to the device on RIN/LIN would set Line Attenuation = 00, resulting in a maximum permissible input level of 190 mVPK on LIN/RIN and an input resistance of 396 kW. The Line Level would be set to 150 mV to correspond to the TX audio deviation level set by the TX_AUDIO_DEVIATION property. An application providing a 1 VPK input to the device on RIN/LIN would set Line Attenuation = 11, resulting in a maximum permissible input level of 636 mVPK on LIN/RIN and an input resistance of 60 kW. An external series resistor on LIN and RIN inputs of 40 kW would create a resistive voltage divider that would keep the maximum line level on RIN/LIN below 636 mVPK. The Line Level would be set to 636 mVPK to correspond to the TX audio deviation level set by the TX_AUDIO_DEVIATION property. The CTS bit (and optional interrupt) is set when it is safe to send the next command. This property may only be set or read when in powerup mode. The default input level and peak line level is 636 mVPK with an input impedance of 60 kW.''',
                              elements = [Element(name = 'Reserved_14', idx_lowest_bit = 14, n_bits = 2, value = 0,
                                                  read_only = True,
                                                  description = '''Always write to 0.'''),
                                          Element(name = 'LIATTEN', idx_lowest_bit = 12, n_bits = 2, value = 0,
                                                  description = '''Line Attenuation.
00 = Max input level = 190 mVPK; input resistance = 396 kW
01 = Max input level = 301 mVPK; input resistance = 100 kW 
10 = Max input level = 416 mVPK; input resistance = 74 kW
11 = Max input level = 636 mVPK; input resistance = 60 kW (default)'''),
                                          Element(name = 'Reserved_10', idx_lowest_bit = 10, n_bits = 2, value = 0,
                                                  read_only = True,
                                                  description = '''Always write to 0.'''),
                                          Element(name = 'LILEVEL', idx_lowest_bit = 0, n_bits = 10, value = 0,
                                                  description = '''Line Level.
Maximum line amplitude level on the LIN/RIN pins in mVPK. The default is 0x27C or 636 mVPK.'''),
                                          ], default_value = 0))

    registers.append(Register(name = 'TX_LINE_INPUT_MUTE', address = 8453,
                              description = '''Selectively mutes the left and right audio inputs. The CTS bit (and optional interrupt) is set when it is safe to send the next command. This property may only be set or read when in powerup mode.''',
                              elements = [Element(name = 'Reserved_2', idx_lowest_bit = 2, n_bits = 14, value = 0,
                                                  read_only = True,
                                                  description = '''Always write to 0.'''),
                                          Element(name = 'LIMUTE', idx_lowest_bit = 1, n_bits = 1, value = 0,
                                                  description = '''Mutes L Line Input.
0 = No mute (default) 1= Mute'''),
                                          Element(name = 'RIMUTE', idx_lowest_bit = 0, n_bits = 1, value = 0,
                                                  description = '''Mutes R Line Input.
0 = No mute (default) 1= Mute'''),
                                          ], default_value = 0))

    registers.append(Register(name = 'TX_PREEMPHASIS', address = 8454,
                              description = '''Sets the transmit pre-emphasis to 50 μs, 75 μs or off. The CTS bit (and optional interrupt) is set when it is safe to send the next command. This property may only be set or read when in powerup mode. The default is 75 μs.''',
                              elements = [Element(name = 'Reserved_2', idx_lowest_bit = 2, n_bits = 14, value = 0,
                                                  read_only = True,
                                                  description = '''Always write to 0.'''),
                                          Element(name = 'FMPE', idx_lowest_bit = 0, n_bits = 2, value = 0,
                                                  description = '''FM Pre-Emphasis.
00 = 75 μs. Used in USA (default)
01 = 50 μs. Used in Europe, Australia, Japan 10 = Disabled
11 = Reserved'''),
                                          ], default_value = 0))

    registers.append(Register(name = 'TX_PILOT_FREQUENCY', address = 8455,
                              description = '''This property is used to set the frequency of the stereo pilot in 1 Hz steps. The stereo pilot is nominally set to     19 kHz for stereo operation, however the pilot can be set to any frequency from 0 Hz to 19 kHz to support the generation of an audible test tone. The pilot tone is enabled by setting the PILOT bit (D0) of the TX_COMPONENT_ENABLE property. When using the stereo pilot as an audible test generator it is recommended that the RDS bit (D2) be disabled. The CTS bit (and optional interrupt) is set when it is safe to send the next command. This property may only be set or read when in powerup mode.''',
                              elements = [Element(name = 'FREQ', idx_lowest_bit = 0, n_bits = 16, value = 0,
                                                  description = '''Stereo Pilot Frequency
Sets the frequency of the stereo pilot in 1 Hz steps. Range 0 Hz–19000 Hz (default is 0x4A38 or 19 kHz).'''),
                                          ], default_value = 0))

    registers.append(Register(name = 'TX_ACOMP_ENABLE', address = 8704,
                              description = '''Selectively enables the audio dynamic range control and limiter. The CTS bit (and optional interrupt) is set when it is safe to send the next command. This property may only be set or read when in powerup mode. The default is limiter enabled and audio dynamic range control disabled.''',
                              elements = [Element(name = 'Reserved_2', idx_lowest_bit = 2, n_bits = 14, value = 0,
                                                  read_only = True,
                                                  description = '''Always write to 0.'''),
                                          Element(name = 'LIMITEN', idx_lowest_bit = 1, n_bits = 1, value = 0,
                                                  description = '''Audio Limiter.
0 = Disable
1 = Enable (default)'''),
                                          Element(name = 'ACEN', idx_lowest_bit = 0, n_bits = 1, value = 0,
                                                  description = '''Transmit Audio Dynamic Range Control Enable. 
0 = Audio dynamic range control disabled (default) 
1 = Audio dynamic range control enabled
'''),
                                          ], default_value = 0))

    registers.append(Register(name = 'TX_ACOMP_THRESHOLD', address = 8705,
                              description = '''Sets the threshold for audio dynamic range control from 0 dBFS to –40 dBFS in 1 dB units in 2's complement notation. For example, a setting of –40 dB would be 65536 – 40 = 65496 = 0xFFD8. The threshold is the level below which the device applies the gain set by the TX_ACOMP_GAIN property, and above which the device applies the compression defined by (gain + threshold) / threshold. The CTS bit (and optional interrupt) is set when it is safe to send the next command. This property may only be set or read when in powerup mode. The default is 0xFFD8, or –40 dBFS.''',
                              elements = [Element(name = 'THRESHOLD', idx_lowest_bit = 0, n_bits = 16, value = 0,
                                                  description = '''Transmit Audio Dynamic Range Control Threshold.
Range is from –40 to 0 dBFS in 1 dB steps (0xFFD8–0x0). Default is 0xFFD8 (–40 dBFS).'''),
                                          ], default_value = 0))

    registers.append(Register(name = 'TX_ACOMP_ATTACK_TIME', address = 8706,
                              description = '''Sets the time required for the device to respond to audio level transitions from below the threshold in the gain region to above the threshold in the compression region. The CTS bit (and optional interrupt) is set when it is safe to send the next command. This property may only be set or read when in powerup mode. The default is 0.5 ms, or 0.''',
                              elements = [Element(name = 'Reserved_4', idx_lowest_bit = 4, n_bits = 12, value = 0,
                                                  read_only = True,
                                                  description = '''Always write to 0.'''),
                                          Element(name = 'ATTACK', idx_lowest_bit = 0, n_bits = 4, value = 0,
                                                  description = '''Transmit Audio Dynamic Range Control Attack Time.
0 = 0.5 ms (default)
1 = 1.0 ms
2 = 1.5 ms
3 = 2.0 ms
4 = 2.5 ms
5 = 3.0 ms
6 = 3.5 ms
7 = 4.0 ms
8 = 4.5 ms
9 = 5.0 ms'''),
                                          ], default_value = 0))

    registers.append(Register(name = 'TX_ACOMP_RELEASE_TIME', address = 8707,
                              description = '''Sets the time required for the device to respond to audio level transitions from above the threshold in the compression region to below the threshold in the gain region. The CTS bit (and optional interrupt) is set when it is safe to send the next command. This property may only be set or read when in powerup mode. The default is 1000 ms, or 4.''',
                              elements = [Element(name = 'Reserved_3', idx_lowest_bit = 3, n_bits = 13, value = 0,
                                                  read_only = True,
                                                  description = '''Always write to 0.'''),
                                          Element(name = 'RELEASE', idx_lowest_bit = 0, n_bits = 3, value = 0,
                                                  description = '''Transmit Audio Dynamic Range Control Release Time.
0 = 100 ms
1 = 200 ms
2 = 350 ms
3 = 525 ms
4 = 1000 ms (default)'''),
                                          ], default_value = 0))

    registers.append(Register(name = 'TX_ACOMP_GAIN', address = 8708,
                              description = '''Sets the gain for audio dynamic range control from 0 to 20 dB in 1 dB units. For example, a setting of 15 dB would be 15 = 0xF. The gain is applied to the audio below the threshold set by the TX_ACOMP_THRESHOLD property. The CTS bit (and optional interrupt) is set when it is safe to send the next command. This property may only be set or read when in powerup mode. The default is 15 dB or 0xF.''',
                              elements = [Element(name = 'Reserved_6', idx_lowest_bit = 6, n_bits = 10, value = 0,
                                                  read_only = True,
                                                  description = '''Always write to 0.'''),
                                          Element(name = 'GAIN', idx_lowest_bit = 0, n_bits = 6, value = 0,
                                                  description = '''Transmit Audio Dynamic Range Control Gain.
Range is from 0 to 20 dB in 1 dB steps. Default is 15.'''),
                                          ], default_value = 0))

    registers.append(Register(name = 'TX_LIMITER_RELEASE_TIME', address = 8709,
                              description = '''Sets the time required for the device to respond to audio level transitions from above the limiter threshold to below the limiter threshold. The CTS bit (and optional interrupt) is set when it is safe to send the next command. This property may only be set or read when in powerup mode. The default is 5.01 ms, or 102.''',
                              elements = [Element(name = 'LMITERTC', idx_lowest_bit = 0, n_bits = 16, value = 0,
                                                  description = '''Sets the limiter release time.
5 = 102.39 ms
6 = 85.33 ms
7 = 73.14 ms
8 = 63.99 ms
10 = 51.19 ms
13 = 39.38 ms
17 = 30.11 ms
25 = 20.47 ms
51 = 10.03 ms
57 = 8.97 ms
64 = 7.99 ms
73 = 7.01 ms
85 = 6.02 ms
102 = 5.01 ms (default)
127 = 4.02 ms
170 = 3.00 ms
255 = 2.00 ms
510 = 1.00 ms
1000 = 0.50 ms
2000 = 0.25 ms'''),
                                          ], default_value = 0))

    registers.append(Register(name = 'TX_ASQ_INTERRUPT_SELECT', address = 8960,
                              description = '''This property is used to enable which Audio Signal Quality (ASQ) measurements trigger ASQ_INT bit in the TX_ASQ_STATUS command. OVERMODIEN bit enables ASQ interrupt by the OVERMOD bit, which turns on with overmodulation of the FM output signal due to excessive input signal level. IALHIEN and IALLIEN bits enable ASQ interrupt by the IALH and IALL bits, which report high or low input audio condition. The CTS bit (and optional interrupt) is set when it is safe to send the next command. This property may only be set or read when in powerup mode.''',
                              elements = [Element(name = 'Reserved_3', idx_lowest_bit = 3, n_bits = 13, value = 0,
                                                  read_only = True,
                                                  description = '''Always write to 0.'''),
                                          Element(name = 'OVERMODIEN', idx_lowest_bit = 2, n_bits = 1, value = 0,
                                                  description = '''Overmodulation Detection Enable.
0 = OVERMOD detect disabled (default). 
1 = OVERMOD detect enabled.'''),
                                          Element(name = 'IALHIEN', idx_lowest_bit = 1, n_bits = 1, value = 0,
                                                  description = '''Input Audio Level Detection High Threshold Enable.
0 = IALH detect disabled (default). 
1 = IALH detect enabled.'''),
                                          Element(name = 'IALLIEN', idx_lowest_bit = 0, n_bits = 1, value = 0,
                                                  description = '''Input Audio Level Detection Low Threshold Enable.
0 = IALL detect disabled (default). 
1 = IALL detect enabled.'''),
                                          ], default_value = 0))

    registers.append(Register(name = 'TX_ASQ_LEVEL_LOW', address = 8961,
                              description = '''This property sets the low audio level threshold relative to 0 dBFS in 1 dB increments, which is used to trigger the IALL bit. This threshold can be set to detect a silence condition in the input audio allowing the host to take an appropriate action such as disabling the RF carrier or powering down the chip. The CTS bit (and optional interrupt) is set when it is safe to send the next command. This property may only be set or read when in powerup mode. The default is 0x0000 and the range is 0 to –70.''',
                              elements = [Element(name = 'Reserved_8', idx_lowest_bit = 8, n_bits = 8, value = 0,
                                                  read_only = True,
                                                  description = '''Always write to 0.'''),
                                          Element(name = 'IALLTH', idx_lowest_bit = 0, n_bits = 8, value = 0,
                                                  description = '''Input Audio Level Low Threshold.
Threshold which input audio level must be below in order to detect a low audio condition. 
Specified in units of dBFS in 1 dB steps (–70 .. 0). Default is 0.'''),
                                          ], default_value = 0))

    registers.append(Register(name = 'TX_ASQ_DURATION_LOW', address = 8962,
                              description = '''This property is used to determine the duration (in 1 ms increments) that the input signal must be below the TX_ASQ_LEVEL_LOW threshold in order for an IALL condition to be generated. The range is 0 ms to 65535 ms, and the default is 0 ms. Note that the TX_ASQ_DURATION_LOW and TX_ASQ_DURATION_HIGH counters start and the TX_ASQ_STATUS command will only return valid data after a call to TX_TUNE_FREQ, TX_TUNE_POWER, or TX_TUNE_MEASURE. The CTS bit (and optional interrupt) is set when it is safe to send the next command. This property may only be set or read when in powerup mode.''',
                              elements = [Element(name = 'IALLDUR', idx_lowest_bit = 0, n_bits = 16, value = 0,
                                                  description = '''Input Audio Level Duration Low.
Required duration the input audio level must fall below IALLTH to trigger an IALL inter- rupt. 
Specified in 1mS increments (0–65535 ms). Default is 0.'''),
                                          ], default_value = 0))

    registers.append(Register(name = 'TX_ASQ_LEVEL_HIGH', address = 8963,
                              description = '''This property sets the high audio level threshold relative to 0 dBFS in 1 dB increments, which is used to trigger the IALH bit. This threshold can be set to detect an activity condition in the input audio allowing the host to take an appropriate action such as enabling the RF carrier after an extended silent period. The CTS bit (and optional interrupt) is set when it is safe to send the next command. This property may only be set or read when in powerup mode. The default is 0x0000 and the range is 0 to –70.''',
                              elements = [Element(name = 'Reserved_8', idx_lowest_bit = 8, n_bits = 8, value = 0,
                                                  read_only = True,
                                                  description = '''Always write to 0.'''),
                                          Element(name = 'IALHTH', idx_lowest_bit = 0, n_bits = 8, value = 0,
                                                  description = '''Input Audio Level High Threshold
Threshold which input audio level must be above in order to detect a high audio condition. 
Specified in units of dBFS in 1 dB steps (–70 .. 0). Default is 0.'''),
                                          ], default_value = 0))

    registers.append(Register(name = 'TX_ASQ_DURATION_HIGH', address = 8964,
                              description = '''This property is used to determine the duration (in 1 ms increments) that the input signal must be above the TX_ASQ_LEVEL_HIGH threshold in order for a IALH condition to be generated. The range is 0 to 65535 ms, and the default is 0 ms. Note that the TX_ASQ_DURATION_LOW and TX_ASQ_DURATION_HIGH counters start and the TX_ASQ_STATUS command will only return valid data after a call to TX_TUNE_FREQ, TX_TUNE_POWER, or TX_TUNE_MEASURE. The CTS bit (and optional interrupt) is set when it is safe to send the next command. This property may only be set or read when in powerup mode.''',
                              elements = [Element(name = 'IALHDUR', idx_lowest_bit = 0, n_bits = 16, value = 0,
                                                  description = '''Input Audio Level Duration High.
Required duration the input audio level must exceed IALHTH to trigger an IALH inter- rupt. 
Specified in 1 ms increments (0 – 65535 ms). Default is 0.'''),
                                          ], default_value = 0))

    registers.append(Register(name = 'TX_RDS_INTERRUPT_SOURCE', address = 11264,
                              description = '''Configures the RDS interrupt sources. The CTS bit (and optional interrupt) is set when it is safe to send the next command. This property may only be set or read when in powerup mode.''',
                              elements = [Element(name = 'RDSPSXMIT', idx_lowest_bit = 4, n_bits = 1, value = 0,
                                                  description = '''0 = Do not interrupt (default).
1 = Interrupt when a RDS PS Group has been transmitted. The interrupt occurs when a PS group begins transmission.'''),
                                          Element(name = 'RDSCBUFXMIT', idx_lowest_bit = 3, n_bits = 1, value = 0,
                                                  description = '''0 = Do not interrupt (default).
1 = Interrupt when a RDS Group has been transmitted from the Circular Buffer. The interrupt occurs when a group is fetched from the buffer.'''),
                                          Element(name = 'RDSFIFOXMIT', idx_lowest_bit = 2, n_bits = 1, value = 0,
                                                  description = '''0 = Do not interrupt (default).
1 = Interrupt when a RDS Group has been transmitted from the FIFO Buffer. The interrupt occurs when a group is fetched from the buffer.'''),
                                          Element(name = 'RDSCBUFWRAP', idx_lowest_bit = 1, n_bits = 1, value = 0,
                                                  description = '''0 = Do not interrupt (default).
1 = Interrupt when the RDS Group Circular Buffer has wrapped. The interrupt occurs when the last group is fetched from the buffer.'''),
                                          Element(name = 'RDSFIFOMT', idx_lowest_bit = 0, n_bits = 1, value = 0,
                                                  description = '''0 = Do not interrupt (default).
1 = Interrupt when the RDS Group FIFO Buffer is empty. The interrupt occurs when the last group is fetched from the FIFO.'''),
                                          ], default_value = 0))

    registers.append(Register(name = 'TX_RDS_PI', address = 11265,
                              description = '''Sets the RDS PI code to be transmitted in block A and block C (for type B groups). The CTS bit (and optional interrupt) is set when it is safe to send the next command. This property may only be set or read when in powerup mode.''',
                              elements = [Element(name = 'RDSPI', idx_lowest_bit = 0, n_bits = 16, value = 0,
                                                  description = '''Transmit RDS Program Identifier.
RDS program identifier data.'''),
                                          ], default_value = 0))

    registers.append(Register(name = 'TX_RDS_PS_MIX', address = 11266,
                              description = '''Sets the ratio of RDS PS (group 0A) and circular buffer/FIFO groups. The CTS bit (and optional interrupt) is set when it is safe to send the next command. This property may only be set or read when in powerup mode.''',
                              elements = [Element(name = 'Reserved_3', idx_lowest_bit = 3, n_bits = 13, value = 0,
                                                  read_only = True,
                                                  description = '''Always write to 0.'''),
                                          Element(name = 'RDSPSMIX', idx_lowest_bit = 0, n_bits = 3, value = 0,
                                                  description = '''Transmit RDS Mix.
000 = Only send RDS PS if RDS Group Buffer is empty 001 = Send RDS PS 12.5% of the time
010 = Send RDS PS 25% of the time
011 = Send RDS PS 50% of the time (default) 100 = Send RDS PS 75% of the time
101 = Send RDS PS 87.5% of the time
110 = Send RDS PS 100% of the time'''),
                                          ], default_value = 0))

    registers.append(Register(name = 'TX_RDS_PS_MISC', address = 11267,
                              description = '''Configures miscellaneous RDS flags. The CTS bit (and optional interrupt) is set when it is safe to send the next command. This property may only be set or read when in powerup mode.''',
                              elements = [Element(name = 'RDSD3', idx_lowest_bit = 15, n_bits = 1, value = 0,
                                                  description = '''Dynamic PTY code.
0 = Static PTY (default).
1 = Indicates that the PTY code is dynamically switched.'''),
                                          Element(name = 'RDSD2', idx_lowest_bit = 14, n_bits = 1, value = 0,
                                                  description = '''Compressed code.
0 = Not compressed (default). 
1 = Compressed.'''),
                                          Element(name = 'RDSD1', idx_lowest_bit = 13, n_bits = 1, value = 0,
                                                  description = '''Artificial Head code.
0 = Not artificial head (default). 
1 = Artificial head.'''),
                                          Element(name = 'RDSD0', idx_lowest_bit = 12, n_bits = 1, value = 0,
                                                  description = '''Mono/Stereo code.
0 = Mono.
1 = Stereo (default).'''),
                                          Element(name = 'FORCEB', idx_lowest_bit = 11, n_bits = 1, value = 0,
                                                  description = '''Use the PTY and TP set here in all block B data.
0 = FIFO and BUFFER use PTY and TP as when written (default).
1 = FIFO and BUFFER force PTY and TP to be the settings in this property.'''),
                                          Element(name = 'RDSTP', idx_lowest_bit = 10, n_bits = 1, value = 0,
                                                  description = '''Traffic Program Code (default = 0).'''),
                                          Element(name = 'RDSPTY', idx_lowest_bit = 5, n_bits = 5, value = 0,
                                                  description = '''Program Type Code (default = 0).'''),
                                          Element(name = 'RDSTA', idx_lowest_bit = 4, n_bits = 1, value = 0,
                                                  description = '''Traffic Announcement Code (default = 0).'''),
                                          Element(name = 'RDSMS', idx_lowest_bit = 3, n_bits = 1, value = 0,
                                                  description = '''Music/Speech Switch Code.
0 = Speech.
1 = Music (default).'''),
                                          Element(name = 'Reserved_0', idx_lowest_bit = 0, n_bits = 3, value = 0,
                                                  read_only = True,
                                                  description = '''Always write to 0.'''),
                                          ], default_value = 0))

    registers.append(Register(name = 'TX_RDS_PS_REPEAT_COUNT', address = 11268,
                              description = '''Sets the number of times a program service group 0A is repeated. The CTS bit (and optional interrupt) is set when it is safe to send the next command. This property may only be set or read when in powerup mode.''',
                              elements = [Element(name = 'Reserved_8', idx_lowest_bit = 8, n_bits = 8, value = 0,
                                                  read_only = True,
                                                  description = '''Always write to 0.'''),
                                          Element(name = 'RDSPSRC', idx_lowest_bit = 0, n_bits = 8, value = 0,
                                                  description = '''Transmit RDS PS Repeat Count.
Number of times to repeat transmission of a PS message before transmitting the next PS message.'''),
                                          ], default_value = 0))

    registers.append(Register(name = 'TX_RDS_PS_MESSAGE_COUNT', address = 11269,
                              description = '''Sets the number of program service messages through which to cycle. The CTS bit (and optional interrupt) is set when it is safe to send the next command. This property may only be set or read when in powerup mode.''',
                              elements = [Element(name = 'Reserved_4', idx_lowest_bit = 4, n_bits = 12, value = 0,
                                                  read_only = True,
                                                  description = '''Always write to 0.'''),
                                          Element(name = 'RDSPSMC', idx_lowest_bit = 0, n_bits = 4, value = 0,
                                                  description = '''Transmit RDS PS Message Count.
Number of PS messages to cycle through. Default is 1.'''),
                                          ], default_value = 0))

    registers.append(Register(name = 'TX_RDS_PS_AF', address = 11270,
                              description = '''Sets the AF RDS Program Service Alternate Frequency. This provides the ability to inform the receiver of a single alternate frequency using AF Method A coding and is transmitted along with the RDS_PS Groups. The CTS bit (and optional interrupt) is set when it is safe to send the next command. This property may only be set or read when in powerup mode.''',
                              elements = [Element(name = 'RDSAF', idx_lowest_bit = 0, n_bits = 16, value = 0,
                                                  description = '''Transmit RDS Program Service Alternate Frequency.
0xE101 = 1 AF @ 87.6 MHz
0xE102 = 1 AF @ 87.7 MHz
...
0xE1CB = 1 AF @ 107.8 MHz
0xE1CC = 1 AF @ 107.9 MHz
0xE0E0 = No AF exists (default)'''),
                                          ], default_value = 0))

    registers.append(Register(name = 'TX_RDS_FIFO_SIZE', address = 11271,
                              description = '''Sets the RDS FIFO size in number of blocks. Note that the value written must be one larger than the desired FIFO size. The number of blocks allocated will reduce the size of the Circular RDS Group Buffer by the same amount. For instance, if RDSFIFOSZ = 20, then the RDS Circular Buffer will be reduced by 20 blocks. The minimum number of blocks which should be allocated is 4. This provides enough room for a single group of any type (xA or xB) to be transmitted. Groups xA require 3 Blocks, Groups xB require 2 Blocks as block C' is always the same as the RDS PI code. Before setting this value, determine the available blocks through the TX_RDS_FIFO command, as the buffer size may vary between versions or part numbers. The guaranteed minimum FIFO size, however, is 53 blocks. The RDS FIFO and the RDS Circular Buffer should be emptied with the TX_RDS_FIFO command prior to changing the size of the FIFO. The CTS bit (and optional interrupt) is set when it is safe to send the next command. This property may only be set or read when in powerup mode.''',
                              elements = [Element(name = 'Reserved_8', idx_lowest_bit = 8, n_bits = 8, value = 0,
                                                  read_only = True,
                                                  description = '''Always write 0.'''),
                                          Element(name = 'RDSFIFOSZ', idx_lowest_bit = 0, n_bits = 8, value = 0,
                                                  description = '''Transmit RDS FIFO Size.
0 = FIFO disabled (default)'''),
                                          ], default_value = 0))

    return registers



def _get_registers_map():

    # elements_names = [ele.name for reg in _get_all_registers() for ele in reg._elements]
    # duplicated_elements_names = list((n for n in set(elements_names) if elements_names.count(n) > 1))
    # print(duplicated_elements_names)

    regs_map = RegistersMap(name = 'Si4713', description = 'Si4713 registers.', registers = _get_all_registers())


    return regs_map
