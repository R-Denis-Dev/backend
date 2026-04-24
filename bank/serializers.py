from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Transaction, Transfer, Message

User = get_user_model()

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)

class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)
    confirm_password = serializers.CharField(required=True, write_only=True)

    def validate(self, attrs):
        username = attrs['username']
        password = attrs['password']
        confirm_password = attrs['confirm_password']

        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError("Username уже занят")
        if password != confirm_password:
            raise serializers.ValidationError("Пароли не совпадают")
        return attrs

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password']
        )
        return user

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = [
            "client", "status", "cash", "created_at", "updated_at"
        ]
        read_only_fields = ["created_at", "updated_at", "client"]

class TransferSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transfer
        fields = [ "sender", "recipient", "cash"]
        read_only_fields = ["sender"]

    def validate(self, attrs):
        sender = attrs.get('sender')
        recipient = attrs.get('recipient')

        if sender == recipient:
            raise serializers.ValidationError("Вы не можете перевести самому себе")
        return attrs

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'date_joined', 'first_name', 'email']

class TransferPreviewSerializer(serializers.ModelSerializer):
    recipient = UserSerializer(read_only=True)

    class Meta:
        model = Transfer
        fields = ["sender", "recipient", "cash"]
        read_only_fields = ["sender"]

    def validate_cash(self, value):
        if value <= 0:
            raise serializers.ValidationError("Сумма для перевода не может быть меньше или равна 0")
        return value

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['message', 'created_at', 'is_read']
        read_only_fields = ['created_at']
