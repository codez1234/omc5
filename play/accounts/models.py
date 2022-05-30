
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.core.exceptions import ValidationError
from django.db import models


class UserManager(BaseUserManager):

    def create_superuser(self, email, phone, password, **other_fields):

        other_fields.setdefault('is_admin', True)
        # other_fields.setdefault('is_superuser', True)
        # other_fields.setdefault('is_active', True)

        if other_fields.get('is_admin') is not True:
            raise ValueError(
                'Superuser must be assigned to is_admin=True.')
        # if other_fields.get('is_superuser') is not True:
        #     raise ValueError(
        #         'Superuser must be assigned to is_superuser=True.')

        return self.create_user(email, phone, password, **other_fields)

    def create_user(self, email, phone, password, **other_fields):

        if not email:
            raise ValueError('User must have an email address')

        if not phone:
            raise ValueError('User must have an phone number')

        email = self.normalize_email(email)
        user = self.model(email=email,
                          phone=phone, **other_fields)
        user.set_password(password)
        user.save()
        return user

#  Custom User Model


class User(AbstractBaseUser):
    id = models.BigAutoField(primary_key=True, db_column="fld_ai_id")
    email = models.EmailField(
        verbose_name='Email',
        max_length=100,
        unique=True)
    phone = models.CharField(max_length=100, unique=True)
    user_level = models.IntegerField(blank=True, null=True)
    user_id = models.CharField(max_length=100, blank=True, null=True)
    is_active = models.BooleanField(default=True, db_column="fld_is_active")
    is_admin = models.BooleanField(default=False, db_column="fld_is_admin")

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone']  # these fields must be entered.

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
        # unique_together = (('id', 'user_level', 'user_id', 'fld_first_name', 'fld_last_name', 'email',
        #                    'phone', 'fld_check_in_time', 'fld_check_out_time', 'fld_is_active', 'fld_is_delete', 'fld_created_datetime'),)
