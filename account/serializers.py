from unittest.util import _MAX_LENGTH
from wsgiref import validate
from wsgiref.validate import validator
from rest_framework import serializers
from account.models import User
from database.models import TblAttendance, TblAttendanceLog2, TblUserSites, TblSites, TblUserReimbursements, TblAttendanceLog
from django.utils.encoding import smart_str, force_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from account.utils import Util
from modules.errors import messages
import re
from django.core.validators import MaxValueValidator, MinValueValidator


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # fields = "__all__"
        exclude = ("id", 'password', "is_active", "is_delete",
                   "datetime_timestamp", "is_admin", "user_level")


class UserChangePasswordSerializer(serializers.Serializer):
    password = serializers.CharField(
        max_length=255, style={'input_type': 'password'}, write_only=True)
    password2 = serializers.CharField(
        max_length=255, style={'input_type': 'password'}, write_only=True)

    class Meta:
        fields = ['password', 'password2']

    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        user = self.context.get('user')

        if password != password2:
            raise serializers.ValidationError(
                messages.get("passwords_not_equal"))

        # if not len(re.findall('\d', password)) >= 12:
        #     raise serializers.ValidationError(
        #         messages.get("password_digits"))

        if len(password) < 9:
            raise serializers.ValidationError(
                messages.get("password_length"))

        if not re.findall('[A-Z]', password):
            raise serializers.ValidationError(
                messages.get("password_upper_case"))

        if not re.findall('[a-z]', password):
            raise serializers.ValidationError(
                messages.get("password_lower_case"))

        user.set_password(password)
        user.save()
        return attrs


# # +++++++++++++++++++++++++++++++++++++++++++++++++ #


class TblAttendanceSerializer(serializers.ModelSerializer):
    def on_fld_attendance_status(value):
        if value not in ["current", "check_in", "check_out"]:
            raise serializers.ValidationError(
                "please provide valid fld_attendance_status")

    fld_attendance_status = serializers.CharField(
        validators=[on_fld_attendance_status])
    fld_latitude = serializers.FloatField(
        validators=[MinValueValidator(-90), MaxValueValidator(90)])
    fld_longitude = serializers.FloatField(
        validators=[MinValueValidator(-180), MaxValueValidator(180)])
    # fld_ip_address = serializers.CharField()
    fld_date = serializers.DateField()
    fld_time = serializers.TimeField()

    class Meta:
        model = TblAttendance
        fields = ("fld_user_id", "fld_attendance_status", "visit_id",
                  "fld_latitude", "fld_longitude", "fld_ip_address", "fld_date", "fld_time")

        def create(self, validated_data):
            return TblAttendance.objects.create(**validated_data)


'''
txt = "(-6.377934, -172.377934)"
x = re.search(
    r"^\([+|-]*((90|[1-8][0-9]|[0-9])|(([1-8][0-9]|[0-9])\.\d+)|90\.[0]+)\,\s[+|-]*((180|1[0-7][0-9]|[1-9][0-9]|[0-9])|((1[0-7][0-9]|[1-9][0-9]|[0-9])[\.]\d+)|180\.[0]+)\)$", txt)
print(x)
'''


class TblSitesSerializer(serializers.ModelSerializer):
    class Meta:
        model = TblSites
        fields = ('fld_site_omc_id', 'fld_site_type', 'fld_site_name', "fld_state",
                  "fld_district", "fld_latitude", "fld_longitude")


class TblUserSitesSerializer(serializers.ModelSerializer):
    fld_sites = TblSitesSerializer(read_only=True, many=True)

    class Meta:
        model = TblUserSites
        fields = ('fld_sites', "fld_assigned_date")


class UserReimbursementsSerializer(serializers.ModelSerializer):
    class Meta:
        model = TblUserReimbursements
        # fields = "__all__"
        exclude = ("id", 'user_id', "is_active", "is_delete")


class TblAttendanceLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = TblAttendanceLog2
        # fields = "__all__"
        exclude = ("id", 'user_id', "is_active",
                   "is_delete", "created_datetime")
