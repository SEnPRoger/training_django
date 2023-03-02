from rest_framework import serializers
from account.models import Account
from django.core.exceptions import ValidationError
from django.utils.encoding import smart_str, force_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils import timezone

class AccountRegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type':'password'}, write_only=True)

    class Meta:
        model = Account
        fields = ['username', 'email', 'password', 'password2']
        extra_kwargs = {
            'password' : {'write_only':True}
        }
    
    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')

        if password != password2:
            raise serializers.ValidationError('Both passwords should be equal')
        return attrs
    
    def create(self, validate_data):
        return Account.objects.create_user(**validate_data)
    
class AccountLoginSerializer(serializers.ModelSerializer):
    username_or_email = serializers.CharField(max_length=32)

    class Meta:
        model = Account
        fields = ['username_or_email', 'password']

class AccountDetailSerializer(serializers.ModelSerializer):
    photo = serializers.SerializerMethodField('get_account_photo')
    created_at = serializers.SerializerMethodField('get_normal_created_at_datetime')
    changed_username = serializers.SerializerMethodField('get_normal_changed_username_datetime')

    def get_account_photo(self, obj):
        return obj.get_image()
    
    def get_normal_created_at_datetime(self, obj):
        return timezone.localtime(obj.created_at).strftime('%d %B %Y %H:%M')
    
    def get_normal_changed_username_datetime(self, obj):
        return timezone.localtime(obj.changed_username).strftime('%d %B %Y %H:%M')

    class Meta:
        model = Account
        fields = ['username', 'email', 'photo', 'is_moderator', 'created_at', 'changed_username']

class AccountChangePasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=88, style={'input_type':'password'}, write_only=True)
    password2 = serializers.CharField(max_length=88, style={'input_type':'password'}, write_only=True)

    class Meta:
        model = Account
        fields = ['password', 'password2']

    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        user = self.context.get('user')

        if password != password2:
            raise serializers.ValidationError('Both passwords should be equal')
        
        user.set_password(password)
        user.save()
        return attrs
    
class AccountSendResetPasswordSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=32)
    
    class Meta:
        model = Account
        fields = ['email']

    def validate(self, attrs):
        email = attrs.get('email')
        if Account.objects.filter(email=email).exists():
            account = Account.objects.get(email=email)
            uid = urlsafe_base64_encode(force_bytes(account.id))
            token = PasswordResetTokenGenerator().make_token(account)
            link = 'http://127.0.0.1:8000/api/account/reset_password/'+uid+'/'+token

            print('Encoded UID', uid)
            print('Password Reset Token', token)
            print('Password Reset Link', link)
            return attrs
        else:
            raise serializers.ValidationError('You are not auth user!')
        
class AccountResetPasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=88, style={'input_type':'password'}, write_only=True)
    password2 = serializers.CharField(max_length=88, style={'input_type':'password'}, write_only=True)

    class Meta:
        model = Account
        fields = ['password', 'password2']

    def validate(self, attrs):
        try:
            password = attrs.get('password')
            password2 = attrs.get('password2')
            uid = self.context.get('uid')
            token = self.context.get('token')

            if password != password2:
                raise serializers.ValidationError('Both passwords should be equal')
            
            id = smart_str(urlsafe_base64_decode(uid))
            account = Account.objects.get(id=id)

            if not PasswordResetTokenGenerator().check_token(account, token):
                raise ValidationError('Token is not valid')
            
            account.set_password(password)
            account.save()
            return attrs
        except DjangoUnicodeDecodeError as identifier:
            PasswordResetTokenGenerator().check_token(account, token)
            raise ValidationError('Token is not valid')
        
class AccountPhotoUploadSerializer(serializers.Serializer):
    file = serializers.ImageField()

class AccountChangeUsernameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['username']

class AccountCheckEmailAvailableSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=32)
    class Meta:
        fields = ['email']