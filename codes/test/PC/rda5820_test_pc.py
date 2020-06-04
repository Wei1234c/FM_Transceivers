import fx2lp
from fm_transceivers import RDA5820
import time


bus = fx2lp.I2C(as_400KHz = True)

# freq = 88.80e6
freq = 97.7e6

rda = RDA5820(bus, freq = freq)

rda.power_down()
rda.power_up()
# rda._soft_reset()
time.sleep(0.1)

# rda._enable_i2s(True)
rda.set_work_mode(mode = 'FM_Receiver')
# rda.set_work_mode(mode = 'Audio_Amplifier')
rda._set_band('US_Europe')
rda._set_channel_spacing(100)
rda._enable_audio_output(True)
rda._enable_soft_mute(True)
rda.mute(False)
rda.set_volume(5)
rda._enable_afc(True)
rda.stereo = True
rda._enable_bass_boost(True)
rda._seek_mode_wrap_around(True)
rda._seek_in_up_direction(True)
rda._seek(True)
print(rda.seek_completed)


print(rda._read_element_by_name('CHAN').value )
print(rda._read_element_by_name('READCHAN').value )


print(rda.frequency)


rda.set_frequency(freq)



rda._set_fmtx_pga_gain( gain = 15)


print(rda._read_element_by_name('CHAN').value )
print(rda._read_element_by_name('READCHAN').value )
print(rda.frequency)

# rda.map.reset()
# print(rda.registers_values)
# rda.write_all_registers()
