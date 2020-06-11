import fx2lp
from fm_transceivers.kt08xx.kt0803l import KT0803L


bus = fx2lp.I2C(as_400KHz = True)

kt = KT0803L(bus, freq = 88.80e6, emphasis_us = 75,
             audio_deviation = 75e3, input_level_dB = 0, bass_boost_level_dB = 11,
             tx_power_dBuV = 108)

print(kt.registers_values)

kt.read_all_registers()
print(kt.registers_values)

print(kt.frequency)
