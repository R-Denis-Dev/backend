from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    pass


class Transaction(models.Model):
    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name="transaction_client")
    STATUS_CHOICES = [
        ('registered', 'Зарегистрирована'),
        ('denied', 'Отменена'),
        ('approved', 'Одобрена'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    cash = models.DecimalField(decimal_places=2, max_digits=15) 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
class Transfer(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent_transfers")
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name="received_transfers")
    cash = models.DecimalField(decimal_places=2, max_digits=15)

class Message(models.Model):
    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name="messages")
    message = models.CharField(max_length=512)
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
