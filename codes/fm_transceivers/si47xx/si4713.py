try:
    from .si471x import Si471x
except:
    from si471x import Si471x



class Si4713(Si471x):

    def init(self):
        super().init()

        # Configuration
        assert self.part_number == 0x0D  # 0x0D = Si4713
