from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated

from authuser.serializers.userserializer import UserCreateSerializer, UserLoginSerializer, UserSerializer
from authuser.models import User
from tickets.serializers import CreateTicketSerializer, UpdateTicketSerializer
from tickets.models import Tickets

class UserListView(APIView):
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user = request.user
        print(user.roles)
        # if user.roles != 'admin' or user.roles != 'supadmin': #RBAC 
        #     response = {
        #         'success': False,
        #         'status_code': status.HTTP_403_FORBIDDEN,
        #         'message': 'You are not authorized to perform this action'
        #     }
        #     return Response(response, status.HTTP_403_FORBIDDEN)
        # else:
        if user.roles == 'supadmin' or user.roles == 'admin':
            users = User.objects.all()
            serializer = self.serializer_class(users, many=True)
            response = {
                'success': True,
                'status_code': status.HTTP_200_OK,
                'message': 'Successfully fetched users',
                'users': serializer.data

            }
            return Response(response, status=status.HTTP_200_OK)

        else:
            response = {
                'success': False,
                'status_code': status.HTTP_403_FORBIDDEN,
                'message': 'You are not authorized to perform this action'
            }
            return Response(response, status.HTTP_403_FORBIDDEN)

class UserCreateAPIView(generics.CreateAPIView):
    serializer_class = UserCreateSerializer
    queryset = User.objects.all()


class UserLoginAPIView(APIView):
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = UserLoginSerializer(data=data)
        # if not serializer.is_valid():
        #     raise ValidationError(serializer.errors)
        if serializer.is_valid(raise_exception=True):
            new_data = serializer.data
            return Response(new_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CreateTicket(generics.CreateAPIView):
    queryset = Tickets.objects.all()
    serializer_class = CreateTicketSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class UpdateTicketValidation(generics.UpdateAPIView):
    queryset = Tickets.objects.all()
    serializer_class = UpdateTicketSerializer
    permission_classes = (IsAuthenticated,)

    def update(self, request, *args, **kwargs):
        user = request.user
        if user.roles == 'admin' or user.roles == 'supadmin':
            instance = self.get_object()
            instance.ticket_approved = request.data.get("ticket_approved")
            instance.save()

            serializer = self.get_serializer(instance)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)

            response = {
                'success': True,
                'status_code': status.HTTP_200_OK,
                'message': 'Successfully updated ticket',
                'users': serializer.data

            }

            return Response(response, status=status.HTTP_200_OK)
        else:
            response = {
                'success': False,
                'status_code': status.HTTP_403_FORBIDDEN,
                'message': 'You are not authorized to perform this action'
            }
            return Response(response, status.HTTP_403_FORBIDDEN)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)