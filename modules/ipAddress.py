import ipaddress


def validate_ip_address(address=None):
    try:
        ip = ipaddress.ip_address(address)
        # print("IP address {} is valid. The object returned is {}".format(address, ip))
        return address
    except:
        return None


# print(validate_ip_address(None))
