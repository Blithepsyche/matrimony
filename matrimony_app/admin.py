from django.contrib import admin
from .models import User
# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = ('uid', 'first_name', 'last_name', 'date_of_birth', 'email', 'phone_number', 'age', 'gender', 'religion', 'mother_tongue',  'password', 'profile_image')
    
admin.site.register(User, UserAdmin)