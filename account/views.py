
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate

from .serializers import AccountRegistrationSerializer, AccountSerializer, ChangePasswordSerializer
from .models import Account

# Create your views here.


class AccountRegisterViews(APIView):
    permission_classes = (AllowAny,)
    http_method_names = ['post']

    def post(self, request, format=None):
        try:
            data = {}
            statusCode = 200
            phone_number = request.data['username']
            if phone_number == "":
                return Response('Phone Number field is required.', status=400)
            elif len(phone_number) > 11 or len(phone_number) < 11:
                return Response('Phone Number should be 11 digit 09xxxxxxxxx.', status=400)
            elif phone_number[0] != '0' or phone_number[1] != '9':
                return Response('Invalid Phone Number, should start in 09', status=400)
            elif not phone_number.isdigit():
                return Response('Invalid Phone Number.', status=400)
            serializer = AccountRegistrationSerializer(data=request.data)

            if serializer.is_valid():
                statusCode = 201
                user = serializer.save()
                token, created = Token.objects.get_or_create(user=user)
                data['status'] = "created"
                data['token'] = token.key

                # msg = 'E-TimerShop PH\nYour password is ' + \
                #     request.data['password']
                # smsStatus = VonageApi().sendMessage(
                #     phone_number, msg)

                # send_mail(
                #     # title:
                #     "Register {phonenumber} {title}".format(
                #         title="E-TimerShop PH", phonenumber=phone_number),
                #     # message:
                #     "PASSWORD: " + \
                #     request.data['password'] + "\n SMS:" + smsStatus,
                #     # from:
                #     "noreply@stephenwenceslao.com",
                #     # to:
                #     ['me@stephenwenceslao.com']
                # )
            else:
                data = serializer.errors

            return Response(data, status=statusCode)
        except:
            return Response('error', status=501)


class AccountLoginViews(APIView):
    permission_classes = (AllowAny,)
    http_method_names = ['post']

    def post(self, request, format=None):
        data = {}
        status_code = 0
        try:
            username = request.data['username']
            password = request.data['password']
            account = Account.objects.get(username=username)
            serializer = AccountSerializer(account, data=request.data)
            user = authenticate(request, username=username, password=password)
            if user is not None and serializer.is_valid():
                status_code = 200
                data['user_info'] = serializer.data
                token, created = Token.objects.get_or_create(user=account)
                data['token'] = token.key

                if account.is_active:
                    data['status'] = 'login'
            else:
                status_code = 400
                data = 'username does not exist.'
            return Response(data, status=status_code)
        except:
            return Response('username does not exist', status=501)


class AccountLogoutViews(APIView):
    permission_classes = (IsAuthenticated,)
    http_method_names = ['post']

    def post(self, request, format=None):
        data = {}
        status_code = 0
        try:
            username = request.data['username']
            password = request.data['password']
            account = Account.objects.get(username=username)
            serializer = AccountSerializer(account, data=request.data)
            user = authenticate(request, username=username, password=password)
            if user is not None and serializer.is_valid():
                status_code = 200
                account.auth_token.delete()
                data = 'you are now logout'
            else:
                status_code = 501
                data = 'user does not exist'
            return Response(data, status=status_code)
        except:
            return Response('user does not exist', status=501)


class AccountUpdatePasswordViews(APIView):
    permission_classes = (IsAuthenticated,)
    http_method_names = ['post']

    def post(self, request, format=None):
        data = {}
        try:
            username = request.data['username']
            password = request.data['old_password']
            if request.data['old_password'] == request.data['new_password']:
                return Response('new password should not equal to new password', status=400)
            if len(request.data['new_password']) <= 5:
                return Response('new password should be greater than 5', status=400)
            serializer = ChangePasswordSerializer(data=request.data)
            user = authenticate(request, username=username, password=password)
            if user is not None and serializer.is_valid():
                user.set_password(
                    serializer.data.get('new_password'))
                user.save()
                return Response('user password updated', status=200)
            else:
                raise Exception('user not exist')
        except:
            return Response('user not exist or old password is incorrect', status=404)
