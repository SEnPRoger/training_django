from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from account.serializers import *
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
from django.middleware import csrf
from JWTAuth.views import JWTToken
import requests
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.
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
            JWTToken.set_refresh_to_header(response, refresh_token, header_name='refresh_token')
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
                JWTToken.set_refresh_to_header(response, refresh_token, header_name='REFRESH-TOKEN')
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

        # raw_refresh_token = JWTToken.get_refresh_token(request, cookie_name='refresh_token')
        # raw_access_token = JWTToken.get_access_token(request)
        
        # response = Response(
        #         data={'status':'success',
        #                 'refresh': raw_refresh_token,
        #                 'access': raw_access_token},
        #                 status=status.HTTP_200_OK
        #         )

        serializer = AccountDetailSerializer(request.user)
        response = Response({'account':serializer.data},
                            status=status.HTTP_200_OK)
        
        response['X-CSRFToken'] = csrf.get_token(request)
        return response
    
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