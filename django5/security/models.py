from django.db import models
# import default user class
from django.contrib.auth.models import User

# Create your models here.
class UserProfileInfo(models.Model):
    # user class to provide additional info that default User doesnt have
    # like username,email,fname,lname

    user=models.OneToOneField(User, on_delete=models.CASCADE,)
    # additional
    portfolio_site=models.URLField(blank=True)
    profile_pic=models.ImageField(upload_to='profile_pics',blank=True)

    def __str__(self):
        return self.user.username
