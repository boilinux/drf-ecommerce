from rest_framework import serializers
from .models import Account


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['id', 'username', 'email', 'full_name',
                  'last_login', 'is_active', 'is_admin']


class AccountRegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(
        style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = Account
        fields = ['username', 'email', 'full_name',
                  'password', 'password2']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def save(self):
        account = Account(
            username=self.validated_data['username'],
            email=self.validated_data['email'],
            full_name=self.validated_data['full_name'],
        )

        password = self.validated_data['password']
        password2 = self.validated_data['password2']

        if password != password2:
            raise serializers.ValidationError(
                {'password': 'Password must match.'})

        account.set_password(password)
        account.save()

        return account


class ChangePasswordSerializer(serializers.Serializer):
    model = Account

    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
