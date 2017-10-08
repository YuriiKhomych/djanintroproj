from django.shortcuts import render
from django.http import JsonResponse
from django.core.mail import send_mail
from django.contrib.auth import authenticate, login, logout

from utils import random_word
from utils import gen_page_list


from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework.authtoken.models import Token
from rest_framework.pagination import PageNumberPagination
from accounts.models import User


from .serializers import (UserLoginSerializer, UserSerializer,
    UserCreationSerializer, UserChangePasswordSerializer,
    UserMainInfoSerializer, UserRegistrationSerializer,
    MyUserChangePasswordSerializer, UserForgetPasswordSerializer,
    UserShortInfoSerializer)


# accounts API view
class UsersView(GenericAPIView):
    """
    Get all info about users
    """
    serializer_class = UserSerializer

    def get_queryset(self):
        return User.objects.all().order_by('id')

    def get(self, request, *args, **kwargs):
        if kwargs.get('pk'):
            user = self.get_object()
            serializer = self.serializer_class(user)
            return Response(serializer.data)
        else:
            return self.list(request)

    def list(self, request):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)


class UserShortInfoAPI(ListAPIView):
    """
    This view will return response with
    short information(id, username, email, date_joined) about all users,
    and divided into 10 users objects at the one page.
    """
    queryset = User.objects.all()
    serializer_class = UserShortInfoSerializer
    pagination_class = PageNumberPagination


class UserLoginAPI(APIView):
    """
    This view will check input user email and password then,
     if data is valid, login him in system
    end send back response with user basic information:
     username, email, first_name, date_joined.
    """
    serializer_class = UserLoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if request.user.is_authenticated():
            return Response({'Sorry, you are already login'},
                            status=status.HTTP_409_CONFLICT)
        else:
            if serializer.is_valid():
                validate_data = serializer.validated_data
                # authenticate user
                user = authenticate(email=validate_data.get('email'),
                                    password=validate_data.get('password'))
                if user:
                    # collect information about user
                    user_data = User.objects.get(
                        email__iexact=validate_data.get('email'))
                    context = {
                        'username': user_data.username,
                        'email': user_data.email,
                        'first_name': user_data.first_name,
                        'date_joined': user_data.date_joined,
                        }
                    return Response(context)
                else:
                    return 'User does not exist'
            else:
                return Response(
                    serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST
                )


class UserRegistrationAPI(APIView):
    """
    This view will check input user name, email,
    password then, if data is valid, create new user, login him in system
    and send back response with user Token.
    """
    serializer_class = UserRegistrationSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        # Add permission class in future
        if request.user.is_authenticated():
            return Response({'Sorry, you are registered'},
                            status=status.HTTP_409_CONFLICT)
        else:
            if serializer.is_valid():
                validate_data = serializer.validated_data
                # create user
                user = User.objects.create_user(
                    username=validate_data.get('username'),
                    email=validate_data.get('email'),
                )
                user.set_password(validate_data.get('password'))
                user.save()
                # login user
                login(request, authenticate(
                    email=validate_data.get('email'),
                    password=validate_data.get('password')))
                # create token
                token = Token.objects.create(user=user)
                return JsonResponse(token.key)
            else:
                return Response(
                    serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST)


class UserForgetPasswordAPI(APIView):
    """
    This view will check input user name or email,
    then generate new password and sent it to user email.
    """
    serializer_class = UserForgetPasswordSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            validate_data = serializer.validated_data
            # find user object
            if '@' in validate_data.get('email_or_username'):
                user = User.objects.get(
                    email=validate_data.get('email_or_username'))
            else:
                user = User.objects.get(
                    username=validate_data.get('email_or_username'))
            # generate and password
            password = random_word(10)
            user.set_password(password)
            user.save()
            # send mail
            send_mail('Your new password',
                      'Hi, it\'s you new password: {}'.format(password),
                      'yuriykhomich@gmail.com',
                      [user.email]
                      )
            return Response({'success': True})
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)


class ChangeUserPasswordView(APIView):
    serializer_class = MyUserChangePasswordSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        serializer = self.serializer_class(
            data=request.data,
            context={'user': request.user})
        if serializer.is_valid():
            validated_data = serializer.validated_data
            request.user.set_password(validated_data.get('new_password'))
            request.user.save()
            return Response({'success': True})
        else:
            return Response(serializer.errors)

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)


class MainUserFieldsView(APIView):
    serializer_class = UserMainInfoSerializer

    def post(self, request):
        username = request.data.get('email', None)
        password = request.data.get('password', None)
        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                user_info = {
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "email": user.email,
                    "username": user.username
                }
                return Response(user_info)
            else:
                return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)
