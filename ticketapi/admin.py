from django.contrib import admin
from .models import Concert

admin.site.register(Concert)

from django.contrib.auth.models import User
admin_user = User.objects.get(username='info2002@gmail.com')
admin_user.is_staff  # ← must be True

