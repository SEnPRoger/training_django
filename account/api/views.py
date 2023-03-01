from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from account.api.serializers import *
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import FileUploadParser
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime, timedelta
from django.utils import timezone
from django.utils.timezone import localdate
import requests
from pathlib import Path
from django.conf import settings
import datetime, time
from JWTAuth.views import JWTToken
from account.models import Account
from django.middleware import csrf

class AccountRegister(APIView):
    def post(self, request, format=None):
        serializer = AccountRegisterSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            try:
                serializer.validated_data['country'], serializer.validated_data['city'] = self.get_location_by_ip(request)
            except KeyError:
                pass
            account = serializer.save()

            refresh_token, access_token = JWTToken.generate_tokens(user_id=account.id)
            response = Response({'status':'successfully registered',
                            'access_token':access_token},
                            status=status.HTTP_200_OK)
            JWTToken.set_refresh_to_cookie(response, refresh_token, cookie_name='refresh_cookie')
            response['X-CSRFToken'] = csrf.get_token(request)
            return response
        else:
            return Response({'status':'register failed',
                         'error':serializer.errors},
                        status=status.HTTP_400_BAD_REQUEST)
    
    GEOLOCATION_API_KEY = "668139cd225e4b99a80573fe0aba97eb"

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    def get_location_by_ip(self, request):
        ip = self.get_client_ip(request)
        response = requests.get("https://api.ipgeolocation.io/ipgeo?apiKey={0}&ip={1}".format(self.GEOLOCATION_API_KEY, ip))
        ip_location = response.json()
        return ip_location['country_name'], ip_location['city']

class AccountLogin(APIView):
    def post(self, request, format=None):
        serializer = AccountLoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):

            username_or_email = serializer.data.get('username_or_email')
            password = serializer.data.get('password')

            account = authenticate(username=username_or_email, password=password)
            if account is not None:
                refresh_token, access_token = JWTToken.generate_tokens(user_id=account.id)
                response = Response({'status':'successfully logged',
                                'access_token':access_token},
                                status=status.HTTP_200_OK)
                JWTToken.set_refresh_to_cookie(response, refresh_token, cookie_name='refresh_cookie')
                response['X-CSRFToken'] = csrf.get_token(request)
                return response
            else:
                return Response({'status':'account not found!'},
                                    status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'status':'login failed',
                         'error':serializer.errors},
                        status=status.HTTP_400_BAD_REQUEST)

class AccountProfile(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, format=None):
        serializer = AccountDetailSerializer(request.user)
        response = Response({'account':serializer.data},
                            status=status.HTTP_200_OK)
        
        response['X-CSRFToken'] = csrf.get_token(request)
        return response

