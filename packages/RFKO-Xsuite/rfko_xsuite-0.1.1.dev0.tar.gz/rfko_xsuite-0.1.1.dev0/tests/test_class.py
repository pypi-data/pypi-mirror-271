import pytest
from RFKO_Xsuite.Rfko import Rfko
import RFKO_Xsuite

class TestRfko:
    @classmethod
    def setup_class(cls):
        # Assume the Rfko requires a parameter during initialization
        try:
            cls.rfko = Rfko()
        except:
            assert 1==0, 'The class inizialization failed'

    def test_init(self):

        self.rfko = Rfko()
        self.rfko.setup_line()


    def test_simulations(self):

        RFKO_Xsuite.xh.tracking(self.rfko)

        RFKO_Xsuite.quad_ripples.tracking(self.rfko)


