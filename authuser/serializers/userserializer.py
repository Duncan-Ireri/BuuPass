from rest_framework import serializers
from .. import models
import re
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.contrib.auth.models import User, update_last_login
from dj_rest_auth.registration.serializers import RegisterSerializer
from django.db import transaction

class UserSerializer(serializers.ModelSerializer):
    """
    USER SERIALIZER WITH ROLES Method INJECTED (DEPENDANCY INJECTION)
    """
    roles = serializers.SerializerMethodField()

    def get_roles(self, obj):
        return obj.roles.values()

    class Meta:
        model = models.User
        fields = '__all__'
        depth = 1

class UserModifySerializer(serializers.ModelSerializer):
    '''
    SERIALIZER TO CHECK PHONE NUMBER VALIDATION
    '''
    phone_number = serializers.CharField(max_length=15)

    class Meta:
        model = models.User
        fields = ['id', 'first_name', 'last_name', 'email', 'image',  'supervisor',
                 'roles', 'phone_number']

    def validate_mobile(self, phone_number):
        REGEX_PHONE = "^0(7(?:(?:[129][0-9])|(?:0[0-8])|(4[0-1]))[0-9]{6})$" # CHANGE THIs TO ANY FORMAT, THIS CHECKS FOR 07xxxxxxxx
        if not re.match(REGEX_PHONE, phone_number):
            raise serializers.ValidationError("INVALID PHONE NUMBER")
        return phone_number


# class UserCreateSerializer(serializers.ModelSerializer): TODO: FIX THIS THROWING A FALSR POSITIVE BECAUSE OF USERNAME
#     '''
#     CREATE USER
#     '''
#     email = serializers.CharField(required=True, allow_blank=False)
#     phone_number = serializers.CharField(max_length=11)

#     class Meta:
#         model = models.User
#         fields = ['id', 'first_name', 'last_name', 'email', 'image',
#                   'phone_number', 'password']

#     def validate_email(self, email):
#         if models.User.objects.filter(email=email):
#             raise serializers.ValidationError(email + ' NOT VALID EMAIL')
#         return email

#     def validate_mobile(self, phone_number):
#         REGEX_PHONE = "^0(7(?:(?:[129][0-9])|(?:0[0-8])|(4[0-1]))[0-9]{6})$" #TODO: CHANGE THIs TO ANY FORMAT, THIS CHECKS FOR 07xxxxxxxx
#         if not re.match(REGEX_PHONE, phone_number):
#             raise serializers.ValidationError("ERROR")
#         if models.User.objects.filter(phone_number=phone_number):
#             raise serializers.ValidationError("ERROR") #TODO: BETTER EXCEPTION ERROR
#         return phone_number

#     def create(self, validated_data):
#         auth_user = models.User.objects.create_user(**validated_data)
#         return auth_user


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = (
            'first_name',
            'last_name',
            'phone_number',
            'username',
            'email',
            'password',
            # 'image',   # NOT PLAYING NICE WITH HEROKU

        )

    def create(self, validated_data):
        auth_user = models.User.objects.create_user(**validated_data)
        return auth_user

class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(max_length=128, write_only=True)
    access = serializers.CharField(read_only=True)
    roles = serializers.CharField(read_only=True)
    refresh = serializers.CharField(read_only=True)

    def create(self, validated_date):
        pass

    def update(self, instance, validated_data):
        pass

    def validate(self, data):
        email = data['email']
        password = data['password']
        user = authenticate(email=email, password=password)

        if user is None:
            raise serializers.ValidationError("Invalid login credentials")

        try:
            refresh = RefreshToken.for_user(user)
            refresh_token = str(refresh)
            access_token = str(refresh.access_token)

            update_last_login(None, user)

            validation = {
                'access': access_token,
                'refresh': refresh_token,
                'email': user.email,
                'roles': user.roles,
            }

            return validation
        except User.DoesNotExist:
            raise serializers.ValidationError("Invalid login credentials")

class AuthUserRegisterSerializer(RegisterSerializer):
    first_name = serializers.CharField(max_length=30)
    last_name = serializers.CharField(max_length=30)
    # phone_number = serializers.CharField(max_length=30)

    # Define transaction.atomic to rollback the save operation in case of error
    @transaction.atomic
    def save(self, request):
        user = super().save(request)
        user.first_name = self.data.get('first_name')
        user.last_name = self.data.get('last_name')
        # user.phone_number = self.data.get('phone_number')
        user.save()
        return user

class AuthUserDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.User
        fields = (
            'email',
            # 'phone_number',
            'first_name',
            'last_name',
        )
        read_only_fields = ('email', 'first_name', 'last_name')