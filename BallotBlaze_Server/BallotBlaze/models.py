from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
import uuid

'''User registration'''
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)
    
class CustomUser(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True, null=False)
    username = models.CharField(max_length=100, null=False) 

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = CustomUserManager()

    def __str__(self):
        return f"{self.email} ({self.username})"

class BlacklistedToken(models.Model):
    token = models.CharField(max_length=255, unique=True)
    blacklisted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Blacklisted at {self.blacklisted_at}"
    
'''Polls'''
class Poll(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    def __str__(self):
        return self.title


class PollOption(models.Model):
    poll = models.ForeignKey(Poll, related_name='options', on_delete=models.CASCADE)
    option_text = models.CharField(max_length=255)
    vote_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.option_text} ({self.poll.title})"


class Vote(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    selected_option = models.ForeignKey(PollOption, on_delete=models.CASCADE)
    voted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'poll')  # prevent duplicate votes
        indexes = [
            models.Index(fields=["poll"]),
            models.Index(fields=["user"]),
            models.Index(fields=["selected_option"]),
        ]