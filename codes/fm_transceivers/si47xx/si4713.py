try:
    from .si471x import Si471x
except:
    from si471x import Si471x



class Si4713(Si471x):

    def init(self):
        super().init()

        # Configuration
        if not self.is_virtual_device:
            assert self.part_number == 0x0D  # 0x0D = Si4713
