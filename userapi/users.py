from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import UserSerializer
from django.contrib.auth.models import User

from django.conf import settings
from django.core.mail import send_mail
from django.utils import timezone
from datetime import timedelta
from .models import VerifiedEmail
from random import randint

from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token


@api_view(['POST'])
def send_email_otp(request):
    email = request.data.get('email')

    if not email:
        return Response({"error": "Email is required."}, status=400)

    otp_code = str(randint(100000, 999999))
    otp_expires_at = timezone.now() + timedelta(minutes=5)

    VerifiedEmail.objects.update_or_create(
        email=email,
        defaults={"otp_code": otp_code, "otp_expires_at": otp_expires_at, "is_verified": False},
    )

    send_mail(
        f' {otp_code} is Your OTP Code',
        f'Your OTP code is: {otp_code}',
        'truedost5@gmail.com',
        [email],
        fail_silently=False,
    )

    return Response({"message": "OTP sent to your email. Please verify."}, status=200)

@api_view(['POST'])
def verify_email_otp(request):
    email = request.data.get('email')
    otp_code = request.data.get('otp')

    if not email or not otp_code:
        return Response({"error": "Email and OTP are required."}, status=400)

    try:
        verified_email = VerifiedEmail.objects.get(email=email, otp_code=otp_code)

        if verified_email.otp_expires_at < timezone.now():
            return Response({"error": "OTP has expired. Please request a new one."}, status=400)

        verified_email.is_verified = True
        verified_email.save()

        return Response({"message": "Email verified successfully."}, status=200)

    except VerifiedEmail.DoesNotExist:
        return Response({"error": "Invalid email or OTP."}, status=400)

@api_view(['POST'])
def register(request):
    if request.method == 'POST':
        email = request.data.get('email')
        try:
            verified_email = VerifiedEmail.objects.get(email=email)
            if not verified_email.is_verified:
                return Response({"error": "Email not verified. Please verify your email first."}, status=400)
            
            serializer = UserSerializer(data=request.data)

            if serializer.is_valid():
                serializer.save() 
                return Response({"message": "User registered successfully."}, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        except VerifiedEmail.DoesNotExist:
            return Response({"error": "Email not found. Please start with email verification."}, status=400)

@api_view(['POST'])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')

    if not username or not password:
        return Response({"error": "Number and password are required."}, status=status.HTTP_400_BAD_REQUEST)

    user = authenticate(username=username, password=password)
    if user is not None:
       
        token, created = Token.objects.get_or_create(user=user)
        print(created)
        return Response({
            "message": "Login successful.",
            "token": token.key,
            "username": user.username,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name
        }, status=status.HTTP_200_OK)

    return Response({"error": "Invalid number or password."}, status=status.HTTP_401_UNAUTHORIZED)
