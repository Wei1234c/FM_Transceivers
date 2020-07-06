try:
    from utilities.adapters import peripherals
    from fm_transceivers.si47xx.si4713_proxy import Si4713_proxy
    import fx2lp


    bus = fx2lp.I2C(as_400KHz = True)
    pin_reset = fx2lp.GPIO().Pin(id = 1, mode = fx2lp.Pin.OUT, value = 1)

except:

    #  for ESP32 ===========================
    import peripherals
    from si4713_proxy import Si4713_proxy


    with_hardware_device = True

    if with_hardware_device:
        _i2c = peripherals.I2C.get_uPy_i2c(id = -1, scl_pin_id = 5, sda_pin_id = 4, freq = 400000)
        pin_reset = peripherals.Pin.get_uPy_pin(15, output = True)
    else:
        _i2c = pin_reset = None  # using None for testing without actual hardware device.

    bus = peripherals.I2C(_i2c)
    #  for ESP32 ===========================

freq = 88.8e6
# freq = 88.0e6

si = Si4713_proxy(bus = bus, pin_reset = pin_reset, freq = freq)

print('frequency:', si.frequency)
print('tx_power:', si.tx_power)
