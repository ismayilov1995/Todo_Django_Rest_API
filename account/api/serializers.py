from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, Serializer


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['pk', 'first_name', 'last_name', 'email', 'username']


class RegisterSerializer(ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['pk', 'first_name', 'last_name', 'username', 'password']

    def validate(self, attrs):
        validate_password(attrs['password'])
        return attrs

    def create(self, validated_data):
        user = User.objects.create(username=validated_data['username'], first_name=validated_data['first_name'],
                                   last_name=validated_data['last_name'])
        user.set_password(validated_data['password'])
        user.save()
        return user

class ChangePasswordSerializers(Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    # Shifreni yoxlayiriq
    def validate_new_password(self, value):
        validate_password(value)
        return value

