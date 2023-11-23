from django.db import models
from django.contrib.auth.models import User
import random
import string


class Room(models.Model):
    admin = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    is_public = models.BooleanField(default=False)
    language = models.CharField(max_length=100)
    country_code = models.CharField(max_length=20)
    flag_url = models.CharField(max_length=100)
    key = models.CharField(max_length=100,unique=True, blank=True)

    def save(self, *args, **kwargs):
        self.flag_url = f'https://flagcdn.com/w320/{self.country_code.lower()}.png'
        if not self.key:
            base_key = generate_random_string()
            unique_key = base_key
            while Room.objects.filter(key=unique_key).exists():
                unique_key = generate_random_string()
            self.key = unique_key
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Message(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='messages')
    user = models.CharField(max_length=100)
    content = models.TextField()

    def __str__(self):
        return f'{self.content} - {self.user}'
    

def generate_random_string(length=10):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))