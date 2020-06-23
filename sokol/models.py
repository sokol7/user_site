from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from mptt.models import MPTTModel


class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name = 'profile')
    avatar = models.ImageField(upload_to='profile_images', blank=True)
    slug = models.SlugField(max_length=40, blank=True)
    username = models.CharField(max_length=40, blank=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.user.username)
        self.username = self.user.username
        super(UserProfile, self).save(*args, **kwargs)

    @property
    def get_photo_url(self):
        if self.avatar and hasattr(self.avatar, 'url'):
            return self.avatar.url
        else:
            return "/static/images/main.jpg"


    def __str__(self):
        return self.user.username


class Status(models.Model):
    user_fk = models.OneToOneField(UserProfile, related_name = 'status')
    timestamp = models.DateTimeField(auto_created=True)
    is_online = models.BooleanField(default=True)
