try:
    from utilities.adapters import peripherals
    from fm_transceivers.si47xx.si4713_proxy import Si4713_proxy
    import fx2lp
except:
    import peripherals
    from si4713_proxy import Si4713_proxy

#  for ESP32 ===========================
with_hardware_device = False

if with_hardware_device:
    _i2c = peripherals.I2C.get_uPy_i2c(scl_pin_id = 5, sda_pin_id = 4, freq = 400000)
    pin_reset = peripherals.Pin.get_uPy_pin(15, output = True)
else:
    _i2c = None  # using None for testing without actual hardware device.

bus = peripherals.I2C(_i2c)
#  for ESP32 ===========================


bus = fx2lp.I2C(as_400KHz = True)
pin_reset = fx2lp.GPIO().Pin(id = 1, mode = fx2lp.Pin.OUT, value = 1)

freq = 88.8e6

si = Si4713_proxy(bus, pin_reset, freq = freq)

print(si.frequency)
print(si.tx_power)
