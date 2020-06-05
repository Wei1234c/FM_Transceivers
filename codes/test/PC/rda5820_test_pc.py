import fx2lp
from fm_transceivers import RDA5820


bus = fx2lp.I2C(as_400KHz = True)

# freq = 88.80e6
freq = 97.7e6

rda = RDA5820(bus, freq = 97.7e6, work_mode = 'FM_Receiver')
# rda = RDA5820(bus, freq = 88.8e6, work_mode = 'FM_Transmitter', tx_power_dBm = 3)

# rda.set_work_mode(mode = 'Audio_Amplifier')

rda.stereo = True
# rda.receiver.seek()


print(rda.frequency)

rda.set_frequency(freq)
print(rda.frequency)
