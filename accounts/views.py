# from django.shortcuts import render
from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from .models import Account, TokenManager

# Create your views here.


class AccountViewSet(ViewSet):
    """
    Viewset for handling account creation and login
    """

    permission_classes = [AllowAny]

    def create(self, request):
        """
        Create a new account
        :param request:
        :return:
        """
        received_data = request.data

        try:
            if Account.objects.filter(email=received_data['email']).exists():
                raise IntegrityError
            Account.objects.create_user(email=received_data['email'], password=received_data['password'])
        except IntegrityError:
            return Response({'status': 'Account Already Exists'}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'status': 'Account Created'}, status=status.HTTP_201_CREATED)

    @action(methods=['post'], detail=False, url_path='login')
    def login_user(self, request):
        """
        Login a user
        :param request:
        :return:
        """

        received_data = request.data

        user = get_object_or_404(Account, email=received_data['email'])

        if user.check_password(received_data['password']):
            user_token_info = TokenManager(user=user)
            user_token_info.save()
            return Response({'detail': 'Login Successful', 'token': user_token_info.token}, status=status.HTTP_200_OK)
        return Response({'detail': 'Login failed!'}, status=status.HTTP_400_BAD_REQUEST)
