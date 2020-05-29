try:
    from utilities.adapters import peripherals
    from fm_transceivers.si47xx import Si4713
except:
    import peripherals
    from si4713 import Si4713

with_hardware_device = False

if with_hardware_device:
    _i2c = peripherals.I2C.get_uPy_i2c(id = -1, scl_pin_id = 5, sda_pin_id = 4, freq = 400000)
    _pin_reset = peripherals.Pin.get_uPy_pin(15, output = True)
else:
    _i2c = _pin_reset = None  # using None for testing without actual hardware device.

bus = peripherals.I2C(_i2c)

freq = 88.80e6

si = Si4713(bus, pin_reset = _pin_reset, freq = freq)
si.set_rds(program_id = 0x0520,
           station_name = "Wei Lin",
           radio_text = "My Radio Station !",
           program_type_code = 4,
           rds_fifo_size = 20)

print(si.frequency)
