import logging
import time

from lib.spi_device import SpiDevice

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)

__author__ = "Sheng Dong"
__email__ = "s.dong@mails.ccnu.edu.cn"


class CeeSpiConfig:
    def __init__(self, ipbus_link):
        self._ipbus_link = ipbus_link
        self.reg_name_base = ''

        self.spi_data = []
        self.spi_dev = SpiDevice(self._ipbus_link)

        # self.reset_spi()
        self.spi_data = [0, 0, 0, 0, 0, 0, 0, 0]
        self.set_spi()

        log.info("CEE SPI initial.")

    def w_reg(self, reg_name, reg_val, is_pulse, go_dispatch):
        """
        The register write function for Twominus device.

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
        The register read function for Twominus device.

        :param reg_name:
        :return:
        """
        return self._ipbus_link.r_reg(self.reg_name_base, reg_name)

    def is_busy_spi(self):
        """
        Check whether spi us busy.

        :return:
        """
        reg_name = "BUSY"
        spi_busy = self.r_reg(reg_name)
        if spi_busy == 1:
            return True
        else:
            return False

    def reset_spi(self, go_dispatch=True):
        """
        Reset SPI.

        :param go_dispatch:
        :return:
        """
        reg_name = "RST"
        self.w_reg(reg_name, 0, is_pulse=True, go_dispatch=go_dispatch)

    # def set_spi_data(self, d0):
    #     # self.update_spi_reg()
    #     self.spi_data[0] = d0
        

    def set_spi(self, data_len=16, ie=False, ass=True, lsb=False, rx_neg=False, tx_neg=False, div=4, ss=0x00):
        """
        SPI configuration.

        @param data_len: Number of characters to be sent, default=200.
        @param ie: The interrupt output is set active after a transfer is finished.
        @param ass: Set how ss signal is generated.
        @param lsb: LSB or MSB send first.
        @param rx_neg: Receive data at which edge.
        @param tx_neg: Send data at which edge.
        @param div: Clock division.
        @param ss: Write to ss register.
        @return:
        """
        self.spi_dev.set_data_len(data_len)
        self.spi_dev.set_ie(ie)
        self.spi_dev.set_ass(ass)
        self.spi_dev.set_lsb(lsb)
        self.spi_dev.set_rx_neg(rx_neg)
        self.spi_dev.set_tx_neg(tx_neg)
        self.spi_dev.w_div(div)
        self.spi_dev.r_div()
        self.spi_dev.w_ctrl()
        self.spi_dev.w_ss(ss)

    def start_spi_config(self):
        """
        Config SPI.

        :return:
        """
        # if self.is_busy_spi():
        #     log.error("SPI is busy now! Stop!")
        # else:
            # spi_data = self.set_spi_data()
        self.spi_dev.w_data_regs(self.spi_data)
        self.spi_dev.w_ctrl()
        self.spi_dev.start()

    def set_spi_data(self, trans_data):
        self.spi_data[0] = trans_data

    def cee_spi_trans(self, rw, addr, data):
        trans_data = (rw << 15) + (addr << 8) + data
        self.set_spi_data(trans_data)
        self.start_spi_config()

    def conf_pixel(self, pixel_addr, dac_h4, dac_l8, we, pulse_en, mask):
        self.cee_spi_trans(rw=0, addr=0x20, data=pixel_addr)
        self.cee_spi_trans(rw=0, addr=0x21, data=dac_l8)
        self.cee_spi_trans(rw=0, addr=0x22, data=((we<<7))+(pulse_en<<6)+(mask<<4)+dac_h4)


