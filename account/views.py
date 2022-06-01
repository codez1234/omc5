from datetime import datetime, timedelta
from email import message
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework import status
from rest_framework.views import APIView

from account.models import User
from database.models import TblUserDevices, TblUserSites, TblAttendanceLog, TblAttendanceLog2

from account.phone_number_validation import check_phone_number
from account.serializers import *
from django.contrib.auth import authenticate
from account.renderers import UserRenderer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from modules.createOrWriteTextFile import request_text_file, response_text_file, date_now
from modules.errors import messages
from modules.deviceCheck import check_device
from modules.ipAddress import validate_ip_address
from modules.distanceCalculation import total_distance
from modules.imeiNumber import isValidIMEI
from modules.geoBound import is_arrived
from django.shortcuts import get_object_or_404


# ++++++++++++++++++++++++++++++++++++++++ #

# ++++++++++++++++++++++++++++++++++++++++++++++++ #


# Generate Token Manually


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'access_token': str(refresh.access_token),
        'refresh_token': str(refresh),
    }


class UserLoginView(APIView):
    renderer_classes = [UserRenderer]

    def post(self, request, format=None):
        # https://www.valentinog.com/blog/drf-request/#:~:text=Surprise!-,request.,object%20and%20modify%20the%20copy.
        request_text_file(user=request.user.id,
                          value=request.data, dir="UserLoginView")
        email_or_phone = request.data.get("email_or_phone")
        password = request.data.get('password')
        email = ""
        print(request.data)
        if validate_ip_address(request.data.get('ip_address')) is None:
            response_text_file(
                value={"status": "error", 'message': messages.get("ip_error")})
            return Response({"status": "error", 'message': messages.get("ip_error")}, status=status.HTTP_400_BAD_REQUEST)

        if isValidIMEI(int(request.data.get('imei_number'))) is False:
            response_text_file(
                value={"status": "error", 'message': messages.get("IMEI_error")})
            return Response({"status": "error", 'message': messages.get("IMEI_error")}, status=status.HTTP_400_BAD_REQUEST)

        if "@" in email_or_phone:
            email = email_or_phone
        else:
            validate_phone_number = check_phone_number(email_or_phone)
            user = {}
            try:
                user = User.objects.get(
                    mobile=validate_phone_number)
            except:
                user = {}
            if user:
                email = user.email
            else:
                (email, password) = (None, None)

        user = authenticate(email=email, password=password)

        if user is not None:
            obj = check_device(user.id, request.data.get(
                'device_model'),  request.data.get('imei_number'))

            if obj is not None:
                token = get_tokens_for_user(user)
                response_text_file(user=user.id, value={"status": "success", 'message': messages.get(
                    "login_success"), "data": token}, dir="UserLoginView")
                return Response({"status": "success", 'message': messages.get("login_success"), "data": token}, status=status.HTTP_200_OK)
            response_text_file(user=user.id, value={
                               "status": "error", 'message': messages.get("device_information_error")})
            return Response({"status": "error", 'message': messages.get("device_information_error")}, status=status.HTTP_404_NOT_FOUND)
        else:
            response_text_file(value={"status": "error", 'message': messages.get(
                "wrong_email_or_phone_and_password")})
            return Response({"status": "error", 'message': messages.get("wrong_email_or_phone_and_password")}, status=status.HTTP_404_NOT_FOUND)


class UserProfileView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        print(request.user.id)
        request_text_file(user=request.user.id, value=request.data)
        serializer = UserProfileSerializer(request.user)
        response_text_file(user=request.user.id, value={
                           "status": "success", 'message': "user data", "data": serializer.data})
        return Response({"status": "success", 'message': "user data", "data": serializer.data}, status=status.HTTP_200_OK)


class UserChangePasswordView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        request_text_file(user=request.user.id, value=request.data)
        password = request.data.get('password')
        password2 = request.data.get('password2')

        if validate_ip_address(request.data.get('ip_address')) is None:
            response_text_file(
                value={"status": "error", 'message': messages.get("ip_error")})
            return Response({"status": "error", 'message': messages.get("ip_error")}, status=status.HTTP_400_BAD_REQUEST)

        if isValidIMEI(int(request.data.get('imei_number'))) is False:
            response_text_file(
                value={"status": "error", 'message': messages.get("IMEI_error")})
            return Response({"status": "error", 'message': messages.get("IMEI_error")}, status=status.HTTP_400_BAD_REQUEST)

        obj = check_device(request.user.id, request.data.get(
            'device_model'),  request.data.get('imei_number'))

        if obj is not None:
            serializer = UserChangePasswordSerializer(
                data={"password": password, "password2": password2}, context={'user': request.user})
            serializer.is_valid(raise_exception=True)
            response_text_file(user=request.user.id,
                               value={"status": "success", 'message': messages.get("password_changed")})
            return Response({"status": "success", 'message': messages.get("password_changed")}, status=status.HTTP_200_OK)
        response_text_file(user=request.user.id, value={
            "status": "error", 'message': messages.get("device_information_error")})
        return Response({"status": "error", 'message': messages.get("device_information_error")}, status=status.HTTP_404_NOT_FOUND)


