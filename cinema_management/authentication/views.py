# views.py
from django.shortcuts import render, redirect
from rest_framework import generics, status
from .serializers import RegisterSerializer  # Fix the typo in the serializer import
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User
from .utils import Util
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
import jwt
from django.conf import settings
from rest_framework.views import APIView  # Import APIView
from django.views import View
from django.contrib import messages

class RegisterView(generics.GenericAPIView):

    serializer_class = RegisterSerializer  # Fix the typo in the serializer class name

    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data = serializer.data

        user = User.objects.get(email=user_data['email'])

        token = RefreshToken.for_user(user).access_token

        current_site = get_current_site(request).domain
        relative_link = reverse('email-verify')
        
        absurl = 'http://' + current_site + relative_link + "?token=" + str(token)
        email_body = 'Hi ' + user.username+' Use link below to verify your email \n' + absurl
        data = {'email_body': email_body, 'to_email': user.email, 'email_subject': 'Verify your email'}
        Util.send_email(data)

        return Response(user_data, status=status.HTTP_201_CREATED)
        
class VerifyEmail(APIView):
    def get(self, request):
        token = request.GET.get('token')
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            user = User.objects.get(id=payload['user_id'])
            if not user.is_verified:
                user.is_verified = True
                user.save()

                # Thông báo xác thực thành công
                messages.success(request, 'Xác thực thành công!')

                # Chuyển hướng đến trang đăng nhập admin
                admin_login_url = reverse('admin:login')  # Sử dụng tên đường dẫn admin:login
                return redirect(admin_login_url)
        except jwt.ExpiredSignatureError as identifier:
            messages.error(request, 'Activation Expired')
        except jwt.exceptions.DecodeError as identifier:
            messages.error(request, 'Invalid token')

        # Chuyển hướng về trang đăng nhập admin nếu có lỗi
        admin_login_url = reverse('admin:login')  # Sử dụng tên đường dẫn admin:login
        return redirect(admin_login_url)