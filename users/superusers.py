from django.contrib.auth.models import User
print(User.objects.filter(is_superuser=True))