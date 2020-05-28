import fx2lp
from fm_transceivers.si47xx import Si4713


bus = fx2lp.I2C(as_400KHz = True)
pin_reset = fx2lp.GPIO().Pin(id = 1, mode = fx2lp.Pin.OUT, value = 1)

freq = 88.80e6

si = Si4713(bus, pin_reset = pin_reset, freq = freq)
si.set_rds(program_id = 0x0520,
           station = "Wei Lin",
           message = "My Radio Station !",
           pty_code = 4,
           rds_fifo_size = 20)

print()
