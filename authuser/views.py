from django.shortcuts import render
from . import models
from .serializers import userserializer
# Create your views here.
from rest_framework import generics, serializers
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated

from .models import User, AuthPermissions, Role
from .serializers import permissionserializer, userserializer, roleserializers

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


# class UserListView(generics.ListAPIView): # TODO: CHANGE TO APIVIEW
#     queryset = models.User.objects.all()
#     serializer_class = userserializer.UserSerializer

class AuthUserCreateView(APIView):
    serializer_class = userserializer.UserCreateSerializer
    permission_classes = (AllowAny, )

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        valid = serializer.is_valid(raise_exception=True)

        if valid:
            serializer.save()
            status_code = status.HTTP_201_CREATED

            response = {
                'success': True,
                'statusCode': status_code,
                'message': 'Registred Successfully',
                'user': serializer.data
            }

            return Response(response, status=status_code)

class AuthUserLoginView(APIView):
    serializer_class = userserializer.UserLoginSerializer
    permission_classes = (AllowAny, )

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        valid = serializer.is_valid(raise_exception=True)

        if valid:
            status_code = status.HTTP_200_OK

            response = {
                'success': True,
                'statusCode': status_code,
                'message': 'User logged in successfully',
                'access': serializer.data['access'],
                'refresh': serializer.data['refresh'],
                'authenticatedUser': {
                    'email': serializer.data['email'],
                    'roles': serializer.data['roles']
                }
            }

            return Response(response, status=status_code)


class UserListView(APIView):
    serializer_class = userserializer.UserSerializer
    permission_classes = (IsAuthenticated,)

    @swagger_auto_schema(responses={200: userserializer.UserSerializer(many=True)})
    def get(self, request):
        user = request.user
        if user.roles != 'admin' or user.roles != 'supadmin':
            response = {
                'success': False,
                'status_code': status.HTTP_403_FORBIDDEN,
                'message': 'You are not authorized to perform this action'
            }
            return Response(response, status.HTTP_403_FORBIDDEN)
        else:
            users = User.objects.all()
            serializer = self.serializer_class(users, many=True)
            response = {
                'success': True,
                'status_code': status.HTTP_200_OK,
                'message': 'Successfully fetched users',
                'users': serializer.data

            }
            return Response(response, status=status.HTTP_200_OK)