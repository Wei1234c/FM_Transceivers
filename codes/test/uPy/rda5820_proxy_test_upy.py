try:
    from utilities.adapters import peripherals
    from fm_transceivers.rda58xx.rda5820_proxy import RDA5820_proxy
    import fx2lp


    bus = fx2lp.I2C(as_400KHz = True)

except:

    #  for ESP32 ===========================
    import peripherals
    from rda5820_proxy import RDA5820_proxy


    with_hardware_device = True

    if with_hardware_device:
        _i2c = peripherals.I2C.get_uPy_i2c(id = -1, scl_pin_id = 5, sda_pin_id = 4, freq = 400000)
    else:
        _i2c = None  # using None for testing without actual hardware device.

    bus = peripherals.I2C(_i2c)
    #  for ESP32 ===========================

# rda = RDA5820_proxy(bus, freq = 97.7e6, work_mode = 'FM_Receiver')
rda = RDA5820_proxy(bus, freq = 88.8e6, work_mode = 'FM_Transmitter', tx_power_dBm = 3)
# rda = RDA5820_proxy(bus, work_mode = 'Audio_Amplifier')

# rda.set_work_mode(mode = 'Audio_Amplifier')

print('frequency:', rda.frequency)
print('tx_power:', rda.tx_power)
