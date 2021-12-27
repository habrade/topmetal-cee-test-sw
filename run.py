#!/usr/bin/env python3
import time
import logging
import os

import coloredlogs

from lib.global_device import GlobalDevice
from lib.dac8568_device import Dac8568Device
from lib.ipbus_link import IPbusLink
from lib.cee_spi_config import CeeSpiConfig

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)
coloredlogs.install(level='DEBUG', logger=log)

__author__ = "Sheng Dong"
__email__ = "s.dong@mails.ccnu.edu.cn"


class MainConfig(object):
    def __init__(self):
        self.GLOBAL_RESET = True
        self.JADEPIX_ANA_DATA = False


def main():
    ipbus_link = IPbusLink()

    global_dev = GlobalDevice(ipbus_link)
    dac8568_dev0 = Dac8568Device(ipbus_link, dev_nr=0)
    dac8568_dev1 = Dac8568Device(ipbus_link, dev_nr=1)
    cee_spi_dev =  CeeSpiConfig(ipbus_link)

    ''' Soft global reset '''
    global_dev.set_soft_rst()

    """ DAC8568 dev 0 Settings"""
    global_dev.set_dac_nr(0)
    dac8568_dev0.reset_dev()
    dac8568_dev0.select_ch(0xff)
    dac8568_dev0.set_volt(ch=0, volt=1.0)
    dac8568_dev0.start_conv()

    """ DAC8568 dev 1 Settings"""
    global_dev.set_dac_nr(0)
    dac8568_dev1.reset_dev()
    dac8568_dev1.select_ch(0xff)
    dac8568_dev1.set_volt(ch=1, volt=1.0)
    dac8568_dev1.start_conv()

    """ Config CEE """
    cee_spi_dev.conf_pixel(pixel_addr=1, dac_h4=0x0, dac_l8=0x0f, we=1, pulse_en=1, mask=0)
    cee_spi_dev.cee_spi_trans(rw=0, addr=0x01, data=0x00)


if __name__ == '__main__':
    main()
