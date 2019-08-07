from django.db import models
from django.conf import settings
from django.utils import timezone
# from django.contrib.auth.models import User
from accounts.models import Profile


class Register(models.Model):
    title = models.CharField(max_length=100)
    pub_date = models.DateField(auto_now_add=True, null=True)
    expireDate = models.DateField()
    organizer = models.ForeignKey(
        Profile, on_delete=models.CASCADE, blank=True, null=True)
    organization = models.CharField(max_length=100)
    minValue = models.IntegerField()
    maxValue = models.IntegerField()
    currentAmount = models.IntegerField(default=0)
    targetAmount = models.IntegerField()
    content = models.TextField()
    contentImage = models.ImageField(upload_to='images/%Y/%m/%d')
    like_user_set = models.ManyToManyField(
        Profile, blank=True, related_name='like_user_set', through='Like')
    pay_user_set = models.ManyToManyField(
        Profile, blank=True, related_name='pay_user_set', through='Donation'
    )
    hit = models.PositiveIntegerField(default=0)

    @property
    def like_count(self):
        return self.like_user_set.count()

    @property
    def update_counter(self):
        self.hit = self.hit + 1
        self.save()
        return self.hit

    def __str__(self):
        return self.title


class Like(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    register = models.ForeignKey(Register, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = (('user', 'register'))

class Donation(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    amount = models.IntegerField(default=0)
    register = models.ForeignKey(Register, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (('user', 'register'))