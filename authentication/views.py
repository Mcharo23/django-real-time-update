from rest_framework.decorators import api_view, APIView
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed

from .serializers import UserSerializer
from .models import User

import jwt
import datetime
import environ
import bcrypt

env = environ.Env()
environ.Env.read_env()


@api_view(['GET'])
def getRoutes(request):
    routes = [
        f'{env("BASE")}/auth/',
        f'{env("BASE")}/auth/register/',
        f'{env("BASE")}/auth/logout/',
    ]
    return Response(routes)


def AuthenticateUser(request):
    token = request.COOKIES.get('jwt')

    if not token:
        raise AuthenticationFailed('Unauthenticated')

    try:
        payload = jwt.decode(token, env('SECRET_KEY'), algorithms=['HS256'])
        user = User.objects.get(user_id=payload['user_id'])
    except jwt.ExpiredSignatureError:
        raise AuthenticationFailed('Unauthenticated')

    return user


class RegistrationView(APIView):
    serializer_class = UserSerializer

    @action(methods=['POST'], detail=True)
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data)


class LoginView(APIView):

    @action(methods=['POST'], detail=True)
    def post(self, request):
        email = request.data['email']
        password = request.data['password']

        user = User.objects.filter(email=email).first()

        if user is None:
            raise AuthenticationFailed()

        if not bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
            raise AuthenticationFailed()

        payload = {
            'user_id': str(user.user_id),
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=40),
            'iat': datetime.datetime.utcnow(),
        }

        token = jwt.encode(payload, env('SECRET_KEY'), algorithm='HS256')

        response = Response()
        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data = {'token': token, }

        return response


class LogoutView(APIView):

    def post(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message': 'Successfully logged out',
        }

        return response
