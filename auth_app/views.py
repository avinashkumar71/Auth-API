from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializer import (UserRegisterSerializer,UserLoginSerializer,UserProfileSerializer
,UserPasswordChangeSerializer,UserPasswordResetSerializer,UserPasswordResetSubmitSerializer)
from django.contrib.auth import authenticate
from auth_app.renderers import UseRenderers
from rest_framework_simplejwt.tokens import RefreshToken
from random import randint

# Create your views here.

# method to generate jwt token
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

def random_with_N_digits():
    return randint(111111, 999999)

otp =''

# user registration
class UserRegistrationViews(APIView):
    renderer_classes = [UseRenderers]

    def post(self,request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token = get_tokens_for_user(user)
            return Response({'token':token,'msg':'successfully created'},status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

# user login view
class UserLoginView(APIView):
    renderer_classes = [UseRenderers]

    def post(self,request):
        serializer = UserLoginSerializer(data=request.data)
        print(serializer)
        if serializer.is_valid():
            email = serializer.data.get('email')
            password = serializer.data.get('password')
            user = authenticate(email=email,password=password)
            if user is not None:
                token = get_tokens_for_user(user)
                return Response({'token':token,'msg':'successfully login'},status=status.HTTP_202_ACCEPTED)
            else:
                return Response({'msg':'check your credential'},status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors,status=status.HTTP_404_NOT_FOUND)


# user profile view
class UserProfileView(APIView):
    renderer_classes = [UseRenderers]
    permission_classes = [IsAuthenticated]
    
    def get(self,request):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data)


# password change
class UserPasswordChange(APIView):
    renderer_classes = [UseRenderers]
    permission_classes = [IsAuthenticated]

    def post(self,request):
        serializer = UserPasswordChangeSerializer(data=request.data,context={'user':request.user})
        if serializer.is_valid(raise_exception=True):
            return Response({'msg':'password changed successfully'},status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_304_NOT_MODIFIED)


class UserPasswordResetView(APIView):
    renderer_classes = [UseRenderers]

    def post(self,request):
        serializer = UserPasswordResetSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            return Response({'msg':'reset password email send , check your email '},status=status.HTTP_200_OK)
        return Response(serializer.errors)


class UserPasswordResetSubmit(APIView):
    renderer_classes = [UseRenderers]
    
    def post(self,request,uid,token):
        serializer = UserPasswordResetSubmitSerializer(data=request.data,context={'uid':uid,'token':token})
        if serializer.is_valid(raise_exception=True):
            return Response({'msg':'checked reset by email successfully'})
        else:
            return Response(serializer.errors)


