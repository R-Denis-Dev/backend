from rest_framework import serializers
from rest_framework.authentication import get_user_model
from .models import (
    Transaction,Transfer,Message
)

class LoginSerializer(serializers.ModelSerializer):
    username=serializers.CharField(required=True)
    password=serializers.CharField(required=True, write_only=True)
    
    
class RegisterSerializer(serializers.Serializer):
    username=serializers.CharField(required=True)
    password=serializers.CharField(required=True, write_only=True)
    confirm_password=serializers.CharField(required=True, write_only=True)
    
    def validate(self, attrs):
        username,password,confirm_password = attrs['username'],attrs['password'],attrs['confirm_password']
        if get_user_model().objects.filter(username=username).exists():
            raise serializers.ValidationError("Username уже занят")
        if password != confirm_password:
            raise serializers.ValidationError("Пароли не совпадают")
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('confirm_password')
        return get_user_model().objects.create_user(**validated_data)
    
class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = [
            "client",
            "status",
            "cash",
            "created_at",
            "updated_at"
        ]
        extra_kwargs = {
            'client':{
                'required':False
            }
        }
        read_only_fields = [
            "created_at",
            "updated_at"
        ]
        
class TransferSerialzer(serializers.ModelSerializer):
    class Meta:
        model = Transfer
        fields =[
            "sender",
            "addressee",
            "cash",
        ]
        extra_kwargs = {
            'sender':{
                'required':False
            }
        }
        
    def validate(self, attrs):
        if attrs['sender'] == attrs['addressee']:
            raise serializers.ValidationError("Вы не можете перевести самому себе")
        return attrs
        
class UserSerialzier(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = [
            'username',
            'date_joined',
            'first_name',
            'email'
        ]
        
class TransferPreviewSerialzer(serializers.ModelSerializer):
    addressee = UserSerialzier()
    class Meta:
        model = Transfer
        fields =[
            "sender",
            "addressee",
            "cash",
        ]
        extra_kwargs = {
            'sender':{
                'required':False
            }
        }
    def validate_cash(self,value):
        if value <= 0:
            raise serializers.ValidationError("Сумма для перевода не может быт ьменьше 1")
        return value
    
    def validate_addressee(self,value):
        if not get_user_model().objects.filter(id=value).exists():
            raise serializers.ValidationError("Такого пользователя не существует")
        return value
    
class MessageSerialzier(serializers.ModelSerializer):
    class Meta:
        model =Message
        fields = [
            'message',
            'created_at'
            ]