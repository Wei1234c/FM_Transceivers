try:
    from signal_generators import interfaces
except:
    import interfaces

FREQ_DEFAULT = None



class Device(interfaces.Device):
    FREQ_REF = None


    def __init__(self, freq = FREQ_DEFAULT, freq_correction = 0,
                 registers_map = None, registers_values = None,
                 commands = None):
        super().__init__(freq = freq, freq_correction = freq_correction, phase = None, shape = None,
                         registers_map = registers_map, registers_values = registers_values,
                         commands = commands)


    @property
    def is_virtual_device(self):
        return self._bus.is_virtual_device


    @property
    def status(self):
        raise NotImplementedError()


    def print_register_by_address(self, register_address):
        self._read_register_by_address(register_address).print()


    @property
    def frequency(self):
        raise NotImplementedError()


    @property
    def current_frequency(self):
        raise NotImplementedError()


    def set_frequency(self, freq, freq_correction = None):
        self._action = 'set_frequency {}'.format(freq)
        raise NotImplementedError()


    def set_power(self, power):
        raise NotImplementedError()


    @property
    def tx_power(self):
        raise NotImplementedError()


    def enable_output(self, value = True):
        self._action = 'enable_output: {}'.format(value)
        raise NotImplementedError()


    def init(self):
        self._action = 'init'
        raise NotImplementedError()


    def _read_register(self, register):
        raise NotImplementedError()


    def mute_line_input(self, value = True):
        raise NotImplementedError()


    def mute(self, value = True):
        raise NotImplementedError()


    @property
    def stereo(self):
        raise NotImplementedError()


    @stereo.setter
    def stereo(self, value = True):
        raise NotImplementedError()