class UserSitesView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        id = request.user.id
        request_text_file(user=id, value=request.data)
        # may cause error if "sites" doesnot exists.
        sites = get_object_or_404(TblUserSites, fld_user_id=id)
        # print(id)
        serializer = TblUserSitesSerializer(sites)
        response_text_file(user=id, value={
                           "status": "success", 'message': "user sites", "data": serializer.data})
        return Response({"status": "success", 'message': "user sites", "data": serializer.data}, status=status.HTTP_200_OK)


class AttendanceLogView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        request_text_file(user=request.user.id, value=request.data)
        # try:
        #     obj = TblAttendanceLog.objects.get(
        #         user_id=request.user, date=date_now())
        # except:
        #     obj = None
        obj = TblAttendanceLog2.objects.filter(
            user_id=request.user, date=request.data.get("date"))
        serializer = TblAttendanceLogSerializer(obj, many=True)
        response_text_file(user=request.user.id, value={
                           "status": "success", 'message': "user data", "data": serializer.data})
        return Response({"status": "success", 'message': "user data", "data": serializer.data}, status=status.HTTP_200_OK)


class UserTblAttendanceView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        # print(f'request.headers == {request.headers}')
        user = request.user.id
        values = request.data.get('attendence')
        request_text_file(user=user, value=values)

        try:
            sites = TblUserSites.objects.filter(
                fld_user_id=user).last().fld_sites.all()
        except:
            # sites = None
            # print(request.headers)
            response_text_file(
                user=user, value={
                    "status": "error", 'message': messages.get("site_not_assined_yet")})
            return Response({
                            "status": "error", 'message': messages.get("site_not_assined_yet")}, status=status.HTTP_404_NOT_FOUND)
        sites_lat_lon = []
        sites_details = []  # site object
        for i in sites:
            sites_lat_lon.append(
                                (i.fld_latitude, i.fld_longitude))
            sites_details.append(i)  # site object
            # print((i.fld_latitude, i.fld_longitude))

        print(f'sites_details == {sites_details}')

        for value in values:
            ip_address = value.get('ip_address')
            if validate_ip_address(ip_address) is None:
                response_text_file(
                    user=user, value={"status": "error", 'message': messages.get("ip_error")})
                return Response({"status": "error", 'message': messages.get("ip_error")}, status=status.HTTP_400_BAD_REQUEST)

            if isValidIMEI(int(value.get('imei_number'))) is False:
                response_text_file(
                    user=user, value={"status": "error", 'message': messages.get("IMEI_error")})
                return Response({"status": "error", 'message': messages.get("IMEI_error")}, status=status.HTTP_400_BAD_REQUEST)

            obj = check_device(user, value.get(
                'device_model'), value.get('imei_number'))

            if obj is not None:
                data = {}
                data["fld_attendance_status"] = value.get("attendance_status")
                data["fld_latitude"] = value.get("latitude")
                data["fld_longitude"] = value.get("longitude")
                data["fld_date"] = value.get("date")
                data["fld_time"] = value.get("time")
                data["fld_user_id"] = user
                data["fld_ip_address"] = ip_address
                data["visit_id"] = f'OMCVISIT_{value.get("date")}_{user}'
                # print(data["fld_time"])
                current_data_lat_lon = (
                    data["fld_latitude"], data["fld_longitude"])
                try:
                    previous_data = TblAttendance.objects.filter(
                        fld_user_id=user, fld_date=data["fld_date"]).last()
                except:
                    previous_data = None
                if previous_data:
                    print(f'previous_data is available')
                    # attendance_log, created = TblAttendanceLog.objects.get_or_create(
                    #     user_id=request.user, date=data["fld_date"], visit_id=data["visit_id"])
                    previous_data_lat_lon = (
                        previous_data.fld_latitude, previous_data.fld_longitude)
                    # current_data_lat_lon = (
                    #     data["fld_latitude"], data["fld_longitude"])
                    serializer = TblAttendanceSerializer(
                        data=data)
                    if serializer.is_valid():
                        serializer.save()
                    else:
                        response_text_file(user=user, value=serializer.errors)
                        # print(serializer.errors)
                        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

                    user_reimbursement, created = TblUserReimbursements.objects.get_or_create(
                        user_id=request.user, date=data["fld_date"], visit_id=data["visit_id"])
                    distance_calculated = total_distance(
                        [previous_data_lat_lon, current_data_lat_lon])
                    # previous_distance = user_reimbursement.distance
                    # user_reimbursement.distance = previous_distance + distance_calculated
                    user_reimbursement.distance += distance_calculated
                    user_reimbursement.save()
                    if is_arrived(current_data_lat_lon, sites_lat_lon) is not None:
                        value_for_list = is_arrived(
                            current_data_lat_lon, sites_lat_lon)  # return just index position.
                        # caution point :-site_id = sites_details[value_for_list]
                        # be sure to verify
                        print(f'value_for_list == {value_for_list}')

                        user_attendence_log, created = TblAttendanceLog2.objects.get_or_create(
                            user_id=request.user, site_id=sites_details[value_for_list], date=data["fld_date"], visit_id=data["visit_id"])

                        if user_attendence_log.start_latitude:
                            user_attendence_log.end_latitude = data["fld_latitude"]
                            user_attendence_log.end_longitude = data["fld_longitude"]
                            user_attendence_log.end_time = data["fld_time"]
                            user_attendence_log.save()

                        else:
                            user_attendence_log.start_latitude = data["fld_latitude"]
                            user_attendence_log.start_longitude = data["fld_longitude"]
                            user_attendence_log.start_time = data["fld_time"]
                            user_attendence_log.end_latitude = data["fld_latitude"]
                            user_attendence_log.end_longitude = data["fld_longitude"]
                            user_attendence_log.end_time = data["fld_time"]
                            user_attendence_log.save()

                        """
                            start_latitude=data["fld_latitude"], start_longitude=data["fld_longitude"], end_latitude=data["fld_latitude"], end_longitude=data["fld_longitude"],start_time=data["fld_time"], end_time=data["fld_time"],
                        """
                else:
                    if data["fld_attendance_status"] == "check_in":
                        print(f'previous_data is not available')
                        serializer = TblAttendanceSerializer(
                            data=data)
                        if serializer.is_valid():
                            serializer.save()
                            user_reimbursement, created = TblUserReimbursements.objects.get_or_create(
                                user_id=request.user, date=data["fld_date"], visit_id=data["visit_id"], distance=0)

                            print(current_data_lat_lon,
                                  sites_lat_lon, user_reimbursement)

                            if is_arrived(current_data_lat_lon, sites_lat_lon) is not None:
                                value_for_list = is_arrived(
                                    current_data_lat_lon, sites_lat_lon)  # return just index position.
                                # caution point :-site_id = sites_details[value_for_list]
                                # be sure to verify
                                print(
                                    f'site_id = {sites_details[value_for_list]}')
                                user_attendence_log, created = TblAttendanceLog2.objects.get_or_create(
                                    user_id=request.user, site_id=sites_details[value_for_list], date=data["fld_date"], visit_id=data["visit_id"], start_latitude=data["fld_latitude"], start_longitude=data["fld_longitude"], end_latitude=data["fld_latitude"], end_longitude=data["fld_longitude"], start_time=data["fld_time"], end_time=data["fld_time"])

                                print("from else")

                        else:
                            response_text_file(
                                user=user, value=serializer.errors)
                            # print(serializer.errors)
                            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

                    else:
                        response_text_file(
                            user=user, value={
                                "status": "error", 'message': messages.get("check_in_first")})
                        # print(serializer.errors)
                        return Response({
                            "status": "error", 'message': messages.get("check_in_first")}, status=status.HTTP_400_BAD_REQUEST)

            else:
                response_text_file(user=user, value={
                    "status": "error", 'message': messages.get("device_information_error")})
                return Response({"status": "error", 'message': messages.get("device_information_error")}, status=status.HTTP_404_NOT_FOUND)

        response_text_file(user=user, value={
            "status": "success", 'message': messages.get("data_created")})
        return Response({"status": "success", 'message': messages.get("data_created")}, status=status.HTTP_200_OK)


class UserReimbursementsView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        request_text_file(user=request.user.id, value=request.data)
        query_set = TblUserReimbursements.objects.filter(
            user_id=request.user, date__gte=datetime.now()-timedelta(days=7))
        serializer = UserReimbursementsSerializer(query_set, many=True)
        response_text_file(user=request.user.id, value={
            "status": "success", 'message': serializer.data})
        return Response({"status": "success", 'message': serializer.data}, status=status.HTTP_200_OK)
