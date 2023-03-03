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
        fields = ['username', 'email', 'photo', 'created_at', 'is_moderator', 'changed_username']

class AccountPhotoUploadSerializer(serializers.Serializer):
    file = serializers.ImageField()