from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from django.contrib.auth import logout
from account.models import Account

from rest_framework.views import APIView
from rest_framework.exceptions import AuthenticationFailed
import jwt, datetime
import requests

from account.api.serializers import AccountSerializer

GEOLOCATION_API_KEY = "668139cd225e4b99a80573fe0aba97eb"

class RegisterView(APIView):
    def post(self, request):
        serializer = AccountSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
class LoginView(APIView):
    def post(self, request):

        ip = request.META.get('HTTP_X_FORWARDED_FOR', request.META.get('REMOTE_ADDR', '')).split(',')[0].strip()

        auth = ''

        if 'username' in request.data:
            auth = request.data['username']
            user = Account.objects.get(username=auth)
        else:
            auth = request.data['email']
            user = Account.objects.get(email=auth)

        password = request.data['password']

        if user is None:
            raise AuthenticationFailed('User not found')
        if not user.check_password(password):
            raise AuthenticationFailed('Incorrect password')
        
        payload = {
            'id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.utcnow() 
        }

        token = jwt.encode(payload, 'secret', algorithm='HS256').decode('utf-8')

        response = Response()
        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data = {
            'message': 'success',
            'ip': ip,
            'jwt': token
        }
        return response
    
class UserView(APIView):
    def get(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated connection')
        
        try:
            payload = jwt.decode(token, 'secret', algorithm=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated connection')
        
        user = Account.objects.get(id=payload['id'])
        serializer = AccountSerializer(user)

        return Response(serializer.data)
    
class APItest(APIView):
    def get(request):
        return Response({"ip": get_client_ip(request),
                        "country": get_location_by_ip(request)})

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def get_location_by_ip(request):
    ip = get_client_ip(request)
    response = requests.get("https://api.ipgeolocation.io/ipgeo?apiKey={0}&ip={1}".format(GEOLOCATION_API_KEY, ip))
    ip_location = response.json()
    return ip_location["country_name"]

class LogoutView(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message' : 'success'
        }
        return response

# @api_view(['POST',])
# def registration_view(request):
#     if request.method == 'POST':
#         serializer = RegistrationSerializer(data=request.data)
#         data = {}
#         if serializer.is_valid():
#             account = serializer.save()
#             data['status'] = "User has been registered"
#             token = Token.objects.get(user=account).key
#             data['token'] = token
#         else:
#             data['status'] = serializer.errors
#         return Response(data)
    
# @api_view(['POST',])
# def username_available_view(request):
#     if request.method == 'POST':
#         username = request.data["username"]
#         data = {}
#         if Account.objects.filter(username = username).exists():
#             data['available'] = "This username has already used"
#         else:
#             data['available'] = "Username can be used"
            
#         return Response(data)
    
# @api_view(['POST',])
# def email_available_view(request):
#     if request.method == 'POST':
#         email = request.data["email"]
#         data = {}
#         if Account.objects.filter(email = email).exists():
#             data['available'] = "This email has already used"
#         else:
#             data['available'] = "Email can be used"
            
#         return Response(data)
    
# @api_view(["POST"])
# @permission_classes([IsAuthenticated])
# def logout_view(request):
#     request.user.auth_token.delete()
#     logout(request)

#     return Response('User Logged out successfully')

# class LoginView(APIView):
#     def post(self, request):
#         email = request.data['email']
#         password = request.data['password']

#         user = Account.objects.get(email=email)

#         # if email != None:
#         #     user = Account.objects.get(email=email)
#         # else:
#         #     username = request.data['username']
#         #     user = Account.objects.get(username=username)

#         if user is None:
#             raise AuthenticationFailed('User not found')
#         if not user.check_password(password):
#             raise AuthenticationFailed('Incorrect password')
        
#         payload = {
#             'id': Account.id,
#             'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
#             'iat': datetime.datetime.utcnow() 
#         }

#         token = jwt.encode(payload, 'secret', algorithm='HS256').decode('utf-8')
        
#         return Response({'message': 'success', 'jwt': token})