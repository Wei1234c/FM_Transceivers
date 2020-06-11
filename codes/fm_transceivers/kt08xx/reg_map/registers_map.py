try:
    from utilities.register import *
except:
    from register import *



def _get_all_registers():
    registers = []

    registers.append(Register(name = '0x00', address = 0, description = '''0x00''',
                              elements = [Element(name = 'CHSEL_8_1', idx_lowest_bit = 0, n_bits = 8, value = 0,
                                                  description = '''FM Channel Selection[8:1]'''),
                                          ], default_value = 0))

    registers.append(Register(name = '0x01', address = 1, description = '''0x01''',
                              elements = [Element(name = 'RFGAIN_1_0', idx_lowest_bit = 6, n_bits = 2, value = 0,
                                                  description = '''Transmission Range Adjustment with RFGAIN[3] in Reg 0x02[6] and RFGAIN[2] in Reg 0x13[7] (See Table 4 below)'''),
                                          Element(name = 'PGA', idx_lowest_bit = 3, n_bits = 3, value = 0,
                                                  description = '''PGA Gain Control (see PGA_LSB description, Reg 0x04) 
111: 12dB
110: 8dB
101: 4dB
100: 0dB
000: 0dB
001: -4dB
010: -8dB
011: -12dB'''),
                                          Element(name = 'CHSEL_11_9', idx_lowest_bit = 0, n_bits = 3, value = 0,
                                                  description = '''FM Channel Selection[11:9]'''),
                                          ], default_value = 0))

    registers.append(Register(name = '0x02', address = 2, description = '''0x02''',
                              elements = [Element(name = 'CHSEL_0', idx_lowest_bit = 7, n_bits = 1, value = 0,
                                                  description = '''LSB of CHSEL'''),
                                          Element(name = 'RFGAIN_3', idx_lowest_bit = 6, n_bits = 1, value = 0,
                                                  description = '''MSB of RFGAIN'''),
                                          Element(name = 'Reserved_4', idx_lowest_bit = 4, n_bits = 2, value = 0,
                                                  read_only = True,
                                                  description = '''Reserved'''),
                                          Element(name = 'MUTE', idx_lowest_bit = 3, n_bits = 1, value = 0,
                                                  description = '''Software Mute
0: MUTE Disabled
1: MUTE Enabled'''),
                                          Element(name = 'PLTADJ', idx_lowest_bit = 2, n_bits = 1, value = 0,
                                                  description = '''Pilot Tone Amplitude Adjustment 
0: Amplitude low
1: Amplitude high'''),
                                          Element(name = 'Reserved_1', idx_lowest_bit = 1, n_bits = 1, value = 0,
                                                  read_only = True,
                                                  description = '''Reserved'''),
                                          Element(name = 'PHTCNST', idx_lowest_bit = 0, n_bits = 1, value = 0,
                                                  description = '''Pre-emphasis Time-Constant Set 
0: 75 μs (USA, Japan)
1: 50 μs (Europe, Australia)'''),
                                          ], default_value = 0))

    registers.append(Register(name = '0x04', address = 4, description = '''0x04''',
                              elements = [Element(name = 'ALC_EN', idx_lowest_bit = 7, n_bits = 1, value = 0,
                                                  description = '''Automatic Level Control Enable Control 
0 = Disable ALC
1 = Enable ALC'''),
                                          Element(name = 'MONO', idx_lowest_bit = 6, n_bits = 1, value = 0,
                                                  description = '''0 = Stereo
1 = Mono'''),
                                          Element(name = 'PGA_LSB', idx_lowest_bit = 4, n_bits = 2, value = 0,
                                                  description = ''''''),
                                          Element(name = 'Reserved_2', idx_lowest_bit = 2, n_bits = 2, value = 0,
                                                  read_only = True,
                                                  description = '''Reserved'''),
                                          Element(name = 'BASS', idx_lowest_bit = 0, n_bits = 2, value = 0,
                                                  description = '''Bass Boost Control 
00 : Disabled
01 : 5dB
10 : 11dB
11 : 17dB'''),
                                          ], default_value = 0))

    registers.append(Register(name = '0x0B', address = 11, description = '''0x0B''',
                              elements = [Element(name = 'Standby', idx_lowest_bit = 7, n_bits = 1, value = 0,
                                                  description = '''Chip Standby Control Bit 
0 = Normal operation
1 = Standby enable'''),
                                          Element(name = 'Reserved_6', idx_lowest_bit = 6, n_bits = 1, value = 0,
                                                  read_only = True,
                                                  description = '''Reserved'''),
                                          Element(name = 'PDPA', idx_lowest_bit = 5, n_bits = 1, value = 0,
                                                  description = '''Power Amplifier Power Down
0 = Power amplifier power on
1 = Power amplifier power down'''),
                                          Element(name = 'Reserved_4', idx_lowest_bit = 4, n_bits = 1, value = 0,
                                                  read_only = True,
                                                  description = '''Reserved'''),
                                          Element(name = 'Reserved_3', idx_lowest_bit = 3, n_bits = 1, value = 0,
                                                  read_only = True,
                                                  description = '''Reserved'''),
                                          Element(name = 'AUTO_PADN', idx_lowest_bit = 2, n_bits = 1, value = 0,
                                                  description = '''Automatic Power Down Power Amplifier When Silence is Detected
0 = Disable this feature
1 = Enable this feature'''),
                                          Element(name = 'Reserved_1', idx_lowest_bit = 1, n_bits = 1, value = 0,
                                                  read_only = True,
                                                  description = '''Reserved'''),
                                          Element(name = 'Reserved_0', idx_lowest_bit = 0, n_bits = 1, value = 0,
                                                  read_only = True,
                                                  description = '''Reserved'''),
                                          ], default_value = 0))

    registers.append(Register(name = '0x0C', address = 12, description = '''0x0C''',
                              elements = [Element(name = 'ALC_DECAY_TIME', idx_lowest_bit = 4, n_bits = 4, value = 0,
                                                  description = '''ALC Decay Time Selection 
0000 = 25us
0001 = 50us
0010 = 75us
0011 = 100us
0100 = 125us
0101 = 150us
0110 = 175us
0111 = 200us
1000 = 50ms
1001 = 100ms
1010 = 150ms
1011 = 200ms
1100 = 250ms
1101 = 300ms
1110 = 350ms
1111 = 400ms'''),
                                          Element(name = 'ALC_ATTACK_TIME', idx_lowest_bit = 0, n_bits = 4, value = 0,
                                                  description = '''ALC Attack Time Selection 
0000 = 25us
0001 = 50us
0010 = 75us
0011 = 100us
0100 = 125us
0101 = 150us
0110 = 175us
0111 = 200us
1000 = 50ms
1001 = 100ms
1010 = 150ms
1011 = 200ms
1100 = 250ms
1101 = 300ms
1110 = 350ms
1111 = 400ms'''),
                                          ], default_value = 0))

    registers.append(Register(name = '0x0E', address = 14, description = '''0x0E''',
                              elements = [Element(name = 'Reserved_2', idx_lowest_bit = 2, n_bits = 6, value = 0,
                                                  read_only = True,
                                                  description = '''Reserved'''),
                                          Element(name = 'PA_BIAS', idx_lowest_bit = 1, n_bits = 1, value = 0,
                                                  description = '''PA Bias Current Enhancement. 
0 = Disable PA bias
1 = Enable PA bias'''),
                                          Element(name = 'Reserved_0', idx_lowest_bit = 0, n_bits = 1, value = 0,
                                                  read_only = True,
                                                  description = '''Reserved'''),
                                          ], default_value = 0))

    registers.append(Register(name = '0x0F', address = 15, description = '''0x0F''',
                              elements = [Element(name = 'Reserved_7', idx_lowest_bit = 7, n_bits = 1, value = 0,
                                                  read_only = True,
                                                  description = '''Reserved'''),
                                          Element(name = 'Reserved_6', idx_lowest_bit = 6, n_bits = 1, value = 0,
                                                  read_only = True,
                                                  description = '''Reserved'''),
                                          Element(name = 'Reserved_5', idx_lowest_bit = 5, n_bits = 1, value = 0,
                                                  read_only = True,
                                                  description = '''Reserved'''),
                                          Element(name = 'PW_OK', idx_lowest_bit = 4, n_bits = 1, value = 0,
                                                  read_only = True,
                                                  description = '''Power OK Indicator'''),
                                          Element(name = 'Reserved_3', idx_lowest_bit = 3, n_bits = 1, value = 0,
                                                  read_only = True,
                                                  description = '''Reserved'''),
                                          Element(name = 'SLNCID', idx_lowest_bit = 2, n_bits = 1, value = 0,
                                                  read_only = True,
                                                  description = '''1 when Silence is Detected'''),
                                          Element(name = 'Reserved_1', idx_lowest_bit = 1, n_bits = 1, value = 0,
                                                  read_only = True,
                                                  description = '''Reserved'''),
                                          Element(name = 'Reserved_0', idx_lowest_bit = 0, n_bits = 1, value = 0,
                                                  read_only = True,
                                                  description = '''Reserved'''),
                                          ], default_value = 0))

    registers.append(Register(name = '0x10', address = 16, description = '''0x10''',
                              elements = [Element(name = 'Reserved_5', idx_lowest_bit = 5, n_bits = 3, value = 0,
                                                  read_only = True,
                                                  description = '''Reserved'''),
                                          Element(name = 'Reserved_3', idx_lowest_bit = 3, n_bits = 2, value = 0,
                                                  read_only = True,
                                                  description = '''Reserved'''),
                                          Element(name = 'Reserved_1', idx_lowest_bit = 1, n_bits = 2, value = 0,
                                                  read_only = True,
                                                  description = '''Reserved'''),
                                          Element(name = 'PGAMOD', idx_lowest_bit = 0, n_bits = 1, value = 0,
                                                  description = '''PGA Mode Selection 
0 = 4dB step
1 = 1dB step with PGA_LSB[1:0 ] used'''),
                                          ], default_value = 0))

    registers.append(Register(name = '0x12', address = 18, description = '''0x12''',
                              elements = [Element(name = 'SLNCDIS', idx_lowest_bit = 7, n_bits = 1, value = 0,
                                                  description = '''Silence Detection Disable 
0 : Enable
1 : Disable'''),
                                          Element(name = 'SLNCTHL', idx_lowest_bit = 4, n_bits = 3, value = 0,
                                                  description = '''Silence Detection Low Threshold 
000 : 0.25mv
001 : 0.5mv
010 : 1mv
011 : 2mv
100 : 4mv
101 : 8mv
110 : 16mv
111 : 32mv'''),
                                          Element(name = 'SLNCTHH', idx_lowest_bit = 1, n_bits = 3, value = 0,
                                                  description = '''Silence Detection High Threshold 
000 : 0.5mv
001 : 1mv
010 : 2mv
011 : 4mv
100 : 8mv
101 : 16mv
110 : 32mv
111 : 64mv'''),
                                          Element(name = 'SW_MOD', idx_lowest_bit = 0, n_bits = 1, value = 0,
                                                  description = '''Switching Channel Mode Selection. 
0 = Mute when changing channel
1 = PA off when changing channel'''),
                                          ], default_value = 0))

    registers.append(Register(name = '0x13', address = 19, description = '''0x13''',
                              elements = [Element(name = 'RFGAIN_2', idx_lowest_bit = 7, n_bits = 1, value = 0,
                                                  description = '''PA (Power amplifier) power (combined with Reg 0x01[7:6] and Reg 0x02[6]) to set up transmission range)'''),
                                          Element(name = 'Reserved_3', idx_lowest_bit = 3, n_bits = 4, value = 0,
                                                  read_only = True,
                                                  description = '''Reserved'''),
                                          Element(name = 'PA_CTRL', idx_lowest_bit = 2, n_bits = 1, value = 0,
                                                  description = '''Power amplifier structure selection
0 = Internal power supply, KT0803 compatible 
1 = External power supply via external inductor
Note : When an external inductor is used, this bit must be set to 1 immediately after the Power OK indicator Reg 0x0F[4] is set to 1. Otherwise, the device may be destroyed!'''),
                                          Element(name = 'Reserved_0', idx_lowest_bit = 0, n_bits = 2, value = 0,
                                                  read_only = True,
                                                  description = '''Reserved'''),
                                          ], default_value = 0))

    registers.append(Register(name = '0x14', address = 20, description = '''0x14''',
                              elements = [Element(name = 'SLNCTIME_2_0', idx_lowest_bit = 5, n_bits = 3, value = 0,
                                                  description = '''Silence Detection Low Level and High Level Duration Time
000 : 50ms (16s if SLNCTIME[3] = 1)
001 : 100ms (24s if SLNCTIME[3] = 1)
010 : 200ms (32s if SLNCTIME[3] = 1)
011 : 400ms (40s if SLNCTIME[3] = 1)
100 : 1s (48s if SLNCTIME[3] = 1)
101 : 2s (56s if SLNCTIME[3] = 1)
110 : 4s (60s if SLNCTIME[3] = 1)
111 : 8s (64s if SLNCTIME[3] = 1)'''),
                                          Element(name = 'SLNCCNTHIGH', idx_lowest_bit = 2, n_bits = 3, value = 0,
                                                  description = '''Silence Detection High Level Counter Threshold 
000 : 15
001 : 31
010 : 63
011 : 127
100 : 255
101 : 511
110 : 1023
111 : 2047'''),
                                          Element(name = 'Reserved_1', idx_lowest_bit = 1, n_bits = 1, value = 0,
                                                  read_only = True,
                                                  description = '''Reserved'''),
                                          Element(name = 'SLNCTIME_3', idx_lowest_bit = 0, n_bits = 1, value = 0,
                                                  description = '''Silence Detection Long Duration Time Enable
0 = Short duration time enable
1 = Long duration time enable'''),
                                          ], default_value = 0))

    registers.append(Register(name = '0x15', address = 21, description = '''0x15''',
                              elements = [Element(name = 'ALCCMPGAIN', idx_lowest_bit = 5, n_bits = 3, value = 0,
                                                  description = '''ALC Compressed Gain Setting 
100 = 06 (6dB)
101 = 03 (3dB)
110 = 00 (0dB)
111= 1D (-3dB)
000 = 1A(-6dB)
001 = 17(-9dB)
010 = 14(-12dB)
011 = 11(-15dB)'''),
                                          Element(name = 'Reserved_0', idx_lowest_bit = 0, n_bits = 5, value = 0,
                                                  read_only = True,
                                                  description = '''Reserved'''),
                                          ], default_value = 0))

    registers.append(Register(name = '0x16', address = 22, description = '''0x16''',
                              elements = [Element(name = 'Reserved_3', idx_lowest_bit = 3, n_bits = 5, value = 0,
                                                  read_only = True,
                                                  description = '''Reserved'''),
                                          Element(name = 'SLNCCNTLOW', idx_lowest_bit = 0, n_bits = 3, value = 0,
                                                  description = '''Silence Low Counter
000 : 1
001 : 2
010 : 4
011 : 8
100 : 16
101 : 32
110 : 64
111 : 128'''),
                                          ], default_value = 0))

    registers.append(Register(name = '0x17', address = 23, description = '''0x17''',
                              elements = [Element(name = 'Reserved_7', idx_lowest_bit = 7, n_bits = 1, value = 0,
                                                  read_only = True,
                                                  description = '''Reserved'''),
                                          Element(name = 'FDEV', idx_lowest_bit = 6, n_bits = 1, value = 0,
                                                  description = '''Frequency Deviation Delection 
0 = 75kHz deviation
1 = 112.5kHz deviation'''),
                                          Element(name = 'AU_ENHANCE', idx_lowest_bit = 5, n_bits = 1, value = 0,
                                                  description = '''Audio Frequency Response Enhancement Enable
0 = Disable
1 = Enable'''),
                                          Element(name = 'Reserved_4', idx_lowest_bit = 4, n_bits = 1, value = 0,
                                                  read_only = True,
                                                  description = '''Reserved'''),
                                          Element(name = 'XTAL_SEL', idx_lowest_bit = 3, n_bits = 1, value = 0,
                                                  description = '''Software Controlled Crystal Oscillator Selection 
0 = 32.768kHz crystal
1 = 7.6MHz crystal'''),
                                          Element(name = 'Reserved_0', idx_lowest_bit = 0, n_bits = 3, value = 0,
                                                  read_only = True,
                                                  description = '''Reserved'''),
                                          ], default_value = 0))

    registers.append(Register(name = '0x1E', address = 30, description = '''0x1E''',
                              elements = [Element(name = 'Reserved_7', idx_lowest_bit = 7, n_bits = 1, value = 0,
                                                  read_only = True,
                                                  description = '''Reserved'''),
                                          Element(name = 'DCLK', idx_lowest_bit = 6, n_bits = 1, value = 0,
                                                  description = '''Multiple Reference Clock Selection Enable
0 = Disable multiple reference clock feature and reference clock or crystal oscillator can only select through SW1/SW2 pins.
1 = Enable multiple reference clock and user can select different reference clock through REF_CLK[3:0]'''),
                                          Element(name = 'XTALD', idx_lowest_bit = 5, n_bits = 1, value = 0,
                                                  description = '''Crystal Oscillator Disable Control 
0 = Enable crystal oscillator
1 = Disable crystal oscillator'''),
                                          Element(name = 'Reserved_4', idx_lowest_bit = 4, n_bits = 1, value = 0,
                                                  read_only = True,
                                                  description = '''Reserved'''),
                                          Element(name = 'REF_CLK', idx_lowest_bit = 0, n_bits = 4, value = 0,
                                                  description = '''Reference Clock Selection
0000 = 32.768kHz
0001 = 6.5MHz
0010 = 7.6MHz
0011 = 12MHz
0100 = 13MHz
0101 = 15.2MHz
0110 = 19.2MHz
0111 = 24MHz
1000 = 26MHz
Others = Reserved'''),
                                          ], default_value = 0))

    registers.append(Register(name = '0x26', address = 38, description = '''0x26''',
                              elements = [Element(name = 'ALCHOLD', idx_lowest_bit = 5, n_bits = 3, value = 0,
                                                  description = '''ALC Hold Time Selection 
000 = 50ms
001 = 100ms
010 = 150ms
011 = 200ms
100 = 1s
101 = 5s
110 = 10s
111 = 15s'''),
                                          Element(name = 'Reserved_4', idx_lowest_bit = 4, n_bits = 1, value = 0,
                                                  read_only = True,
                                                  description = '''Reserved'''),
                                          Element(name = 'ALCHIGHTH', idx_lowest_bit = 1, n_bits = 3, value = 0,
                                                  description = '''ALC High Threshold Selection 
000 = 0.6
001 = 0.5
010 = 0.4
011 = 0.3
100 = 0.2
101 = 0.1
110 = 0.05
111 = 0.01'''),
                                          Element(name = 'Reserved_0', idx_lowest_bit = 0, n_bits = 1, value = 0,
                                                  read_only = True,
                                                  description = '''Reserved'''),
                                          ], default_value = 0))

    registers.append(Register(name = '0x27', address = 39, description = '''0x27''',
                              elements = [Element(name = 'Reserved_4', idx_lowest_bit = 4, n_bits = 4, value = 0,
                                                  read_only = True,
                                                  description = '''Reserved'''),
                                          Element(name = 'ALCLOWTH', idx_lowest_bit = 0, n_bits = 4, value = 0,
                                                  description = '''ALC Low Threshold 
0000 = 0.25
0001 = 0.2
0010 = 0.15
0011 = 0.1
0100 = 0.05
0101 = 0.03
0110 = 0.02
0111 = 0.01
1000 = 0.005
1001 = 0.001
1010 = 0.0005
1011 = 0.0001'''),
                                          ], default_value = 0))

    return registers