class AccountPhotoUpload(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        # set 'data' so that you can use 'is_vaid()' and raise exception
        # if the file fails validation
        serializer = AccountPhotoUploadSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            # once validated, grab the file from the request itself
            file = request.FILES['file']
            extension = str(file).split('.')[1]
            
            if extension == 'gif' and request.user.is_moderator == False:
                return Response({'status':'you cannot upload gif as account photo'},
                                status=status.HTTP_403_FORBIDDEN)
            else:
                account = Account.objects.get(id=request.user.id)
                if account.photo != None:
                    account.photo.delete()
                account.photo = file
                account.save()

                return Response({'status':'successfully uploaded photo'},
                                    status=status.HTTP_200_OK)

class AccountChangeUsername(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, format=None):
        serializer = AccountChangeUsernameSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            account = Account.objects.get(id=request.user.id)
            username = serializer.data.get('username')
            try:
                check_available_username = Account.objects.get(username=username)
            except ObjectDoesNotExist:
                if (timezone.now() - account.changed_username) < timedelta(days=1):
                    return Response({'status':'username change available once at day'},
                        status=status.HTTP_400_BAD_REQUEST)
                account.username = username
                account.changed_username = datetime.now()
                account.save()
                return Response({'status':'successfully changed nickname',
                             'username':account.username},
                    status=status.HTTP_200_OK)

class AccountChangePassword(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, format=None):
        serializer = AccountChangePasswordSerializer(data=request.data, context={'user':request.user})
        if serializer.is_valid(raise_exception=True):
            password = serializer.data.get('password')
            password2 = serializer.data.get('password2')
            
            if password == password2:
                return Response({'status':'successfully changed password'},
                        status=status.HTTP_200_OK)
            return Response({'status':'fail',
                         'error':serializer.errors},
                        status=status.HTTP_200_OK)

class AccountLogout(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, format=None):
        response = Response({'msg':'successfully logout from account!'},
                            status=status.HTTP_200_OK)
        
        response.delete_cookie('refresh_cookie')
        response.delete_cookie('X-CSRFToken')
        return response
    
class AccountDelete(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, format=None):
        account = Account.objects.get(id=request.user.id)
        account.delete()
        return Response({'status':'success'},
                        status=status.HTTP_200_OK)
        
class AccountCheckUsernameAvailable(APIView):
    def get(self, request, format=None):
        serializer = AccountChangeUsernameSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            entered_username = serializer.data.get('username')
            try:
                username_check = Account.objects.get(username=entered_username)
                return Response({'status':'username is not available'},
                                status=status.HTTP_200_OK)
            except ObjectDoesNotExist:
                if len(entered_username) > 3:
                        return Response({'status':'username available'},
                                        status=status.HTTP_200_OK)
                else:
                        return Response({'status':'username should be have more then 3 characters'},
                                        status=status.HTTP_200_OK)
        return Response({'status':'fail',
                         'error':serializer.errors},
                        status=status.HTTP_400_BAD_REQUEST)
    
class AccountCheckEmailAvailable(APIView):
    def get(self, request, format=None):
        serializer = AccountCheckEmailAvailableSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            entered_email = serializer.data.get('email')
            try:
                email_check = Account.objects.get(email=entered_email)
                return Response({'status':'email is not available'},
                                                status=status.HTTP_200_OK)
            except ObjectDoesNotExist:
                return Response({'status':'email available'},
                                        status=status.HTTP_200_OK)
        return Response({'status':'fail',
                         'error':serializer.errors},
                        status=status.HTTP_400_BAD_REQUEST)
    
class AccountGetAnother(APIView):
    def get(self, request, username=None, format=None):
        try:
            account = Account.objects.get(username=username)
            if account is not None:
                return Response({'status':'successfully got account',
                                'account':{
                                        'username': account.username,
                                        'photo': account.get_image(),
                                        'is_moderator': account.is_moderator,
                                        'created_at': self.get_normal_created_at_datetime(account)
                                    }
                                },status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response({'status':'account not found!'},
                                        status=status.HTTP_404_NOT_FOUND)
    
    def get_normal_created_at_datetime(self, obj):
        return timezone.localtime(obj.created_at).strftime('%d %B %Y %H:%M')

class AccountGetTrash(APIView):
    def get(self, request, format=None):
        response = Response({'status':'success wtf'},status=status.HTTP_200_OK)
        response.set_cookie(key = 'fuck',
                            value = 'wtf is going on here',
                            expires = 2147483647,
                            samesite = 'None',
                            secure = True,
                            httponly = True)
        response.set_cookie(key = 'http_off',
                            value = 'http_off',
                            expires = 2147483647,
                            samesite = 'None',
                            secure = True)
        response.set_cookie(key = 'http_off',
                            value = 'http_off',
                            expires = 2147483647,
                            samesite = 'None',
                            path='/sign_in',
                            secure = True)
        return response

# class AccountSendEmailResetPassword(APIView):
#     def post(self, request, format=None):
#         serializer = AccountSendResetPasswordSerializer(data=request.data)
#         if serializer.is_valid(raise_exception=True):
#             return Response({'status':'success',
#                          'msg':'Password reset link sent. Check your Email'},
#                         status=status.HTTP_200_OK)
#         return Response({'status':'fail',
#                          'error':serializer.errors},
#                         status=status.HTTP_400_BAD_REQUEST)
    
# class AccountResetPassword(APIView):
#     def post(self, request, uid, token, format=None):
#         serializer = AccountResetPasswordSerializer(data=request.data,
#                                                      context={'uid':uid, 'token':token})
#         if serializer.is_valid(raise_exception=True):
#             return Response({'status':'success'},
#                         status=status.HTTP_200_OK)
#         return Response({'status':'fail',
#                          'error':serializer.errors},
#                         status=status.HTTP_400_BAD_REQUEST)