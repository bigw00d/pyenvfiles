import pyvisa

def main():
    print('Hello, World!')
    rm = pyvisa.ResourceManager()
    visa_list = rm.list_resources()
    print('list len: ' + str(len(visa_list)))
    usb_1 = visa_list[0]
    inst_1 = rm.open_resource(usb_1)

    inst_1.write('*IDN?')
    out = inst_1.read()
    print(out)

if __name__ == '__main__':
    main()