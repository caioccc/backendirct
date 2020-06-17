from django.contrib.auth.models import User
from django.db import models


# Create your models here.

class TimeStamped(models.Model):
    class Meta:
        abstract = True

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Role(TimeStamped):
    name = models.CharField(max_length=100, blank=True, null=True, default='OPERATOR')

    def __str__(self):
        return "%s" % self.name

    def __unicode__(self):
        return "%s" % self.name


class Group(TimeStamped):
    name = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return "%s" % self.name

    def __unicode__(self):
        return "%s" % self.name


class CustomUser(TimeStamped):
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)

    def __str__(self):
        return "%s" % self.user

    def __unicode__(self):
        return "%s" % self.user
