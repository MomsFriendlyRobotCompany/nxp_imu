from fake_rpi.smbus import SMBus as fakeSMBus

class SMBus(fakeSMBus):
    resp = {
        0x21: 0xD7,
        0x1F: 0xC7
    }

    # @printf
    def read_byte_data(self, i2c_addr, register):
        # return self.resp[i2c_addr]
            ret = 0xff
            if i2c_addr == 0x21:
                    ret = 0xD7
            elif i2c_addr == 0x1F:
                    ret = 0xC7
            return ret
