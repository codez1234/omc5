from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.core.exceptions import ValidationError
from django.db import models
from database.models import TblUserLevel


class UserManager(BaseUserManager):

    def create_superuser(self, email, mobile, password, **other_fields):

        other_fields.setdefault('is_admin', True)
        # other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        if other_fields.get('is_admin') is not True:
            raise ValueError(
                'Superuser must be assigned to is_admin=True.')
        if other_fields.get('is_active') is not True:
            raise ValueError(
                'Superuser must be assigned to is_active=True.')

        return self.create_user(email, mobile, password, **other_fields)

    def create_user(self, email, mobile, password, **other_fields):

        if not email:
            raise ValueError('User must have an email address')

        if not mobile:
            raise ValueError('User must have an phone number')

        email = self.normalize_email(email)
        user = self.model(email=email,
                          mobile=mobile, **other_fields)
        user.set_password(password)
        user.save()
        return user


class User(AbstractBaseUser):
    id = models.BigAutoField(primary_key=True, db_column="fld_ai_id")
    email = models.EmailField(
        verbose_name='Email',
        max_length=100,
        unique=True, db_column="fld_email")
    mobile = models.CharField(
        max_length=100, unique=True, db_column="fld_mobile")
    password = models.CharField(max_length=255, db_column="fld_password")
    # user_level = models.IntegerField(
    #     blank=True, null=True, db_column="fld_user_level")
    user_level = models.ForeignKey(
        TblUserLevel, on_delete=models.SET_NULL, null=True, blank=True, db_column="fld_user_level")
    # user_id = models.CharField(
    #     max_length=100, blank=True, null=True, unique=True, db_column="fld_user_id")
    first_name = models.CharField(
        max_length=100, blank=True, null=True, db_column="fld_first_name")
    last_name = models.CharField(
        max_length=100, blank=True, null=True, db_column="fld_last_name")
    address = models.CharField(
        max_length=255, blank=True, null=True, db_column="fld_address")
    check_in_time = models.TimeField(
        blank=True, null=True, db_column="fld_check_in_time")
    check_out_time = models.TimeField(
        blank=True, null=True, db_column="fld_check_out_time")
    last_login = models.DateTimeField(
        blank=True, null=True, verbose_name='last login', db_column="fld_last_login_datetime")
    is_active = models.BooleanField(
        default=True, db_column="fld_is_active")
    is_delete = models.BooleanField(
        default=False, db_column="fld_is_delete")
    created_datetime = models.DateTimeField(
        blank=True, null=True, db_column="fld_created_datetime")
    datetime_timestamp = models.DateTimeField(
        blank=True, null=True, db_column="fld_datetime_timestamp")
    is_admin = models.BooleanField(default=False, db_column="fld_is_admin")

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['mobile', "password"]  # these fields must be entered.

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return self.is_admin

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

    class Meta:
        db_table = 'tbl_users'
