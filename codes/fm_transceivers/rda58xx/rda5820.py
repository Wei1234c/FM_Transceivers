try:
    from .rda58xx import RDA58xx
except:
    from rda58xx import RDA58xx



class RDA5820(RDA58xx):

    def init(self):
        super().init()

        # Configuration
        if not self.is_virtual_device:
            assert self.chip_id == 0x5820
