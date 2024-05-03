import smbus2
import time
import logging
import logging.config
from os import path

log_file_path = path.join(path.dirname(path.abspath(__name__)), 'logger.config')
logging.config.fileConfig(log_file_path)
logger = logging.getLogger("Energy")

device_address = 0x10
bus = smbus2.SMBus(1)
R_sense = 0.004
sample_rate = 1024

PAC1954_REFRESH_CMD_ADDR = 0x00
PAC1954_CTRL_ADDR = 0x01
PAC1954_ACC_COUNT_ADDR = 0x02
PAC1954_VPOWER1_ACC_ADDR = 0x03
PAC1954_VPOWER2_ACC_ADDR = 0x04
PAC1954_VPOWER3_ACC_ADDR = 0x05
PAC1954_VPOWER4_ACC_ADDR = 0x06
PAC1954_VBUS1_ADDR = 0x07
PAC1954_VBUS2_ADDR = 0x08
PAC1954_VBUS3_ADDR = 0x09
PAC1954_VBUS4_ADDR = 0x0A
PAC1954_VSENSE1_ADDR = 0x0B
PAC1954_VSENSE2_ADDR = 0x0C
PAC1954_VSENSE3_ADDR = 0x0D
PAC1954_VSENSE4_ADDR = 0x0E
PAC1954_VBUS1_AVG_ADDR = 0x0F
PAC1954_VBUS2_AVG_ADDR = 0x10
PAC1954_VBUS3_AVG_ADDR = 0x11
PAC1954_VBUS4_AVG_ADDR = 0x12
PAC1954_VSENSE1_AVG_ADDR = 0x13
PAC1954_VSENSE2_AVG_ADDR = 0x14
PAC1954_VSENSE3_AVG_ADDR = 0x15
PAC1954_VSENSE4_AVG_ADDR = 0x16
PAC1954_VPOWER1_ADDR = 0x17
PAC1954_VPOWER2_ADDR = 0x18
PAC1954_VPOWER3_ADDR = 0x19
PAC1954_VPOWER4_ADDR = 0x1A
PAC1954_CHANNEL_DIS_ADDR = 0x1C
PAC1954_NEG_PWR_ADDR = 0x1D
PAC1954_REFRESH_G_CMD_ADDR = 0x1E
PAC1954_REFRESH_V_CMD_ADDR = 0x1F
PAC1954_SLOW_ADDR = 0x20
PAC1954_CTRL_ACT_ADDR = 0x21
PAC1954_CHANNEL_DIS_ACT_ADDR = 0x22
PAC1954_NEG_PWR_ACT_ADDR = 0x23
PAC1954_CTRL_LAT_ADDR = 0x24
PAC1954_CHANNEL_DIS_LAT_ADDR = 0x25
PAC1954_NEG_PWR_LAT_ADDR = 0x26
PAC1954_PRODUCT_ID_ADDR = 0xFD
PAC1954_MANUFACTURER_ID_ADDR = 0xFE
PAC1954_REVISION_ID_ADDR = 0xFF


def setup():
    bus.write_byte(device_address, PAC1954_CHANNEL_DIS_ADDR, 0x72)
    bus.write_byte(device_address, PAC1954_NEG_PWR_ADDR, 0x88)
    logging.debug("Energy setup done")
    time.sleep(0.1)
    Refresh()


def Refresh():
    bus.write_byte(device_address, PAC1954_REFRESH_CMD_ADDR)


def Refresh_V():
    bus.write_byte(device_address, PAC1954_REFRESH_V_CMD_ADDR)


def bin_list_to_dec(bin_list):
    multi = 1
    result = 0
    for i in range(len(bin_list)):
        result = result + (bin_list[(len(bin_list) - 1 - i)] * multi)
        multi = multi * 256

    return result


def read_reg(reg, b):
    result = bus.read_i2c_block_data(device_address, reg, b)
    result = bin_list_to_dec(result)

    return result


# Abfrage der verbrauchten Energie mit Energy()
def Energy():
    Refresh_V()
    time.sleep(0.1)

    V_acc_1 = read_reg(PAC1954_VPOWER1_ACC_ADDR, 6)
    V_acc_2 = read_reg(PAC1954_VPOWER4_ACC_ADDR, 6)
    acc_count = read_reg(PAC1954_ACC_COUNT_ADDR, 6)

    energy1 = V_acc_1 / (2 ** 30) * (3.2 ** 2 / R_sense) / 1024 * 79.24
    energy2 = V_acc_2 / (2 ** 30) * (3.2 ** 2 / R_sense) / 1024 * 79.24
    logging.debug("Energie abgefragt")
    return energy1 + energy2