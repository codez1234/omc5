
def trim(value):
    phone_number = ""
    if value[:3] in ["+91", "+92"]:
        phone_number = value[3:]
    else:
        phone_number = ""
    return phone_number


def check_phone_number(value):
    phone_number = value
    if len(value) == 13:
        phone_number = trim(value)

    if len(phone_number) == 10:
        if phone_number[0] in ["9", "8", "7", "6"]:
            return phone_number

    # print(phone_number)
    return None


# print(check_phone_number("+937121212121"))


# if "s" in ["s", "k"]:
#     print("ok")
