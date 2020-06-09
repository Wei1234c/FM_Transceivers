import fx2lp
from fm_transceivers import RDA5820N


bus = fx2lp.I2C(as_400KHz = True)

# rda = RDA5820N(bus, freq = 97.7e6, work_mode = 'FM_Receiver')
rda = RDA5820N(bus, freq = 88.8e6, work_mode = 'FM_Transmitter', tx_power_dBm = 3)
# rda = RDA5820N(bus, work_mode = 'Audio_Amplifier')

# rda.set_work_mode(mode = 'Audio_Amplifier')

rda.stereo = True
# rda.receiver.seek()


print(rda.frequency)
