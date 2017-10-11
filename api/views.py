from django.shortcuts import render
from django.http import JsonResponse
from django.core.mail import send_mail
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q
from django.shortcuts import get_object_or_404


from utils import random_word
from utils import gen_page_list

from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework.authtoken.models import Token
from rest_framework.pagination import PageNumberPagination, \
    LimitOffsetPagination

from accounts.models import User
from blog.models import Article
from trips.models import Trip

from .serializers import (UserLoginSerializer,
                          UserSerializer,
                          UserMainInfoSerializer,
                          UserRegistrationSerializer,
                          MyUserChangePasswordSerializer,
                          UserForgetPasswordSerializer,
                          UserShortInfoSerializer,
                          ArticleSerializer,
                          ArticleFullDataSerializer,
                          ArticleCreateSerializer,
                          ArticleRemoveSerializer,
                          ArticleSearchSerializer,
                          TripCreateSerializer,
                          TripFullDataSerializer,
                          TripRemoveSerializer,
                          TripSearchSerializer,
                          TripSerializer
                          )


# accounts API view
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
            return Response({'Success': False}, status=status.HTTP_400_BAD_REQUEST)
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
                return Response({'token': token.key})
            else:
                return Response(
                    serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST)


class UserShortInfoAPI(ListAPIView):
    """
    This view will return response with
    short information(id, username, email, date_joined) about all users,
    and divided into 10 users objects at the one page.
    """
    queryset = User.objects.all()
    serializer_class = UserShortInfoSerializer
    pagination_class = PageNumberPagination


class UsersViewAPI(GenericAPIView):
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


class UserLoginAPI(APIView):
    # Serializer not valid
    """
    This view will check input user email and password, after that
     if data is valid, login him in system
     and send back response with user basic information:
     username, email, first_name, date_joined.
    """
    serializer_class = UserLoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if request.user.is_authenticated():
            return Response({'Sorry, you are already login'},
                            status=status.HTTP_400_BAD_REQUEST)
        else:
            if serializer.is_valid():
                validate_data = serializer.validated_data

                user = get_object_or_404(User, email=validate_data.get('email'))
                Token.objects.get_or_create(user=user)
                token = get_object_or_404(Token, user=user)

                # authenticate user
                authenticate(email=validate_data.get('email'),
                             password=validate_data.get('password'))

                return Response({'token': token.key})
            else:
                return Response(
                    serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST
                )


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


class ChangeUserPasswordAPI(APIView):
    """
        User can change old password to new.
    """
    serializer_class = MyUserChangePasswordSerializer
    permission_classes = IsAuthenticated

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


# blog API
class ArticlesView(GenericAPIView):
    serializer_class = ArticleSerializer

    def get_queryset(self):
        return Article.objects.all().order_by('id')

    def get(self, request, *args, **kwargs):
        if kwargs.get('pk'):
            article = self.get_object()
            serializer = self.serializer_class(article)
            return Response(serializer.data)
        else:
            return self.list(request)

    def list(self, request):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)


class ArticlesAllAPI(ListAPIView):
    """
    This view will return response with full articles
    (title, body, data, author, liked_by),
    but divided into 10 users objects at the one response.
    Used limit and offset.
    """
    queryset = Article.objects.all()
    serializer_class = ArticleFullDataSerializer
    pagination_class = LimitOffsetPagination


class ArticleCreateAPI(APIView):
    """
    This view will check input user unique title name and then,
    if data is valid, create new article
    and return success message
    """
    serializer_class = ArticleCreateSerializer
    permission_classes = IsAuthenticated

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            validate_data = serializer.validated_data
            # create new article and save in base
            Article.objects.create(
                title=validate_data.get('title'),
                body=validate_data.get('body'),
                author=request.user
            )
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_409_CONFLICT)


class ArticleRemoveAPI(APIView):
    """
    This view will check if input user title is exist and then,
    if data is valid,
    check if current user is author of article with request title.
    If check is correct, article with request title will be remove from base.
    """
    serializer_class = ArticleRemoveSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            validate_data = serializer.validated_data
            article = Article.objects.get(title=validate_data.get('title'))
            # check if user is author of article with request title
            if article.author != request.user:
                raise ValidationError(
                    'Sorry, but you can\'t delete not your articles')
            # remove article with request title
            else:
                article.delete()
                return Response({'success': True})
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)


class ArticlesSearchAPI(APIView):
    """
    This view will found all articles by input user keyword in title and body,
    and return all of them.
    """
    serializer_class = ArticleSearchSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            keyword = serializer.validated_data.get('search_keyword')
            # filter by input user keyword in articles title and body
            articles = Article.objects.filter(
                Q(title__contains=keyword) | Q(body__contains=keyword))
            return Response(ArticleFullDataSerializer(
                articles, many=True).data)
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)


# trip API
class TripView(GenericAPIView):
    serializer_class = TripSerializer

    def get_queryset(self):
        return Trip.objects.all().order_by('id')

    def get(self, request, *args, **kwargs):
        if kwargs.get('pk'):
            trip = self.get_object()
            serializer = self.serializer_class(trip)
            return Response(serializer.data)
        else:
            return self.list(request)

    def list(self, request):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)


class TripAllAPI(ListAPIView):
    """
    This view will return response with full articles
    (title, body, data, author, liked_by),
    but divided into 10 users objects at the one response.
    Used limit and offset.
    """
    queryset = Trip.objects.all()
    serializer_class = TripFullDataSerializer
    pagination_class = LimitOffsetPagination


class TripCreateAPI(APIView):
    """
    This view will check input user unique title name and then,
    if data is valid, create new article
    and return success message
    """
    serializer_class = TripCreateSerializer

    # permission_classes = IsAuthenticated

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            validate_data = serializer.validated_data
            # create new article and save in base
            new_trip = Trip.objects.create(
                from_city=validate_data.get('from_city'),
                destination_city=validate_data.get('destination_city'),
                date=validate_data.get('date'),
                time=validate_data.get('time'),
                max_passengers=validate_data.get('max_passengers'),
                driver=request.user
            )
            return Response({'success': True})
        else:
            return Response(serializer.errors, status=status.HTTP_409_CONFLICT)


class TripRemoveAPI(APIView):
    # TODO Make remove api
    """
    This view will check if input user from_city and destination_city is exist and then,
    if data is valid,
    check if current user is driver of trip with request from_city and destination_city.
    If check is correct, article with request title will be remove from base.
    """
    serializer_class = TripRemoveSerializer
    permission_classes = IsAuthenticated

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            validate_data = serializer.validated_data
            trip = Trip.objects.get(
                from_city=validate_data.get('from_city'),
                destination_city=validate_data.get('destination_city')
            )
            if trip.driver != request.user:
                raise ValidationError(
                    'Sorry, but you can\'t delete not your trip')
            else:
                trip.delete()
                return Response({'success': True})
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)


class TripSearchAPI(APIView):
    """
    This view will found all trips by input user from_city_keyword
    and destination_city_keyword
    and return all of them.
    """
    serializer_class = TripSearchSerializer
    permission_classes = AllowAny

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            from_city_keyword = serializer.validated_data.get('from_city')
            destination_city_keyword = serializer.validated_data.get(
                'destination_city')
            trip = Trip.objects.filter(
                Q(from_city__contains=from_city_keyword) &
                Q(destination_city__contains=destination_city_keyword)
            )
            return Response(TripFullDataSerializer(trip, many=True).data)
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
