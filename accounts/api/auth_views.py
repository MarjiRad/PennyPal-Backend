
from rest_framework import generics, status
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework.renderers import JSONRenderer
from accounts.api.serializers import RegisterSerializer, LoginSerializer


# -------------------- REGISTER (SIGN UP) --------------------
class RegisterView(generics.CreateAPIView):
    
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        token, _ = Token.objects.get_or_create(user=user)
        return Response({
            "message": "Signup successful!",
            "token": token.key,
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
            }
        }, status=status.HTTP_201_CREATED)


# -------------------- SIGN IN (LOGIN) --------------------
class SignInView(generics.GenericAPIView):
    
    serializer_class = LoginSerializer
    renderer_classes = [JSONRenderer]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data['username']
        password = serializer.validated_data['password']
        user = authenticate(username=username, password=password)

        if user:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({
                "message": "Sign in successful!",
                "token": token.key,
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                }
            }, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Invalid username or password"}, status=status.HTTP_400_BAD_REQUEST)

