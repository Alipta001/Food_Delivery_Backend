import random
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User, LoginOTP
from .serializers import RegisterSerializer, LoginSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated


#---------- Verify email with activation link ----------#

# @api_view(["POST"])
# @permission_classes([AllowAny])
# def register_user(request):
#     serializer = RegisterSerializer(data=request.data)

#     if serializer.is_valid():
#         user = serializer.save()
#         user.is_active = True
#         user.save()

#         token = default_token_generator.make_token(user)
#         uid = urlsafe_base64_encode(force_bytes(user.pk))

#         activation_link = f"http://localhost:8000/api/users/activate/{uid}/{token}/"

#         send_mail(
#             subject="Activate your account",
#             message=f"Click the link to activate your account:\n{activation_link}",
#             from_email=settings.EMAIL_HOST_USER,
#             recipient_list=[user.email],
#             fail_silently=False,
#         )

#         return Response(
#             {"message": "Activation link sent to email"},
#             status=status.HTTP_201_CREATED
#         )

#     return Response(serializer.errors, status=400)

# @api_view(["GET"])
# @permission_classes([AllowAny])
# def activate_user(request, uidb64, token):
#     try:
#         uid = force_str(urlsafe_base64_decode(uidb64))
#         user = User.objects.get(pk=uid)
#     except Exception:
#         return Response({"error": "Invalid activation link"}, status=400)

#     if default_token_generator.check_token(user, token):
#         user.is_active = True
#         user.save()
#         return Response({"message": "Account activated successfully"})

#     return Response({"error": "Invalid or expired token"}, status=400)

# @api_view(["POST"])
# @permission_classes([AllowAny])
# def login_user(request):
#     serializer = LoginSerializer(data=request.data)
#     serializer.is_valid(raise_exception=True)

#     email = serializer.validated_data["email"]
#     password = serializer.validated_data["password"]

#     user = authenticate(username=email, password=password)

#     if not user:
#         return Response({"error": "Invalid credentials"}, status=401)

#     if not user.is_active:
#         return Response({"error": "Email not verified"}, status=403)

#     otp = str(random.randint(100000, 999999))

#     LoginOTP.objects.filter(user=user, is_used=False).delete()
#     LoginOTP.objects.create(user=user, otp=otp)


#     send_mail(
#         subject="Your Login OTP",
#         message=f"Your OTP is {otp}. It is valid for 5 minutes.",
#         from_email=settings.EMAIL_HOST_USER,
#         recipient_list=[user.email],
#         fail_silently=False,
#     )

#     return Response({"message": "OTP sent to email"}, status=200)

# @api_view(["POST"])
# @permission_classes([AllowAny])
# def verify_login_otp(request):
#     email = request.data.get("email")
#     otp = request.data.get("otp")

#     if not email or not otp:
#         return Response(
#             {"error": "email and otp are required"},
#             status=400
#         )

#     try:
#         user = User.objects.get(email=email)
#     except User.DoesNotExist:
#         return Response({"error": "Invalid data"}, status=400)

#     otp_obj = LoginOTP.objects.filter(
#         user=user,
#         otp=otp,
#         is_used=False
#     ).last()

#     if not otp_obj:
#         return Response({"error": "Invalid OTP"}, status=400)

#     if otp_obj.is_expired():
#         return Response({"error": "OTP expired"}, status=400)

#     otp_obj.is_used = True
#     otp_obj.save()

#     refresh = RefreshToken.for_user(user)

#     return Response({
#         "access": str(refresh.access_token),
#         "refresh": str(refresh),
#         "user": {
#             "id": user.id,
#             "email": user.email,
#             "role": user.role
#         }
#     }, status=200)



#---------- Verify with OTP implementation ----------#
def generate_otp():
    return str(random.randint(100000, 999999))

@api_view(["POST"])
@permission_classes([AllowAny]) 
def register_user(request):
    serializer = RegisterSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    user = serializer.save()

    otp = generate_otp()
    LoginOTP.objects.filter(user=user).delete()
    LoginOTP.objects.create(user=user, otp=otp)

    send_mail(
        subject="Verify your account",
        message=f"Your registration OTP is {otp}. It is valid for 5 minutes.",
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[user.email],
    )

    return Response(
        {"message": "OTP sent to email for account verification"},
        status=status.HTTP_201_CREATED
    )

@api_view(["POST"])
@permission_classes([AllowAny])
def verify_registration_otp(request):
    email = request.data.get("email")
    otp = request.data.get("otp")

    if not email or not otp:
        return Response({"error": "email and otp required"}, status=400)

    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return Response({"error": "Invalid email"}, status=400)

    otp_obj = LoginOTP.objects.filter(
        user=user,
        otp=otp,
        is_used=False
    ).last()

    if not otp_obj:
        return Response({"error": "Invalid OTP"}, status=400)

    if otp_obj.is_expired():
        return Response({"error": "OTP expired"}, status=400)

    otp_obj.is_used = True
    otp_obj.save()

    user.is_active = True
    user.save()

    return Response({"message": "Account verified successfully"}, status=200)

@api_view(["POST"])
@permission_classes([AllowAny])
def login_user(request):
    serializer = LoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    email = serializer.validated_data["email"]
    password = serializer.validated_data["password"]

    user = authenticate(username=email, password=password)

    if not user:
        return Response({"error": "Invalid credentials"}, status=401)

    if not user.is_active:
        return Response({"error": "Account not verified"}, status=403)

    otp = generate_otp()
    LoginOTP.objects.filter(user=user, is_used=False).delete()
    LoginOTP.objects.create(user=user, otp=otp)

    send_mail(
        subject="Login OTP",
        message=f"Your login OTP is {otp}. Valid for 5 minutes.",
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[user.email],
    )

    return Response({"message": "OTP sent to email"}, status=200)

@api_view(["POST"])
@permission_classes([AllowAny])
def verify_login_otp(request):
    email = request.data.get("email")
    otp = request.data.get("otp")

    if not email or not otp:
        return Response({"error": "email and otp required"}, status=400)

    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return Response({"error": "Invalid email"}, status=400)

    otp_obj = LoginOTP.objects.filter(
        user=user,
        otp=otp,
        is_used=False
    ).last()

    if not otp_obj:
        return Response({"error": "Invalid OTP"}, status=400)

    if otp_obj.is_expired():
        return Response({"error": "OTP expired"}, status=400)

    otp_obj.is_used = True
    otp_obj.save()

    refresh = RefreshToken.for_user(user)

    return Response({
        "message": "Login successful",
        "access": str(refresh.access_token),
        "refresh": str(refresh),
        "user": {
            "id": user.id,
            "email": user.email,
            "role": user.role
        }
    })
