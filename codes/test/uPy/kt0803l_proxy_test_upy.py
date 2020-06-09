try:
    from utilities.adapters import peripherals
    from fm_transceivers.kt08xx.kt0803l_proxy import KT0803L_proxy
    import fx2lp


    bus = fx2lp.I2C(as_400KHz = True)

except:

    #  for ESP32 ===========================
    import peripherals
    from kt0803l_proxy import KT0803L_proxy


    with_hardware_device = True

    if with_hardware_device:
        _i2c = peripherals.I2C.get_uPy_i2c(id = -1, scl_pin_id = 5, sda_pin_id = 4, freq = 400000)
    else:
        _i2c = None  # using None for testing without actual hardware device.

    bus = peripherals.I2C(_i2c)
    #  for ESP32 ===========================

kt = KT0803L_proxy(bus, freq = 88.8e6, emphasis_us = 75, audio_deviation = 112.5e3,
                   input_level_dB = 12, tx_power_dBuV = 108)

kt.power_down()
print('frequency:', kt.frequency)
print('tx_power:', kt.tx_power)
