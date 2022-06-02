from ast import mod
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.conf import settings
User = settings.AUTH_USER_MODEL


class Audittrail(models.Model):
    datetime = models.DateTimeField()
    script = models.CharField(max_length=255, blank=True, null=True)
    user = models.CharField(max_length=255, blank=True, null=True)
    action = models.CharField(max_length=255, blank=True, null=True)
    table = models.CharField(max_length=255, blank=True, null=True)
    field = models.CharField(max_length=255, blank=True, null=True)
    keyvalue = models.TextField(blank=True, null=True)
    oldvalue = models.TextField(blank=True, null=True)
    newvalue = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'audittrail'


class Subscriptions(models.Model):
    user = models.CharField(max_length=255, blank=True, null=True)
    endpoint = models.TextField()
    publickey = models.CharField(max_length=255)
    authenticationtoken = models.CharField(max_length=255)
    contentencoding = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'subscriptions'


class TblAdmin(models.Model):
    fld_ai_id = models.BigAutoField(primary_key=True)
    fld_name = models.CharField(max_length=100, blank=True, null=True)
    fld_username = models.CharField(max_length=100, blank=True, null=True)
    fld_password = models.CharField(max_length=255, blank=True, null=True)
    fld_created_datetime = models.DateTimeField(
        auto_now_add=True)

    class Meta:
        managed = False
        db_table = 'tbl_admin'


class TblAttendance(models.Model):
    ATTENDANCE_STATUS_CHOICE = (
        ('check_in', 'check_in'),
        ('current', 'current'),
        ('check_out', 'check_out'),
    )
    # models.CharField(max_length=1, choices=MAYBECHOICE)
    fld_ai_id = models.BigAutoField(primary_key=True)
    # fld_user_id = models.BigIntegerField(blank=True, null=True)
    fld_user_id = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True)
    # fld_attendance_status = models.CharField(
    #     max_length=9, blank=True, null=True)
    # use only enum('check_in,'current',check_out')
    fld_attendance_status = models.CharField(
        max_length=9, blank=True, null=True, choices=ATTENDANCE_STATUS_CHOICE)
    # fld_latitude = models.CharField(max_length=100, blank=True, null=True)
    # fld_longitude = models.CharField(max_length=100, blank=True, null=True)
    fld_latitude = models.FloatField(
        validators=[MinValueValidator(-90), MaxValueValidator(90)], blank=True, null=True)
    fld_longitude = models.FloatField(
        validators=[MinValueValidator(-180), MaxValueValidator(180)], blank=True, null=True)
    # no need of fld_device_info, since we check it from TblUserDevices for a user
    fld_device_info = models.CharField(max_length=100, blank=True, null=True)
    # GenericIPAddressField is used for storing Pv4 or IPv6 address, in string format, so it is basically a CharField with validation of IP Address. "models.GenericIPAddressField()"
    # fld_ip_address = models.CharField(max_length=100, blank=True, null=True)
    # fld_ip_address = models.GenericIPAddressField(blank=True, null=True)
    fld_ip_address = models.CharField(max_length=100, blank=True, null=True)
    visit_id = models.CharField(
        max_length=50, blank=True, null=True, db_column="fld_visit_id")
    fld_is_active = models.BooleanField(default=True)
    fld_is_delete = models.BooleanField(default=False)
    # no need of fld_date, fld_time
    fld_date = models.DateField(blank=True, null=True)
    fld_time = models.TimeField(blank=True, null=True)
    fld_created_datetime = models.DateTimeField(
        auto_now_add=True)

    class Meta:
        managed = True
        db_table = 'tbl_attendance'


class TblRates(models.Model):
    fld_ai_id = models.AutoField(primary_key=True)
    # fld_state = models.IntegerField(blank=True, null=True)
    fld_state = models.CharField(max_length=50, blank=True, null=True)
    # fld_rate = models.IntegerField()
    fld_rate = models.PositiveSmallIntegerField(blank=True, null=True)
    fld_is_active = models.BooleanField(default=True)
    fld_created_datetime = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = True
        db_table = 'tbl_rates'


class TblSites(models.Model):
    fld_ai_id = models.AutoField(primary_key=True)
    fld_site_omc_id = models.CharField(max_length=10, blank=True, null=True)
    fld_site_type = models.CharField(max_length=6, blank=True, null=True)
    fld_site_name = models.CharField(max_length=100, blank=True, null=True)
    fld_state = models.CharField(max_length=50, blank=True, null=True)
    # fld_state = models.PositiveSmallIntegerField(blank=True, null=True)
    # use state id,
    fld_district = models.CharField(max_length=100, blank=True, null=True)
    fld_latitude = models.CharField(max_length=100, blank=True, null=True)
    fld_longitude = models.CharField(max_length=100, blank=True, null=True)
    fld_is_active = models.BooleanField(default=True)
    fld_is_delete = models.BooleanField(default=False)
    fld_created_datetime = models.DateTimeField(
        auto_now_add=True)

    class Meta:
        managed = True
        db_table = 'tbl_sites'


