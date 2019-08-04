from django.db import models


class Register(models.Model):
    title = models.CharField(max_length=100)
    # pub_date = models.DateTimeField('date published')
    expireDate = models.DateField()
    organization = models.CharField(max_length=100)
    minValue = models.IntegerField()
    maxValue = models.IntegerField()
    targetAmount = models.IntegerField()
    content = models.TextField()
    contentImage = models.ImageField(upload_to='images/')

    def __str__(self):
        return self.title
