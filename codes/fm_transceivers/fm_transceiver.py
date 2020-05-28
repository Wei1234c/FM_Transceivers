import signal_generators.interfaces


FREQ_DEFAULT = None



class Device(signal_generators.interfaces.Device):
    FREQ_REF = None


    def __init__(self, freq = FREQ_DEFAULT, freq_correction = 0,
                 registers_map = None, registers_values = None,
                 commands = None):
        super().__init__(freq = freq, freq_correction = freq_correction, phase = None, shape = None,
                         registers_map = registers_map, registers_values = registers_values,
                         commands = commands)


    @property
    def is_virtual_device(self):
        raise NotImplementedError()


    @property
    def status(self):
        raise NotImplementedError()


    def set_frequency(self, freq, freq_correction = None):
        self._action = 'set_frequency {}'.format(freq)
        raise NotImplementedError()


    @property
    def current_frequency(self):
        raise NotImplementedError()


    def enable_output(self, value = True):
        self._action = 'enable_output: {}'.format(value)
        raise NotImplementedError()


    def init(self):
        self._action = 'init'
        raise NotImplementedError()


    def _read_register(self, register):
        raise NotImplementedError()
