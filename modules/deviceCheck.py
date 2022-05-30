from database.models import TblUserDevices


def check_device(user_id=None, device_model=None, imei_number=None):
    return "ok"
    try:
        obj = TblUserDevices.objects.get(
            fld_user_id=user_id, fld_device_model=device_model, fld_imei_1=imei_number)
    except:
        obj = None

    return obj
