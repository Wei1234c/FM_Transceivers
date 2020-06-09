try:
    from utilities.adapters import peripherals
    from fm_transceivers.kt08xx.kt0803l import KT0803L
    import fx2lp


    bus = fx2lp.I2C(as_400KHz = True)

except:

    #  for ESP32 ===========================
    import peripherals
    from kt0803l import KT0803L


    with_hardware_device = True

    if with_hardware_device:
        _i2c = peripherals.I2C.get_uPy_i2c(id = -1, scl_pin_id = 5, sda_pin_id = 4, freq = 400000)
    else:
        _i2c = None  # using None for testing without actual hardware device.

    bus = peripherals.I2C(_i2c)
    #  for ESP32 ===========================

kt = KT0803L(bus, freq = 88.80e6, emphasis_us = 75, audio_deviation = 112.5e3,
             input_level_dB = 12, tx_power_dBuV = 108, bass_boost_level_dB = 11)

print(kt.registers_values)

kt.read_all_registers()
print(kt.registers_values)

print(kt.frequency)
