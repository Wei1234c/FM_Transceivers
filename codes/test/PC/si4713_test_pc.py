import fx2lp
from fm_transceivers.si47xx import Si4713


# can't use FTDI FT232H: we need I2C and a reset pin, however, FT232H doesn't support I2C and GPIO simultaneously.

bus = fx2lp.I2C(as_400KHz = True)

pin_reset = fx2lp.GPIO().Pin(id = 1, mode = fx2lp.Pin.OUT, value = 1)

freq = 88.80e6

si = Si4713(bus, pin_reset = pin_reset, freq = freq)

print(si.registers_values)

si.rds.set_up(program_id = 0x0520,
              station_name = "Wei Lin",
              radio_text = "My Radio Station !",
              program_type_code = 4,
              repeat_count = 3, message_count = 1, rds_mix_ratio = 50,
              rds_fifo_size = 20,
              enable = True)

print(si.frequency)
