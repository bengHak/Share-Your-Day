from django.db import models
from django.conf import settings
# from django.contrib.auth.models import User
from accounts.models import Profile


class Register(models.Model):
    title = models.CharField(max_length=100)
    # pub_date = models.DateTimeField('date published')
    expireDate = models.DateField()
    organization = models.CharField(max_length=100)
    minValue = models.IntegerField()
    maxValue = models.IntegerField()
    # currentAmount = models.IntegerField(default=0)
    targetAmount = models.IntegerField()
    content = models.TextField()
    contentImage = models.ImageField(upload_to='images/')
    like_user_set = models.ManyToManyField(
        Profile, blank=True, related_name='like_user_set', through='Like')

    @property
    def like_count(self):
        return self.like_user_set.count()

    def __str__(self):
        return self.title


class Like(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    register = models.ForeignKey(Register, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = (('user', 'register'))
