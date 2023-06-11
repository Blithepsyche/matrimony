from django.db import models

# Create your models here.
class User(models.Model):
    uid=models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    date_of_birth = models.DateField(null=True)
    email = models.EmailField(max_length=255)
    phone_number = models.CharField(max_length=255)
    age = models.IntegerField(null=True)
    gender = models.CharField(max_length=255, default="", null=True)
    religion = models.CharField(max_length=255, default="", null=True)
    mother_tongue = models.CharField(max_length=255, default="", null=True)
    password = models.CharField(max_length=255, default="")
    profile_image = models.ImageField(max_length=255, upload_to="uploads/users/profile/", null=True, blank=True)

    def __str__(self):
        return self.first_name