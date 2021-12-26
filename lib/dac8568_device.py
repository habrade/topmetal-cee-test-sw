import logging

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

__author__ = "Sheng Dong"
__email__ = "s.dong@mails.ccnu.edu.cn"

from lib.dac8568_defs import *

class Dac8568Device:
    def __init__(self, ipbus_link, dev_nr):
        self.reg_name_base = "dac8568_dev" + str(dev_nr) + "."
        self._ipbus_link = ipbus_link

    def w_reg(self, reg_name, reg_val, is_pulse, go_dispatch):
        """ 
        The register write function for DAC8568 device.

        :param reg_name:
        :param reg_val:
        :param is_pulse:
        :param go_dispatch:
        :return:
        """
        self._ipbus_link.w_reg(self.reg_name_base, reg_name,
                               reg_val, is_pulse, go_dispatch)

    def r_reg(self, reg_name):
        """ 
        The register read function for DAC8568 device.

        :param reg_name:
        :return:
        """
        self._ipbus_link.r_reg(self.reg_name_base, reg_name)

    def is_busy(self):
        reg_name = "busy"
        return self.r_reg(reg_name) == 1

    def reset_dev(self):
        reg_name = "rst_n"
        self.w_reg(reg_name, 0, is_pulse=True, go_dispatch=True)

    def start_conv(self):
        reg_name = "start"
        self.w_reg(reg_name, 0, is_pulse=True, go_dispatch=True)

    def select_ch(self, ch):
        """ 8bit channel map """
        reg_name = self.reg_name_base + "sel_ch"
        self.w_reg(reg_name, reg_val=ch, is_pulse=False, go_dispatch=True)

    def set_data(self, ch, data):
        """
        data_ch: STRINGS data_ch0, data_ch1, ... , data_ch7
        data: 16 bits
        """
        reg_name = "data_ch" + str(ch)
        self.w_reg(reg_name, reg_val=data, is_pulse=False, go_dispatch=True)
    
    def set_volt(self, ch, volt):
        self.set_data(ch, self.anaVal_2_digVal(volt))

    @staticmethod
    def anaVal_2_digVal(anaVal):
        """
        Static method, calculate the digital number for giving analog voltage.

        :param anaVal: Maximum equals to reference voltage: 2.5V
        :return:
        """
        if anaVal > DAC8568_REF_VOLT or anaVal < .0:
            raise ValueError(
                'Unexpected analog output value: {0}, should be less than reference voltage'.format(anaVal))
        digVal = int((2 ** 16) * anaVal / DAC8568_REF_VOLT)
        log.debug("Convert analog to digital: {:f} {:d}".format(anaVal, digVal))
        return digVal
