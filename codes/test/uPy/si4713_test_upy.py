try:
    from utilities.adapters import peripherals
    from fm_transceivers.si47xx import Si4713
    import fx2lp


    bus = fx2lp.I2C(as_400KHz = True)
    pin_reset = fx2lp.GPIO().Pin(id = 1, mode = fx2lp.Pin.OUT, value = 1)

except:

    #  for ESP32 ===========================
    import peripherals
    from si4713 import Si4713


    with_hardware_device = True

    if with_hardware_device:
        _i2c = peripherals.I2C.get_uPy_i2c(id = -1, scl_pin_id = 5, sda_pin_id = 4, freq = 400000)
        pin_reset = peripherals.Pin.get_uPy_pin(15, output = True)
    else:
        _i2c = pin_reset = None  # using None for testing without actual hardware device.

    bus = peripherals.I2C(_i2c)
    #  for ESP32 ===========================

freq = 88.8e6

si = Si4713(bus = bus, pin_reset = pin_reset, freq = freq)

si.set_rds(program_id = 0x0520,
           station_name = "Wei Lin",
           radio_text = "My Radio Station !",
           program_type_code = 4,
           repeat_count = 3, message_count = 1, rds_mix_ratio = 50,
           rds_fifo_size = 20,
           enable = True)

print('frequency:', si.frequency)
print('tx_power:', si.tx_power)