def _get_registers_map():
    # # check if there is duplicated element names.
    # elements_names = [ele.name for reg in _get_all_registers() for ele in reg._elements]
    # duplicated_elements_names = list((n for n in set(elements_names) if elements_names.count(n) > 1))
    # print(duplicated_elements_names)

    regs_map = RegistersMap(name = 'KT0803L', description = 'KT0803L registers.', registers = _get_all_registers())

    # FACTORY_DEFAULT_REGISTERS_VALUES = ((0x00, 0x5c),
    #                                     (0x01, 0xc3),
    #                                     (0x02, 0x40),
    #                                     (0x04, 0x00),
    #                                     (0x0b, 0x00),
    #                                     (0x0c, 0x00),
    #                                     (0x0e, 0x02),
    #                                     (0x0f, 0x00),
    #                                     (0x10, 0x00),
    #                                     (0x12, 0x80),
    #                                     (0x13, 0x80),
    #                                     (0x14, 0x00),
    #                                     (0x15, 0xe0),
    #                                     (0x16, 0x00),
    #                                     (0x17, 0x00),
    #                                     (0x1e, 0x00),
    #                                     (0x26, 0xa0),
    #                                     (0x27, 0x00))

    default_values = ((0x00, 0x5c),
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

    for addr, value in default_values:
        regs_map.registers_by_address[addr].default_value = value

    return regs_map