class TblUserDevices(models.Model):
    fld_ai_id = models.BigAutoField(primary_key=True)
    # fld_user_id = models.IntegerField(blank=True, null=True)
    fld_user_id = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True)
    fld_device_model = models.CharField(max_length=100, blank=True, null=True)
    fld_imei_1 = models.CharField(max_length=100, blank=True, null=True)
    fld_imei_2 = models.CharField(max_length=100, blank=True, null=True)
    fld_device_id_token = models.CharField(
        max_length=255, blank=True, null=True)
    fld_is_active = models.BooleanField(default=True)
    fld_created_datetime = models.DateTimeField(
        auto_now_add=True)

    class Meta:
        managed = True
        db_table = 'tbl_user_devices'


class TblUserLevel(models.Model):
    fld_ai_id = models.AutoField(primary_key=True)
    fld_user_level_name = models.CharField(
        max_length=20, blank=True, null=True)
    fld_is_active = models.BooleanField(default=True)
    fld_created_datetime = models.DateTimeField(
        auto_now_add=True)

    def __str__(self) -> str:
        return self.fld_user_level_name

    class Meta:
        managed = True
        db_table = 'tbl_user_level'


class TblUserSites(models.Model):
    fld_ai_id = models.AutoField(primary_key=True)
    # fld_user_id = models.IntegerField()
    fld_user_id = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True)
    # fld_sites = models.CharField(max_length=255, blank=True, null=True)
    fld_sites = models.ManyToManyField(TblSites)
    fld_assigned_date = models.DateTimeField(blank=True, null=True)
    fld_is_active = models.BooleanField(default=True)
    fld_is_delete = models.BooleanField(default=False)
    fld_created_datetime = models.DateTimeField(
        auto_now_add=True)

    class Meta:
        managed = True
        db_table = 'tbl_user_sites'


class TblUserReimbursements(models.Model):
    REIMBURSEMENTS_STATUS_CHOICE = (
        ('completed', 'completed'),
        ('pending', 'pending'),
    )
    id = models.AutoField(primary_key=True, db_column="fld_ai_id")
    user_id = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, db_column="fld_user_id")
    claim_id = models.CharField(
        max_length=100, blank=True, null=True, db_column="fld_claim_id")
    visit_id = models.CharField(
        max_length=50, blank=True, null=True, db_column="fld_visit_id")
    distance = models.IntegerField(
        blank=True, null=True, db_column="fld_distance")
    amount = models.IntegerField(
        blank=True, null=True, db_column="fld_amount")
    status = models.CharField(
        max_length=20, blank=True, null=True, choices=REIMBURSEMENTS_STATUS_CHOICE, default="pending", db_column="fld_status")
    is_active = models.BooleanField(
        default=True, db_column="fld_is_active")
    is_delete = models.BooleanField(
        default=False, db_column="fld_is_delete")
    date = models.DateField(blank=True, null=True, db_column="fld_date")
    created_datetime = models.DateTimeField(
        blank=True, null=True, db_column="fld_created_datetime")

    class Meta:
        db_table = 'tbl_user_reimbursements'


class TblAttendanceLog(models.Model):
    id = models.AutoField(primary_key=True, db_column="fld_ai_id")
    user_id = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, db_column="fld_user_id")
    site_id = models.CharField(
        max_length=100, blank=True, null=True, db_column="fld_site_omc_id")
    site_name = models.CharField(
        max_length=100, blank=True, null=True, db_column="fld_site_name")
    distance = models.FloatField(
        blank=True, null=True, db_column="fld_distance")
    visit_id = models.CharField(
        max_length=50, blank=True, null=True, db_column="fld_visit_id")
    check_in_time = models.TimeField(
        blank=True, null=True, db_column="fld_check_in_time")
    check_out_time = models.TimeField(
        blank=True, null=True, db_column="fld_check_out_time")
    date = models.DateField(blank=True, null=True, db_column="fld_date")
    is_active = models.BooleanField(
        default=True, db_column="fld_is_active")
    is_delete = models.BooleanField(
        default=False, db_column="fld_is_delete")

    created_datetime = models.DateTimeField(
        blank=True, null=True, db_column="fld_created_datetime")

    class Meta:
        db_table = 'tbl_attendance_log'
