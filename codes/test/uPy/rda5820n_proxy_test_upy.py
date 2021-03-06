try:
    from utilities.adapters import peripherals
    from fm_transceivers.rda58xx.rda5820n_proxy import RDA5820N_proxy
    import fx2lp


    bus = fx2lp.I2C(as_400KHz = True)

except:

    #  for ESP32 ===========================
    import peripherals
    from rda5820n_proxy import RDA5820N_proxy


    with_hardware_device = True

    if with_hardware_device:
        _i2c = peripherals.I2C.get_uPy_i2c(id = -1, scl_pin_id = 5, sda_pin_id = 4, freq = 400000)
    else:
        _i2c = None  # using None for testing without actual hardware device.

    bus = peripherals.I2C(_i2c)
    #  for ESP32 ===========================

# rda = RDA5820N_proxy(bus, freq = 97.7e6, work_mode = 'Receiver')

freq = 88.8e6
# freq = 88.0e6

rda = RDA5820N_proxy(bus, freq = freq, work_mode = 'Transmitter', tx_power_dBm = 3)

# rda = RDA5820N_proxy(bus, work_mode = 'Audio_Amplifier')

# rda.set_work_mode(mode = 'Audio_Amplifier')

print('frequency:', rda.frequency)
print('tx_power:', rda.tx_power)
